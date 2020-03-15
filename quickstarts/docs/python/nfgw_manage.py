#!/usr/bin/python3
"""Manage Gateways on the NFN Network."""
import yaml
from os import environ, path
from datetime import datetime
import argparse
import re
from subprocess import Popen, PIPE, TimeoutExpired
import nf_token as nftn
import nf_network as nfnk
import nf_gateway as nfgw
import nf_tf_main_file as nftmf


def clear_log():
    """Clear logs."""
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    """Write a log."""
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def terraform_command(command):
    """Execute Terraform Commands."""
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
    """Update config file."""
    try:
        with open(filename, 'w') as f:
            yaml.dump(new_config, f)
    except Exception as e:
        writelog(str(e))


def gateway_delete_update(netUrl, name, token, action, **kargs):
    """Delete or Update a given gateway."""
    gwUrl = nfgw.find_gateway(netUrl, name, token)
    if gwUrl:
        # action is to delete the existing gateway
        if action == 'delete':
            nfgw.delete_gateway(gwUrl, token)
    else:
        # action is to add a new gateway if one does not exist
        if action == 'add':
            name, regkey = nfgw.create_gateway(kargs['env'], netUrl,
                                               kargs['region'], kargs['cloud'],
                                               kargs['index'], token, gwName=name)
            return regkey


def main(filename, action):
    """Manage creating and deploying to cloud NFN Cloud Gateways."""
    # when processing string from POPEN need to strip escape characters
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    # clear logoutput file
    nftn.clear_log()
    # get resources to configure from file
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        writelog(str(e))
    # initialized env variable with the passed Environment Variable
    env = environ.get('ENVIRONMENT')
    if action == 'create' or action == 'delete' or action == 'add':
        # get network url
        token = nftn.get_token(env, environ.get('SMOKE_TEST_USER'),
                               environ.get('SMOKE_TEST_PASS'))
        writelog('Searching for network id')
        netUrl = nfnk.find_network(env, environ.get('NFN_NAME'), token)
        print(netUrl)

        # manage gateways (list of gateways)
        for gateway in config['gateway_list']:
            # need to add this be comparable with script using the yaml file as input for action
            if action == 'create-terraform':
                gateway['action'] = 'create-terraform'
            if action == 'delete-terraform':
                gateway['action'] = 'delete-terraform'
            if action == 'add-terraform':
                gateway['action'] = 'add-terraform'
            if action == 'create':
                gateway['action'] = 'create'
                index = 0
                while index < gateway['count']:
                    name, regkey = nfgw.create_gateway(env, netUrl,
                                                       gateway['region'],
                                                       gateway['cloud'],
                                                       index, token)
                    index += 1
                    gateway['names'] = gateway['names'] + [name]
                    gateway['regkeys'] = gateway['regkeys'] + [regkey]
            if action == 'delete' and gateway['names']:
                gateway['action'] = 'delete'
                for name in gateway['names']:
                    gateway_delete_update(netUrl, name, token, gateway['action'])
                gateway['names'] = []
                gateway['regkeys'] = []
            if action == 'add' and gateway['names']:
                gateway['action'] = 'add'
                for name in gateway['names']:
                    regkey = gateway_delete_update(netUrl, name, token,
                                                   gateway['action'],
                                                   region=gateway['region'],
                                                   cloud=gateway['cloud'],
                                                   index=gateway['count'],
                                                   env=env)
                    gateway['regkeys'] = gateway['regkeys'] + [regkey]
        # update config file
        update_config_file(filename, config)
    if action == 'create-terraform':
        # create template for terraform
        nftmf.create_file(config)

        command = "terraform init -no-color %s" % path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

        command = "terraform workspace new -state=%s %s" % \
            (path.expanduser(config['terraform']['work_dir']), env)
        sout, serr = terraform_command(command)
        newSerr = ansi_escape.sub('', serr).rstrip().lower().replace('\"', '')
        if newSerr == ('workspace %s already exists' % env):
            command = "terraform workspace select %s" % env
            terraform_command(command)

        # command = "terraform apply --auto-approve %s" % \
        # os.path.expanduser(config['terraform']['work_dir'])
        # terraform_command(command)

    if action == 'delete-terraform':
        # update config file
        update_config_file(filename, config)

        command = "terraform init -no-color %s" % path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

        command = "terraform workspace select %s" % env
        terraform_command(command)

        # command = "terraform destroy --auto-approve %s" %
        # path.expanduser(config['terraform']['work_dir'])
        # terraform_command(command)

    if action == 'add-terraform':
        # create template for terraform
        nftmf.add_to_file(config)

        command = "terraform init -no-color %s" % path.expanduser(config['terraform']['work_dir'])
        terraform_command(command)

        command = "terraform workspace new -state=%s %s" %\
            (path.expanduser(config['terraform']['work_dir']), env)
        sout, serr = terraform_command(command)
        newSerr = ansi_escape.sub('', serr).rstrip().lower().replace('\"', '')
        if newSerr == ('workspace %s already exists' % env):
            command = "terraform workspace select %s" % env
            terraform_command(command)

        # command = "terraform apply --auto-approve %s" % \
        # path.expanduser(config['terraform']['work_dir'])
        # terraform_command(command)

    # manage deployment of gateways with terraform
    if config.get('terraform'):
        # if options for terraform are configured, execute the following conditional statements
        if config['terraform']['output'] == "yes":

            command = "terraform init -no-color %s" % \
                path.expanduser(config['terraform']['work_dir'])
            terraform_command(command)

            command = "terraform workspace select %s" % env
            terraform_command(command)

            # command = "terraform output -state=%s" % \
            # path.expanduser(config['terraform']['work_dir'])
            command = "terraform output -json"
            outs, errs = terraform_command(command)
            print(outs)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network build script')
    parser.add_argument("--file", help="json file with netfoundry resources details \
                        to create/update/delete", required=True)
    parser.add_argument("--action", choices=['create', 'delete', 'add', 'create-terraform',
                                             'delete-terraform', 'add-terraform'],
                        help="json file with netfoundry resources details\
                                             to create/add/delete", required=True)
    args = parser.parse_args()
    main(args.file, args.action)
