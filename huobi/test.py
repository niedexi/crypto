from huobi import *

if __name__ == '__main__':
    # print(get_balance()['data']['list'])
    #print(get_accounts())
    # for item in get_balance()['data']['list']:
    #     if item['currency'] == 'eth':
    #         print(item)
    
    # print(getKline('btcusdt', '30min'))
    # print(getAccounts()['data'][0]['id'])

    #ID = '5916263'
    ID = '5951446'
    #orderID = '21599510973'

    # while True:
    #     print()

    # res = makeOrder(ID, 'ethusdt', '1', 'buy-market', price=None, source='api')
    

    # res = getBalance(ID)

    # res = orderInfo(orderID)

    # res = getMatchresults('ethusdt')

    #res = getAccounts()

    # res = float(getBalance(ID, 'eth'))

    res = getKline('ethusdt', '30min', 10)['data']

    print(res)