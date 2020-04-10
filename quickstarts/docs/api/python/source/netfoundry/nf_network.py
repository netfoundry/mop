#!/usr/bin/python3
"""Manage NF Network in MOP Environment."""
import sys
import time
from datetime import datetime
import argparse
from nf_requests import nf_req as nfreq


def clear_log():
    """Clear logs."""
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    """Write a log."""
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def create_network(env, name, token):
    """Create NF Resources in MOP Environment."""
    # Create new Network specified by --name commandline argument
    net_name = name
    writelog('\nCreating new Network! \n')
    url = 'https://gateway.' + env + '.netfoundry.io/rest/v1/networks'
    start = datetime.now()
    network_id = nfreq((url, {"name": net_name}), "post", token)
    #  "productFamily": "Ziti_Enabled", "productVersion" : "4.19.0-57168534"
    end = datetime.now()
    diff = end - start
    create_time = diff.seconds + diff.microseconds / (1000 * 1000.0)
    writelog("response_time = " + str(create_time))
    try:
        netUrl = network_id['_links']['self']['href']
    except Exception as e:
        writelog(e)
        writelog('\nnetwork not created!\n' + str(network_id))
        sys.exit(0)
    start = datetime.now()
    try:
        net_status = False
        writelog('\nWaiting for network \"' + network_id['name']
                 + '\" to be ready @ 10 to 20 minutes! \n')
        while not net_status:
            now = datetime.now()
            delta = now - start
            minutes = delta.seconds / 60.0
            result = nfreq(netUrl, "get", token)
            if result['status'] == 200:
                status = 'NOT READY'
                writelog('\nnetwork build status = ' + status +
                         ' time waiting = ' + str(minutes) + ' Minutes')
            if result['status'] == 300:
                writelog('\nnetwork build status = FINISHED, time waited = '
                         + str(minutes) + 'Minutes')
                net_status = True
            if minutes > 30:
                writelog('\nExcesive time waitng for Network to transition!\n')
                writelog('deleting network: ' + url)
                nfreq(url, "delete", token)
                sys.exit(0)
            time.sleep(20)
    except Exception as e:
        writelog(e)
        writelog('\nError Unable to check network status!\n')
        sys.exit(0)
    return netUrl


def find_network(env, name, token):
    """Find NF Network in MOP Environment."""
    url = 'https://gateway.' + env + '.netfoundry.io/rest/v1/networks'
    networks = nfreq(url, "get", token)['_embedded']['networks']
    writelog('\nNetworks found are\n')
    writelog(networks)
    for network in networks:
        writelog('\nNetwork name searched is ' + network['name'])
        writelog('\nNetwork name given is ' + name)
        if network['name'] == name:
            net_url = (network['_links']['self']['href'])
            return net_url
    writelog('network not found!')
    return None


def delete_network(netUrl, token):
    """Delete NF Network in MOP Environment."""
    data = nfreq(netUrl, "delete", token)
    writelog(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Network build script')
    parser.add_argument("--action", help="", required=True)
    parser.add_argument("--name", help="network name to be used")
    parser.add_argument("--token", help="session token", required=True)
    parser.add_argument("--env", help="NetFoundry Enviroment")
    parser.add_argument("--url", help="existing network url")
    args = parser.parse_args()
    if args.action == "create":
        print(create_network(args.env, args.name, args.token))
    if args.action == "find":
        print(find_network(args.env, args.name, args.token))
    if args.action == "delete":
        delete_network(args.url, args.token)
