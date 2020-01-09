#!/usr/bin/python3

import os
import time
import re
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute.models import DiskCreateOption

# setup Azure Login Credentials from Environmental Variables
credentials = ServicePrincipalCredentials(
    client_id = os.environ.get('ARM_CLIENT_ID'),
    secret = os.environ.get('ARM_CLIENT_SECRET'),
    tenant = os.environ.get('ARM_TENANT_ID')
)

# Connect to Azure APIs and get session details
storage_client = StorageManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))
compute_client = ComputeManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

# Trying to create a managed disk from a blob storage disk
async_managed_disk_creation = compute_client.disks.create_or_update(
    'my_resource_group',
    'my_disk_name',
    {
        'location': 'eastus',
        'creation_data': {
            'create_option': DiskCreateOption.import_enum,
            'source_uri': 'https://bg09.blob.core.windows.net/vm-images/non-existent.vhd'
        }
    }
)
disk_resource = async_managed_disk_creation.result()

# Trying to create an image from a blob storage disk
async_image_creation = compute_client.images.create_or_update(
    'my_resource_group',
    'my_image_name',
    {
        'location': 'eastus',
        'storage_profile': {
           'os_disk': {
              'os_type': 'Linux',
              'os_state': "Generalized",
              'blob_uri': 'https://bg09.blob.core.windows.net/vm-images/non-existent.vhd',
              'caching': "ReadWrite",
           }
        }
    }
)
image_resource = async_managed_disk_creation.result()
