
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def pasta_al(url):

    data = urlopen(Request(url, headers={'User-Agent': 'Mozilla'})).read()
    soup = BeautifulSoup(data, 'html.parser')

    pasta = soup.code.text

    return str(pasta)