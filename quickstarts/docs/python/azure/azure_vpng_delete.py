#!/usr/bin/python3

import os
import time
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id = os.environ.get('ARM_CLIENT_ID'),
    secret = os.environ.get('ARM_CLIENT_SECRET'),
    tenant = os.environ.get('ARM_TENANT_ID')
)

# Connect to Azure APIs and get session details
network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# Delete Server VM

# Delete VPNG
async_vpng_deletion = network_client.vpn_gateways.delete(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VPNG_NAME'),
    custom_headers=None,
    raw=False,
    polling=True
)
async_vpng_deletion.wait()
print(async_vpng_deletion.result())
print('VPNG Deleted')
