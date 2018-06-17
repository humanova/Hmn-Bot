
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from googletrans import Translator



def Cevir(curr,hedef,yazi):

    translator = Translator()
    translator = Translator(service_urls=[
      'translate.google.com',
      'translate.google.com.tr/',
    ])
    
    suanki_dil = curr.upper() 
    hedef_dil = hedef.upper()

    translations = translator.translate(yazi,src=curr,dest=hedef)

    if curr == "auto":
        oran = translator.detect(yazi).confidence
        suanki_dil = translations.src.upper()
        algilamaOrani = translations.src.upper() + " algılandı (%" +str ("%.1f" % (oran*100)) + ")"
    else:
        algilamaOrani = suanki_dil.upper() + " algılandı (%100)" 
    
    return translations.text,suanki_dil,hedef_dil,algilamaOrani
    
    