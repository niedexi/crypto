from poloniex import Poloniex

import pandas as pd
import numpy as np

import time
from datetime import datetime
import threading

m = 60
h = m * 60
d = h * 24

curPair = 'USDT_ETH'
proportion = 0.5
differ = 0.9
bprice = 0.9
sprice = 1.014
temp = []


def clear(pair):
    order = return_open_orders(pair)
    for item in order:
        if item['type'] == 'buy':
            print('\nCancel:\n', cancel_order(item['orderNumber'])['message'])


def sellorder():
    for item in temp:
        ordernumber = item['orderNumber']
        for order in return_order_trades(ordernumber):
            if order != 'error':
                amount = float(order['amount'])
                rate = float(order['rate'])
                fee = float(order['fee'])
                srate = rate * sprice
                samount = amount * (1 - fee)
                print('\n#Sell Order#\nAmount: %s\nRate: %s' % (samount, srate))
                print(sell(curPair, str(srate), str(samount)))
    temp[:] = []


def main():
    threading.Timer(900, main).start()
    now = int(time.time())
    start = now - 6 * h
    js = return_chart_data(curPair, str(start), '9999999999', '900')
    eth = pd.read_json(js)
    eth["10d"] = np.round(eth["weightedAverage"].rolling(window=10, center=False).mean(), 2)
    eth["20d"] = np.round(eth["weightedAverage"].rolling(window=20, center=False).mean(), 2)
    day10 = eth['10d'].tolist()[-2]
    day20 = eth['20d'].tolist()[-2]

    div = '+' * 30
    print('\n\n', div, '\nTime:', str(datetime.utcnow()))
    print('10 day MA:', day10)
    print('20 day MA:', day20)

    if day10 <= (day20 * differ):
        clear(curPair)
        sellorder()
        usdt = float(return_balances()['USDT'])
        spend = usdt * proportion
        rate = day10 * bprice
        amount = spend / rate
        print('\n#Buy Order#\nTotal USD: %s\nSpending: %s\nRate: %s\nAmount: %s\n' % (usdt, spend, rate, amount))
        buyorder = buy(curPair, str(rate), str(amount))
        temp.append(buyorder)
        print(buyorder)


if __name__ == "__main__":
    main()
