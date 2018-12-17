import urllib.parse
import requests
import time
import hmac
import hashlib


class Poloniex:
    PUBLIC = 'https://poloniex.com/public'
    TRADING = "https://poloniex.com/tradingApi"


    def __init__(self, key, secret):
        self.KEY = key
        self.SECRET = secret.encode('utf8')
        self.nonce = int(time.time())


    def auth(self, message):
        '''
        Helper for sending post request
        '''
        data = urllib.parse.urlencode(message).encode('utf8')
        sign = hmac.new(self.KEY, data, hashlib.sha512).hexdigest()
        headers = {'Sign': sign, 'Key': self.KEY}
        res = requests.post(Poloniex.TRADING, data=message, headers=headers)
        return res.json()


    @staticmethod
    def returnTicker():
        '''
        Returns the ticker for all markets
        '''
        command = {'command': 'returnTicker'}
        res = requests.get(Poloniex.PUBLIC, params = command)
        return res.json()


    @staticmethod
    def return24Volume():
        '''
        Returns the 24-hour volume for all markets, plus totals for primary currencies
        '''
        command = {'command': 'return24hVolume'}
        r = requests.get(Poloniex.PUBLIC, params=command)
        return r.json()


    @staticmethod
    def returnOrderBook(currencyPair='all', depth: int=None):
        '''
        Returns the order book for a given market
        '''
        if depth:
            command = {'command': 'returnOrderBook', 'currencyPair': currencyPair, 'depth': depth}
        else:
            command = {'command': 'returnOrderBook', 'currencyPair': currencyPair}
        r = requests.get(Poloniex.PUBLIC, params=command)
        return r.json()


    @staticmethod
    def returnPTH(currencyPair, start=None, end=None):
        '''
        returnPublicTradeHistory
        Returns the past 200 trades for a given market,
        or up to 50,000 trades between a range specified in UNIX timestamps
        '''
        if start and end:
            command = {'command': 'returnTradeHistory', 'currencyPair': currencyPair, 'start': start, 'end': end}
        else:
            command = {'command': 'returnTradeHistory', 'currencyPair': currencyPair}
        r = requests.get(Poloniex.PUBLIC, params=command)
        return r.json()


    @staticmethod
    def returnChartData(currencyPair, start, end, period='300'):
        '''
        Returns candlestick chart data.
        '''
        command = {'command': 'returnChartData', 'currencyPair': currencyPair, 'start': start, 'end': end, 'period': period}
        r = requests.get(Poloniex.PUBLIC, params=command)
        return r.json()


    @staticmethod
    def returnCurrencies():
        '''Returns information about currencies.
        '''
        command = {'command': 'returnCurrencies'}
        r = requests.get(Poloniex.PUBLIC, params=command)
        return r.json()




    ### ACCOUNT INFORMATION ###
    def returnBalances(self):
        '''Returns all of your available balances
        '''
        self.nonce += 1
        message = {'command': 'returnBalances', 'nonce': self.nonce}
        return self.auth(message)


    def returnCompleteBalances(self):
        '''Returns all of your balances, including available balance, balance on orders,
        and the estimated BTC value of your balance
        '''
        self.nonce += 1
        message = {'command': 'returnCompleteBalances', 'nonce': self.nonce}
        return self.auth(message)


    def returnOpenOrders(self, curpair='all'):
        '''Returns your open orders for a given market
        '''
        self.nonce += 1
        message = {'command': 'returnOpenOrders', 'nonce': self.nonce, 'currencyPair': curpair}
        return self.auth(message)


    def returnTradeHistory(self, curpair='all', start=None, end=None):
        '''Returns your trade history for a given market
        You may optionally specify a range via "start" and/or "end" parameters, given in UNIX timestamp format
        if you do not specify a range, it will be limited to one day.
        '''
        self.nonce += 1
        if start and end:
            message = {'command': 'returnTradeHistory', 'nonce': self.nonce, 'currencyPair': curpair, 'start': start, 'end': end}
        else:
            message = {'command': 'returnTradeHistory', 'nonce': self.nonce, 'currencyPair': curpair}
        return self.auth(message)


    def returnOrderTrades(self, ordernumber):
        '''Returns all trades involving a given order
        '''
        self.nonce += 1
        message = {'command': 'returnOrderTrades', 'nonce': self.nonce, 'orderNumber': ordernumber}
        return self.auth(message)



    ### BUY & SELL ###

    def buy(self, curpair, rate, amount, option=None):
        '''Places a limit buy order in a given market.
        option: ["fillOrKill", "immediateOrCancel", "postOnly"]
        '''
        self.nonce += 1
        if option:
            message = {'command': 'buy', 'nonce': self.nonce, 'currencyPair': curpair, 'rate': rate, 'amount': amount, option: '1'}
        else:
            message = {'command': 'buy', 'nonce': self.nonce, 'currencyPair': curpair, 'rate': rate, 'amount': amount}
        return self.auth(message)


    def sell(self, curpair, rate, amount, option=None):
        '''Places a sell order in a given market.
        option: ["fillOrKill", "immediateOrCancel", "postOnly"]
        '''
        self.nonce += 1
        if option:
            message = {'command': 'sell', 'nonce': self.nonce, 'currencyPair': curpair, 'rate': rate, 'amount': amount, option: '1'}
        else:
            message = {'command': 'sell', 'nonce': self.nonce, 'currencyPair': curpair, 'rate': rate, 'amount': amount}
        return self.auth(message)


    def cancel_order(self, ordernumber):
        '''Cancels an order you have placed in a given market
        '''
        self.nonce += 1
        message = {'command': 'cancelOrder', 'nonce': self.nonce, 'orderNumber': ordernumber}
        return self.auth(message)


    def move_order(self, ordernumber, rate):
        '''Cancels an order and places a new one of the same type in a single atomic transaction
        '''
        self.nonce += 1
        message = {'command': 'moveOrder', 'nonce': self.nonce, 'orderNumber': ordernumber, 'rate': rate}
        return self.auth(message)



    ### DEPOSIT & WITHDRAWL ###

    def returnDepositsWithdrawals(self, start, end):
        '''Returns your deposit and withdrawal history within a range in UNIX timestamps.
        '''
        self.nonce += 1
        message = {'command': 'returnDepositsWithdrawals', 'nonce': self.nonce, 'start': start, 'end': end}
        return self.auth(message)


    def return_deposit_addresses(self):
        '''Returns all of your deposit addresses
        '''
        self.nonce += 1
        message = {'command': 'returnDepositAddresses', 'nonce': self.nonce}
        return self.auth(message)


    def generate_new_address(self, currency):
        '''Generates a new deposit address for the currency specified
        '''
        self.nonce += 1
        message = {'command': 'generateNewAddress', 'nonce': self.nonce, 'currency': currency}
        return self.auth(message)


    def withdraw(self, currency, amount, address):
        '''Immediately places a withdrawal for a given currency
        '''
        self.nonce += 1
        message = {'command': 'returnBalances', 'nonce': self.nonce, 'currency': currency, 'amount': amount, 'address': address}
        return self.auth(message)



    ### MARGIN TRADE ###

    def returnAAB(self, account=None):
        '''returnAvailableAccountBalances: Returns balances sorted by account.
        '''
        self.nonce += 1
        if account:
            message = {'command': 'returnAvailableAccountBalances', 'nonce': self.nonce, 'account': account}
        else:
            message = {'command': 'returnAvailableAccountBalances', 'nonce': self.nonce}
        return self.auth(message)


    def returnTB(self):
        '''returnTradableBalances:
        Returns current tradable balances for each currency in each market for which margin TRADING is enabled.
        '''
        self.nonce += 1
        message = {'command': 'returnTradableBalances', 'nonce': self.nonce}
        return self.auth(message)


    def returnMAS(self):
        '''returnMarginAccountSummary: Returns a summary of your entire margin account.
        '''
        self.nonce += 1
        message = {'command': 'returnMarginAccountSummary', 'nonce': self.nonce}
        return self.auth(message)


    def transferBalance(self, currency, amount, fromAccount, toAccount):
        '''Transfers funds from one account to another.
        '''
        self.nonce += 1
        message = {'command': 'transferBalance', 'nonce': self.nonce, 'currency': currency, 'amount': amount, 'fromAccount': fromAccount, 'toAccount': toAccount}
        return self.auth(message)


    def marginBuy(self, currencyPair, rate, amount, lendingRate=None):
        '''Places a margin buy order in a given market.
        '''
        self.nonce += 1
        if lendingRate:
            message = {'command': 'marginBuy', 'nonce': self.nonce, 'currencyPair': currencyPair, 'rate': rate, 'amount': amount, 'lendingRate': lendingRate}
        else:
            message = {'command': 'marginBuy', 'nonce': self.nonce, 'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return self.auth(message)


    def marginSell(self, currencyPair, rate, amount, lendingRate=None):
        '''Places a margin sell order in a given market.
        '''
        self.nonce += 1
        if lendingRate:
            message = {'command': 'marginSell', 'nonce': self.nonce, 'currencyPair': currencyPair, 'rate': rate, 'amount': amount, 'lendingRate': lendingRate}
        else:
            message = {'command': 'marginSell', 'nonce': self.nonce, 'currencyPair': currencyPair, 'rate': rate, 'amount': amount}
        return self.auth(message)


    def getMarginPosition(self, currencyPair='all'):
        '''Returns information about your margin position in a given market.
        '''
        self.nonce += 1
        message = {'command': 'getMarginPosition', 'nonce': self.nonce, 'currencyPair': currencyPair}
        return self.auth(message)


    def closeMarginPosition(self, currencyPair):
        '''Closes your margin position in a given market.
        '''
        self.nonce += 1
        message = {'command': 'closeMarginPosition', 'nonce': self.nonce, 'currencyPair': currencyPair}
        return self.auth(message)



    ### OTHER ###

    def returnFeeInfo(self):
        '''returns your current TRADING fees and trailing 30-day volume in BTC.
        '''
        self.nonce += 1
        message = {'command': 'returnFeeInfo', 'nonce': self.nonce}
        return self.auth(message)