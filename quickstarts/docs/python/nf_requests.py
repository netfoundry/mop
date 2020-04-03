#!/usr/bin/python3
"""Construct the headers and make request to NF API Server for the requested REST method."""
import requests
import time
from datetime import datetime
from json import dumps


def clear_log():
    """Clear logs."""
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    """Write a log."""
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()


def nf_req(req, method, token=None):
    """Construct the headers and make request to NF API Server for the requested REST method."""
    verify = True
    timeout = 15
    count = 0
    handle = -1
    if req[1] and token is None:
        payload = req[1]
    else:
        payload = dumps(req[1], separators=(',', ':'))
    if token is None:
        headers = {'content-type': 'application/json'}
    elif method == 'get':
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json',
                   'Cache-Control': 'no-cache'}
    else:
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    if (method == 'post') and (token is None):
        while count < 3:
            try:
                handle = requests.post(req[0], data=payload, timeout=timeout, verify=verify)
                writelog(str(handle.status_code))
                writelog(handle.headers)
                return handle.json()
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'post':
        while count < 3:
            try:
                handle = requests.post(req[0], data=payload, timeout=timeout, headers=headers,
                                       verify=verify)
                writelog(str(handle.status_code))
                writelog(handle.headers)
                return handle.json()
            except Exception as e:
                writelog(e)
                print(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'get':
        while count < 3:
            try:
                handle = requests.get(req, timeout=timeout, headers=headers, verify=verify)
                writelog(str(handle.status_code))
                writelog(handle.headers)
                return handle.json()
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'delete':
        while count < 3:
            try:
                handle = requests.delete(req, timeout=timeout, headers=headers, verify=verify)
                writelog(str(handle.status_code))
                writelog(handle.headers)
                return handle
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'put':
        while count < 3:
            try:
                handle = requests.put(req[0], data=payload, timeout=timeout, headers=headers,
                                      verify=verify)
                writelog(str(handle.status_code))
                writelog(handle.headers)
                return handle.json()
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    return handle


if __name__ == '__main__':
    pass
