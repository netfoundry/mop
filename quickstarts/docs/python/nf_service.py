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


def create_service(env, netUrl, serviceList, token):
        # Create Services on GW from a service list
        url = netUrl+'/services'
        for service in serviceList:
            if service['type'] == 'Host':
                data = {
                          "serviceClass": "GW",
                          "name": gw_name + '-' + ip,
                          "serviceInterceptType": "IP",
                          "serviceType": "ALL",
                          "endpointId": gw_id,
                          "lowLatency": "NO",
                          "dataInterleaving": "NO",
                          "transparency": "NO",
                          "multicast": "OFF",
                          "dnsOptions": "NONE",
                          "icmpTunnel": "YES",
                          "cryptoLevel": "STRONG",
                          "permanentConnection": "YES",
                          "collectionLocation": "BOTH",
                          "pbrType": "WAN",
                          "rateSmoothing": "NO",
                          "gatewayClusterId": None,
                          "interceptIp": ip,
                          "gatewayIp": ip,
                          "gatewayCidrBlock": cidr,
                          "localNetworkGateway": "YES"
                        }
            if service['data'] == 'Network':
                data =  {
                          "serviceClass": "GW",
                          "name": gw_name + '-' + ip,
                          "serviceInterceptType": "IP",
                          "serviceType": "ALL",
                          "endpointId": gw_id,
                          "lowLatency": "NO",
                          "dataInterleaving": "NO",
                          "transparency": "NO",
                          "multicast": "OFF",
                          "dnsOptions": "NONE",
                          "icmpTunnel": "YES",
                          "cryptoLevel": "STRONG",
                          "permanentConnection": "YES",
                          "collectionLocation": "BOTH",
                          "pbrType": "WAN",
                          "rateSmoothing": "NO",
                          "gatewayClusterId": None,
                          "interceptIp": ip,
                          "gatewayIp": ip,
                          "gatewayCidrBlock": cidr,
                          "localNetworkGateway": "YES"
                        }
            try:
                result = post_data(url, data, token)
                print(result, '\n')
                service_list.append((result['_links']['self']['href'], result['_links']['self']['href'].split('/')[8]))
                time.sleep(1)
            except Exception as e:
                writelog(e)
                print('\nPrint error creating service for ' + ip + '!\n')

        # print service_list

        # check status of service readiness to add to appwan

        print('Assigning services to APPWAN01!\n')
        add_list = []
        for service in service_list:
            serviceStatus = False
            try:
                count = 0
                while not serviceStatus:
                    if count > 5:
                        print '\nTimed out waiting for service ' + service[1] + ' status change!\n'
                        break
                    result = get_data(service[0], token)
                    if result['status'] == 300:
                        service_status = True
                        print '\nservice ' + service[1] + ' ready to assign to appwan!\n'
                        add_list.append(service[1])
                    else:
                        time.sleep(5)
                    count += 1
            except Exception as e:
                writelog(e)
                print "\nPrint error checking status on " + service[1]
                continue

        if not len(add_list):
            "\nService add list is empty!"
            sys.exit(0)
        # add services to appwan
        data = {"ids": add_list}
        try:
            add_result = post_data(appwan_service_url, data, token)
            print add_result
        except Exception as e:
            writelog(e)


def update_service(env, netUrl, loc, type, index, token):
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
    new_gw = nfreq.post_data(gwUrl, {"name": gwType +'_'+ str(index) +'_'+ loc.upper(),
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


def find_service(netUrl, name, token):
    gwsUrl = netUrl + '/endpoints'
    gateways = nfreq.get_data(gwsUrl, token)['_embedded']['endpoints']
    gwUrl = ''
    for gateway in gateways:
        if gateway['name'] == name:
            gwUrl = gateway['_links']['self']['href']
    return gwUrl


def delete_service(gwUrl, token):
    data = nfreq.delete_nf(gwUrl, token)
    writelog(data)


if __name__ == '__main__':
    pass
