#!/usr/bin/python3

import os
import argparse
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

def connect():
    # setup Azure Login Credentials from Environmental Variables
    credentials = ServicePrincipalCredentials(
        client_id = os.environ.get('ARM_CLIENT_ID'),
        secret = os.environ.get('ARM_CLIENT_SECRET'),
        tenant = os.environ.get('ARM_TENANT_ID')
    )

    network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

    return network_client

def update_security_group(rules):
    sgName = os.environ.get('ZEDE_NAME') + '-securityGroup'
    network_client = connect()
    # Trying to update  security group named as sgName
    for index, rule in enumerate(rules):
        # trying to split the string to seperate protocol from port
        name = rule.split(',')[0] + '_' + rule.split(',')[1]
        async_sg_update = network_client.security_rules.create_or_update(
            os.environ.get('GROUP_NAME'),
            sgName,
            name,
            security_rule_parameters = {
                'protocol': rule.split(',')[0],
                'source_port_range': '*',
                'destination_port_range': rule.split(',')[1],
                'source_address_prefix': '*',
                'destination_address_prefix': '*',
                'access': 'allow',
                'priority': 1010 + index,
                'direction': 'Inbound',
                'name': name
            }
        )
        async_sg_update.wait()
        print(async_sg_update.result())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Security Group Operations')
    parser.add_argument("--action", choices=['update'], help="Action you want to do on a given security group", required=True)
    parser.add_argument("--rules", nargs='+', help='List of rule (port, protocol) to add to a given security group , e.g. [ "tcp,22" "tcp,443" ]', required=True)
    args = parser.parse_args()
    if args.action == 'update':
        update_security_group(args.rules)
