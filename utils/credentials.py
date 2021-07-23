'''
Date: 2021-07-24 00:57:16
LastEditors: LIULIJING
LastEditTime: 2021-07-24 01:28:01
'''
from __future__ import print_function

from utils.globals import URS_URL

import logging
import logging.handlers
import re
import base64
import itertools
import json
import math
import netrc
import os.path
import ssl
import sys
import time
from getpass import getpass

try:
    from urllib.parse import urlparse
    from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor
    from urllib.error import HTTPError, URLError
except ImportError:
    from urlparse import urlparse
    from urllib2 import urlopen, Request, HTTPError, URLError, build_opener, HTTPCookieProcessor

def get_username():
    username = ''

    # For Python 2/3 compatibility:
    try:
        do_input = raw_input  # noqa
    except NameError:
        do_input = input

    while not username:
        username = do_input('Earthdata username: ')
    return username


def get_password():
    password = ''
    while not password:
        password = getpass('password: ')
    return password

def get_credentials():
    """Get user credentials from .netrc or prompt for input."""
    global URS_URL
    credentials = None
    errprefix = ''
    try:
        info = netrc.netrc()
        username, account, password = info.authenticators(urlparse(URS_URL).hostname)
        errprefix = 'netrc error: '
    except Exception as e:
        if (not ('No such file' in str(e))):
            print('netrc error: {0}'.format(str(e)))
        username = None
        password = None

    while not credentials:
        if not username:
            username = get_username()
            password = get_password()
        credentials = '{0}:{1}'.format(username, password)
        credentials = base64.b64encode(credentials.encode('ascii')).decode('ascii')

        # if url:
        #     try:
        #         req = Request(url)
        #         req.add_header('Authorization', 'Basic {0}'.format(credentials))
        #         opener = build_opener(HTTPCookieProcessor())
        #         opener.open(req)
        #     except HTTPError:
        #         print(errprefix + 'Incorrect username or password')
        #         errprefix = ''
        #         credentials = None
        #         username = None
        #         password = None

    return credentials