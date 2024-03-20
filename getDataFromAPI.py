# encoding = utf-8

 

import requests

import os

import sys

import time

import datetime

from datetime import timedelta

from datetime import datetime as dt

import json

import re

import pickle

 

# a function that changes permissions and group for a given path location

def setPermissions(location, group='splunkadm', permissions='755'):

    os.system(f'chmod -R {permissions} {location}')

    os.system(f'chgrp -R {group} {location}')       

 

# find latest scan ID to be used as checkpoint for the program

def findLatestCp(cpFile):

        # check if id cp already exists and read it - if not, create a new one.

    if os.path.exists(cpFile):

        try:

            # try to read the cp

            with open(cpFile, 'rb') as fn:

                return str(pickle.load(fn))

        except:

            # couldnt read from the cp file. treated as first run.

            return "0"

    else:

        with open(cpFile, 'wb') as fn:

            # dumps the data into the file

            pickle.dump("0", fn)

            return "0"

 

 

# update checkpoint using a given file name and checkpoint value

def updateCp(filename,latest_cp):

    # save a checkpoint of latest timestamp fetched from logs

    with open(filename, 'wb') as fn:

        # dumps the data into the file

        pickle.dump(latest_cp, fn)

 

 

# fetch data using a GET request

def getData(proxies, verify_ssl, helper, ew):

   

    token = helper.get_arg("api_token")

    url = helper.get_arg("api_url")

 

       

    headers = {

        'Content-Type': 'application/json'

    }

    # make the request

    response = requests.get(url, headers=headers, auth=(f'{token}', 'token'), proxies=proxies, verify=verify_ssl)

   

    resData = response.json()

    sys.stderr.write(str(resData))

    sys.exit(1)

       

        

def validate_input(helper, definition):

    """Implement your own validation logic to validate the input stanza configurations"""

    # This example accesses the modular input variable

    # client_id = definition.parameters.get('client_id', None)

    # client_secret = definition.parameters.get('client_secret', None)

    # username = definition.parameters.get('username', None)

    # password = definition.parameters.get('password', None)

    # dns = definition.parameters.get('dns', None)

    pass

 

 

 

# this function is mandatory by Splunk - DO NOT delete it.

# this is the main function called by Splunk.

def collect_events(helper, ew):

    # define arguments from user input

    # should verify ssl:

    verify_ssl = helper.get_arg("verify_ssl")

    # set local path of the add-on files

    local_path = helper.get_arg('local_path')

   

    # set file path for checkpoimt files

    # !!make sure the order matches the returned_checkpoints order!!

    #cp_files = {

    #    "time_cp_filename": f"{local_path}cp_timestamp.pk",

    #    "id_cp_filename": f"{local_path}cp_id.pk"

    #    }

    # time_cp_filename = f'{local_path}cp_timestamp.pk'

    # id_cp_filename = f'{local_path}cp_id.pk'

   

    # check if proxy is enabled; if True - set proxy parameters; for False send None (default)

    proxies = {}

    try:

        proxy_settings = helper.get_proxy()

       

        if proxy_settings['proxy_url']:

            proxies['https'] = f"http://{proxy_settings['proxy_url']}:{proxy_settings['proxy_port']}"

        else:

            proxies = None

 

    except:

        proxies = None

   

    getData(proxies, verify_ssl, helper, ew)

    # verify permissions

    # setPermissions(local_path)

    # # set checkpoint variables

    # latest_id_cp = findLatestCp(cp_files["id_cp_filename"])

    # # load and format time checkpoint

    # try:

    #     latest_time_cp = dt.strptime(findLatestCp(cp_files["time_cp_filename"]),'%Y-%m-%d %H:%M:%S').strftime('%s')

    # # if loading failed or time_cp file doesnt exist - initiate as 0 epoch time

    # except Exception as e:

    #     latest_time_cp = dt.strptime(findLatestCp(cp_files["time_cp_filename"]),'%S').strftime('%s')

    #     # sys.stderr.write(f'Error: Couldn\'t format time from time_cp - initiated as 0 epochtime | program will continue to execute normally.')

       

    # updated_cp = (getData(latest_id_cp, proxies, should_verify, helper, ew))

   

    # # update the ID checkpoint file with new id_cp value

    # updateCp(id_cp_filename,updated_id_cp)

    # # update time checkpoint with current run time

    # updateCp(time_cp_filename,time_now)

   

    # update multiple checkpoints

    # for cpfile, cp in zip(cp_files.values(), updated_cp.values()):

    #     updateCp(cpfile, cp)
