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


def create_service(netUrl, gwUrl, attributes, token):
    """
    Create Service on Gateway
    :param netUrl: REST Url endpoint for network
    :param gwUrl: REST Url endpoint for gateway
    :param serviceAttributes: service paramaters, e.g. service type or name, etc
    :param token:  seesion token for NF Console
    :return serviceId, serviceUrl: created service details
    """
    url = netUrl+'/services'
    gwId = gwUrl.split('/')[8]
    serviceName = attributes['gateway']+'--'+str(attributes['ip'])+'--'+str(attributes['port'])
    if attributes['type'] == 'host':
        data = {
                  "serviceClass" : "CS",
                  "name" : serviceName,
                  "serviceInterceptType" : "IP",
                  "serviceType" : "ALL",
                  "endpointId" : gwId,
                  "pbrType" : "WAN",
                  "dataInterleaving": "NO",
                  "transparency": "NO",
                  "networkIp" : attributes['ip'],
                  "networkFirstPort" : attributes['port'],
                  "networkLastPort" : attributes['port'],
                  "interceptIp" : attributes['ip'],
                  "interceptFirstPort" : attributes['port'],
                  "interceptLastPort" : attributes['port']
                }
    if attributes['type'] == 'network':
        data =  {
                  "serviceClass": "GW",
                  "name": attributes['netIp']+'-'+attributes['netCidr'],
                  "serviceInterceptType": "IP",
                  "serviceType": "ALL",
                  "endpointId": gwId,
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
                  "interceptIp": attributes['netIp'],
                  "gatewayIp": attributes['netIp'],
                  "gatewayCidrBlock": attributes['netCidr'],
                  "localNetworkGateway": "YES"
                }
    returnData = nfreq.post_data(url, data, token)
    serviceUrl = returnData['_links']['self']['href']
    time.sleep(1)

    return serviceUrl, serviceName


def find_service(netUrl, serviceName, token):
    """
    Find url of an exiting service
    :param netUrl: REST Url endpoint for network
    :param serviceName: service name
    :param token:  seesion token for NF Console
    :return serviceUrl: url of the found service
    """
    servicesUrl = netUrl + '/services'
    services = nfreq.get_data(servicesUrl, token)['_embedded']['services']
    for service in services:
        if service['name'] == serviceName:
            serviceUrl = service['_links']['self']['href']
    return serviceUrl


def delete_service(serviceUrl, token):
    """
    Delete an exiting service
    :param serviceUrl: REST endpoint for the service marked for deletion
    :param token:  seesion token for NF Console
    :return none:
    """
    try:
        data = nfreq.delete_nf(serviceUrl, token)
        writelog(data)
    except Exception as e:
        writelog(e)


if __name__ == '__main__':
    pass
