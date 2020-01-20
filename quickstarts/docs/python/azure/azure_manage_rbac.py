#!/usr/bin/python3

import os
import sys
import argparse
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.common.credentials import ServicePrincipalCredentials

def connect():
    # setup Azure Login Credentials from Environmental Variables
    credentials = ServicePrincipalCredentials(
        client_id = os.environ.get('ARM_CLIENT_ID'),
        secret = os.environ.get('ARM_CLIENT_SECRET'),
        tenant = os.environ.get('ARM_TENANT_ID')
    )

    #network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))
    auth_management_client = AuthorizationManagementClient(credentials,
                                          os.environ.get('ARM_SUBSCRIPTION_ID'),
                                          api_version=None, base_url=None)
    return auth_management_client


def create(roleName, principalId):
    scope = '/subscriptions/%s/resourceGroups/%s' % (
                                os.environ.get("ARM_SUBSCRIPTION_ID"),
                                os.environ.get("GROUP_NAME"))
    roleGUID, roleDefinitionId = list_role_definitions(roleName)
    auth_management_client = connect()
    # Trying to assign role to VM
    async_rbac_create = auth_management_client.role_assignments.create(
        scope,
        roleGUID,
        parameters = {
            'role_definition_id': roleDefinitionId,
            'principal_id': principalId
        }
    )
    print(async_rbac_create)


def delete(roleName):
    scope = '/subscriptions/%s/resourceGroups/%s' % (
                                os.environ.get("ARM_SUBSCRIPTION_ID"),
                                os.environ.get("GROUP_NAME"))
    roleGUID, roleDefinitionId = list_role_definitions(roleName)
    auth_management_client = connect()
    # Trying to assign role to VM
    async_rbac_delete = auth_management_client.role_assignments.delete(
        scope,
        roleGUID
    )
    print(async_rbac_delete)


def list_role_definitions(roleName):
    roleName = roleName.replace("_"," ")
    scope = '/subscriptions/%s/resourceGroups/%s' % (
                                          os.environ.get("ARM_SUBSCRIPTION_ID"),
                                          os.environ.get("GROUP_NAME")
                                          )
    auth_management_client = connect()
    # Trying to assign role to VM
    async_rbac_list_role_def = auth_management_client.role_definitions.list(
        scope,
        filter=None
    )
    for role in async_rbac_list_role_def:
        if role.role_name == roleName:
            return role.name, role.id


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RBAC Operations')
    parser.add_argument("--action", choices=['create', 'delete', 'list_role_definitions'], help="Action to perform for RBAC", required=True)
    parser.add_argument("--role_name", help="Name of the role that need to be \
                        applied, if two words, join them with _, e.g. \
                        Network Contributor = Network_Contributor")
    parser.add_argument("--principal_id", help="Principal ID of the assigned Identity")
    args = parser.parse_args()
    if args.action == 'create':
        if args.role_name and args.principal_id:
            create(args.role_name, args.principal_id)
        else:
            print('role_name or principal_id or both are missing')
            sys.exit(1)
    if args.action == 'delete':
        if args.role_name:
            delete(args.role_name)
        else:
            print('role_name is missing')
            sys.exit(1)
    if args.action == 'list_role_definitions':
        if args.role_name:
            print(list_role_definitions(args.role_name))
        else:
            print('role_name is missing')
            sys.exit(1)
