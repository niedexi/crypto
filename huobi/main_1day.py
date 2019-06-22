import pandas as pd
import threading, time, datetime
from huobi import *

def roundUp(input: str, precision: int) -> str:
    decimal = (10 ** precision)
    return str(int(float(input) * decimal) / decimal)


def record(now, detail):
    print('\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    print('Time: {}\nType: {}\nAmount: {}\nResult: {}'.format(now, detail['type'], detail['amount'], detail['field-cash-amount']))
    #print('{}, {}'.format(entry['trend'], entry['diff']))

    with open('log', 'a') as f:
        f.write('\nTime: {}\nID: {}\nType: {}\nAmount: {}\nResult: {}\n'.format(now, detail['id'], detail['type'], detail['amount'], detail['field-cash-amount']))


ID = '5916263' # account id

symbol = 'ethusdt'
period = '1day'
size = '40'

toSec = 86400

timer = getKline(symbol, period, '1')['data'][0]['id']
print('TimeStamp: {}'.format(timer))

def main():
    global timer

    threading.Timer(30, main).start()
    counter = int(time.time())

    if counter > (timer + toSec):
        #print('\nCounter: {}, Timer: {}'.format(counter, timer))
        timer += toSec
        now = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        
        data = getKline(symbol, period, size)['data'][::-1]
        chart = pd.DataFrame(data)

        # MACD
        chart['ema12'] = chart['close'].ewm(span=12,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['ema26'] = chart['close'].ewm(span=26,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['macd'] = chart['ema12'] - chart['ema26']
        chart['signal'] = chart['macd'].ewm(span=9,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['diff'] = chart['macd'] - chart['signal']
        # MA
        chart['sma30'] = chart['close'].rolling(window=30,center=False).mean()
        chart['ema20'] = chart['close'].ewm(span=20,min_periods=0,adjust=True,ignore_na=False).mean()
        chart['trend'] = chart['ema20'] - chart['sma30']
        
        entry = chart.iloc[-2]

        print('\n{}\n{}, {}'.format(now, entry['trend'], entry['diff']))

        # Bearish
        if entry['trend'] < 0:
            coinBalance = getBalance(ID, 'eth')

            if float(coinBalance) > 0.1:
                time.sleep(1)
                amount = roundUp(coinBalance, 4)
                sell = makeOrder(ID, 'ethusdt', amount, 'sell-market')
                orderID = sell['data']

                time.sleep(1)
                detail = orderInfo(orderID)['data']
                
                record(now, detail)

        # Bullish
        if entry['trend'] > 0:
            coinBalance = getBalance(ID, 'eth')
            usdtBalance = getBalance(ID, 'usdt')

            if float(usdtBalance) > 10:
                if entry['diff'] > 0:
                    time.sleep(1)
                    amount = roundUp(usdtBalance, 2)
                    buy = makeOrder(ID, 'ethusdt', amount, 'buy-market')
                    orderID = buy['data']

                    time.sleep(1)
                    detail = orderInfo(orderID)['data']

                    record(now, detail)

            if float(coinBalance) > 0.1:
                if entry['diff'] < 0:
                    time.sleep(1)
                    amount = roundUp(coinBalance, 4)
                    sell = makeOrder(ID, 'ethusdt', amount, 'sell-market')
                    orderID = sell['data']

                    time.sleep(1)
                    detail = orderInfo(orderID)['data']

                    record(now, detail)


if __name__ == "__main__":
    print('\nStarting at: {}\nRunning...'.format(datetime.datetime.now().strftime('%m-%d %H:%M')))
    main()
