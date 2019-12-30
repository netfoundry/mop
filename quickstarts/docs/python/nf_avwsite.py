#!/usr/bin/python3

import os
import sys
import time
import datetime
import logging
import argparse
import yaml
import nf_requests as nfreq
import nf_gateway as nfgw
import nf_network as nfnk
import nf_token as nftn
from azure.mgmt.network import NetworkManagementClient
from azure.common.credentials import ServicePrincipalCredentials

def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' avwsite-log ' + str(message) + '\n')
    logfile.close()


def vpn_site_connection_creation(siteName):
    # setup Azure Login Credentials from Environmental Variables
    credentials = ServicePrincipalCredentials(
        client_id = os.environ.get('ARM_CLIENT_ID'),
        secret = os.environ.get('ARM_CLIENT_SECRET'),
        tenant = os.environ.get('ARM_TENANT_ID')
    )

    # declaire Test Input Variables
    CONNECTION_PARAMS = {
        'enable_bgp': True,
        'remote_vpn_site': {
          'id': "/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/vpnSites/%s" % (os.environ.get('ARM_SUBSCRIPTION_ID'), os.environ.get('GROUP_NAME'), siteName)
        }
    }

    # Connect to Azure APIs and get session details
    network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

    # Delay for 30 seconds before deleting resources
    time.sleep(60)

    # Create VPN Site Connection to VPNG
    async_vpn_site_connection_creation = network_client.vpn_connections.create_or_update(
        os.environ.get('GROUP_NAME'),
        os.environ.get('VPNG_NAME'),
        'CONNECTION_' + siteName,
        CONNECTION_PARAMS,
        custom_headers=None,
        raw=False,
        polling=True
    )
    async_vpn_site_connection_creation.wait()
    print(async_vpn_site_connection_creation.result())


def vpn_site_connection_deletion(siteName):
    # setup Azure Login Credentials from Environmental Variables
    credentials = ServicePrincipalCredentials(
        client_id = os.environ.get('ARM_CLIENT_ID'),
        secret = os.environ.get('ARM_CLIENT_SECRET'),
        tenant = os.environ.get('ARM_TENANT_ID')
    )

    # Connect to Azure APIs and get session details
    network_client = NetworkManagementClient(credentials, os.environ.get('ARM_SUBSCRIPTION_ID'))

    # Show VPN Site Connection to VPNG
    async_vpn_site_connection_show = network_client.vpn_connections.get(
        os.environ.get('GROUP_NAME'),
        os.environ.get('VPNG_NAME'),
        'CONNECTION_' + siteName,
        custom_headers=None,
        raw=False
    )
    print(async_vpn_site_connection_show)

    # Delete VPN Site Connection to VPNG
    async_vpn_site_connection_deletion = network_client.vpn_connections.delete(
        os.environ.get('GROUP_NAME'),
        os.environ.get('VPNG_NAME'),
        'CONNECTION_' + siteName,
        custom_headers=None,
        raw=False,
        polling=True
    )
    print(async_vpn_site_connection_deletion.result())
    print('VPN Site Connection to VPNG Deleted')


def create_avw_site(filename):
    # environment used
    env = os.environ.get('ENVIRONMENT')
    # clear logoutput file
    nftn.clear_log()
    # get resources to configure from file
    try:
        with open(filename, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        writelog(str(e))
    # get session token
    token = nftn.get_token(env, os.environ.get('SMOKE_TEST_USER'), os.environ.get('SMOKE_TEST_PASS'))
    # find configuration detali for avw gateway from file
    for gateway in config['gateway_list']:
        if gateway['cloud'] == 'vwan':
            loc = gateway['region']
            gwName = gateway['names'][0]
    # url for NF Datacenters details
    url = 'https://gateway.' + env + '.netfoundry.io/rest/v1/dataCenters'
    # find dc id based on location code
    datacenters = nfreq.get_data(url, token)['_embedded']['dataCenters']
    dcId = None
    for dc in datacenters:
        if dc['locationCode'] == loc:
            dcId = dc['_links']['self']['href'].split('/')[6]
    # get network url
    nfn_url = nfnk.find_network(env, os.environ.get('NFN_NAME'), token)
    # find gateway Id for avwsite gateway
    gwId = nfgw.find_gateway(nfn_url, gwName, token).split('/')[8]
    # build Azure Subscriptions Url for a given NF Enviroment API
    azureSubscriptionsURL = 'https://gateway.' + env + '.netfoundry.io/rest/v1/azureSubscriptions'
    # get Azure Subscriptions url of the first one, the assumption is that there is only one.
    try:
        avwSiteUrl = nfreq.get_data(azureSubscriptionsURL, token)['_embedded']['azureSubscriptions'][0]['_links']['self']['href']+'/virtualWanSites'
    except KeyError as kerr:
        print(kerr.args)
        if kerr.args[0] == '_embedded':
            data = nfreq.post_data(azureSubscriptionsURL, {
                                    "name" : "AVW Packet Test",
                                    "subscriptionId" : os.environ.get('ARM_SUBSCRIPTION_ID'),
                                    "tenantId" : os.environ.get('ARM_TENANT_ID'),
                                    "applicationId" : os.environ.get('ARM_CLIENT_ID'),
                                    "applicationKey" : os.environ.get('ARM_CLIENT_SECRET')
                                  }, token)

            avwSiteUrl = data['_links']['self']['href']+'/virtualWanSites'
    print(avwSiteUrl)
    # create avw vpn site
    azureVirtualWanId = "/subscriptions/"+os.environ.get('ARM_SUBSCRIPTION_ID')+"/resourceGroups/"+os.environ.get('GROUP_NAME')+"/providers/Microsoft.Network/virtualWans/"+os.environ.get('VWAN_NAME')
    createData = nfreq.post_data(avwSiteUrl, {
                                        "name": gwName,
                                        "endpointId": gwId,
                                        "azureResourceGroupName": os.environ.get('GROUP_NAME'),
                                        "azureVirtualWanId" : azureVirtualWanId,
                                        "publicIpAddress" : os.environ.get('AVW_SITE_PUBLIC_IP'),
                                        "dataCenterId": dcId,
                                        "bgp" : {
                                        "localPeeringAddress" : {
                                          "ipAddress" : os.environ.get('AVW_SITE_PRIVATE_IP'),
                                          "asn" : 65000
                                        },
                                        "bgpPeerWeight" : 0,
                                        "deviceLinkSpeed" : 0,
                                        "deviceVendor" : None,
                                        "deviceModel" : None,
                                        "neighborPeers" : [ {
                                          "ipAddress" : os.environ.get('AVW_SITE_PEER_PRIVATE_IP'),
                                          "asn" : 65000
                                        } ],
                                        "advertiseLocal" : True,
                                        "advertisedPrefixes" : []
                                        }
                                       }, token)
    deployData = nfreq.put_data(createData['_links']['self']['href']+"/deploy", {}, token)
    # Connect th enewly created site to the Azure VPN Gateway
    vpn_site_connection_creation(gwName)
    return createData, deployData


def delete_avw_site():
    # get session token
    token = nftn.get_token(os.environ.get('ENVIRONMENT'), os.environ.get('SMOKE_TEST_USER'), os.environ.get('SMOKE_TEST_PASS'))
    # get network url
    nfn_url = nfnk.find_network(os.environ.get('ENVIRONMENT'), os.environ.get('NFN_NAME'), token)
    # get AVW Site url of the first one, the assumption is that there is only one.
    avwSite = nfreq.get_data(nfn_url+'/virtualWanSites', token)['_embedded']['azureVirtualWanSites'][0]
    # Disconnect the VPN site under test from the Azure VPN Gateway
    vpn_site_connection_deletion(avwSite['name'])
    # Delete the site from the NF Network
    data = nfreq.delete_nf(avwSite['_links']['self']['href'], token)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AVW VPN Site build script')
    parser.add_argument("--action", help="", required=True)
    parser.add_argument("--file", help="json file with netfoundry resources details to create/update/delete")
    args = parser.parse_args()
    if args.action == "create":
        print(create_avw_site(args.file))
    if args.action == "delete":
        print(delete_avw_site())
