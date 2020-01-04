#!/usr/bin/python3

import os
import time
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials
import logging
logging.basicConfig()
logging.getLogger('msrest').setLevel(logging.DEBUG)

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id = os.environ.get('ARM_CLIENT_ID'),
    secret = os.environ.get('ARM_CLIENT_SECRET'),
    tenant = os.environ.get('ARM_TENANT_ID')
)

# Connect to Azure APIs and get session details
network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

serverVnet = "westus2-vNet"

# Create Virtual Network
async_vnet_list = network_client.virtual_networks.list(
    os.environ.get('GROUP_NAME'),
    custom_headers=None,
    raw=False,
    polling=True
)
for item in async_vnet_list:
    if item.name == serverVnet:
        # add vNet to the vHub connection parameters
        VHUB_PARAMS = {
            "id": "/subscriptions/8699c8dd-f425-46fa-85ef-cefe299aeb4f/resourceGroups/clouddev-smoke/providers/Microsoft.Network/virtualHubs/AVW-PT-VHUB",
            "location": "westus2",
            'virtual_network_connections': [{
                #"name": item.name,
                'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualHubs/%s/hubVirtualNetworkConnections/%s" % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'), os.environ.get('VHUB_NAME'), item.name)
                #"etag": "W/\"2b3110c5-4aea-4612-813a-81babecef5fb\"",
                #"properties": {
                  #"provisioningState": "Succeeded",
                  #"resourceGuid": "8b463835-ef3c-4f14-a172-1d73623e2424",
                #  "remoteVirtualNetwork": {
                #    "id": "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualNetworks/%s" % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'), item.name)
                #  },
                #  "allowHubToRemoteVnetTransit": True,
                #  "allowRemoteVnetToUseHubVnetGateways": True,
                #  "enableInternetSecurity": True
                #}
                #"type": "Microsoft.Network/virtualHubs/hubVirtualNetworkConnections"
            }]
        }
        # Adding Server vNet to the vHub
        async_vhub_creation = network_client.virtual_hubs.create_or_update(
            os.environ.get('GROUP_NAME'),
            os.environ.get('VHUB_NAME'),
            VHUB_PARAMS,
            custom_headers=None,
            raw=False,
            polling=True
        )
