# -*- coding: utf-8 -*-
"""
Project: TCBot
File: Main.py
Author: Diana
Creation Date: 05/18/2014
Creation Time: 7:46 PM

The frontend for my trading bot.

Copyright (C) 2016  Diana Land
Read LICENSE for more information
"""
import atexit
import math
import os
import sys
import time

from colorama import init, deinit, Fore, reinit
from lxml import html

from RbxAPI import GetPass, GetNum, GetValidation, TC_URL, GetCash, GetRate, Login, ListAccounts, LoadAccounts, \
    IsTradeActive, Pause, Session, GetBuxToTixEstimate, GetTixToBuxEstimate, DebugLog
from RbxAPI.errors import NoAccountsError, SetupError

if getattr(sys, 'frozen', False):
    os.environ["REQUESTS_CA_BUNDLE"] = os.path.abspath(
        os.path.join(os.path.abspath(sys.argv[0]), os.pardir, "cacert.pem"))

values = {
    'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OrderType': 'LimitOrderRadioButton',
    'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$AllowSplitTradesCheckBox': 'on',
    '__EVENTTARGET': 'ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$SubmitTradeButton'
}

version = '3.0'

Banner = """Trade Currency Bot made by Iaz3, offically distrubuted on reddit/bitbucket via MEGA. BOT IS PROVIDED AS IS.
ROBLOX TCBot version {0}, Copyright (C) 2015 Diana
ROBLOX TCBot comes with ABSOLUTELY NO WARRANTY; for details, refer to the LICENSE file.
This is free software, and you are welcome to redistribute it under certain conditions; read the LICENSE file for \
details.
""".format(version)


# noinspection PyUnusedLocal,PyUnreachableCode
def cancel(num):
    """
    Cancel trade.
    Doesnt work properly and i never figured out why.

    :param num: Trade number to delete, starting at zero. Currently not used.
    """
    raise NotImplementedError
    state, event = GetValidation(TC_URL)
    # tra = str(c)  # what to cancel. starts at 0, goes +1
    values2 = {
        'ctl00$ctl00$ScriptManager': ('ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenOffers$OpenOffersUpdat'
                                      'ePanel|ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenOffers$OpenOffers'
                                      'ListView$ctrl0$ctl00$CancelOfferButton'),
        '__EVENTTARGET': ('ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OpenOffe'
                          'rs$OpenOffersListView$ctrl0$ctl00$CancelOfferButton'), '__ASYNCPOST': 'true',
        '__VIEWSTATE': state, '__EVENTVALIDATION': event
    }

    values3 = {
        'ctl00$ctl00$ScriptManager': ('ctl00$ctl00$cphRoblox$cphMyRobloxConte'
                                      'nt$ctl00$OpenBids$OpenBidsUpdatePanel|ctl00$ctl00$c'
                                      'phRoblox$cphMyRobloxContent$ctl00$OpenBids$OpenBidsL'
                                      'istView$ctrl0$ctl00$CancelBidButton'),
        '__EVENTTARGET': ('ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl0'
                          '0$OpenBids$OpenBidsListView$ctrl0$ctl00$CancelBidButton'), '__ASYNCPOST': 'true',
        '__VIEWSTATE': state, '__EVENTVALIDATION': event
    }

    r = s.get(TC_URL)
    tree = html.fromstring(r.text)
    Tremain = tree.xpath(('//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenBids_OpenBidsU'
                          'pdatePanel"]/table/tr[2]/td[2]/text()'))
    Rremain = tree.xpath(('//*[@id="ctl00_ctl00_cphRoblox_cphMyRobloxContent_ctl00_OpenOffers_'
                          'OpenOffersUpdatePanel"]/table/tr[2]/td[2]/text()'))
    try:
        print('Remaining: ' + str(Rremain[0]))
    except Exception as ex:
        print(ex)
    s.post(TC_URL, data=values2)
    s.post(TC_URL, data=values3)


def SubmitTrade(AmountToTrade, ReceiveAmount, CurrencyToTrade):
    """
    Submit a Trade on ROBLOX

    :param AmountToTrade: Amount of Tickets or Robux to trade
    :type AmountToTrade: int
    :param ReceiveAmount: Amount of Tickets or Robux you want to receive.
    :type ReceiveAmount: int
    :param CurrencyToTrade: What currency the AmountToTrade is.
    :type CurrencyToTrade: str
    """
    # if Fast:
    #     values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$OrderType'] = 'MarketOrderRadioButton'
    state, event = GetValidation(TC_URL)
    values['__VIEWSTATE'] = state
    values['__EVENTVALIDATION'] = event
    values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$HaveAmountTextBoxRestyle'] = AmountToTrade
    values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$WantAmountTextBox'] = ReceiveAmount
    if CurrencyToTrade == "Robux":
        values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$HaveCurrencyDropDownList'] = "Robux"
        values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$WantCurrencyDropDownList'] = "Tickets"
    else:
        values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$HaveCurrencyDropDownList'] = "Tickets"
        values['ctl00$ctl00$cphRoblox$cphMyRobloxContent$ctl00$WantCurrencyDropDownList'] = "Robux"
    Session.post(TC_URL, data=values)


def Calculate():
    """
    Where the trade/profit "calculation" happens
    """
    lastBux, lastTix = GetCash()
    print("The bot has started. Do not fear if nothing is shown on screen/it doesnt change for a long time. It is "
          "working\n")
    while True:
        waitTime = 0
        while IsTradeActive():
            waitTime = 1
            # waitTime += 1
            # print("Progress {:2.1%}".format(waitTime / 10), end="\r")
            print('Waiting for trade to go through.', end='\r')
            time.sleep(10)
        if waitTime == 1:
            print("\nDone Waiting For Trade to go through.\n")
        bux, tix = GetCash()  # Money
        buxRate, tixRate = GetRate()
        DebugLog.debug("\nRobux: {0}\nTickets: {1}\n".format(bux, tix))
        DebugLog.debug("Robux Rate: {0}\nTickets Rate: {1}\n".format(buxRate, tixRate))
        # spread = GetSpread()
        if (buxRate == 0.0000) or (tixRate == 0.0000) or (abs(buxRate - tixRate) >= 10):
            DebugLog.info("Bad Rates")
            continue
        if bux:  # Bux to Tix
            tixWant = int(math.floor(bux * tixRate))
            if tixWant > lastTix:
                print("Getting {0} Tix for {1} Bux\n".format(tixWant, bux))
                DebugLog.debug("\n\nGetting {0} Tix for {1} Bux\n\n".format(tixWant, bux))

                lastBux = bux
                SubmitTrade(bux, tixWant, "Robux")
        elif tix:  # Tix to Bux
            buxWant = int(math.floor(tix / buxRate))
            tixCost = int(math.ceil(buxWant * buxRate))

            buxProfit = buxWant - lastBux
            tixProfit = tix - tixCost

            DebugLog.debug("BuxWant: {0}\nTixCost: {1}\nBuxProfit: {2}\nTixProfit:"
                           " {3}\nLastBux: {4}\nLastTix: {5}".format(buxWant, tixCost, buxProfit, tixProfit, lastBux,
                                                                     lastTix))

            if buxProfit > 0 and tixProfit > 0 or buxProfit > 0 and abs(tixProfit) <= 5:
                print("Getting {0} Bux for {1} Tix with "
                      "a potential profit of:\n{2} Robux\n{3} Tickets\n".format(buxWant, tixCost, buxProfit, tixProfit))
                DebugLog.debug("\n\nGetting {0} Bux for {1} Tix with "
                               "a potential profit of:\n{2} Robux\n{3} Tickets\n\n".format(buxWant, tixCost, buxProfit,
                                                                                           tixProfit))
                lastTix = tix + tixProfit
                SubmitTrade(tixCost, buxWant, 'Tickets')
        time.sleep(2)


def FastCalculate(lastTix=None, lastBux=None):
    """
    Fast Trade calculations happen here.

    :param lastBux:
    :type lastBux:
    :param lastTix:
    :type lastTix:
    """
    print("WARNING: THIS IS AN EXPERIMENTAL FEATURE."
          "\nTESTS SHOW THAT IT CAN MAKE A LOT OF PROFIT QUICKLY, AT TIMES."
          "\nBUT ALSO IT CAN LOSE MONEY. CURRENTLY UNRELIABLE. YOU HAVE BEEN WARNED")
    if lastTix is None and lastBux is None:
        lastTix, lastBux = GetCash()
    else:
        lastTix, lastBux = lastTix, lastBux
    while True:
        bux, tix = GetCash()
        if bux:  # Bux to Tix.
            lastBux = bux
            want = GetBuxToTixEstimate(bux)
            while True:  # Calculates minimum required robux required to get same amount of tix.
                bux -= 1
                if GetBuxToTixEstimate(bux) < want:
                    bux += 1
                    break
            GetTix = lastTix + 20
            if want > GetTix:
                if GetBuxToTixEstimate(bux) >= want:  # Make sure still getting the same, correct, amount.
                    print("Getting {0} Tickets".format(want))
                    SubmitTrade(bux, 'Robux', want, 'Tickets', Fast=True)
                else:
                    FastCalculate(lastTix, lastBux)
        elif tix:  # Tix to bux
            lastTix = tix
            want = GetTixToBuxEstimate(tix)
            while True:  # Calculates minimum required tickets required to get same amount of robux.
                tix -= 1
                if GetTixToBuxEstimate(tix) < want:
                    tix += 1
                    break
            if want > lastBux:
                if GetTixToBuxEstimate(tix) >= want:
                    print("Getting {0} Robux".format(want))
                    SubmitTrade(tix, 'Tickets', want, 'Robux', Fast=True)
                else:
                    FastCalculate(lastTix, lastBux)


def _mode():
    """
    What Trading Mode?

    :return: Trading Mode. True means Default. False means FAST.
    :rtype: bool
    """
    reinit()
    print(Fore.WHITE + '   1: Default Trading')
    print(Fore.WHITE + '   2: Fast Trading')
    choice = GetNum()
    if choice == 1:
        return True
    elif choice == 2:
        return False
    print(Fore.RESET + "")


def setup():
    """
    Setup the bot.

    :raises: SetupError, NoAccountsError
    """
    init(convert=True)
    print(Fore.WHITE + '   1: Log In?')
    print(Fore.WHITE + '   2: Load Account?')
    choice = GetNum()
    if not choice:
        raise SetupError()
    if choice == 1:
        deinit()
        while True:
            user = input('Username: ')
            if user:
                Login(user, GetPass())
                break
    elif choice == 2:
        accounts = ListAccounts()
        if not accounts:
            raise NoAccountsError()
        print(Fore.YELLOW + 'Accounts:')
        for acc in accounts:
            print(Fore.YELLOW + '*  ' + acc)
        while True:
            account = input('Log in to: ')
            if account in accounts:
                LoadAccounts(account)
                break
    deinit()


def main():
    """
    The main function.
    It all starts here
    """
    if True:  # _mode():
        Calculate()
    else:  # Fast Trade
        FastCalculate()
        # TODO: Log of trades and profits.


@atexit.register
def closing():
    """

    :return:
    :rtype:
    """
    deinit()
    Pause()


if __name__ == '__main__':
    print(Banner)
    try:
        setup()
        main()
    except KeyboardInterrupt:
        pass
