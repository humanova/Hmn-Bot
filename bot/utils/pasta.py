# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def get_pasta(url):

    data = urlopen(Request(url, headers={'User-Agent': 'Mozilla'})).read()
    soup = BeautifulSoup(data, 'html.parser')

    pasta = soup.code.text

    return str(pasta)