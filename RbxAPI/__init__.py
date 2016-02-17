# -*- coding: utf-8 -*-
"""
Project: RbxAPI
File: __init__.py
Author: Diana
Creation Date: 10/19/2014

Copyright (C) 2016  Diana Land
Read LICENSE for more information
"""

# Internal
__author__ = 'Diana'
__version__ = '2.0'

import logging
import os
import sys
import time

import requests


# User, Authentication.
class User_:
    loggedIn = False
    loggedInUser = None

    def __init__(self):
        self.LoggedIn = False
        self.Name = None

    def _SetLoggedIn(self, name):
        self.LoggedIn = True
        self.Name = name


# Requests, Session. Internal.
# noinspection PyUnreachableCode
class SessionClass(requests.Session):
    """
    Internal class that provides a wrapper around requests.session()
    """

    def __init__(self):
        """
        Sets up session and headers.
        Initial setup.
        """
        super().__init__()
        self.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0"})

    def get(self, url, **kwargs):
        """
        Overrides requests.Session.get and provides retry on connection fail.

        :param url: Url to access
        :type url: str
        :param kwargs: Extra args
        """
        self.checkLoggedIn()
        while True:
            try:
                return super(SessionClass, self).get(url, **kwargs)
            except (TimeoutError, requests.Timeout):
                print("Warning: Connection Timed Out. Waiting and Retrying...")
                time.sleep(5)
                continue
            except (ConnectionError, requests.ConnectionError):
                print("Warning: Connection error. Retrying...")
                time.sleep(5)
                continue
            break

    def post(self, url, data=None, json=None, **kwargs):
        """
        Overrides requests.Session.post and provides retry on connection fail.

        :param url: URL to access
        :type url: str
        :param data: Data to send in reuqest
        :type data: dict | bytes | filelike-object
        :param json: Json to send in body of request
        :type json: dict
        :param kwargs: Extra args
        """
        self.checkLoggedIn()
        while True:
            try:
                return super(SessionClass, self).post(url, data=data, json=json, **kwargs)
            except (TimeoutError, requests.Timeout):
                print("Warning: Connection Timed Out. Waiting and Retrying...")
                time.sleep(5)
                continue
            except (ConnectionError, requests.ConnectionError):
                print("Warning: Connection error. Retrying...")
                time.sleep(5)
                continue
            break

    def checkLoggedIn(self):
        if not User.loggedIn:
            return
        if '.ROBLOSECURITY' in self.cookies and self.cookies['.ROBLOSECURITY'] != '':
            return
        else:
            LoadAccounts(User.Name)


Session = SessionClass()
User = User_()
DebugLog = logging.getLogger("Debug")
DebugLog.setLevel(logging.DEBUG)
DebugHandler = logging.FileHandler("Debug.log")
DebugHandler.setLevel(logging.DEBUG)
DebugLog.addHandler(DebugHandler)

APILog = logging.getLogger("API")

# URLs. Constants.
TC_URL = "http://www.roblox.com/My/Money.aspx"
CURRENCY_URL = "http://api.roblox.com/currency/balance"
CHECK_URL = "http://www.roblox.com/home"
LOGIN_URL = "https://www.roblox.com/newlogin"
ESTIMATE_URL = "http://www.roblox.com/Marketplace/EconomyServices.asmx?WSDL"

# Requests CA. Required for freezing. Internal.
if getattr(sys, 'frozen', False):
    os.environ["REQUESTS_CA_BUNDLE"] = os.path.abspath(
        os.path.join(os.path.abspath(sys.argv[0]), os.pardir, "cacert.pem"))

from .inputPass import GetNum, GetPass, Pause
from .general import GetValidation, Login, ListAccounts, LoadAccounts, WriteConfig, ReadConfig
from .trade import GetSpread, GetCash, GetRate, IsTradeActive, GetBuxToTixEstimate, GetTixToBuxEstimate
