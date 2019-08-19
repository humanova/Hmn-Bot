
# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot hava
# KAYNAK :
#           openweathermap.com
#           mgm.gov.tr

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pyowm
from datetime import datetime
from dateutil import tz

token = os.environ['OWM_TOKEN']
owm = pyowm.OWM(token)
iconURL = "http://openweathermap.org/img/w/"
havaURL = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

zaman_kusagi = 3  #utc + 3


def havaParseOWM(sehir):
    yer = sehir

    try:
        raw_hava = owm.weather_at_place(yer)
    except:
        yer = None
        sicaklik = None
        nem_orani = None
        ruzgar_hizi = None
        gun_dogumu = None
        gun_batimi = None
        durum_ikon_url = None


    if not yer == None:

        hava = raw_hava.get_weather()
        #kisa_durum = hava.get_status()
        ruzgar_hizi = hava.get_wind()['speed']
        nem_orani = hava.get_humidity()
        sicaklik = hava.get_temperature('celsius')['temp']
        #sicaklik_max = hava.get_temperature('celsius').temp_max
        #sicaklik_min = hava.get_temperature('celsius').temp_min
        
        gun_dogumu_saat = hava.get_sunrise_time('iso')[11:13]
        gun_dogumu_dak = hava.get_sunrise_time('iso')[14:16]
        gun_batimi_saat = hava.get_sunset_time('iso')[11:13]
        gun_batimi_dak = hava.get_sunset_time('iso')[14:16]

        gun_dogumu = str(((int(gun_dogumu_saat) + zaman_kusagi) % 24)) + ":" + str(gun_dogumu_dak)
        gun_batimi = str(((int(gun_batimi_saat) + zaman_kusagi) % 24)) + ":" + str(gun_batimi_dak)
        #zaman = hava.get_reception_time(timeformat='iso')   
        ikon = hava.get_weather_icon_name()
        #print("asad")
        #print(gun_batimi)
        
        durum_ikon_url = iconURL + ikon + ".png"

    return yer,sicaklik,nem_orani,ruzgar_hizi,gun_dogumu,gun_batimi,durum_ikon_url




def havaParse(sehir):
    sehir,num = sehirAlgila(sehir)
    if not sehir == None:
        data = urlopen(Request(havaURL, headers={'User-Agent': 'Mozilla'})).read()
        parse = BeautifulSoup(data,'xml')

        #tarih = parse.find_all('PeryotBaslama')[0]
        havadurumu = parse.find_all('Durum')[num]
        #maks = parse.find_all('Mak')[num]
        #minn = parse.find_all('Min')[num]
        #peryot = parse.find_all('Peryot')[num]

        
        return sehir,havadurumu.get_text()

    else:
        return None, None

def sehirAlgila(sehir):
    if sehir.upper() == "ISTANBUL":  
        sehir = "ISTANBUL"
        sehir_num = 0

    elif sehir.upper() == "EDIRNE":
        sehir = "EDIRNE"
        sehir_num = 1
        
    elif sehir.upper() == "KOCAELI":
        sehir = "KOCAELI"
        sehir_num = 2
        
    elif sehir.upper() == "IZMIR":
        sehir = "IZMIR"
        sehir_num = 3
        
    elif sehir.upper() == "AFYON" or sehir.upper() == "AFYONKARAHISAR":
        sehir = "A.KARAHISAR"
        sehir_num = 4
        
    elif sehir.upper() == "DENIZLI":
        sehir = "DENIZLI"
        sehir_num = 5
        
    elif sehir.upper() == "ADANA":
        sehir = "ADANA"
        sehir_num = 6
        
    elif sehir.upper() == "ANTALYA":
        sehir = "ANTALYA"
        sehir_num = 7
        
    elif sehir.upper() == "ISPARTA" or sehir == "ısparta":
        sehir = "ISPARTA"
        sehir_num = 8
        
    elif sehir.upper() == "ANKARA":
        sehir = "ANKARA"
        sehir_num = 9
        
    elif sehir.upper() == "ESKISEHIR" or sehir.upper() == "ESKIŞEHIR":
        sehir = "ESKISEHIR"
        sehir_num = 10
        
    elif sehir.upper() == "KONYA":
        sehir = "KONYA"
        sehir_num = 11
        
    elif sehir.upper() == "BOLU":
        sehir = "BOLU"
        sehir_num = 12
        
    elif sehir.upper() == "ZONGULDAK":
        sehir = "ZONGULDAK"
        sehir_num = 13
        
    elif sehir.upper() == "KASTAMONU":
        sehir = "KASTAMONU"
        sehir_num = 14
        
    elif sehir.upper() == "SAMSUN":
        sehir = "SAMSUN"
        sehir_num = 15
        
    elif sehir.upper() == "TOKAT":
        sehir = "TOKAT"
        sehir_num = 16
        
    elif sehir.upper() == "TRABZON":
        sehir = "TRABZON"
        sehir_num = 17
        
    elif sehir.upper() == "ERZURUM":
        sehir = "ERZURUM"   
        sehir_num = 18
        
    elif sehir.upper() == "MALATYA":
        sehir = "MALATYA"
        sehir_num = 19
        
    elif sehir.upper() == "VAN":
        sehir = "VAN"
        sehir_num = 20
        
    elif sehir.upper() == "DIYARBAKIR":
        sehir = "DIYARBAKIR"
        sehir_num = 21
        
    elif sehir.upper() == "GAZIANTEP":
        sehir = "GAZIANTEP"
        sehir_num = 22
         
    elif sehir.upper() == "SANLIURFA":
        sehir = "SANLIURFA"
        sehir_num = 23
        
    elif sehir.upper() == "BURSA":
        sehir = "BURSA"
        sehir_num = 24
        
    elif sehir.upper() == "KUTAHYA":
        sehir = "KUTAHYA"
        sehir_num = 25
        
    elif sehir.upper() == "NIGDE":
        sehir = "NIGDE"
        sehir_num = 26
        
    elif sehir.upper() == "KARABUK":
        sehir = "KARABUK"
        sehir_num = 27
        
    elif sehir.upper() == "ARTVIN":
        sehir = "ARTVIN"
        sehir_num = 28
        
    elif sehir.upper() == "ARDAHAN":
        sehir = "ARDAHAN"
        sehir_num = 29
        
    elif sehir.upper() == "KILIS":
        sehir = "KILIS"
        sehir_num = 30
        
    elif sehir.upper() == "KARABUK":
        sehir = "KARABUK"
        sehir_num = 31
        
    else:
        sehir = None
        sehir_num = 0
        
    return sehir,sehir_num
