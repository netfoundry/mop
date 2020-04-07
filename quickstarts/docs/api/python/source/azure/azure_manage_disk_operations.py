#!/usr/bin/python3
"""Manage the image disk."""
import os
import argparse
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials


def connect():
    """Set up Azure Login Credentials from Environmental Variables."""
    credentials = ServicePrincipalCredentials(
        client_id=os.environ.get('ARM_CLIENT_ID'),
        secret=os.environ.get('ARM_CLIENT_SECRET'),
        tenant=os.environ.get('ARM_TENANT_ID')
    )
    compute_client = ComputeManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))
    imageName = 'nf-' + os.environ.get('IMAGE_TYPE') + '-' + os.environ.get('IMAGE_VERSION')
    return compute_client, imageName


def image_create():
    """Try to create an image from a blob storage disk."""
    imageId = os.environ.get('IMAGE_ID')
    compute_client, imageName = connect()
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
    """Try to delete create image from blob storage disk."""
    compute_client, imageName = connect()
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
    """Try to show details of the created image from blob storage disk."""
    compute_client, imageName = connect()
    async_image_get = compute_client.images.get(
        os.environ.get('GROUP_NAME'),
        imageName,
        custom_headers=None,
        raw=False,
        polling=True
    )
    print(async_image_get)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='New Image Operations')
    parser.add_argument("--action", choices=['create', 'delete', 'get'],
                        help="Action you want to do on the new image create, delete",
                        required=True)
    args = parser.parse_args()
    if args.action == 'create':
        image_create()
    if args.action == 'delete':
        image_delete()
    if args.action == 'get':
        image_get()
