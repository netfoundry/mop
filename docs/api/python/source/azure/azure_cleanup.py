#!/usr/bin/python3

"""Cleanup storage accounts that are created when VMs are spun up in Azure."""

import os
import re
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id=os.environ.get('ARM_CLIENT_ID'),
    secret=os.environ.get('ARM_CLIENT_SECRET'),
    tenant=os.environ.get('ARM_TENANT_ID')
)

# Connect to Azure APIs and get session details
storage_client = StorageManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))
compute_client = ComputeManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# looking for a storage account created by vwan using vwan name
string = re.compile(os.environ.get('VWAN_NAME').lower().replace('-', ''))
for item in storage_client.storage_accounts.list_by_resource_group(os.environ.get('GROUP_NAME')):
    if re.search(string, item.name):
        storageAccountName = item.name
        # Delete VWAN Storage Account
        async_storage_deletion = storage_client.storage_accounts.delete(
            os.environ.get('GROUP_NAME'),
            storageAccountName,
            custom_headers=None,
            raw=False,
            polling=True
        )
        print(async_storage_deletion)
        print('VWAN Storage Account %s Deleted' % storageAccountName)
