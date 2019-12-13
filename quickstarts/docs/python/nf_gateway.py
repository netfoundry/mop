#!/usr/bin/python3

import os
import sys
import time
import datetime
import logging
import nf_requests as nfreq


def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def create_gateway(env, netUrl, loc, type, index, token):
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
    new_gw = nfreq.post_data(gwUrl, {"name": gwType +'-'+ str(index) +'-'+ loc.upper(),
                             "endpointType": gwType,
                             "geoRegionId": None,
                             "dataCenterId": dcId,
                             "o365BreakoutNextHopIp": None}, token)
    gwName = new_gw['name']
    gwRegKey = new_gw['registrationKey']
    gwId = new_gw['_links']['self']['href'].split('/')[8]
    gwstatus = False
    writelog('\nWaiting for GW to be ready for service assignment!\n')
    while not gwstatus:
        try:
            result = nfreq.get_data(gwUrl, token)
            for gw in result['_embedded']['endpoints']:
                if gw['name'] == gwName:
                    if gw['status'] == 300:
                        writelog('\ngw is ready to assign service!\n')
                        gwstatus = True
        except Exception as e:
            writelog(e)
            writelog('\nError checking GW status!\n')
        time.sleep(5)
    return gwName, gwRegKey


def find_gateway(netUrl, name, token):
    gwsUrl = netUrl + '/endpoints'
    gateways = nfreq.get_data(gwsUrl, token)['_embedded']['endpoints']
    gwUrl = ''
    for gateway in gateways:
        if gateway['name'] == name:
            gwUrl = gateway['_links']['self']['href']
    return gwUrl


def delete_gateway(gwUrl, token):
    data = nfreq.delete_nf(gwUrl, token)
    writelog(data)


if __name__ == '__main__':
    pass
