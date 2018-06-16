
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot Doviz islemleri

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def DovizParse(kur):
    kur = DovizAlgila(kur)

    if not kur == "hata":
        if kur.startswith("btc"):

            if kur == "btc-try":
                kurURL = 'https://tr.investing.com/crypto/bitcoin/btc-try'

            elif kur == "btc-usd":
                kurURL = 'https://tr.investing.com/crypto/bitcoin/btc-usd'

        else:
            kurURL = "http://tr.investing.com/currencies/" + kur + "-try"
        
        data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'html.parser')

        for doviz in parse.find_all('span', id="last_last"):
            liste = list(doviz)
        
        liste = str(liste)
        for char in "[']":
            liste = liste.replace(char,'')

        kur_degeri = liste

        return kur.upper(),kur_degeri
        
    else:
        kur_degeri = "hata"
        return kur,kur_degeri

def DovizAlgila(kur):

    if kur.upper() == "BTC-TRY":  
        kur = "btc-try"
        
    elif kur.upper() == "BTC-USD":
        kur = "btc-usd"

    elif kur.upper() == "USD" or kur.upper() == "DOLAR" or kur.upper() == "DOLLAR":
        kur = "usd"

    elif kur.upper() == "EUR" or kur.upper() == "EURO" or kur.upper() == "AVRO":
        kur = "eur"

    elif kur.upper() == "GBP" or kur.upper() == "POUND" or kur.upper() == "STERLIN":
        kur = "gbp"

    elif kur.upper() == "RUB" or kur.upper() == "RUBLE" or kur.upper() == "RUS" or kur.upper() == "RUSYA":
        kur = "rub"

    elif kur.upper() == "JPY" or kur.upper() == "JAPON" or kur.upper() == "YEN":
        kur = "jpy"

    elif kur.upper() == "CAD" or kur.upper() == "KANADA": 
        kur = "cad"

    elif kur.upper() == "AUD" or kur.upper() == "AVUSTRALYA":
        kur = "aud"

    elif kur.upper() == "CNY" or kur.upper() == "ÇIN" or kur.upper() == "RENMINBI":
        kur = "cny"

    elif kur.upper() == "SEK" or kur.upper() == "SWE" or kur.upper() == "ISVEÇ":
        kur = "sek"

    elif kur.upper() == "CHF" or kur.upper() == "SWI" or kur.upper() == "ISVIÇRE":
        kur = "sek"

    elif kur.upper() == "DKK" or kur.upper() == "DANIMARKA" or kur.upper() == "DAN":
        kur = "dkk"

    elif kur.upper() == "SAR" or kur.upper() == "SAUDI" or kur.upper() == "ARABISTAN":
        kur = "sar"

    elif kur.upper() == "RON" or kur.upper() == "ROMANYA" or kur.upper() == "RUMEN":
        kur = "ron"

    elif kur.upper() == "NOK" or kur.upper() == "NORVEÇ":
        kur = "nok"

    elif kur.upper() == "BGN" or kur.upper() == "BULGARISTAN":
        kur = "bgn"

    elif kur.upper() == "IRR" or kur.upper() == "IRAN":
        kur = "irr"

    elif kur.upper() == "PKR" or kur.upper() == "PAKISTAN":
        kur = "pkr"
    
    elif kur.upper() == "KWD" or kur.upper() == "KUVEYT":
        kur = "kwd"

    else:
        kur = "hata"

    return kur

def KriptoParse(kur,don):
    kur,kisa_ad = KriptoAlgila(kur)

    if not kur == "hata":

        kurURL = "https://tr.investing.com/crypto/" + kur + "/" + kisa_ad + "-" + don
    
        data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'html.parser')

        for doviz in parse.find_all('span', id="last_last"):
            liste = list(doviz)
        
        liste = str(liste)
        for char in "[']":
            liste = liste.replace(char,'')

        kur_degeri = liste

        return kur.upper(),kur_degeri

    else :
        return kur,kisa_ad


def KriptoAlgila(kur):

    if kur.upper() == "BTC" or kur.upper() == "BITCOIN":
        kur = "bitcoin"
        kisa_ad = "btc"
    
    elif kur.upper() == "BTCCASH" or kur.upper() == "BITCOINCASH" or kur.upper() == "BCH":
        kur = "bitcoin-cash"
        kisa_ad = "bch"
    elif kur.upper() == "ETH" or kur.upper() == "ETHEREUM":

        kur = "ethereum"
        kisa_ad = "eth"

    elif kur.upper() == "XRP" or kur.upper() == "RIPPLE":
        kur = "ripple"
        kisa_ad = "xrp"

    elif kur.upper() == "EOS":
        kur = "eos"
        kisa_ad = "eos"

    elif kur.upper() == "XMR" or kur.upper() == "MONERO":
        kur = "monero"
        kisa_ad = "xmr"

    elif kur.upper() == "LITE" or kur.upper() == "LTC" or kur.upper() == "LITECOIN":
        kur = "litecoin"
        kisa_ad = "ltc"

    elif kur.upper() == "XLM" or kur.upper() == "STELLAR":
        kur = "stellar"
        kisa_ad = "xlm"

    else:
        kur = "hata"
        kisa_ad = "hata"

    return kur,kisa_ad