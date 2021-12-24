import urllib.request

import requests
import time
import json

import urllib3.request
from bs4 import BeautifulSoup
from lxml import etree


def main():
    endpoint = 'https://www.okex.com/priapi/v5/market//mult-tickers?t=1640085973124&instIds=ETH-USDT'
    # endpoint = 'http://www.neeq.com.cn/disclosure/supervise.html'

    while True:
        session = requests.session()
        response = session.get(endpoint, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'})

        data = json.loads(response.text)
        price= data['data'][0]['last']

        # soup = BeautifulSoup(response.text, 'html.parser')
        # div = soup.find('div', attrs={'class': 'style__CurrencyMetadata-sc-4nm300-9 fRDtTn'})
        # print(div)
        time.sleep(2)

    # heads = {
    #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    # request = urllib.request.Request(endpoint, headers=heads)
    # response= urllib.request.urlopen(request)
    # html=response.read().decode('utf-8')
    # print(html)


if __name__ == '__main__':
    main()
