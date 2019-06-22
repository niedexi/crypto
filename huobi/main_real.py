import pandas as pd
import threading, time, datetime

from huobi import *

def roundUp(input: str, precision: int) -> str:
    decimal = (10 ** precision)
    return str(int(float(input) * decimal) / decimal)


# 5min: 300, 15min: 900, 30min: 1800, 60min: 3600
ID = '5916263' # account id
inSec = 1800

symbol = 'ethusdt'
period = '30min'
size = '35'

flag = 0
timeStamp = 0

def main():
    global flag
    global timeStamp

    threading.Timer(60, main).start()

    if flag:
        if int(time.time()) > (timeStamp + inSec):
            flag = 0

    else:
        data = getKline(symbol, period, size)['data'][::-1]
        timeStamp = data[-1]['id']
        
        chart = pd.DataFrame(data)
        chart['ema12'] = chart['close'].ewm(span=12,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['ema26'] = chart['close'].ewm(span=26,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['macd'] = chart['ema12'] - chart['ema26']
        chart['signal'] = chart['macd'].ewm(span=9,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['diff'] = chart['macd'] - chart['signal']
        chart['ema20'] = chart['close'].ewm(span=20,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['sma30'] = chart['close'].rolling(window=30,center=False).mean()
        chart['trend'] = chart['ema20'] - chart['sma30']
        
        entry = chart.iloc[-1]

        now = datetime.datetime.now().strftime('%m-%d %H:%M') #%Y-%m-%d %H:%M

        # print('{}, {}, {}, {}'.format(now, timeStamp, entry['trend'], entry['diff']))

        # Bearish
        if entry['trend'] < 0:
            time.sleep(1)
            coinBalance = getBalance(ID, 'eth')

            if float(coinBalance) > 0.1:
                time.sleep(1)
                amount = roundUp(coinBalance, 4)
                sell = makeOrder(ID, 'ethusdt', amount, 'sell-market')
                orderID = sell['data']
                flag = 1

                time.sleep(1)
                detail = orderInfo(orderID)['data']
                
                print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                print('Time: {}\nType: {}\nAmount: {}\nResult: {}'.format(now, detail['type'], detail['amount'], detail['field-cash-amount']))
                print('{}, {}'.format(entry['trend'], entry['diff']))

                with open('log', 'a') as f:
                    f.write('\nTime: {}\nID: {}\nType: {}\nAmount: {}\nResult: {}\n'.format(now, detail['id'], detail['type'], detail['amount'], detail['field-cash-amount']))

        # Bullish
        if entry['trend'] > 0:
            time.sleep(1)
            coinBalance = getBalance(ID, 'eth')
            usdtBalance = getBalance(ID, 'usdt')

            if float(usdtBalance) > 10:
                if entry['diff'] > 0:
                    time.sleep(1)
                    amount = roundUp(usdtBalance, 2)
                    buy = makeOrder(ID, 'ethusdt', amount, 'buy-market')
                    orderID = buy['data']
                    flag = 1

                    time.sleep(1)
                    detail = orderInfo(orderID)['data']

                    print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    print('Time: {}\nType: {}\nAmount: {}\nResult: {}'.format(now, detail['type'], detail['amount'], detail['field-amount']))
                    print('{}, {}'.format(entry['trend'], entry['diff']))

                    with open('log', 'a') as f:
                        f.write('\nTime: {}\nID: {}\nType: {}\nAmount: {}\nResult: {}\n'.format(now, detail['id'], detail['type'], detail['amount'], detail['field-amount']))
                    
            if float(coinBalance) > 0.1:
                if entry['diff'] < 0:
                    time.sleep(1)
                    amount = roundUp(coinBalance, 4)
                    sell = makeOrder(ID, 'ethusdt', amount, 'sell-market')
                    orderID = sell['data']
                    flag = 1

                    time.sleep(1)
                    detail = orderInfo(orderID)['data']

                    print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    print('Time: {}\nType: {}\nAmount: {}\nResult: {}'.format(now, detail['type'], detail['amount'], detail['field-cash-amount']))
                    print('{}, {}'.format(entry['trend'], entry['diff']))
                    
                    with open('log', 'a') as f:
                        f.write('\nTime: {}\nID: {}\nType: {}\nAmount: {}\nResult: {}\n'.format(now, detail['id'], detail['type'], detail['amount'], detail['field-cash-amount']))


if __name__ == "__main__":
    print('\nStarting at: {}\nRunning...\n'.format(datetime.datetime.now().strftime('%m-%d %H:%M')))
    main()
