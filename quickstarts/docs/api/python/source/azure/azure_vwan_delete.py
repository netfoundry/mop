#!/usr/bin/python3
"""Delete VWAN."""
import os
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ.get('ARM_CLIENT_ID'),
    secret=os.environ.get('ARM_CLIENT_SECRET'),
    tenant=os.environ.get('ARM_TENANT_ID')
)

# Connect to Azure APIs and get session details
network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# Delete VHUB
async_vhub_deletion = network_client.virtual_hubs.delete(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VHUB_NAME'),
    custom_headers=None,
    raw=False,
    polling=True
)
async_vhub_deletion.wait()
print(async_vhub_deletion.result())
print('VHUB Deleted')

# Delete VWAN
async_vwan_deletion = network_client.virtual_wans.delete(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VWAN_NAME'),
    custom_headers=None,
    raw=False,
    polling=True
)
async_vwan_deletion.wait()
print(async_vwan_deletion.result())
print('VWAN Deleted')
