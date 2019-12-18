#!/usr/bin/python3

import os
import time
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

AZURE_SUBSCRIPTION_ID=os.environ.get('ARM_SUBSCRIPTION_ID')
credentials = ServicePrincipalCredentials(
    client_id = os.environ.get('ARM_CLIENT_ID'),
    secret = os.environ.get('ARM_CLIENT_SECRET'),
    tenant = os.environ.get('ARM_TENANT_ID')
)

GROUP_NAME = 'clouddev-smoke'
VNET_NAME = 'AVW-PT-vnet'
VNET_PREFIX = '10.10.0.0/16'
SUBNET_PREFIX = '10.10.10.0/24'
VHUB_PREFIX = '172.168.10.0/24'
LOCATION = 'westus2'
SUBNET_NAME = 'AVW-PT-subnet10'
KEY1 = 'AVW Packet Test'
VWAN_NAME = 'AVW-PT-VWAN'
VWAN_PARAMS = {
    'location': LOCATION,
    'tags': {
        'key1': KEY1
    },
    'disable_vpn_encryption': False,
    'allow_branch_to_branch_traffic': True,
    'allow_vnet_to_vnet_traffic': True,
    'office365_local_breakout_category': 'None',
    'type': 'Basic'
}
VHUB_NAME = 'AVW-PT-VHUB'
VHUB_PARAMS = {
    'location': LOCATION,
    'tags': {
        'key1': KEY1
    },
    "virtual_network_connections": [],
    'address_prefix': VHUB_PREFIX,
    'route_table': {
      "routes": []
    },
    'virtual_wan': {
      'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualWans/%s" % (AZURE_SUBSCRIPTION_ID, GROUP_NAME, VWAN_NAME)
    },
    "sku": "Basic"
}

network_client = NetworkManagementClient(credentials, AZURE_SUBSCRIPTION_ID)

# Create Virtual Network
async_vnet_creation = network_client.virtual_networks.create_or_update(
    GROUP_NAME,
    VNET_NAME,
    {
        'location': LOCATION,
        'address_space': {
            'address_prefixes': [VNET_PREFIX]
        }
    }
)
async_vnet_creation.wait()
print(async_vnet_creation.result())

# Create Subnet
async_subnet_creation = network_client.subnets.create_or_update(
    GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME,
    {'address_prefix': SUBNET_PREFIX}
)
async_subnet_creation.wait()
print(async_subnet_creation.result())

# Create VWAN
async_vwan_creation = network_client.virtual_wans.create_or_update(
    GROUP_NAME,
    VWAN_NAME,
    VWAN_PARAMS,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vwan_creation.wait()
print(async_vwan_creation.result())

# Create VHUB
async_vhub_creation = network_client.virtual_hubs.create_or_update(
    GROUP_NAME,
    VHUB_NAME,
    VHUB_PARAMS,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vhub_creation.wait()
print(async_vhub_creation.result())

# Delay for 30 seconds before deleting resources
time.sleep(30)

# Delete VHUB
async_vhub_deletion = network_client.virtual_hubs.delete(
    GROUP_NAME,
    VHUB_NAME,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vhub_deletion.wait()
print(async_vhub_deletion.result())
print('VHUB Delete')

# Delete VWAN
async_vwan_deletion = network_client.virtual_wans.delete(
    GROUP_NAME,
    VWAN_NAME,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vwan_deletion.wait()
print(async_vwan_deletion.result())
print('VWAN Delete')

# Delete Subnet
async_subnet_deletion = network_client.subnets.delete(
    GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME
)
async_subnet_deletion.wait()
print(async_subnet_deletion.result())
print('Subnet Delete')

# Delete Virtual Network
async_vnet_deletion = network_client.virtual_networks.delete(
    GROUP_NAME,
    VNET_NAME
)
async_vnet_deletion.wait()
print(async_subnet_deletion.result())
print('VNET Delete')
