#!/usr/bin/python3
"""
The script will manage a vm.

Requirement for this script to work is to have the following variables:

exported as Environment Variables:
ARM_CLIENT_ID
ARM_CLIENT_SECRET
ARM_TENANT_ID
ARM_SUBSCRIPTION_ID
GROUP_NAME:  resource group name
ZEDE_NAME: virtual machine name
"""


import os
import argparse
from azure.mgmt.compute import ComputeManagementClient
from azure.common.credentials import ServicePrincipalCredentials


def connect():
    """Import Azure Login Credentials from Environmental Variables."""
    credentials = ServicePrincipalCredentials(
        client_id=os.environ.get('ARM_CLIENT_ID'),
        secret=os.environ.get('ARM_CLIENT_SECRET'),
        tenant=os.environ.get('ARM_TENANT_ID')
    )
    # Connect to Azure APIs and return session details
    return ComputeManagementClient(credentials,
                                   os.environ.get('ARM_SUBSCRIPTION_ID'))


def start_vm():
    """Start the VM."""
    compute_client = connect()
    async_vm_start = compute_client.virtual_machines.start(
       os.environ.get('GROUP_NAME'),
       os.environ.get('ZEDE_NAME')
    )
    async_vm_start.wait()
    print(async_vm_start.result())


def restart_vm():
    """Restart the VM."""
    compute_client = connect()
    async_vm_restart = compute_client.virtual_machines.restart(
        os.environ.get('GROUP_NAME'),
        os.environ.get('ZEDE_NAME')
    )
    async_vm_restart.wait()
    print(async_vm_restart.result())


def stop_vm():
    """Stop the VM."""
    compute_client = connect()
    async_vm_stop = compute_client.virtual_machines.power_off(
        os.environ.get('GROUP_NAME'),
        os.environ.get('ZEDE_NAME')
    )
    async_vm_stop.wait()
    print(async_vm_stop.result())


def get_vm():
    """Show VM Details."""
    compute_client = connect()
    async_vm_get = compute_client.virtual_machines.get(
        os.environ.get('GROUP_NAME'),
        os.environ.get('ZEDE_NAME')
    )
    return async_vm_get


def list_vms_by_subscription():
    """List VMs in subscription."""
    compute_client = connect()
    for vm in compute_client.virtual_machines.list_all():
        print("\tVM: {}".format(vm.name))


def list_vms_by_resource_group():
    """List VM in resource group."""
    compute_client = connect()
    for vm in compute_client.virtual_machines.list(os.environ.get('GROUP_NAME')):
        print("\tVM: {}".format(vm.name))


def delete_vm():
    """Delete VM."""
    compute_client = connect()
    async_vm_delete = compute_client.virtual_machines.delete(
        os.environ.get('GROUP_NAME'),
        os.environ.get('ZEDE_NAME')
    )
    async_vm_delete.wait()
    print(async_vm_delete.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Virtual Machine Operations')
    parser.add_argument("--action", choices=['start', 'restart', 'stop', 'get',
                                             'list_by_subscription',
                                             'list_by_resource_group',
                                             'delete'],
                        help="Action one wants to perform on a virtual machine",
                        required=True)
    args = parser.parse_args()
    if args.action == 'start':
        start_vm()
    if args.action == 'restart':
        restart_vm()
    if args.action == 'stop':
        stop_vm()
    if args.action == 'get':
        result = get_vm()
        print(result.identity.principal_id)
    if args.action == 'list_by_subscription':
        list_vms_by_subscription()
    if args.action == 'list_by_resource_group':
        list_vms_by_resource_group()
    if args.action == 'delete':
        delete_vm()
