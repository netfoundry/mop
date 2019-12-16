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


def check_for_status(urlRestEndpoint, token):
    """
    Check for status on the resource creation
    :param urlRestEndpoint: REST Url endpoint for resource
    :param token:  session token for NF Console
    :return returndata: pass the response back from the status check
    """
    itemStatus = False
    try:
        count = 0
        while not itemStatus:
            if count > 6:
                writelog('Timed out waiting for a status change ' + urlRestEndpoint.split('/')[8] +'!')
                break
            returnData = nfreq.get_data(urlRestEndpoint, token)
            print(returnData)
            if returnData['status'] == 300:
                writelog('item ' + urlRestEndpoint.split('/')[8] + ' is ready!')
                break
            else:
                time.sleep(5)
            count += 1
    except Exception as e:
        writelog(e)
    return returnData['status']


def add_item2appwan(appwanUrl, itemUrl, token):
    """
    Add items to existing appwan if not create one
    :param env: enviroment, e.g. production, sandbox
    :param appwanUrl: REST Url endpoint for the appwan under build
    :param itemUrl: REST Url endpoint for item being added to appwan
    :return none:
    """
    # Check if item is ready
    checkStatus = check_for_status(appwanUrl, token)
    # add item to appwan, e.g. gateway, client or service
    try:
        if checkStatus == 300:
            returnData = nfreq.post_data(appwanUrl+'/'+itemUrl.split('/')[7],
                         {'ids': [itemUrl.split('/')[8]]}, token)
            writelog(returnData)
    except Exception as e:
        writelog(e)


def create_appwan(netUrl, appwanName, token):
    """
    Create AppWan
    :param netUrl: REST Url endpoint for network
    :param appwanName: appwan name
    :param token:  seesion token for NF Console
    :return appwanUrl: url of the created appwan
    """
    url = netUrl + '/appWans'
    try:
        returnData = nfreq.post_data(url, {"name": appwanName}, token)
        appwanUrl = returnData['_links']['self']['href']
        time.sleep(1)
    except Exception as e:
        writelog(e)
        writelog('Print error creating appwan for!')
        appwanUrl = ""
    return appwanUrl


def find_appwan(netUrl, appwanName, token):
    """
    Find url of an exiting appwan
    :param netUrl: REST Url endpoint for network
    :param appwanName: appwan name
    :param token:  seesion token for NF Console
    :return appwanUrl: url of the found appwan
    """
    appwansUrl = netUrl + '/appWans'
    appwans = nfreq.get_data(appwansUrl, token)
    if appwans.get('_embedded'):
        for appwan in appwans['_embedded']['appWans']:
            if appwan['name'] == appwanName:
                appwanUrl = appwan['_links']['self']['href']
    else:
        appwanUrl = None
    return appwanUrl


def delete_appwan(appwanUrl, token):
    """
    Delete an exiting appwan
    :param appwanUrl: REST endpoint for the appwan marked for deletion
    :param token:  seesion token for NF Console
    :return none:
    """
    try:
        # Check if item is ready
        checkStatus = check_for_status(appwanUrl, token)
        if checkStatus == 300:
            data = nfreq.delete_nf(appwanUrl, token)
            writelog(data)
    except Exception as e:
        writelog(e)


if __name__ == '__main__':
    pass
