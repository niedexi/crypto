import urllib.parse
import requests
import time
import hmac
import hashlib
from utils import *


def getKline(symbol, period, size=99):
    """
    :param period：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }
    :param size： [1,2000]
    """
    params = {'symbol': symbol,
              'period': period,
              'size': size}

    url = MARKET_URL + '/market/history/kline'
    return requests.get(url, params).json()


def getSymbols():
    """
    """
    url = MARKET_URL + '/v1/common/symbols'
    return requests.get(url).json()


def getCurrency():
    """
    """
    url = MARKET_URL + '/v1/common/currencys'
    return requests.get(url).json()



### TRADING API ###

def getAccounts():
    """
    """
    path = "/v1/account/accounts"
    params = {}
    return api_key_get(params, path)


def getBalance(actID, symbol=None):
    """
    """
    url = "/v1/account/accounts/{0}/balance".format(actID)
    params = {"account-id": actID}

    if not symbol:
        for item in api_key_get(params, url)['data']['list']:
            if float(item['balance']) > 0:
                print(item)
    else:  
        for item in api_key_get(params, url)['data']['list']:
            if item['currency'] == symbol and item['type'] == 'trade':
                return item['balance']


def makeOrder(actID, symbol, amount, method, price=None, source='api'):
    """
    method: {buy-market, sell-market, buy-limit, sell-limit, buy-limit-maker, sell-limit-maker}
    """
    params = {"account-id": actID,
              "amount": amount,
              "symbol": symbol,
              "type": method,
              "source": source}
    if price:
        params["price"] = price

    url = '/v1/order/orders/place'
    return api_key_post(params, url)


def cancelOrder(orderID):
    """
    """
    params = {}
    url = "/v1/order/orders/{0}/submitcancel".format(orderID)
    return api_key_post(params, url)


### ORDER INFO ###

def orderInfo(orderID):
    """
    """
    params = {}
    url = "/v1/order/orders/{0}".format(orderID)
    return api_key_get(params, url)


def orderMatchresults(orderID):
    """
    """
    params = {}
    url = "/v1/order/orders/{0}/matchresults".format(orderID)
    return api_key_get(params, url)


def getOpenOrders(actID, symbol, side=None, size=10):
    """
    """
    params = {}
    url = "/v1/order/openOrders"
    
    if symbol:
        params['symbol'] = symbol
    if actID:
        params['account-id'] = actID
    if side:
        params['side'] = side
    if size:
        params['size'] = size
    
    return api_key_get(params, url)


def getOrders(symbol, states, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol: 
    :param states: 可选值 {pre-submitted 准备提交, submitted 已提交, partial-filled 部分成交, partial-canceled 部分成交撤销, filled 完全成交, canceled 已撤销}
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    url = '/v1/order/orders'

    params = {'symbol': symbol, 'states': states}
    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    
    return api_key_get(params, url)


def getMatchresults(symbol, types=None, start_date=None, end_date=None, _from=None, direct=None, size=None):
    """
    :param symbol: 
    :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
    :param start_date: 
    :param end_date: 
    :param _from: 
    :param direct: 可选值{prev 向前，next 向后}
    :param size: 
    :return: 
    """
    url = '/v1/order/matchresults'

    params = {'symbol': symbol}
    if types:
        params['types'] = types
    if start_date:
        params['start-date'] = start_date
    if end_date:
        params['end-date'] = end_date
    if _from:
        params['from'] = _from
    if direct:
        params['direct'] = direct
    if size:
        params['size'] = size
    
    return api_key_get(params, url)

