#!/usr/bin/python3
"""
This module is to create ziti services and appwans based on pre-configured
indetities, edge routers, and clusters.
"""
import os
import json
import traceback
import argparse
import logging
from subprocess import Popen, PIPE
import requests

def post_request(url, headers, payload, public_key):
    """
    Make http request to a given url and return json data
    :param url:
    :param headers:
    :param payload:
    :return request.content: in json form
    """
    request = requests.post(url=url, data=payload,
                            headers=headers,
                            verify=False)
    data = json.loads(request.content)['data']
    code = request.status_code
    return data, code


def put_request(url, headers, payload, public_key):
    """
    Make http PUT request to a given url and return json data
    :param url:
    :param headers:
    :param payload:
    :return request.content: in json form
    """
    request = requests.put(url=url, data=payload,
                           headers=headers,
                           verify=False)
    data = json.loads(request.content)['data']
    code = request.status_code
    return data, code


def get_request(url, headers, public_key):
    """
    Make http get request to a given url and return json data
    :param url:
    :param headers:
    :param public_key:
    :return request.content: in json form
    """
    request = requests.get(url=url, headers=headers,
                           verify=False)
    data = json.loads(request.content)['data']
    code = request.status_code
    return data, code


def main():
    """
    Main logic
    """
    __version__ = '1.0.0'

    # argument parser from command line
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug log in log file output')
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    parser.add_argument('-u', '--username', default='admin',
                        help='controller username, default is admin')
    parser.add_argument('-p', '--password', required='yes',
                        help='controller password')
    parser.add_argument('-cip', '--controller_ip',
                        required='yes', help='controller ip')
    parser.add_argument('--cluster_name', help='ingress cluster name')
    parser.add_argument('--gateway_name', help='edge gateway name')
    parser.add_argument('--identity_name', help='identity name')
    parser.add_argument('--service_dns', help='service ip or dns')
    parser.add_argument('-ca', '--ca-chain', dest='ca_chain',
                        help='ca chain for the controller')
    # get arguments passed to this module
    args = parser.parse_args()
    # enable debug if requested
    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    # configure logging
    try:
        logging.basicConfig(filename=os.path.expanduser("logoutput.txt"),
                            format='%(asctime)s-ziti-%(levelname)s,%(message)s',
                            datefmt='%Y-%m-%d-%H:%M:%S',
                            level=log_level)
    except Exception as excpt:
        print('configure-ziti-services: '+str(excpt))
    # write separator in log file if debug has been enabled.
    logging.debug("----------------debug-enabled----------------")
    public_key = args.ca_chain
    # login to ontroller to gain a session token
    try:
        url = 'https://%s:1280/authenticate?method=password' % args.controller_ip
        payload = "{\n  \"username\": \"%s\",\n  \"password\": \"%s\"\n}" \
                    % (args.username, args.password)
        content_type = {"content-type": "application/json"}
        data = post_request(url, content_type, payload, public_key)
        session_token = data[0]['token']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # find ingress cluster
    try:
        url = 'https://%s:1280/clusters' % args.controller_ip
        content_type = {"content-type": "application/json", \
                        "zt-session": session_token}
        data = get_request(url, content_type, public_key)
        for cluster in data[0]:
            if cluster['name'] == args.cluster_name:
                clusterId = cluster['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # find ingress cluster
    try:
        url = 'https://%s:1280/gateways' % args.controller_ip
        content_type = {"content-type": "application/json", \
                        "zt-session": session_token}
        data = get_request(url, content_type, public_key)
        for gateway in data[0]:
            if gateway['name'] == args.gateway_name:
                gatewayId = gateway['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # find an identity to be assigned to appWan
    try:
        url = 'https://%s:1280/identities' % args.controller_ip
        content_type = {"content-type": "application/json", \
                        "zt-session": session_token}
        data = get_request(url, content_type, public_key)
        for identity in data[0]:
            if identity['name'] == args.identity_name:
                identityId = identity['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    try:
        url = 'https://%s:1280/services' % args.controller_ip
        payload = "{\"name\":\"iperf3\",\"protocols\": [\"tls\"], \
                    \"dns\":{\"hostname\":\"%s\",\"port\": 5201}, \
                    \"egressRouter\":\"%s\", \
                    \"endpointAddress\":\"tcp://%s:5201\", \
                    \"clusters\": [\"%s\"]}" % (args.service_dns,
                                                gatewayId,
                                                args.service_dns,
                                                clusterId)
        content_type = {"content-type": "application/json", \
                        "zt-session": session_token}
        data = post_request(url, content_type, payload, public_key)
        serviceId = data[0]['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # create AppWan
    try:
        url = 'https://%s:1280/app-wans' % (args.controller_ip)
        payload = "{\"name\":\"appwan01\",\"identities\":[\"%s\"], \
                    \"services\":[\"%s\"]}" % (identityId, serviceId)
        content_type = {"content-type": "application/json", \
                        "zt-session": session_token}
        data = post_request(url, content_type, payload, public_key)
        apWanId = data[0]['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())


if __name__ == '__main__':
    main()
