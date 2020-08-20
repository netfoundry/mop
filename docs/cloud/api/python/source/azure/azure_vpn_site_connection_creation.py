#!/usr/bin/python3
"""Connect VPN Site to VPN Gateway."""
import os
import time
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ.get('ARM_CLIENT_ID'),
    secret=os.environ.get('ARM_CLIENT_SECRET'),
    tenant=os.environ.get('ARM_TENANT_ID')
)

# declaire Test Input Variables
CONNECTION_PARAMS = {
    'enable_bgp': True,
    'remote_vpnsite': {
      'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/vpnSites/%s"
      % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'),
         os.environ.get('VPN_SITE_NAME'))
    }
}

# Trying to find the name of the vpn site created by NF

# Connect to Azure APIs and get session details
network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# Delay for 30 seconds before deleting resources
time.sleep(60)

# Create VPN Site Connection to VPNG
async_vpn_site_connection_creation = network_client.vpn_connections.create_or_update(
    os.environ.get('GROUP_NAME'),
    os.environ.get('VPNG_NAME'),
    'CONNECTION_' + os.environ.get('VPN_SITE_NAME'),
    CONNECTION_PARAMS,
    custom_headers=None,
    raw=False,
    polling=True
)
async_vpn_site_connection_creation.wait()
print(async_vpn_site_connection_creation.result())
