
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

b = BtcConverter()

doviz_api_url = "https://api.canlidoviz.com/web/items?marketId=1&type=0"
altin_api_url = "https://api.canlidoviz.com/web/items?marketId=1&type=1"

def DovizParse(kur, adet = 1, is_detailed = False):
    kur = DovizAlgila(kur)
    if not kur == None and float(adet) > 0:

        if kur == "BTC":
            kur_sonuc = {"kur_adi" : "BTC",
                        "kur_buy_tl" : b.get_latest_price('TRY'),
                        "kur_buy_usd" : b.get_latest_price('USD')}

        elif kur == "ALTIN":
            kur_sonuc = GetAltin()

        elif kur == "osu":
            ay = adet
            adet = float(adet) * 4.0
            kur_adi = "AYLIK SUPPORTER"
            res = GetKur("USD", adet)
            kur_sonuc = {"kur_adi" : kur_adi,
                        "kur_buy" : res['kur_buy'],
                        "discount" : supporterDiscount(ay, res['kur_buy'])}  

        elif kur == "nitro":
            adet = float(adet) * 10.0
            kur_adi = "AYLIK NITRO"
            res = GetKur("USD", adet)
            kur_sonuc = {"kur_adi" : kur_adi,
                        "kur_buy" : res['kur_buy']}  
            
        else:
            kur_adi = kur
            if(is_detailed):
                kur_sonuc = GetKurX(kur)
            else:
                kur_sonuc = GetKur(kur, adet)

        return kur_sonuc
        
    else:
        return None

def GetKurX(kur):
    r = requests.get(doviz_api_url, timeout=2)
    if r.status_code == 200:
        data = r.json()
        for i in data:
            if i['code'] == kur:
                kur_min = float(i['todayLowestBuyPrice'])
                kur_max = float(i['todayHighestBuyPrice'])
                kur_buy = float(i['buyPrice'])
                kur_sell = float(i['sellPrice'])
                kur_change = float(i['dailyChange'])
                kur_change_percentage = float(i['dailyChangePercentage'])
                kur_time = i['lastUpdateDate']

                return {"kur_adi" : kur,
                        "kur_min" : kur_min, "kur_max" : kur_max, 
                        "kur_buy" : kur_buy, "kur_sell" : kur_sell, 
                        "kur_change" : kur_change, "kur_change_percentage" : kur_change_percentage,
                        "kur_time" : kur_time}

            else:
                continue
    return None
    

def GetKur(kur, adet):
    r = requests.get(doviz_api_url, timeout=2)
    if r.status_code == 200:
        data = r.json()
        for i in data:
            if i['code'] == kur:
                kur_buy = float(round(i['buyPrice'],5))
                kur_change = float(round(i['dailyChange'], 5))
                kur_change_percentage = float(round(i['dailyChangePercentage'],5))
                kur_time = i['lastUpdateDate']
                return {"kur_adi" : kur,
                        "kur_buy" : kur_buy * adet, 
                        "kur_change" : kur_change, "kur_change_percentage" : kur_change_percentage, 
                        "kur_time" : kur_time}
            else:
                continue
    return None    

def GetAltin():
    altin = {}
    altin['kur_adi'] = "ALTIN"
    r = requests.get(altin_api_url, timeout=2, headers={"User-Agent": "curl/7.61.0"})
    
    if r.status_code == 200:
        data = r.json()
        altin['kur_time'] = data[0]['lastUpdateDate']
        for i in range(len(data)):
            if i < 5 or (i > 10 and i < 13):
                altin[data[i]['name']] = float(round(data[i]['buyPrice'], 5))
        if not len(altin) == 0:
            return altin
        else:
            return None

    return None

def DovizAlgila(kur):

    if kur.upper() == "BTC":  
        return "BTC"

    elif kur.upper() == "ALTIN" or kur.upper() == "GOLD":
        return "ALTIN"

    elif kur.upper() == "USD" or kur.upper() == "DOLAR" or kur.upper() == "DOLLAR": 
        return "USD"

    elif kur.upper() == "EUR" or kur.upper() == "EURO" or kur.upper() == "AVRO":
        return "EUR"

    elif kur.upper() == "GBP" or kur.upper() == "POUND" or kur.upper() == "STERLIN":
        return "GBP"

    elif kur.upper() == "RUB" or kur.upper() == "RUBLE" or kur.upper() == "RUS" or kur.upper() == "RUSYA":
        return "RUB"

    elif kur.upper() == "JPY" or kur.upper() == "JAPONYA" or kur.upper() == "YEN":
        return "JPY"

    elif kur.upper() == "CAD" or kur.upper() == "KANADA": 
        return "CAD"

    elif kur.upper() == "AUD" or kur.upper() == "AVUSTRALYA":
        return "AUD"

    elif kur.upper() == "CNY" or kur.upper() == "ÇIN" or kur.upper() == "RENMINBI":
        return "CNY"

    elif kur.upper() == "SEK" or kur.upper() == "SWE" or kur.upper() == "ISVEÇ":
        return "SEK"

    elif kur.upper() == "CHF" or kur.upper() == "SWI" or kur.upper() == "ISVIÇRE":
        return "CHF"

    elif kur.upper() == "DKK" or kur.upper() == "DANIMARKA" or kur.upper() == "DAN":
        return "DKK"

    elif kur.upper() == "SAR" or kur.upper() == "SAUDI" or kur.upper() == "ARABISTAN":
        return "SAR"

    elif kur.upper() == "RON" or kur.upper() == "ROMANYA" or kur.upper() == "RUMEN":
        return "RON"

    elif kur.upper() == "NOK" or kur.upper() == "NORVEÇ":
        return "NOK"

    elif kur.upper() == "BGN" or kur.upper() == "BULGARISTAN":
        return "BGN"

    elif kur.upper() == "IRR" or kur.upper() == "IRAN":
        return "IRR"

    elif kur.upper() == "PKR" or kur.upper() == "PAKISTAN":
        return "PKR"
    
    elif kur.upper() == "KWD" or kur.upper() == "KUVEYT":
        return "KWD"

    elif kur.upper() == "SUPPORTER" or kur.upper() == "SUP":
        return "osu"

    elif kur.upper() == "NITRO":
        return "nitro"

    else:
        return None
    

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

    