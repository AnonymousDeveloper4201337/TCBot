# -*- coding: utf-8 -*-
"""
Project: RbxAPI
File: general.py
Author: Diana
Creation Date: 8/2/2014

General use module.
Functions that are commonly used among programs are here.

Copyright (C) 2016  Diana Land
Read LICENSE for more information
"""
import configparser
import json
import os
import pickle
import re
import sys

from bs4 import BeautifulSoup

from RbxAPI import errors, Session, CHECK_URL, LOGIN_URL, User


def _RbxToken(element):
    """
    Parses HTML for ROBLOX XsrfToken.

    Used by beautiful soup.

    :param element: Element received from Beautiful Soup.
    :type element: BeautifulSoup
    :return: True/False depending on weather element matched.
    :rtype: bool
    """
    if element.name.lower() == "script" and re.match(r"^\s*Roblox\.XsrfToken\.setToken.*", element.text, re.IGNORECASE):
        # PATCH: Added ignore whitespace at begining.
        return True
    return False


def GetToken():
    """
    Get X-CSRF-TOKEN for use in sending messages/other activies.

    :return: The Token
    :rtype: str
    """
    token = BeautifulSoup(Session.get('http://www.roblox.com/user.aspx').text, "lxml")
    token = token.find_all(_RbxToken)
    token = re.findall(r"\((.*)\)", token[0].text)[0]
    token = re.sub("'", '', token)
    return token


def GetValidation(url):
    """
    gets validation from webpage for submitting requests

    Works around ROBLOX thingy

    :param url: Url to look at.
    :return: Validation. Returns 2 items.
    """
    b = BeautifulSoup(Session.get(url).text, "lxml")
    viewState = b.findAll("input", {"type": "hidden", "name": "__VIEWSTATE"})
    eventValidation = b.findAll('input', {'type': 'hidden', 'name': '__EVENTVALIDATION'})
    return viewState[0]['value'], eventValidation[0]['value']


def ListAccounts():
    """
    List the accounts currently saved to disk

    :return: List of accounts
    :rtype: list
    """
    accounts = []
    for file in os.scandir(ReturnConfigPath()):
        if file.is_file() and file.name.endswith('.acc'):
            accounts.append(file.name.split('.')[0])
    return accounts


def LoadAccounts(username):
    """
    Load the specififed account

    :param username: The account to load
    :type username: str
    :return: True if success
    :rtype: bool
    """
    username = str(username)
    with open(ReturnConfigPath(username + '.acc'), 'rb') as file:
        try:
            # cookies = pickle.load(file)
            data = pickle.load(file)
        except EOFError:
            raise errors.StorageError()
        # Session.cookies = cookies
        Session.post(LOGIN_URL, data=data)  # For auto login
        if Session.get(CHECK_URL).url != CHECK_URL:
            raise errors.AccountsError()
        User._SetLoggedIn(username)
        return True


def Login(username, pwd):
    """
    Login into the account

    :param pwd: Password used to login
    :type pwd: str
    :param username: Username used to log in
    :type username: str
    """
    username = str(username)
    if not username:
        raise errors.NoUsernameError()
    with open(ReturnConfigPath(username + '.acc'), 'wb') as f:
        data = {'username': username, 'password': pwd}
        Session.post(LOGIN_URL, data=data)  # login
        Session.get(CHECK_URL)
        if '.ROBLOSECURITY' in Session.cookies:
            # pickle.dump(Session.cookies, f)
            pickle.dump(data, f)  # Save the username and password now. This way we can automatically login and
            # support running the bot 24/7 nonstop. Currently the cookie can expire and crash it.
            print('Save Successful')
            User._SetLoggedIn(username)
            return True
        else:
            f.close()
            os.remove(f.name)
            raise errors.AccountsError()


def Convert(obj):
    """
    Convert javascript things to Python types
    Probably a better way to do it....

    :param obj: Objected to be converted to use Python types
    :return Converted object
    """
    # Warning, this will fail if theres a problem with the internet and the page doesnt load correctly. Obj will be bad.
    try:
        return json.loads(obj)
    except json.JSONDecodeError:
        return {}


def ReturnConfigPath(file=None):
    """
    Returns the path used for Data Storage.

    :param file: File to create path to. May or may not exist. optional.
    :type file: str
    :return: Path
    :rtype: str
    """
    # Windows only
    if sys.platform == 'win32':
    	path = os.path.abspath(os.path.join(os.getenv("APPDATA"), "Iaz3Programs", "TCBot"))
    else:
    	path = os.path.abspath('./')
    if not os.path.isdir(path):
        os.makedirs(path)
    if file:
        return os.path.join(path, file)
    if not file:
        return path


def WriteConfig(data):
    """
    Write config file.

    :param data: Data
    :type data: dict
    """
    config = configparser.ConfigParser()
    config[User.loggedInUser] = data
    with open(ReturnConfigPath('config.ini'), 'w') as configfile:
        config.write(configfile)
        configfile.close()


def ReadConfig(username, key):
    """
    Read from config file.

    :param username: User's Data to access
    :type username: str
    :param key: Key/Value to retrieve
    :type key: str
    :return: Value requested, so far only int values.
    :rtype: int
    """
    # TODO: Adapt to user class
    config = configparser.ConfigParser()
    config.read(ReturnConfigPath('config.ini'))
    if username in config:  # Previously saved config.
        userData = config[username]
        return userData.get(key, 0)
    else:  # No existing config file, currently logged in.
        return 0


if __name__ == '__main__':
    pass
