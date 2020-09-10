#!/usr/bin/python3
"""Check VPN Site Connection Status to VPN Gateway."""
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

# Get VPN Site Connection Status to VPNG
async_vpn_site_connection_get = network_client.vpn_connections.get(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VPNG_NAME'),
    'CONNECTION_' + os.environ.get('VPN_SITE_NAME'),
    custom_headers=None,
    raw=False
)
print(async_vpn_site_connection_get.result())
status = async_vpn_site_connection_get.result("connection_status")
print('VPN Site Connection to VPNG Status Checked')
