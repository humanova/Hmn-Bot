
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot Doviz islemleri

#KAYNAK : www.xe.com

import os
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from forex_python.bitcoin import BtcConverter
import requests

api_key = os.environ['FOREX_TOKEN']
b = BtcConverter()

url_base = "https://forex.1forge.com/1.0.3/convert?"
url_api = "&api_key="

def DovizParse(kur,adet):
    kur = DovizAlgila(kur)
    
    if not kur == "hata" and float(adet) > 0:
        if kur.startswith("btc"):

            if kur == "btc-try":
                kur_degeri = b.get_latest_price('TRY')

            elif kur == "btc-usd":
                kur_degeri = b.get_latest_price('USD')
                
        elif kur == "osu":
            
            adet = float(adet) * 4.0
            kur = "AYLIK SUPPORTER"
            kur_url = url_base + "from=USD&to=TRY&quantity=" + str(adet) + url_api + api_key
            r = requests.get(kur_url, timeout=1.3)
            data = r.json()
            kur_degeri = data["value"]

        elif kur == "nitro":

            adet = float(adet) * 10.0
            kur = "AYLIK NITRO"
            kur_url = url_base + "from=USD&to=TRY&quantity=" + str(adet) + url_api + api_key
            r = requests.get(kur_url, timeout=1.3)
            data = r.json()
            kur_degeri = data["value"]

        else:
            kur_url = url_base + "from=" + kur + "&to=TRY&quantity=" + str(adet) + url_api + api_key
            r = requests.get(kur_url, timeout=1.3)
            data = r.json()
            kur_degeri = data["value"]
        

        return kur.upper(),str(kur_degeri)
        
    else:
        kur = "hata"
        kur_degeri = "hata"
        return kur,kur_degeri


def DovizAlgila(kur):

    if kur.upper() == "BTC-TRY":  
        kur = "btc-try"
        return kur
        
    elif kur.upper() == "BTC-USD":
        kur = "btc-usd"
        return kur

    elif kur.upper() == "USD" or kur.upper() == "DOLAR" or kur.upper() == "DOLLAR":
        kur = "usd"
        return kur

    elif kur.upper() == "EUR" or kur.upper() == "EURO" or kur.upper() == "AVRO":
        kur = "eur"
        return kur

    elif kur.upper() == "GBP" or kur.upper() == "POUND" or kur.upper() == "STERLIN":
        kur = "gbp"
        return kur

    elif kur.upper() == "RUB" or kur.upper() == "RUBLE" or kur.upper() == "RUS" or kur.upper() == "RUSYA":
        kur = "rub"
        return kur

    elif kur.upper() == "JPY" or kur.upper() == "JAPONYA" or kur.upper() == "YEN":
        kur = "jpy"
        return kur

    elif kur.upper() == "CAD" or kur.upper() == "KANADA": 
        kur = "cad"
        return kur

    elif kur.upper() == "AUD" or kur.upper() == "AVUSTRALYA":
        kur = "aud"
        return kur

    elif kur.upper() == "CNY" or kur.upper() == "ÇIN" or kur.upper() == "RENMINBI":
        kur = "cny"
        return kur

    elif kur.upper() == "SEK" or kur.upper() == "SWE" or kur.upper() == "ISVEÇ":
        kur = "sek"
        return kur

    elif kur.upper() == "CHF" or kur.upper() == "SWI" or kur.upper() == "ISVIÇRE":
        kur = "sek"
        return kur

    elif kur.upper() == "DKK" or kur.upper() == "DANIMARKA" or kur.upper() == "DAN":
        kur = "dkk"
        return kur

    elif kur.upper() == "SAR" or kur.upper() == "SAUDI" or kur.upper() == "ARABISTAN":
        kur = "sar"
        return kur

    elif kur.upper() == "RON" or kur.upper() == "ROMANYA" or kur.upper() == "RUMEN":
        kur = "ron"
        return kur

    elif kur.upper() == "NOK" or kur.upper() == "NORVEÇ":
        kur = "nok"
        return kur

    elif kur.upper() == "BGN" or kur.upper() == "BULGARISTAN":
        kur = "bgn"
        return kur

    elif kur.upper() == "IRR" or kur.upper() == "IRAN":
        kur = "irr"
        return kur

    elif kur.upper() == "PKR" or kur.upper() == "PAKISTAN":
        kur = "pkr"
        return kur
    
    elif kur.upper() == "KWD" or kur.upper() == "KUVEYT":
        kur = "kwd"
        return kur

    elif kur.upper() == "SUPPORTER" or kur.upper() == "SUP":
        kur = "osu"
        return kur

    elif kur.upper() == "NITRO":
        kur = "nitro"
        return kur

    else:
        kur = "hata"
        return kur
    

def supporterDiscount(ay,ucret):
    ay = float(ay)
    ucret = float(ucret)

    if ay < 4.0:
        indirimli = ucret

    elif ay >= 4.0 and ay < 6:
        indirimli = ucret - (ucret * 0.25)

    elif ay >= 6 and ay < 8:
        indirimli = ucret - (ucret * 0.33)
    
    elif ay >= 8 and ay < 9:
        indirimli = ucret - (ucret * 0.38)
    
    elif ay >= 9 and ay < 10:
        indirimli = ucret - (ucret * 0.39)
    
    elif ay >= 10 and ay < 12:
        indirimli = ucret - (ucret * 0.40)
    
    elif ay >= 12:
        indirimli = ucret - (ucret * 0.46)

    indirimli = round(float(indirimli),3)
    return str(indirimli)


def KriptoParse(kur,don,adet):
    kur,kisa_ad,grafik_link = KriptoAlgila(kur)

    if not kur == "hata" and float(adet) > 0:

        kurURL = 'https://coinmarketcap.com/currencies/' + kur
    
        data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'html.parser')

        k_degisim = parse.find("span", "h2 text-semi-bold positive_change ")

        if k_degisim == None:
            k_degisim = parse.find("span", "h2 text-semi-bold negative_change")
        
        kripto_degisim = k_degisim
        kripto_deger = parse.find("span","h2 text-semi-bold details-panel-item--price__value")

        kur_degeri = kripto_deger.text
        kur_degisim = kripto_degisim.text

        return kur.upper(),kur_degeri,kur_degisim[2:-3],grafik_link

    else :
        kur = "hata"
        kisa_ad = "hata"
        kur_degisim = "hata"
        grafik_link = "hata"
        return kur,kisa_ad,kur_degisim,grafik_link


def KriptoAlgila(kur):

    if kur.upper() == "BTC" or kur.upper() == "BITCOIN":
        kur = "bitcoin"
        kisa_ad = "xbt"
        grafik_link = 'https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1.png'
        return kur,kisa_ad,grafik_link
    
    elif kur.upper() == "BTCCASH" or kur.upper() == "BITCOINCASH" or kur.upper() == "BCH":
        kur = "bitcoin-cash"
        kisa_ad = "bch"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1831.png"
        return kur,kisa_ad,grafik_link
            
    elif kur.upper() == "ETH" or kur.upper() == "ETHEREUM":

        kur = "ethereum"
        kisa_ad = "eth"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1027.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "XRP" or kur.upper() == "RIPPLE":
        kur = "ripple"
        kisa_ad = "xrp"
        grafik_link = 'https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/52.png'
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "EOS":
        kur = "eos"
        kisa_ad = "eos"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1765.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "XMR" or kur.upper() == "MONERO":
        kur = "monero"
        kisa_ad = "xmr"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/328.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "LITE" or kur.upper() == "LTC" or kur.upper() == "LITECOIN":
        kur = "litecoin"
        kisa_ad = "ltc"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/2.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "ETC" or kur.upper() == "ETHEREUM CLASSIC":
        kur = "ethereum-classic"
        kisa_ad = "etc"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1321.png"
        return kur,kisa_ad,grafik_link
    
    elif kur.upper() == "ZEC" or kur.upper() == "ZCASH":
        kur = "zcash"
        kisa_ad = "zec"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1437.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "BCN" or kur.upper() == "BYTECOIN":
        kur = "bytecoin-bcn"
        kisa_ad = "bcn"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/372.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "XLM" or kur.upper() == "STELLAR":
        kur = "stellar"
        kisa_ad = "xlm"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/512.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "ADA" or kur.upper() == "CARDANO":
        kur = "cardano"
        kisa_ad = "ada"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/2010.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "MIOTA" or kur.upper() == "IOTA":
        kur = "iota"
        kisa_ad = "miota"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1720.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "TRX" or kur.upper() == "TRON":
        kur = "tron"
        kisa_ad = "trx"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1958.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "NEO":
        kur = "neo"
        kisa_ad = "neo"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/1376.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "NTY" or kur.upper() == "NEXTY":
        kur = "nexty"
        kisa_ad = "nty"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/2714.png"
        return kur,kisa_ad,grafik_link

    elif kur.upper() == "PPC" or kur.upper() == "PEERCOIN":
        kur = "peercoin"
        kisa_ad = "ppc"
        grafik_link = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/5.png"
        return kur,kisa_ad,grafik_link

    else:
        kur = "hata"
        kisa_ad = "hata"
        grafik_link = "hata"
        return kur,kisa_ad,grafik_link

    