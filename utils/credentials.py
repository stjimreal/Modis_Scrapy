'''
Date: 2021-07-24 00:57:16
LastEditors: LIULIJING
LastEditTime: 2021-07-25 00:55:27
'''
from __future__ import print_function

from utils.globals import URS_URL

import base64
import netrc
from getpass import getpass

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
    
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
    try:
        info = netrc.netrc()
        username, _, password = info.authenticators(urlparse(URS_URL).hostname)
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

    return credentials