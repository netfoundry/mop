#!/usr/bin/python3

import requests
import json
import os
import logging
import time
import datetime


def clear_log():
    logfile = open('logoutput.txt', 'w')
    logfile.close()


def writelog(message):
    logfile = open('logoutput.txt', 'a+')
    logfile.write(str(datetime.datetime.now()) + ' ' + str(message) + '\n')
    logfile.close()

# Function to construct the headers and then make reuqest to NF API Server for the requested REST method.
def nf_req(req, method, token=None):
    verify = True
    timeout = 15
    count = 0
    handle = -1
    if token is None:
        headers = {'content-type': 'application/json'}
    elif method == 'get':
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json', 'Cache-Control': 'no-cache'}
    else:
        headers = {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
    if (method == 'post') and (token is None):
        while count < 3:
            try:
                handle = requests.post(req[0], data=req[1], timeout=timeout, verify=verify)
                writelog(str(handle.status_code))
                return handle.json()
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'post':
        while count < 3:
            try:
                handle = requests.post(req[0], data=req[1], timeout=timeout, headers=headers, verify=verify)
                writelog(str(handle.status_code))
                # print handle.raw.data
                # print handle.content
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
                return handle
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    elif method == 'put':
        while count < 3:
            try:
                handle = requests.put(req[0], data=req[1], timeout=timeout, headers=headers, verify=verify)
                writelog(str(handle.status_code))
                return handle.json()
            except Exception as e:
                writelog(e)
                time.sleep(2)
                count += 1
                continue
    return handle


# Get Netfoundry API operation
def get_data(url, token):
    req = url
    data = nf_req(req, 'get', token)
    return data


# Delete Netfoundry API operation
def delete_nf(url, token):
    req = url
    data = nf_req(req, 'delete', token)
    return data


# Update Netfoundry API operation
def put_data(url, values, token):
    data = json.dumps(values)
    # print data
    req = (url, data)
    # sys.exit(0)
    put_return = nf_req(req, 'put', token)
    return put_return


# Create Netfoundry API operation
def post_data(url, values, token):
    data = json.dumps(values)
    # print data
    req = (url, data)
    post_return = nf_req(req, 'post', token)
    return post_return


if __name__ == '__main__':
    pass
