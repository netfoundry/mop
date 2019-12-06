#!/usr/bin/python3

import os
import logging
import configparser
import datetime
import nf_requests as nfreq

def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def get_token(env, client_id=None, client_secret=None):
    if (not client_id) and (not client_secret):
        config = configparser.ConfigParser()
        config.sections()
        config.read(os.path.expanduser('~/.env'))
        client_id = config[env]['clientId']
        client_secret = config[env]['secretId']
    data = {"client_id": client_id,
            "client_secret": client_secret,
            "audience": "https://gateway." + env + ".netfoundry.io/",
            "grant_type": "client_credentials"}
    url = 'https://netfoundry-' + env + '.auth0.com/oauth/token'
    req = (url, data)
    token = nfreq.nf_req(req, 'post')
    return token['access_token']


if __name__ == '__main__':
    # Get NetFoundry Console token
    print(get_token('sandbox'))
