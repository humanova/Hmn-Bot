
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import dovizIslem as doviz
import requests

kur,deger = doviz.DovizParse("usd","2")

print("Kur : " + kur + "  ||  Deger : " + str(deger))