from bitfinex import KEY, SECRECT




SYMBOL = 'xrpusd'
PRIME = (SYMBOL[:3]).upper()
SECOND = (SYMBOL[3:]).upper()

LEVERAGE = 2
PERCENT = 0.2
BUYPERCENT = 0.5


def wallet(currency: str, market: str, balance: list):
    '''
    '''
    for item in balance:
        if item['currency'] == currency.lower():
            if item['type'] == market:
                return float(item['amount'])
    return 0.0


def printBalance(exPRI, marPRI, exSEC, marSEC):
    '''
    '''
    print('\n')
    print('You have: %s, %f, exchange' %(PRIME, exPRI))
    print('You have: %s, %f, margin' %(PRIME, marPRI))
    print('You have: %s, %f, exchange' %(SECOND, exSEC))
    print('You have: %s, %f, margin' %(SECOND, marSEC))


def main():
    '''
    '''
    balance = balances()

    exPRI = wallet(PRIME, 'exchange', balance)
    marPRI = wallet(PRIME, 'trading', balance)
    exSEC = wallet(SECOND, 'exchange', balance)
    marSEC = wallet(SECOND, 'trading', balance)

    printBalance(exPRI, marPRI, exSEC, marSEC)

    flag = 1
    while flag:
        answer = input('\nWould you like to proceed? (yes/no/exit)\n')
        if answer == 'yes':
            flag = 0
        if answer == 'exit':
            quit()
        if answer == 'no':
            printBalance(exPRI, marPRI, exSEC, marSEC)

    # transfer fund
    trans = str(exPRI * PERCENT)
    print('\n$ Moving: %s, %s, %d percent' %(trans, PRIME, (PERCENT * 100)))
    print(transfer(trans, PRIME, 'exchange', 'trading'))

    marPRI = wallet(PRIME, 'trading', balances())
    print('\n$ You have: %f, %s, in Margin' %(marPRI, PRIME))

    #shorting
    print('\n# Start Margin Sell')
    marginAmount = str(marPRI * LEVERAGE * 0.5)
    short = order(SYMBOL, marginAmount, '1', 'sell', 'market')
    if 'message' in short:
        print(short)
    else:
        print('OrderID: %s, Type: %s, Amount: %s, Price: %s' %(short['order_id'], short['side'], short['original_amount'], short['price']))

    currentPrice = float(ticker(SYMBOL)['last_price'])
    print('\n$ Current Price is: %f' %(currentPrice))

    #longing
    print('\n# Start Margin Buy')
    buyPrice = str(currentPrice * BUYPERCENT)
    lng = order(SYMBOL, marginAmount, buyPrice, 'buy', 'limit')
    if 'message' in lng:
        print(lng)
    else:
        print('OrderID: %s, Type: %s, Amount: %s, Price: %s' %(lng['order_id'], lng['side'], lng['original_amount'], lng['price']))


def long():
	'''
	'''
	lev = 2

	balance = balances()
    marUSD = wallet(SECOND, 'trading', balance)
    amount = str(marUSD * lev)

    lng = order(SYMBOL, amount, '1', 'buy', 'market')

    if 'message' in lng:
        print(lng)
    else:
        print('Type: %s, Amount: %s, Price: %s' %(lng['side'], lng['original_amount'], lng['price']))

    positions = positions()
    orderID = positions[0]['id']


def short():
	'''
	'''
	pass 




if __name__ == '__main__':
    
    # print(candles('15m','tBTCUSD', 'hist', '10'))

    # print(balances())

    # main()

    