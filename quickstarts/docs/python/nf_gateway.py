#!/usr/bin/python3

import os
import sys
import time
import datetime
import logging
import argparse
import nf_requests as nfreq


def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' gateway-log ' + str(message) + '\n')
    logfile.close()


def create_gateway(env, netUrl, loc, type, index, token, **kargs):
    # Create AWS GW(s)
    url = 'https://gateway.' + env + '.netfoundry.io/rest/v1/dataCenters'
    # find dc id based on location code
    datacenters = nfreq.get_data(url, token)['_embedded']['dataCenters']
    dcId = None
    for dc in datacenters:
        if dc['locationCode'] == loc:
            dcId = dc['_links']['self']['href'].split('/')[6]
    gwUrl = netUrl + '/endpoints'
    if type == 'aws':
        gwType = 'AWSCPEGW'
    if type == 'azure':
        gwType = 'AZCPEGW'
    if type == 'vwan':
        gwType = 'AVWGW'
    # checking if gateway name was passed as one of **kargs
    try:
        gwName = kargs['gwName']
    except KeyError:
        gwName = gwType +'x'+ str(index) +'x'+ loc.upper()
    new_gw = nfreq.post_data(gwUrl, {"name": gwName,
                             "endpointType": gwType,
                             "geoRegionId": None,
                             "dataCenterId": dcId,
                             "o365BreakoutNextHopIp": None}, token)
    try:
        gwName = new_gw['name']
    except TypeError as terr:
        print(terr.args[0])
        sys.exit(1)
    gwRegKey = new_gw['registrationKey']
    gwUrl = new_gw['_links']['self']['href']
    gwstatus = False
    writelog('\nWaiting for GW to be ready for service assignment!\n')
    while not gwstatus:
        try:
            result = nfreq.get_data(gwUrl, token)
            if result['status'] == 300:
                writelog('\ngw is ready to assign service!\n')
                gwstatus = True
        except Exception as e:
            writelog(e)
            writelog('\nError checking GW status!\n')
        time.sleep(5)
    return gwName, gwRegKey


def find_gateway(netUrl, name, token):
    gwsUrl = netUrl + '/endpoints'
    try:
        gateways = nfreq.get_data(gwsUrl, token)['_embedded']['endpoints']
        gwUrl = ''
        for gateway in gateways:
            if gateway['name'] == name:
                gwUrl = gateway['_links']['self']['href']
        return gwUrl
    except KeyError:
        return None


def delete_gateway(gwUrl, token):
    data = nfreq.delete_nf(gwUrl, token)
    writelog(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gateway build script')
    parser.add_argument("--action", help="", required=True)
    parser.add_argument("--type", choices=['azure', 'aws'], help="gateway type to be provisioned")
    parser.add_argument("--name", help="existing gateway name to be found")
    parser.add_argument("--url", help="existing gateway url to be delete")
    parser.add_argument("--token", help="session token", required=True)
    parser.add_argument("--env", choices=['sandbox', 'staging', 'production'], help="NetFoundry Enviroment")
    parser.add_argument("--network_url", help="existing network url")
    parser.add_argument("--location", help="gateway location")
    parser.add_argument("--count", default=1, help="gateway count in the same location")
    args = parser.parse_args()
    if args.action == "create":
        print(create_gateway(args.env, args.network_url, args.location, args.type, args.count, args.token))
    if args.action == "find":
        print(find_gateway(args.network_url, args.name, args.token))
    if args.action == "delete":
        delete_gateway(args.url, args.token)
