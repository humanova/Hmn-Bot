
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

saatURL = "http://www.saatkac.com/xml_saat_kod.php?u=TR&lisans=3590dk4fd5123"

def saatParse():
    data = urlopen(Request(saatURL, headers={'User-Agent': 'Mozilla'})).read()
    parse = BeautifulSoup(data,'xml')

    tarih = parse.find_all('kombinasyon1')
    saat = parse.find_all('kombinasyon2')

    return tarih[0].get_text(),saat[0].get_text()

def saat():
    tar,sa = saatParse()
    return sa

def tarih():
    tar,sa = saatParse()
    return tar

def tamTarih():
    tar,sa = saatParse()
    return tar + " " + sa
