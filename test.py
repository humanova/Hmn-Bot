#import dovizIslem as doviz


#kur,kisa_ad,kur_degisim,grafik_link = doviz.KriptoParse("peercoin","usd","1")
#print(str(kur) + " " + str(kisa_ad) + " " + str(kur_degisim) + " " + str(grafik_link))

import havaDurumu as hava


yer = "istanbul"
yer,sicaklik,nem_orani,ruzgar_hizi,gun_dogumu,gun_batimi,durum_ikon_url = hava.havaParseOWM(yer)
print(yer + " " + str(sicaklik) + " " + str(nem_orani) + " " + str(ruzgar_hizi) + " " + str(gun_dogumu) + " " + str(gun_batimi) + " " + durum_ikon_url)