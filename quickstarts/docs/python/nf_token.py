#!/usr/bin/python3
"""Get session token to gain access to MOP environment."""
from os import path
from configparser import ConfigParser
import argparse
import datetime
import nf_requests as nfreq


def clear_log():
    """Clear logs."""
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    """Write a log."""
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def get_token(env, client_id=None, client_secret=None):
    """Get the session token."""
    if (not client_id) and (not client_secret):
        config = ConfigParser()
        config.sections()
        config.read(path.expanduser('~/.env'))
        client_id = config[env]['clientId']
        client_secret = config[env]['clientSecret']
    data = {"client_id": client_id,
            "client_secret": client_secret,
            "audience": "https://gateway." + env + ".netfoundry.io/",
            "grant_type": "client_credentials"}
    url = 'https://netfoundry-' + env + '.auth0.com/oauth/token'
    req = (url, data)
    token = nfreq.nf_req(req, 'post')
    return token['access_token']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Session Token script')
    parser.add_argument("--client_id", help="NF Console Client Id")
    parser.add_argument("--client_secret", help="NF Console Client Secret")
    parser.add_argument("--env", help="NetFoundry Enviroment", required=True)
    parser.add_argument("--clear_logs", action="store_true", help="Clear log file")
    args = parser.parse_args()
    if args.clear_logs:
        clear_log()
    print(get_token(args.env, args.client_id, args.client_secret))
