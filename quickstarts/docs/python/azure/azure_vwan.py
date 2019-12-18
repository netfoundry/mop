#!/usr/bin/python3

import os
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

AZURE_SUBSCRIPTION_ID=os.environ.get('ARM_SUBSCRIPTION_ID')
credentials = ServicePrincipalCredentials(
    client_id = os.environ.get('ARM_CLIENT_ID'),
    secret = os.environ.get('ARM_CLIENT_SECRET'),
    tenant = os.environ.get('ARM_TENANT_ID')
)

GROUP_NAME = 'clouddev-smoke'
VNET_NAME = 'DariuszRG-vnet'
LOCATION = 'westus2'
SUBNET_NAME = 'Dariusz-subnet10'

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
