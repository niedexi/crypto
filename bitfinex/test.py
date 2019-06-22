from bitfinex import Bitfinex




if __name__ == '__main__':
    bit = Bitfinex(KEY, SECRET)

    print(bit.balances())