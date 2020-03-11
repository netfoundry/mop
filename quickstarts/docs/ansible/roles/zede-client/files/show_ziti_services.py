#!/usr/bin/python3
"""Create ziti services and policies based on pre-configured indetities and edge routers."""
from os.path import expanduser
import json
import traceback
import argparse
import logging
from requests import get, post
from sys import exit


def restful(url, rest_method, headers, payload=None):
    """
    Make http request to a given url and return json data.

    Paramters
    ---------
    url :
    rest_method :
    headers :
    payload :

    Returns
    -------
    request.content : in json form
    """
    if payload:
        request = rest_method(url=url, data=payload, headers=headers,  verify=False)
    else:
        request = rest_method(url=url, headers=headers,  verify=False)
    data = json.loads(request.content)['data']
    code = request.status_code
    return data, code


def debug(debug=False):
    """Enable required debug."""
    # enable debug if requested
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    # configure logging
    try:
        logging.basicConfig(filename=expanduser("logoutput.txt"),
                            format='%(asctime)s-ziti-%(levelname)s,%(message)s',
                            datefmt='%Y-%m-%d-%H:%M:%S',
                            level=log_level)
    except Exception as excpt:
        print('configure-ziti-services: '+str(excpt))
    # write separator in log file if debug has been enabled.
    logging.debug("----------------debug-enabled----------------")


def ziti_authenticate(controller_ip, username, password):
    """Authenticate to Ziti Controller and get a session token."""
    # login to controller to gain a session token
    try:
        url = 'https://%s:1280/authenticate?method=password' % controller_ip
        payload = "{\n  \"username\": \"%s\",\n  \"password\": \"%s\"\n}" \
            % (username, password)
        headers = {"content-type": "application/json"}
        response_data = restful(url, post, headers, payload)
        logging.info(response_data[1])
        return response_data[0]['token']
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
        return None


def create_url(controller_ip, endpoint):
    """Create endpoint url to POST/PUT/GET/DELTE against."""
    return 'https://%s:1280/%s' % (controller_ip, endpoint)


def create_headers(session_token):
    """Create headers to use with POST/PUT/GET/DELTE."""
    return {"content-type": "application/json", "zt-session": session_token}


def ziti():
    """Configure Ziti Services."""
    session_token = ziti_authenticate(args.controller_ip, args.username, args.password)
    if not session_token:
        exit(1)
    # print edge routers
    try:
        response_data = restful(create_url(args.controller_ip, "gateways"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        gateways = response_data[0]
        print(gateways)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print identities
    try:
        response_data = restful(create_url(args.controller_ip, "identities"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        identities = response_data[0]
        print(identities)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print config templates
    try:
        response_data = restful(create_url(args.controller_ip, "configs"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        configs = response_data[0]
        print(configs)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print services
    try:
        response_data = restful(create_url(args.controller_ip, "services"),
                                get, create_headers(session_token))

        logging.info(response_data[1])
        services = response_data[0]
        print(services)
    except Exception as excpt:
        print(str(excpt))
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print edge router policies
    try:
        response_data = restful(create_url(args.controller_ip, "edge-router-policies"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        edge_router_policies = response_data[0]
        print(edge_router_policies)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print service policies
    try:
        response_data = restful(create_url(args.controller_ip, "service-policies"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        service_policies = response_data[0]
        print(service_policies)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # print service edge router policies
    try:
        response_data = restful(create_url(args.controller_ip, "service-edge-router-policies"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        service_edge_router_policies = response_data[0]
        print(service_edge_router_policies)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())


def version():
    """Show version of this module when asked."""
    print('1.0.0')


if __name__ == '__main__':
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable debug log in log file output')
    parser.add_argument('-v', '--version', action='version',
                        version='1.0.0')
    parser.add_argument('-u', '--username', default='admin',
                        help='controller username, default is admin')
    parser.add_argument('-p', '--password', required='yes',
                        help='controller password')
    parser.add_argument('-cip', '--controller_ip',
                        required='yes', help='controller ip')
    # get arguments
    args = parser.parse_args()
    if args.debug:
        debug(args.debug)
    else:
        debug()
    ziti()
