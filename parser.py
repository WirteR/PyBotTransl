from lxml.cssselect import CSSSelector

from urllib.request import urlopen
import urllib.request

from lxml.html import fromstring
from bs4 import BeautifulSoup
import requests
'''
url = 'https://myfin.by/crypto-rates/bitcoin'

def get_html(site):
    r = requests.get(site)
    return r.text

def parse(html):
    soup = BeautifulSoup(html, 'lxml')

    line = soup.find('div', id="crypto_exchange").find('table', class_='items').find('tbody').find_all('tr')

    markets = []

    for tr in line:
        td = tr.find_all('td')
        markets.append(td[0].text[:-16])

    return markets
def main():
    markets = parse(get_html(url))
    for i in markets:
        print(i)

if __name__ == "__main__":
    main()
'''



def get_html(site):
    r = requests.get(site)
    return r.text

def parse(html):
    soup = BeautifulSoup(html, 'lxml')

    line = soup.find('div', id="crypto_exchange").find('table', class_='items').find('tbody').find_all('tr')

    markets = []

    for tr in line:
        td = tr.find_all('td')
        markets.append(td[0].text[:-16])

    return markets




var = 'monero'
site = 'https://myfin.by/crypto-rates/'
if str(var) == 'XRP':
    site = 'https://myfin.by/crypto-rates/ripple'
else:
    site += str(var).lower()

markets = parse(get_html(site))
result_markets = '\n'.join(markets)
print(result_markets)
