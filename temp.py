from trading import *
from public import *

import pandas as pd
import numpy as np

import time
from datetime import datetime
import threading
from math import *


CPAIR = 'USDT_BTC'
MARKET = 'USDT'
CURRENCY = 'BTC'

PERIOD = '900'

# MIN = 60
# HOUR = MIN * 60
# DAY = HOUR * 24


def buyAll():
    '''
    '''
    balance = float(returnBalances()[MARKET])
    print('\nStart BUY, Balance:', balance)

    while balance > 99:
        time.sleep(1)
        asks = returnOrderBook(CPAIR)['asks']
        rate = findRate(asks, balance, 'buy')
        amount = str(floor((balance / float(rate) * 100000) / 100000))
        print('\nRate: %s, Amount: %s' %(rate, amount))
        
        print(buy(CPAIR, rate, amount, 'immediateOrCancel'))
        time.sleep(1)
        
        balance = float(returnBalances()[MARKET])
        print('\nAfter Balance:', balance)


def sellAll():
    '''
    '''
    balance = float(returnBalances()[CURRENCY])
    print('\nStart SELL, Amount:', balance)

    while balance > 0.001:
        time.sleep(1)
        bids = returnOrderBook(CPAIR)['bids']
        rate = findRate(bids, balance, 'sell')
        amount = str(balance)
        print('\nRate: %s, Amount: %s' %(rate, amount))
        
        print(sell(CPAIR, rate, amount, 'immediateOrCancel'))
        time.sleep(1)
        
        balance = float(returnBalances()[CURRENCY])
        print('\nAfter Balance:', balance)


def findRate(orderbook, balance, type):
    '''
    '''
    total = 0
    count = 0

    for item in orderbook:
        count += 1
        rate = float(item[0])
        amount = float(item[1])
        if type == 'buy':
            total += (rate * amount)
        if type == 'sell':
            total += amount
        if total > balance:
            print('Taking rate #:', count)
            return str(rate)
    

def main():
    '''
    '''

    now = int(time.time())
    start = str(now - 50 * int(PERIOD))

    data = returnChartData(currencyPair, start, now, PERIOD)
    chart = pd.DataFrame(data)

    chart['ema12'] = pd.ewma(chart['close'], span=12)
    chart['ema26'] = pd.ewma(chart['close'], span=26)
    chart['macd'] = chart['ema12'] - chart['ema26']
    chart['signal'] = pd.ewma(chart['macd'], span=9)


