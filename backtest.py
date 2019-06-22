
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates, ticker
import matplotlib as mpl
from matplotlib.finance import candlestick_ohlc


usd = 10000

totalusd = [usd]
btemp = []
stemp = []
stemp2 = []

proportion = 0.5
differ = 1
bprice = 0.99
sprice = 1.01


for index, row in eth.iterrows():
    if stemp != []:
        high = row['high']
        for item in stemp:
            rate = item[0]
            amount = item[1]
            if rate <= high:
                gain = (rate * amount) * 0.9985
                usd += gain
                totalusd.append(usd)
                stemp2.append(item)
        for copy in stemp2:
            stemp.remove(copy)
        stemp2[:] = []

    
    if btemp != []:
        low = row['low']
        cost = btemp[0]
        rate = btemp[1]
        amount = btemp[2]
        if rate >= low:
            stemp.append([(rate*sprice), amount])
            usd -= cost
            totalusd.append(usd)
        btemp[:] = []

    day10 = row['10d']
    day20 = row['20d']
    if day10 <= day20:
        cost = usd * proportion
        rate = day10 * bprice
        amount = (cost / rate) * 0.9985
        btemp = [cost, rate, amount]


if __name__ == '__main__':
    mpl.style.use('default')

    url = 'https://poloniex.com/public?command=returnChartData&currencyPair=USDT_ETH&start=1503120235&end=1503206635&period=300'
    chart = pd.read_json(url)

    date = chart.index
    open = chart['open'].tolist()
    high = chart['high'].tolist()
    low = chart['low'].tolist()
    close = chart['close'].tolist()

    ohlc = list(zip(date, open, high, low, close))

    fig = plt.subplot()
    ax1 = plt.subplot()
    candlestick_ohlc(ax1, ohlc, width=0.5, colorup='g', colordown='r', alpha=0.8)

    chart["20d"] = np.round(chart["close"].rolling(window=20, center=False).mean(), 2)
    chart["50d"] = np.round(chart["close"].rolling(window=50, center=False).mean(), 2)

    plt.plot(date, chart["20d"])
    plt.plot(date, chart["50d"])

    plt.show()
