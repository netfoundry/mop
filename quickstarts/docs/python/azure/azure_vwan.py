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
LOCATION = 'westus2'
SUBNET_NAME = 'AVW-PT-subnet10'
VWAN_NAME = 'AVW-PT-VWAN'
VWAN_PARAMS = {
    'disable_vpn_encryption': False,
    'allow_branch_to_branch_traffic': True,
    'allow_vnet_to_vnet_traffic': True,
    'office365_local_breakout_category': 'None',
    'type': 'Basic'
}

network_client = NetworkManagementClient(credentials, AZURE_SUBSCRIPTION_ID)

# Create Virtual Network
async_vnet_creation = network_client.virtual_networks.create_or_update(
    GROUP_NAME,
    VNET_NAME,
    {
        'location': LOCATION,
        'address_space': {
            'address_prefixes': ['10.10.0.0/16']
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
    {'address_prefix': '10.10.0.0/24'}
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

# Delay for 30 seconds before deleting resources
time.sleep(30)

# Create VWAN
async_vwan_deletion = network_client.virtual_wans.create_or_update(
    GROUP_NAME,
    VWAN_NAME,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vwan_deletion.wait()
print(async_vwan_deletion.result())

# Delete Subnet
async_subnet_deletion = network_client.subnets.delete(
    GROUP_NAME,
    VNET_NAME,
    SUBNET_NAME
)
async_subnet_deletion.wait()
print(async_subnet_deletion.result())

# Delete Virtual Network
async_vnet_deletion = network_client.virtual_networks.delete(
    GROUP_NAME,
    VNET_NAME
)
async_vnet_deletion.wait()
print(async_subnet_deletion.result())
