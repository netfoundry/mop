#!/usr/bin/python3

import os
import json
import nf_tf_modules as nftm


def create_file(config):
    tf_main = {"module":[],"output":[]}
    for module in config['gateway_list']:
        if module['action'] == 'create' or module['action'] == 'create-terraform':
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
    filename = "%s/main.tf.json" % os.path.expanduser(config['terraform']['work_dir'])
    with open(filename, 'w') as f:
        json.dump(tf_main, f)

#      find_vpc_key = {key: tf_template[key] for key in tf_template.keys()
#                               & {gateway['region']}}
#                    if find_vpc_key:
