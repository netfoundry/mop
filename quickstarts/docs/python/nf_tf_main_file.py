#!/usr/bin/python3

import os
import json
import yaml
import argparse
import nf_tf_modules as nftm

def create_list_keys(list):
    new_list = []
    for item in list:
        for key in item.keys():
            new_list = new_list + [key]
    return new_list

def create_file(config):
    tf_main = {"module":[],"output":[]}
    for module in config['gateway_list']:
        if module['action'] == 'create' or module['action'] == 'create-terraform':
            if module['cloud'] == 'aws':
                vpc = nftm.create_vpc(module['region'],
                                      module['public_subnet'],
                                      module['private_subnet'],
                                      os.path.expanduser(config['terraform']['source']))
                index = 0
                while index < module['count']:
                    vm = nftm.create_vm_aws(module['region'],
                                          module['region'],
                                          module['ami'],
                                          module['names'][index],
                                          module['regkeys'][index],
                                          os.path.expanduser(config['terraform']['source']))
                    tf_main["module"] = tf_main["module"] + [{module['names'][index]: vm}]
                    output = str(module['names'][index])
                    value = nftm.create_output(module['names'][index])
                    tf_main["output"] = tf_main["output"] + [{output: value}]
                    index += 1
                tf_main["module"] = tf_main["module"] + [{module['region']: vpc}]
            if module['cloud'] == 'azure' or module['cloud'] == 'vwan':
                rg = nftm.create_rg_azure(module['resourceGroup'],
                                      module['tag'],
                                      os.path.expanduser(config['terraform']['source']))
                vnet = nftm.create_vnet_azure(module['resourceGroup']['region']+'_rg',
                                      module['region'],
                                      module['regionalCidr'],
                                      module['tag'],
                                      os.path.expanduser(config['terraform']['source']))
                index = 0
                while index < module['count']:
                    vm = nftm.create_vm_azure(module['resourceGroup']['region']+'_rg',
                                          module['region'],
                                          module['names'][index],
                                          module['regkeys'][index],
                                          module['region']+'_vnet',
                                          module['tag'],
                                          os.path.expanduser(config['terraform']['source']),
                                          module.get('imageType', 'marketplace'),
                                          module.get('imageId', ''))
                    tf_main["module"] = tf_main["module"] + [{module['names'][index]: vm}]
                    for item in ['public_ips', 'private_ips']:
                        output = str(module['names'][index]) + '_' + item
                        value = nftm.create_output(module['names'][index], item)
                        tf_main["output"] = tf_main["output"] + [{output: value}]
                    index += 1
                # check if the new modlue is not already created, eliminate duplicates
                check_list = create_list_keys(tf_main["module"])
                if module['resourceGroup']['region']+'_rg' not in check_list:
                    tf_main["module"] = tf_main["module"] + [{module['resourceGroup']['region']+'_rg': rg}]
                if module['region']+'_vnet' not in check_list:
                    tf_main["module"] = tf_main["module"] + [{module['region']+'_vnet': vnet}]
    filename = "%s/main.tf.json" % os.path.expanduser(config['terraform']['work_dir'])
    with open(filename, 'w') as f:
        json.dump(tf_main, f)

def add_to_file(config):
    filename = "%s/main.tf.json" % os.path.expanduser(config['terraform']['work_dir'])
    try:
        with open(filename, 'r') as f:
            tf_main = json.load(f)
    except Exception as e:
        print(str(e))
    for module in config['gateway_list']:
        if module['action'] == 'add' or module['action'] == 'add-terraform':
            if module['cloud'] == 'aws':
                vpc = nftm.create_vpc(module['region'],
                                      module['public_subnet'],
                                      module['private_subnet'],
                                      os.path.expanduser(config['terraform']['source']))
                index = 0
                while index < module['count']:
                    vm = nftm.create_vm_aws(module['region'],
                                          module['region'],
                                          module['ami'],
                                          module['names'][index],
                                          module['regkeys'][index],
                                          os.path.expanduser(config['terraform']['source']))
                    tf_main["module"] = tf_main["module"] + [{module['names'][index]: vm}]
                    output = str(module['names'][index])
                    value = nftm.create_output(module['names'][index])
                    tf_main["output"] = tf_main["output"] + [{output: value}]
                    index += 1
                tf_main["module"] = tf_main["module"] + [{module['region']: vpc}]
            if module['cloud'] == 'azure' or module['cloud'] == 'vwan':
                rg = nftm.create_rg_azure(module['resourceGroup'],
                                      module['tag'],
                                      os.path.expanduser(config['terraform']['source']))
                vnet = nftm.create_vnet_azure(module['resourceGroup']['region']+'_rg',
                                      module['region'],
                                      module['regionalCidr'],
                                      module['tag'],
                                      os.path.expanduser(config['terraform']['source']))
                index = 0
                while index < module['count']:
                    vm = nftm.create_vm_azure(module['resourceGroup']['region']+'_rg',
                                          module['region'],
                                          module['names'][index],
                                          module['regkeys'][index],
                                          module['region']+'_vnet',
                                          module['tag'],
                                          os.path.expanduser(config['terraform']['source']),
                                          module.get('imageType', 'marketplace'),
                                          module.get('imageId', ''))
                    tf_main["module"] = tf_main["module"] + [{module['names'][index]: vm}]
                    for item in ['public_ips', 'private_ips']:
                        output = str(module['names'][index]) + '_' + item
                        value = nftm.create_output(module['names'][index], item)
                        tf_main["output"] = tf_main["output"] + [{output: value}]
                    index += 1
                # check if the new modlue is not already created, eliminate duplicates
                check_list = create_list_keys(tf_main["module"])
                if module['resourceGroup']['region']+'_rg' not in check_list:
                    tf_main["module"] = tf_main["module"] + [{module['resourceGroup']['region']+'_rg': rg}]
                if module['region']+'_vnet' not in check_list:
                    tf_main["module"] = tf_main["module"] + [{module['region']+'_vnet': vnet}]
    filename = "%s/main.tf.json" % os.path.expanduser(config['terraform']['work_dir'])
    with open(filename, 'w') as f:
        json.dump(tf_main, f)

def clear_file(config):
    tf_main = {"module":[],"output":[]}
    filename = "%s/main.tf.json" % os.path.expanduser(config['terraform']['work_dir'])
    with open(filename, 'w') as f:
        json.dump(tf_main, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Terraform Main File Builder')
    parser.add_argument("--file", help="json file with NetFoundry resources details to build", required=True)
    parser.add_argument("--action", choices=['create', 'add', 'clear'], help="action to perform on the Terraform Main File", required=True)
    args = parser.parse_args()
    try:
        with open(args.file, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(str(e))
    if args.action == 'create':
        print(create_file(config))
    if args.action == 'add':
        print(add_to_file(config))
    if args.action == 'clear':
        print(clear_file(config))
