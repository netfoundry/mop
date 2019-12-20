#!/usr/bin/python3

import requests
import json
import yaml
import os
import sys
import time
import datetime
import logging
import argparse
import re
from subprocess import Popen, PIPE, TimeoutExpired
import nf_token as nftn
import nf_network as nfnk
import nf_gateway as nfgw
import nf_tf_main_file as nftmf
import nf_service as nfsrv
import nf_appwan as nfaw


def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def terraform_command(command):
    with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as proc:
        try:
            outs, errs = proc.communicate(timeout=15)
        except TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
    if outs:
        writelog(outs.decode('ascii'))
    elif errs:
        writelog(errs.decode('ascii'))
    else:
        writelog('%s successfully' % command)
    sout = outs.decode('ascii')
    serr = errs.decode('ascii')
    return sout, serr


def update_config_file(filename, new_config):
    # update config file
    try:
        with open(filename, 'w') as f:
            yaml.dump(new_config, f)
    except Exception as e:
        writelog(str(e))


def main(filename, action):
    # when processing string from POPEN need to strip escape characters
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # get resources to configure from file
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        writelog(str(e))
    # get network url
    env = os.environ.get('ENVIRONMENT')
    token = nftn.get_token(env, os.environ.get('SMOKE_TEST_USER'), os.environ.get('SMOKE_TEST_PASS'))
    writelog('Searching for network id')
    netUrl = nfnk.find_network(env, os.environ.get('NFN_NAME'), token)

    # manage gateways (list of gateways)
    for gateway in config['gateway_list']:
        # need to add this be comparable with script using the yaml file as input for action
        if action == 'create-terraform':
            gateway['action'] = 'create-terraform'
        if action == 'delete-terraform':
            gateway['action'] = 'delete-terraform'
        if action == 'create':
            gateway['action'] = 'create'
            index = 0
            while index < gateway['count']:
                name, regkey = nfgw.create_gateway(env, netUrl, gateway['region'],
                                                                      gateway['cloud'], index, token)
                index += 1
                gateway['names'] = gateway['names'] + [name]
                gateway['regkeys'] = gateway['regkeys'] + [regkey]
        if action == 'delete' and gateway['names']:
            gateway['action'] = 'delete'
            for name in gateway['names']:
                try :
                    gwUrl = nfgw.find_gateway(netUrl, name, token)
                    nfgw.delete_gateway(gwUrl, token)
                except Exception as e:
                    writelog(str(e))
            gateway['names'] = []
            gateway['regkeys'] = []
    if list(filter(lambda gateway: action == 'create' or
              action == 'create-terraform', config['gateway_list'])):
        # update config file
        update_config_file(filename, config)

        # create template for terraform
        nftmf.create_file(config)

        command = "terraform init -no-color %s" % os.path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

        command = "terraform workspace new -state=%s %s" % (os.path.expanduser(config['terraform']['work_dir']), env)
        sout, serr = terraform_command(command)
        newSerr = ansi_escape.sub('', serr).rstrip().lower().replace('\"', '')
        if newSerr == ('workspace %s already exists' % env):
            command = "terraform workspace select %s" % env
            terraform_command(command)

        command = "terraform apply --auto-approve %s" % os.path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

    if list(filter(lambda gateway: action == 'delete' or
              action == 'delete-terraform', config['gateway_list'])):
        # update config file
        update_config_file(filename, config)

        command = "terraform init -no-color %s" % os.path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

        command = "terraform workspace select %s" % env
        terraform_command(command)

        command = "terraform destroy --auto-approve %s" % os.path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

    # manage deployment of gateways with terraform
    if config.get('terraform'):
        #if options for terraform are configured, execute the following conditional statements
        if config['terraform']['output'] == "yes":

            command = "terraform init -no-color %s" % os.path.expanduser(config['terraform']['work_dir'])
            terraform_command(command)

            command = "terraform workspace select %s" % env
            terraform_command(command)

            #command = "terraform output -state=%s" % os.path.expanduser(config['terraform']['work_dir'])
            command = "terraform output -json"
            outs, errs = terraform_command(command)
            print(outs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network build script')
    parser.add_argument("--file", help="json file with netfoundry resources details to create/update/delete", required=True)
    parser.add_argument("--action", choices=['create', 'delete', 'create-terraform', 'delete-terraform'], help="json file with netfoundry resources details to create/update/delete", required=True)
    args = parser.parse_args()
    main(args.file, args.action)
