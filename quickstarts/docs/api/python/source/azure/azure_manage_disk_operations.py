#!/usr/bin/python3

import os
import time
import re
import argparse
#from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials
#from azure.storage.common import CloudStorageAccount
#from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
#from azure.mgmt.compute.models import DiskCreateOption

def connect():
    # setup Azure Login Credentials from Environmental Variables
    credentials = ServicePrincipalCredentials(
        client_id = os.environ.get('ARM_CLIENT_ID'),
        secret = os.environ.get('ARM_CLIENT_SECRET'),
        tenant = os.environ.get('ARM_TENANT_ID')
    )

    # Connect to Azure APIs and get session details
    #storage_client = StorageManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))
    compute_client = ComputeManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

    imageName = 'nf-' + os.environ.get('IMAGE_TYPE') + '-' + os.environ.get('IMAGE_VERSION')
    return compute_client, imageName

# Trying to create a managed disk from a blob storage disk
#async_managed_disk_creation = compute_client.disks.create_or_update(
#    os.environ.get('GROUP_NAME'),
#    os.environ.get('MDISK_NAME'),
#    {
#        'location': os.environ.get('DISK_LOC'),
#        'creation_data': {
#            'create_option': DiskCreateOption.import_enum,
#            'source_uri': 'https://edgeimages.blob.core.windows.net/system/Microsoft.Compute/Images/builds/nf-gw-6.0.1-57661618-osDisk.d0839940-a4cf-4826-a4d1-c0ae33a4062e.vhd'
#        }
#    }
#)
#print(async_managed_disk_creation.result())
def image_create():
    imageId = os.environ.get('IMAGE_ID')
    compute_client, imageName = connect()
    # Trying to create an image from a blob storage disk
    async_image_creation = compute_client.images.create_or_update(
        os.environ.get('GROUP_NAME'),
        imageName,
        {
            'location': os.environ.get('DISK_LOC'),
            'hyper_vgeneration': 'v1',
            'storage_profile': {
               'os_disk': {
                  'os_type': 'Linux',
                  'os_state': "Generalized",
                  'blob_uri': "https://edgeimages.blob.core.windows.net/system/Microsoft.Compute/Images/builds/%s-osDisk.%s.vhd" % (imageName, imageId),
                  'caching': "ReadWrite"
               }
            }
        }
    )
    async_image_creation.wait()
    print(async_image_creation.result())

def image_delete():
    compute_client, imageName = connect()
    # trying to delete create image from blob storage disk
    async_image_deletion = compute_client.images.delete(
        os.environ.get('GROUP_NAME'),
        imageName,
        custom_headers=None,
        raw=False,
        polling=True
    )
    async_image_deletion.wait()
    print(async_image_deletion.result())

def image_get():
    compute_client, imageName = connect()
    # trying to show details of the created image from blob storage disk
    async_image_get = compute_client.images.get(
        os.environ.get('GROUP_NAME'),
        imageName,
        custom_headers=None,
        raw=False,
        polling=True
    )
    print(async_image_get)

# Trying to list blobs in an storage account
# List the blobs in the container
#blob_list = container_client.list_blobs()
#for blob in blob_list:
#    print("\t" + blob.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='New Image Operations')
    parser.add_argument("--action", choices=['create', 'delete', 'get'], help="Action you want to do on the new image create, delete", required=True)
    args = parser.parse_args()
    if args.action == 'create':
        image_create()
    if args.action == 'delete':
        image_delete()
    if args.action == 'get':
        image_get()
