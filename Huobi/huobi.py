import urllib.parse
import requests
import time
import hmac
import hashlib


def api_key_get(params, url):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = "https://api.huobi.pro"
    host_name = urllib.parse.urlparse(host_url).hostname.lower()
    # host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)

    # url = host_url + request_path
    # return http_get_request(url, params)
    res = requests.get(url, params = params)
    return res.json()


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature






class Huobi:

    PUBLIC = "https://api.huobi.pro/market"
    TRADING = "https://api.huobi.pro/v1"

    def __init__(self, key, secret):
        self.KEY = key
        self.SECRET = secret
        # self.nonce = int(time.time())



    @staticmethod
    def getKline(symbol, period, size=150):
        '''
        '''
        params = {'symbol': symbol, 'period': period, 'size': size}

        url = Huobi.PUBLIC + '/history/kline'
        res = requests.get(url, params = params)
        return res.json()


    @staticmethod
    def getSymbols():
        '''
        '''
        url = Huobi.TRADING + '/common/symbols'
        res = requests.get(url)
        return res.json()


    @staticmethod
    def getCurrencys():
        '''
        '''
        url = Huobi.TRADING + '/common/currencys'
        res = requests.get(url)
        return res.json()


    @staticmethod
    def getTimestamp():
        '''
        '''
        url = Huobi.TRADING + '/common/timestamp'
        res = requests.get(url)
        return res.json()


    def getAccounts():
        '''
        '''
        url = Huobi.TRADING + "/account/accounts"
        params = {}
        return api_key_get(params, url)






if __name__ == '__main__':
    huo = Huobi(1, 2)
    #print(huo.getKline('btcusdt', '30min'))

    print(huo.getTimestamp())