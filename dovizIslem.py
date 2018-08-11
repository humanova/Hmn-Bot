
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more detail

#hmnBot Doviz islemleri

#KAYNAK : www.xe.com


from bs4 import BeautifulSoup
from urllib.request import urlopen, Request



def DovizParse(kur,adet):
    kur = DovizAlgila(kur)

    if not kur == "hata" and float(adet) > 0:
        if kur.startswith("btc"):

            if kur == "btc-try":
                kurURL = 'https://www.xe.com/currencyconverter/convert/?Amount=' + str(adet) + '&From=XBT&To=TRY'

            elif kur == "btc-usd":
                kurURL = 'https://www.xe.com/currencyconverter/convert/?Amount=' + str(adet) + '&From=XBT&To=USD'

        else:
            if kur == "osu":
                kur = "usd"
                adet = 4 * adet

            kurURL = "https://www.xe.com/currencyconverter/convert/?Amount=" + str(adet) + "&From=" + kur + "&To=TRY"
        
        data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'html.parser')
            
        doviz = parse.find("span","uccResultAmount")

        kur_degeri = doviz.text

        return kur.upper(),kur_degeri
        
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

    else:
        kur = "hata"
        return kur

    
def KriptoParse(kur,don,adet):
    kur,kisa_ad,grafik_link = KriptoAlgila(kur)

    if not kur == "hata" and float(adet) > 0:

        kurURL = 'https://coinmarketcap.com/currencies/' + kur
    
        data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'html.parser')

        k_degisim =parse.find("span", "h2 text-semi-bold positive_change ")

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

    