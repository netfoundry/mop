#!/usr/bin/python3
"""
This module is to create ziti identity and erollit for the loacal endpoint
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
    parser.add_argument('-hd', '--home-directory', dest='home_directory', default='/home/nfadmin',
                        help='set home directory. Default: /home/nfadmin')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-u', '--username', default='admin', help='controller username, default is admin')
    parser.add_argument('-p', '--password', required='yes', help='controller password')
    parser.add_argument('-cip', '--controller-ip', dest='controllerIp', required='yes', help='controller ip')
    parser.add_argument('-i', '--identity', required='yes', help='identity for an endpoint')
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
        logging.basicConfig(filename=os.path.expanduser("~/update_indentity.log"),
                            format='%(asctime)s-identity-%(levelname)s,%(message)s',
                            datefmt='%Y-%m-%d-%H:%M:%S',
                            level=log_level)
    except Exception as excpt:
        print('enroll-ziti-tunneler: '+str(excpt))
    # write separator in log file if debug has been enabled.
    logging.debug("----------------debug-enabled----------------")
    public_key = args.ca_chain
    # login to ontroller to gain a session token
    try:
        url = 'https://%s:1280/authenticate?method=password' % args.controllerIp
        payload = "{\n  \"username\": \"%s\",\n  \"password\": \"%s\"\n}" % (args.username, args.password)
        content_type = {"content-type": "application/json"}
        data = post_request(url, content_type, payload, public_key)
        session_token = data[0]['token']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # create an identity
    try:
        url = 'https://%s:1280/identities' % args.controllerIp
        payload = "{\n  \"name\": \"%s\",\n \"type\":\"Device\",\n \"enrollment\":{\"ott\":true} \n}" % args.identity
        content_type = {"content-type": "application/json", "zt-session": session_token}
        data = post_request(url, content_type, payload, public_key)
        identityId = data[0]['id']
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # download jwt token
    try:
        url = 'https://%s:1280/identities/%s' % (args.controllerIp, identityId)
        content_type = {"content-type": "application/json", "zt-session": session_token}
        data = get_request(url, content_type, public_key)
        jwtFile = "%s/.config/ziti/ziti-identities/%s.jwt" % (args.home_directory, args.identity)
        with open(jwtFile, "w") as f:
            f.write(data[0]['enrollment']['ott']['jwt'])
        logging.info(data[1])
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())
    # enroll identity
    try:
        cmd = ['/usr/local/bin/ziti-enroller', '-j', jwtFile]
        proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if output:
            logging.info(output)
        if error:
            logging.error(error)
    except Exception as excpt:
        logging.error(str(excpt))
        logging.debug(traceback.format_exc())


if __name__ == '__main__':
    main()
