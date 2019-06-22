import requests
import json
import base64
import hashlib
import hmac
import time


# https://api.bitfinex.com/v1/symbols


class Bitfinex:
    API = 'https://api.bitfinex.com/v1/'


    def __init__(self, key, secret):
        self.KEY = key
        self.SECRET = secret
        self.nonce = int(time.time())

    
    def auth(self, url, payload):
        '''
        '''
        j = json.dumps(payload)
        data = base64.standard_b64encode(j.encode('utf8'))
        sign = hmac.new(self.SECRET.encode('utf8'), data, hashlib.sha384).hexdigest()
        headers = {
            'X-BFX-APIKEY': self.KEY,
            'X-BFX-SIGNATURE': sign,
            'X-BFX-PAYLOAD': data
            }
        r = requests.post(url, headers=headers, verify=True)
        return r.json()

        # if r.status_code == 200:
        #     return r.json()
        # else:
        #     print (r.status_code)
        #     return r


    #
    # PUBLIC
    #
    @staticmethod
    def ticker(symbol):
        '''
        '''
        url = f'https://api.bitfinex.com/v1/pubticker/{symbol}'
        res = requests.get(url)
        return res.json()


    @staticmethod
    def stats(symbol):
        '''
        Various statistics about the requested pair.
        '''
        url = f'https://api.bitfinex.com/v1/stats/{symbol}'
        res = requests.get(url)
        return res.json()


    @staticmethod
    def orderBook(symbol):
        '''
        Get the full order book.
        '''
        url = f'https://api.bitfinex.com/v1/book/{symbol}'
        r = requests.get(url)
        return r.json()


    @staticmethod
    def trades(symbol):
        '''
        Get a list of the most recent trades for the given symbol.
        '''
        url = f'https://api.bitfinex.com/v1/trades/{symbol}'
        r = requests.get(url)
        return r.json()


    @staticmethod
    def candles(symbol: str, timeFrame: str, section: str='hist', limit: int=None):
        '''
        symbol: v2 symbols
        timeFrame: (1m, 5m, 15m, 30m, 1h, 3h, 6h, 12h, 1D, 7D, 14D, 1M)
        section: (last, hist)
        limit: number of candles requested
        '''
        url = f'https://api.bitfinex.com/v2/candles/trade:{timeFrame}:{symbol}/{section}'
        if limit:
            option = {'limit': limit}
            r = requests.get(url, params = option)
        else:
            r = requests.get(url)
        return r.json()


    # @staticmethod
    # def lends(currency):
    #     '''
    #     '''
    #     url = 'https://api.bitfinex.com/v1/lends/%s' %(currency)
    #     r = requests.get(url)
    #     return r.json()

    # @staticmethod
    # def fundingBook(currency):
    #     '''
    #     '''
    #     url = f'https://api.bitfinex.com/v1/lendbook/{currency}'
    #     res = requests.get(url)
    #     return res.json()


    #
    # PRIVATE
    #
    def balances(self):
        '''
        See your balances.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'balances'
        payload = {
            'request': '/v1/balances',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)


    def marginInfos(self):
        '''
        See your trading wallet information for margin trading.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'margin_infos'
        payload = {
            'request': '/v1/margin_infos',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)


    def tradeHistory(self, symbol):
        '''
        View your past trades.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'mytrades'
        payload = {
            'request': '/v1/mytrades',
            'nonce': str(self.nonce),
            'symbol': symbol
            }
        return self.auth(url, payload)


    def transfer(self, amount: str, currency: str, wfrom: str, wto: str):
        '''
        Allow you to move available balances between your wallets.
        
        wallet: ('exchange', 'trading'(margin), 'deposit'(funding))
        '''
        self.nonce += 1
        url = Bitfinex.API + 'transfer'
        payload = {
            'request': '/v1/transfer',
            'nonce': str(self.nonce),
            'amount': amount,
            'currency': currency,
            'walletfrom': wfrom,
            'walletto': wto,
            }
        return self.auth(url, payload)


    # ORDERS#

    def order(self, symbol: str, amount: float, price: float, side: str, option: str):
        '''
        Submit a new Order

        price: positive, use any for 'market'
        side: ('buy', 'sell')
        option: ('market', 'limit', 'stop', 'trailing-stop', 'fill-or-kill'
                'exchange market', 'exchange limit', 'exchange trailing-stop', 'exchange fill-or-kill')
        '''
        self.nonce += 1
        url = Bitfinex.API + 'order/new'
        payload = {
            'request': '/v1/order/new',
            'nonce': str(self.nonce),
            'symbol': symbol,
            'amount': amount,
            'price': price,
            'side': side,
            'type': option,
            'exchange': 'bitfinex'
            }
        return self.auth(url, payload)


    def cancelOrder(self, orderID):
        '''
        Cancel an order.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'order/cancel'
        payload = {
            'request': '/v1/order/cancel',
            'nonce': str(self.nonce),
            'id': orderID
            }
        return self.auth(url, payload)


    def cancelAll(self):
        '''
        Cancel all active orders at once.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'order/cancel/all'
        payload = {
            'request': '/v1/order/cancel/all',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)


    def activeOrders(self):
        '''
        View your active orders.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'orders'
        payload = {
            'request': '/v1/orders',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)


    # POSITIONS #

    def positions(self):
        '''
        View your active positions.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'positions'
        payload = {
            'request': '/v1/positions',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)


    def claimPosition(self, positionID: int, amount: int):
        '''
        A position can be claimed if margin is in profit.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'position/claim'
        payload = {
            'request': '/v1/position/claim',
            'nonce': str(self.nonce),
            'position_id': positionID,
            'amount': amount
            }
        return self.auth(url, payload)


    def closePosition(self, positionID: int):
        '''Closes the selected position with a market order.
        '''
        self.nonce += 1
        url = Bitfinex.API + 'position/close'
        payload = {
            'request': '/v1/position/close',
            'nonce': str(self.nonce),
            'position_id': positionID
            }
        return self.auth(url, payload)



    # def activeOffers(self):
    #     '''
    #     '''
    #     self.nonce += 1
    #     url = Bitfinex.API + 'offers'
    #     payload = {
    #         'request': '/v1/offers',
    #         'nonce': str(self.nonce)
    #         }
    #     return self.auth(url, payload)


    # def activeCredits(self):
    #     '''
    #     '''
    #     self.nonce += 1
    #     url = Bitfinex.API + 'credits'
    #     payload = {
    #         'request': '/v1/credits',
    #         'nonce': str(self.nonce)
    #         }
    #     return self.auth(url, payload)

    def accountInfos(self):
        '''
        Return information about your account (trading fees).
        '''
        self.nonce += 1
        url = Bitfinex.API + 'account_infos'
        payload = {
            'request': '/v1/account_infos',
            'nonce': str(self.nonce)
            }
        return self.auth(url, payload)