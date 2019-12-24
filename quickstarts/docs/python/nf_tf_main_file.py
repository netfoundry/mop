#!/usr/bin/python3

import os
import json
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
                    output = "public_ips_" + str(module['names'][index])
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
                                          os.path.expanduser(config['terraform']['source']))
                    tf_main["module"] = tf_main["module"] + [{module['names'][index]: vm}]
                    output = "public_ips_" + str(module['names'][index])
                    value = nftm.create_output(module['names'][index])
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

#      find_vpc_key = {key: tf_template[key] for key in tf_template.keys()
#                               & {gateway['region']}}
#                    if find_vpc_key:
