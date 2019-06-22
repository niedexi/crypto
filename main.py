from trading import *
from public import *

import pandas as pd
import numpy as np

import time
from datetime import datetime
import threading

m = 60
h = m * 60
d = h * 24

curPair = 'USDT_BTC'
macdcur =  0.4064169257833896
macdsig = 0.3717666149468296
macd_last = 0.3893547426780515
macdsig_last = 0.3673695830140241
lowmax = macd_last       #default ema_last, down 0, up 1
highmax = macd_last

tendi = -1
last_high_low = -1
trans_comp = 0 #w0 imcomplete; 1 complete
turn_counter = 0
gate = 36

def buyall():
    act_already = 0
    balance = float(return_balances()['USDT'])
    f = open('log.txt', 'a')
    f.write('\n------------------------------------\n')
    f.write(str(datetime.utcnow()))
    f.write('Trying to Buy\n')
    while balance > 0.0001:
        balance = float(return_balances()['USDT'])
        print('buying')
        buyjs = return_order_book(1)
        buylist = buyjs['asks'][0:1]
        ask_price = float(''.join(str(x) for x in buylist)[2:14])
        ask_amount = float(''.join(str(x) for x in buylist)[17:25][:-1])
        print('lowest price: ',ask_price)
        print('with amount: ', ask_amount)
        affordable_amount = round(balance/ask_price, 8)
        print('amount i could afford: ',affordable_amount)
        if balance < 0.0001 and act_already == 0:
            print('Not enough balance!')
            f.write('Not enough balance!')
        elif balance < 0.0001 and act_already == 1:
            print('Done!')
            break
        if ask_amount >= affordable_amount and ask_amount > 0.0001:
            buy(curPair, ask_price, affordable_amount ,'immediateOrCancel')
            act_already = 1
            print('buying %s at price %s'% (affordable_amount, ask_price))
            f.write('buying %s at price %s\n'% (affordable_amount, ask_price))
            print('money left: ',balance)
        elif ask_amount < affordable_amount:
            buy(curPair, ask_price, ask_amount ,'immediateOrCancel')
            act_already = 1
            print('buying %s at price %s'% ( ask_amount, ask_price))
            f.write('buying %s at price %s\n'% ( ask_amount, ask_price))
            print('money left: ',balance)
    print('Not enough balance')
    f.write('\n------------------------------------\n')
    f.close()


def sellall():
    act_already = 0
    f = open('log.txt' , 'a')
    f.write('\n------------------------------------\n')
    f.write(str(datetime.utcnow()))
    f.write('Trying to Sell\n')
    amount = float(return_balances()['BTC'])
    while amount > 0.00001:
        amount = float(return_balances()['BTC'])
        print('selling')
        selljs = return_order_book(1)
        selllist = selljs['bids'][0:1]
        bid_price = float(''.join(str(x) for x in selllist)[2:14])
        bid_amount = float(''.join(str(x) for x in selllist)[17:25][:-1])

        print('highest price: ',bid_price)
        print('with amount: ',bid_amount)
        if amount < 0.000001 and act_already == 0:
            print('Not enough balance')
            f.write('Not enough balance')
        elif amount < 0.000001 and act_already == 1:
            print('Done!')
            break
        if bid_amount >= amount:
            sell(curPair,bid_price, amount ,'immediateOrCancel')
            act_already = 1
            print('selling %s at price %s'% (amount,bid_price))
            f.write('selling %s at price %s\n'% (amount,bid_price))
        elif bid_amount < amount:
            sell(curPair,bid_price, bid_amount ,'immediateOrCancel')
            act_already = 1
            print('selling %s at price %s'% (bid_amount,bid_price))
            f.write('selling %s at price %s\n'% (bid_amount,bid_price))
    print('Not enough BTC')
    f.write('------------------------------------')
    f.close()

def main():

    global macdcur
    global macdsig
    global macd_last
    global macdsig_last
    global lowmax
    global highmax
    global tendi
    global last_high_low
    global trans_comp
    global turn_counter
    global gate
    
    
    threading.Timer(300, main).start()
    now = int(time.time())
    start = now - 260 * m
    start12 = now - 70 * m
    start26 = now - 140 * m
    
    # f = open('log.txt' , 'a')
    # print('---------------------------------------')
    # print('Time:', str(datetime.utcnow()))
    # f.write('\n------------------------------------\n')
    # f.write(str(datetime.utcnow()))
    
    balance = float(return_balances()['USDT'])
    amount = float(return_balances()['BTC'])

    # print('balance= ', balance)
    # print('BTC= ', amount)
    # print('start time: ', start)
    # f.write('\nbalance= %s'% balance)
    # f.write('\nBTC= %s'% amount)
    # f.write('\nstart time: %s'% start)

    js12 = return_chart_data(curPair, str(start12), '9999999999', '300')
    eth12 = pd.read_json(js12)
    eth12["close"] = np.round(eth12["close"].rolling(window=1, center=False).mean(), 8)
    ema12_list = eth12['close'].tolist()
    ema12 = (sum(ema12_list) - ema12_list[-1]) / (float(len(ema12_list)) - 1)
    
    js26 = return_chart_data(curPair, str(start26), '9999999999', '300')
    eth26 = pd.read_json(js26)
    eth26["close"] = np.round(eth26["close"].rolling(window=1, center=False).mean(), 8)
    ema26_list = eth26['close'].tolist()
    ema26 = (sum(ema26_list) - ema26_list[-1]) / (float(len(ema26_list)) - 1)
    
    sig = (macdcur - macdsig)* 0.2 + macdsig
    
    js50 = return_chart_data(curPair, str(start), '9999999999', '300')
    eth50 = pd.read_json(js50)
    eth50["close"] = np.round(eth50["close"].rolling(window=1, center=False).mean(), 8)
    ema50_list = eth50['close'].tolist()

    macd = ema12 - ema26
    macd_last = macdcur
    macdcur = macd
    macdsig_last = macdsig
    macdsig = sig

    # print('macd: ', macd)
    # f.write('\nmacd: %s'% macd)
    # print('macd_last: ', macd_last)
    # f.write('\nmacd_last: %s'% macd_last)
    # print('macdsig: ', macdsig)
    # f.write('\nmacdsig: %s'% macdsig)
    # print('macdsig_last: ', macdsig_last)
    # f.write('\nmacdsig_last: %s'% macdsig_last)
    return

    if gate > 0:
        gate = gate - 1
        # print('Ajusting macd & sig, remaining time %s mins' % str(gate*5))
        # f.write('Ajusting macd & sig, remaining time %s mins' % str(gate*5))
        return
    
    if macd > macd_last:
        if tendi == -1:
            tendi = 1
            lowmax = macd_last
            # print('going up; macd - lowmax:', macd - lowmax)
            # f.write('\ngoing up; macd - lowmax:%s'% str(macd - lowmax))
            return()
            if (macd - lowmax> 0.1):
                buyall()
                trans_comp = 1
        elif tendi == 0:
            tendi = 1
        
            if turn_counter == 0:
                turn_counter = 1
            else:
                turn_counter = 0  

            if trans_comp == 1:
                trans_comp = 0
                lowmax = macd_last
                # print('going up; macd - lowmax:',macd - lowmax)
                # f.write('\ngoing up; macd - lowmax:%s'% str(macd - lowmax))
                if (macd - lowmax> 0.1):
                    buyall()
                    trans_comp = 1
            elif turn_counter == 0:
                last_high_low = highmax
                lowmax = macd_last
                # print('going up; macd - lowmax:',macd - lowmax)
                # f.write('\ngoing up; macd - lowmax:%s'% str(macd - lowmax))
                if (macd - lowmax> 0.1):
                    buyall()
                    trans_comp = 1
            else:
                lowmax = last_high_low
                # print('going up; macd - lowmax:', macd - lowmax)
                # f.write('\ngoing up; macd - lowmax:%s'% str(macd - lowmax))
                if (macd - lowmax> 0.1):
                    buyall()
                    trans_comp = 1
                    turn_counter = 0
        elif tendi == 1:
            # print('going up; macd - lowmax:',macd - lowmax)
            # f.write('\ngoing up; macd - lowmax:%s'% str(macd - lowmax))
            if (macd - lowmax> 0.1):
                buyall()
                trans_comp = 1
                
    elif macd < macd_last:
        if tendi == -1:
            tendi = 0;
            highmax = macd_last
            # print('going down, highmax - macd:',highmax - macd)
            # f.write('\ngoing down, highmax - macd: %s'% str(highmax - macd))
            if (highmax - macd > 0.1):
                sellall()
                trans_comp = 1
        elif tendi == 0:
            # print('going down, highmax - macd:',highmax - macd)
            # f.write('\ngoing down, highmax - macd: %s'% str(highmax - macd))
            if (highmax - macd > 0.1):
                sellall()
                trans_comp = 1
        elif tendi == 1:
            tendi = 0
        
        
            if turn_counter == 0:
                turn_counter = 1
            else:
                turn_counter = 0
            
            
            if trans_comp == 1:
                trans_comp = 0
                highmax = macd_last
                # print('going down, highmax - macd:',highmax - macd)
                # f.write('\ngoing down, highmax - macd: %s'% str(highmax - macd))
                if (highmax - macd > 0.1):
                    sellall()
                    trans_comp = 1
            elif turn_counter == 0:
                last_high_low = lowmax
                highmax = macd_last
                # print('going down, highmax - macd:',highmax - macd)
                # f.write('\ngoing down, highmax - macd: %s'% str(highmax - macd))
                if (highmax - macd > 0.1):
                    sellall()
                    trans_comp = 1
            else:
                highmax = last_high_low
                # print('going down, highmax - macd:',highmax - macd)
                # f.write('\ngoing down, highmax - macd: %s'% str(highmax - macd))
                if (highmax - macd > 0.1):
                    sellall()
                    trans_comp = 1
                    turn_counter = 0
    
    elif macd > macdsig and macd_last < macdsig_last:
        buyall()
        trans_comp = 1
        
    elif macd < macdsig and macd_last > macdsig_last:
        sellall()
        trans_comp = 1
        
    # print('lowmax: ', lowmax)
    # print('highmax: ', highmax)
    # print('tendi: ', tendi)
    # f.write('\nlowmax: %s'% lowmax)
    # f.write('\nhighmax: %s'% highmax)
    # f.write('\ntendi: %s'% tendi)
    # f.close()
    
#------------------------------------------------------------------------
if __name__ == "__main__":
    main()

