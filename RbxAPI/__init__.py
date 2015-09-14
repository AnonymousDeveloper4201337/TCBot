# -*- coding: utf-8 -*-
"""
Project: ROBLOX
File: __init__.py
Author: Diana
Creation Date: 10/19/2014

Copyright (C) 2015  Diana Land
Read LICENSE for more information
"""

import os

import requests


# Internal
__author__ = 'Diana'
__version__ = 2.0

# Requests, Session. Internal.
Session = requests.session()
Session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0"})

# URLs
TCUrl = "http://www.roblox.com/My/Money.aspx"
CurrencyURL = "http://api.roblox.com/currency/balance"
CheckURL = "http://www.roblox.com/home"
LoginURL = "https://www.roblox.com/newlogin"

# Requests CA. Required for freezing. Internal.
# FIXME: Only do this when frozen.
# os.environ["REQUESTS_CA_BUNDLE"] = os.path.join('cacert.pem')
# os.environ["REQUESTS_CA_BUNDLE"] = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'cacert.pem'))
os.environ["REQUESTS_CA_BUNDLE"] = os.path.abspath(os.path.join(os.path.realpath("__file__"), os.pardir, "cacert.pem"))


# TODO: Move imports here. Create an API. Add constants.
from .inputPass import getnum, getpass
from .general import getValidation, login, listAccounts, loadAccounts, writeConfig, readConfig
from .trade import getSpread, getCash, getRate, checkTrades
