import requests
import json
import base64
import hashlib
import hmac
import time
import urllib.parse
# from websocket import create_connection

from key import *




key = SECRET.encode('utf8')
nonce = int(time.time())

API = 'https://api.bitfinex.com/v2/'


##### PUBLIC #####

def tickers(symbols):
    '''
    symbols: 'tBTCUSD,tLTCUSD,fUSD'
    trading: [SYMBOL, BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
    funding: [SYMBOL, FRR, BID, BID_SIZE, BID_PERIOD,ASK, ASK_SIZE,ASK_PERIOD,DAILY_CHANGE,DAILY_CHANGE_PERC, LAST_PRICE,VOLUME,HIGH, LOW]
    '''
    url = API + 'tickers'
    cmd = {'symbols': symbols}
    r = requests.get(url, params = cmd)
    return r.json()


def ticker(symbol):
    '''
    symbol: 'tBTCUSD'
    trading: [BID, BID_SIZE, ASK, ASK_SIZE, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW ]
    funding: [FRR, BID, BID_SIZE, BID_PERIOD, ASK, ASK_SIZE, ASK_PERIOD, DAILY_CHANGE, DAILY_CHANGE_PERC, LAST_PRICE, VOLUME, HIGH, LOW]
    '''
    url = API + ('ticker/%s' %(symbol))
    r = requests.get(url)
    return r.json()


#!!!
def trades(symbol):
    '''
    trading: [ID, MTS, AMOUNT, PRICE]
    funding: [ID, MTS, AMOUNT, RATE, PERIOD]
    '''
    url = API + ('trades/%s/hist' %(symbol))
    r = requests.get(url)
    return r.json()


def books(symbol, precision):
    '''
    precision: (P0, P1, P2, P3, R0)
    trading: [PRICE, COUNT, AMOUNT]
    funding: [RATE, PERIOD, COUNT, AMOUNT]

    Trading: if AMOUNT > 0 then bid, else ask.
    Funding: if AMOUNT > 0 then ask, else bid.
    '''
    url = API + ('book/%s/%s' %(symbol, precision))
    r = requests.get(url)
    return r.json()


def stats():
    '''
    '''
    pass


#!!!
def candles(timeFrame, symbol, section):
    '''
    timeFrame: (1m, 5m, 15m, 30m, 1h, 3h, 6h, 12h, 1D, 7D, 14D, 1M)
    section: (last, hist)
    '''
    pass


def marketAveragePrice():
    '''
    '''
    url = API + 'calc/trade/avg'
    # params = {'symbol': symbol}
    r = requests.request("POST", url)
    return r.text




##### TRADING #####

def main(path, nonce: str, body):
    '''
    '''
    signature = ('/api/v2/' + path + nonce + body).encode('utf8')
    sign = hmac.new(key, signature, hashlib.sha384).hexdigest()
    header = {'bfx-nonce': nonce, 'bfx-apikey': KEY, 'bfx-signature': sign, 'content-type': 'application/json'}
    url = (API + path)
    r = requests.post(url, headers=header, data=body, verify=True)

    if r.status_code == 200:
        return r.json()
    else:
        print (r.status_code)
        return r


def orders():
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/orders'
    body = json.dumps({})
    return main(path, str(nonce), body)


def wallets():
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/wallets'
    body = json.dumps({})
    return main(path, str(nonce), body)


def ordersHistory(symbol=None):
    '''
    '''
    global nonce
    nonce += 1
    if symbol:
        path = 'auth/r/orders/%s/hist' %(symbol)
    else:
        path = 'auth/r/orders/hist'
    body = json.dumps({})
    return main(path, str(nonce), body)


def orderTrades(orderID):
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/order/%s/trades' %(orderID)
    body = json.dumps({})
    return main(path, str(nonce), body)


def trades(symbol):
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/trades/%s/hist' %(symbol)
    body = json.dumps({})
    return main(path, str(nonce), body)


def positions():
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/positions'
    body = json.dumps({})
    return main(path, str(nonce), body)


def fundingOffers(symbol):
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/funding/offers/%s' %(symbol)
    body = json.dumps({})
    return main(path, str(nonce), body)


def fundingOffersHistory(symbol):
    '''
    '''
    global nonce
    nonce += 1
    path = 'auth/r/funding/offers/%s/hist' %(symbol)
    body = json.dumps({})
    return main(path, str(nonce), body)





##### WEBSOCKET #####

# def testsocket():
#     '''
#     '''
#     ws = create_connection('wss://api.bitfinex.com/ws/2')
 
#     #data = {'event': "subscribe", 'channel': "ticker", 'symbol': 'tBTCUSD'}


#     ws.send(json.dumps(testauth()))
#     info = json.loads(ws.recv())
#     print('Received: %s' %(info))

#     ws.send(json.dumps(testauth()))
#     info = json.loads(ws.recv())
#     print('Received: %s' %(info))


#     ws.close()


# def testauth():
#     '''
#     '''
#     ws = create_connection('wss://api.bitfinex.com/ws/2')

#     nonce = int(time.time() * 10000000)
#     authPayload = 'AUTH{}'.format(nonce)
#     sig = hmac.new(key, authPayload.encode('utf8'), hashlib.sha384).hexdigest()
#     payload = {
#         'event': 'auth',
#         'apiKey': KEY,
#         'authPayload': authPayload,
#         'authSig': sig,
#         'authNonce': str(nonce),
#         'filter': ['wallet']
#         }

#     while True:
#         ws.send(json.dumps(payload))
#         msg = json.loads(ws.recv())
#         print('Received: %s' %(msg))

    # ws.send(json.dumps(payload))
    # msg = json.loads(ws.recv())
    # print('Received: %s' %(msg))

    # ws.send(json.dumps(payload))
    # msg = json.loads(ws.recv())
    # print('Received: %s' %(msg))



    



if __name__ == '__main__':
    # print (books('tETHUSD', 'P0'))

    print(testauth())