import requests
import time
import json


def obtain_price(names):
    """
    :param names: url list
    """
    while True:
        session = requests.session()
        for name in names:
            response = session.get(name, headers={
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})
            price = json.loads(response.text)['data'][0]['last']
            print('current price:' + price)
            time.sleep(10)


def main():
    stock_names = ['ETH-USDT', 'AVAX-USDT']
    stock_number = {'ETH-USDT': '1640089666667', 'AVAX-USDT': '1640089080391'}
    url_names = []
    for stock_name in stock_names:
        url_names.append('https://www.okex.com/priapi/v5/market//mult-tickers?t=' + stock_number[
            stock_name] + '&instIds=' + stock_name)
    obtain_price(url_names)


if __name__ == '__main__':
    main()
