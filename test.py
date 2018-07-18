import dovizIslem as doviz

kur,kisa_ad,kur_degisim,grafik_link = doviz.KriptoParse("peercoin","usd","1")

print(str(kur) + " " + str(kisa_ad) + " " + str(kur_degisim) + " " + str(grafik_link))