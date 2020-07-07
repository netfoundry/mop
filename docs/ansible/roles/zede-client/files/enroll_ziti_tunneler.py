#!/usr/bin/python3
"""The module is to create ziti identity and eroll it for the loacal endpoint."""
from os.path import expanduser
from json import loads
import traceback
import argparse
import logging
from subprocess import Popen, PIPE
from requests import post, get
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
    data = loads(request.content)['data']
    code = request.status_code
    return data, code


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


def debug(debug=False):
    """Enable required debug."""
    # enable debug if requested
    if debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    # configure logging
    try:
        logging.basicConfig(filename=expanduser("~/update_indentity.log"),
                            format='%(asctime)s-ziti-%(levelname)s,%(message)s',
                            datefmt='%Y-%m-%d-%H:%M:%S',
                            level=log_level)
    except Exception as excpt:
        print('enroll-ziti-tunneler: '+str(excpt))
    # write separator in log file if debug has been enabled.
    logging.debug("----------------debug-enabled----------------")


def create_url(controller_ip, endpoint):
    """Create endpoint url to POST/PUT/GET/DELTE against."""
    return 'https://%s:1280/%s' % (controller_ip, endpoint)


def create_headers(session_token):
    """Create headers to use with POST/PUT/GET/DELTE."""
    return {"content-type": "application/json", "zt-session": session_token}


def ziti_tunnel():
    """Enroll Ziti Tunneller."""
    # login to controller to gain a session token
    session_token = ziti_authenticate(args.controller_ip, args.username, args.password)
    if not session_token:
        exit(1)

    # create an identity
    try:
        payload = "{\"name\":\"%s\",\"type\":\"Device\",\"isAdmin\":false,\"roleAttributes\":[],\
            \"enrollment\":{\"ott\":true}}" % args.identity_name
        response_data = restful(create_url(args.controller_ip, "identities"),
                                post, create_headers(session_token), payload)
        logging.info(response_data[1])
        identity_id = response_data[0]['id']
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # download jwt token
    try:
        response_data = restful(create_url(args.controller_ip, "identities/"+identity_id),
                                get, create_headers(session_token))
        logging.info(response_data[1])
        jwt_file = "%s/.config/ziti/ziti-identities/%s.jwt" \
            % (args.home_directory, args.identity_name)
        with open(jwt_file, "w") as f:
            f.write(response_data[0]['enrollment']['ott']['jwt'])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())

    # enroll identity
    try:
        cmd = ['/usr/local/bin/ziti-enroller', '-j', jwt_file]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if output:
            logging.info(output)
        if error:
            logging.error(error)
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
    parser.add_argument('-hd', '--home_directory', default='/home/nfadmin',
                        help='set home directory. Default: /home/nfadmin')
    parser.add_argument('-v', '--version', action='version',
                        version='1.0.0')
    parser.add_argument('-u', '--username', default='admin',
                        help='controller username, default is admin')
    parser.add_argument('-p', '--password', required='yes', help='controller password')
    parser.add_argument('-cip', '--controller_ip', required='yes', help='controller ip')
    parser.add_argument('-i', '--identity_name', required='yes', help='identity for an endpoint')

    # get arguments
    args = parser.parse_args()
    if args.debug:
        debug(args.debug)
    else:
        debug()
    ziti_tunnel()
