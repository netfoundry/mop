#!/usr/bin/python3
"""Create ziti edge services and policies based on pre-configured indetities and edge routers."""
from os.path import expanduser
import json
import traceback
import argparse
import logging
from requests import post, get, patch
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
    print(request)
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
        print('configure-ziti-edge-services: '+str(excpt))
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
    """Configure Ziti Edge Services."""
    session_token = ziti_authenticate(args.controller_ip, args.username, args.password)
    if not session_token:
        exit(1)
    # find edge router and add role attribute
    try:
        response_data = restful(create_url(args.controller_ip, "edge-routers"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        edge_routers = response_data[0]
        for edge_router in edge_routers:
            if edge_router['name'] == args.edge_router_name:
                edge_router_id = edge_router['id']
                payload = "{\"name\":\"%s\",\"roleAttributes\": [\"%s\"]}" \
                    % (args.edge_router_name, "test")
                response_data = restful(create_url(args.controller_ip,
                                                   "edge-routers/"+edge_router_id),
                                        patch, create_headers(session_token),
                                        payload)
                logging.info(response_data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # find an identity to be assigned to service/edge router with role #test
    try:
        response_data = restful(create_url(args.controller_ip, "identities"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        identities = response_data[0]
        for identity in identities:
            if identity['name'] == args.identity_name:
                if not identity['enrollment']:
                    identity_id = identity['id']
                    payload = "{\"name\": \"%s\", \"roleAttributes\": [\"%s\"],\
                        \"isAdmin\": false, \"type\": \"Device\"}" \
                        % (args.identity_name, "test")
                    response_data = restful(create_url(args.controller_ip,
                                                       "identities/"+identity_id),
                                            patch, create_headers(session_token),
                                            payload)
                    logging.info(response_data[1])
                    print(response_data[0])
                else:
                    print("Identity %s has not been enrolled yet" % identity['name'])
        if not identity_id:
            logging.info("Identity %s '[not]' found" % args.identity_name)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # find config type id
    try:
        response_data = restful(create_url(args.controller_ip, "config-types"),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        config_types = response_data[0]
        for config_type in config_types:
            if config_type['name'] == "ziti-tunneler-client.v1":
                config_type_id = config_type['id']
                print("config_type_id is %s" % config_type_id)
        if not config_type_id:
            print("Could not find id for config-type ziti-tunneler-client.v1" )
            exit(1)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # create config template
    try:
        payload = "{\"name\":\"tunnel-client-01\",\"type\": \"%s\",\
                    \"data\":{\"hostname\":\"%s\",\"port\": %s}}" % (config_type_id,
                                                                     args.service_dns,
                                                                     args.service_port)
        response_data = restful(create_url(args.controller_ip, "configs"),
                                post, create_headers(session_token), payload)
        config_id = response_data[0]['id']
        print(config_id)
        logging.info(response_data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # create service
    try:
        payload = "{\"name\":\"iperf3\",\"roleAttributes\": [\"test\"],\
                    \"egressRouter\":\"%s\",\"endpointAddress\":\"tcp://%s:%s\",\
                     \"configs\":[\"tunnel-client-01\"]}" % (edge_router_id,
                                                             args.service_dns,
                                                             args.service_port)
        response_data = restful(create_url(args.controller_ip, "edge-services"),
                                post, create_headers(session_token), payload)
        service_id = response_data[0]['id']
        logging.info(response_data[1])
        print(service_id)
    except Exception as excpt:
        print(str(excpt))
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # create edge router policy
    try:
        payload = "{\"name\":\"router-policy01\",\"edgeRouterRoles\":[\"#%s\"],\
                    \"identityRoles\":[\"#%s\"],\"semantic\": \"AllOf\"}" \
                        % ("test", "test")
        response_data = restful(create_url(args.controller_ip, "edge-router-policies"),
                                post, create_headers(session_token), payload)
        edge_router_policy_id = response_data[0]['id']
        logging.info(response_data[1])
        print(edge_router_policy_id)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # create service policy
    try:
        payload = "{\"name\":\"service-policy01\",\"serviceRoles\":[\"#%s\"],\
                    \"identityRoles\":[\"#%s\"],\"type\":\"Dial\",\"semantic\": \"AllOf\"}"\
                        % ("test", "test")
        response_data = restful(create_url(args.controller_ip, "service-policies"),
                                post, create_headers(session_token), payload)
        service_policy_id = response_data[0]['id']
        logging.info(response_data[1])
        print(service_policy_id)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # create service edge router policy
    try:
        payload = "{\"name\":\"service-router-policy01\",\"edgeRouterRoles\":[\"#%s\"],\
                    \"serviceRoles\":[\"#%s\"],\"semantic\": \"AllOf\"}"\
                        % ("test", "test")
        response_data = restful(create_url(args.controller_ip, "service-edge-router-policies"),
                                post, create_headers(session_token), payload)
        service_edge_router_policy_id = response_data[0]['id']
        logging.info(response_data[1])
        print(service_edge_router_policy_id)
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
    parser.add_argument('--edge_router_name', help='edge edge router name')
    parser.add_argument('--identity_name', help='identity name')
    parser.add_argument('--service_dns', help='service ip or dns')
    parser.add_argument('--service_port', help='service port')
    # get arguments
    args = parser.parse_args()
    if args.debug:
        debug(args.debug)
    else:
        debug()
    ziti()
