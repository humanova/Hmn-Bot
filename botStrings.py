
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#  hmnBot Yazilari


bot_game = {
    "meme" : "lookin' at r/dankmemes",
    "cok-komik" : "Aklınla" #oynuyor hahahaha
}

yardim = {
    "komutlar" :    "\n\n\n" +"**[Komutlar]**\n",
    "eglence" :     "```\n**-Eğlence-**\n```",
    "genel" :       "```\n**-Genel-**\n```",
    "yonetim" :     "\n\n**-Yönetim-**\n```",
    "bitis" :       "```:spider::spider::spider::spider::spider::spider::spider::spider::spider:",
    "surum" :       "!sürüm,!version        (versiyonum!)\n",
    "statu" :       "!statü,!stats          (istatisiklerim!)\n",
    "server" :      "!server                (server bilgileri!)\n",
    "hava" :        "!hava                  (şehrindeki hava durumunu gör!)\n",
    "roller" :      "!roller,roles          (serverdaki roller!)\n",
    "rolver" :      "!rolver                (etiketlenen kullanicilara rol ver!)\n",
    "gelistirici" : "!dev,!geliştirici      (beni yazan kişi!)\n",
    "sence" :       "!sence                 (bana soru sor![evet-hayır])\n",
    "google" :      "!google,!ara           (google'da ara!)\n",
    "davet" :       "!davet,!invite         (kanal davet linki olustur!)\n",
    "lmgtfy" :      "!lmgtfy                (birisine googlelamayı öğret!)\n",
    "btc" :         "!bitcoin,!btc          (anlık bitcoin kuru!)\n" ,
    "kripto" :      "!kripto,!crypto        (kripto para kurlari!)\n",
    "doviz" :       "!döviz                 (anlık doviz kurlari!)\n",
    "self" :        "!ben,!self             (kendi kendini öv!)\n",
    "ceviri":       "!cevir                 (ceviri yap!)\n",
    "oyla" :        "!oyla,!vote            (oylama baslat!)\n",
    "durt" :        "!dürt,!ping            (birisini dürt!)\n",
    "firlat" :      "!fırlat,!flip          (yazı mı, tura mı!)\n",
    "sikayet" :     "!şikayet               (bir durumu yetkiliye sikayet et!)\n",
    "karakter" :    "\nNot: Türkçe komutları türkçe karakter kullanmadan da çalıştırabilirsiniz. ```!sürüm == !surum, !döviz usd == !doviz usd```"
}


komut = {
    "yardim" : yardim["komutlar"] + yardim["yonetim"] + yardim["sikayet"] + yardim["rolver"] + yardim["genel"] + yardim["durt"] + yardim["oyla"] + yardim["ceviri"] + yardim["google"] + yardim["lmgtfy"] + yardim["doviz"] + yardim["kripto"] + yardim["btc"] + yardim["davet"] + yardim["server"] + yardim["roller"] +  yardim["gelistirici"]  +yardim["statu"] + yardim["surum"] + yardim["eglence"] + yardim["sence"] + yardim["self"] + yardim["bitis"] + yardim["karakter"],
    "join_sahip" : "Merhaba %s!\nSana ve Serverdaki **%d** kullanıcıya yardımcı olmaya hazırım! Tek yapman gereken !yardım yazarak komutlarımı öğrenmek.",
    "gelistirici" : "Merhaba <@%s>, <@%s> tarafından geliştiriliyorum.\n\n **GitHub** : https://github.com/humanova\n **Steam** : http://steamcommunity.com/id/humanovan",
    "statu" : "%d Serverda,\n%d Kullaniciya,\n%d Kanala hizmet veriyorum!",
    "sikayet_admin" : "[ŞIKAYET]\nTarih : %s\nServer : %s\nKanal : %s\nKullanıcı : %s(%s)\n\nŞikayet : %s\n(Not: Hatali sikayet durumunda lutfen gelistiriciye bildirin)",
    "sikayet_kullanici" :  "Şikayet iletildi!",
    "sikayet_hata" : "Şikayet iletilemedi, yeniden deneyin.",
    "durt" : "<@%s>, <@%s> seni dürttü!",
    "durt2" : "<@%s> Kendi kendini dürttün!",
    "oyla" : '<@%s> bir oylama başlattı!\n"**%s**"',
    "bitcoin" : "Bitcoin değeri : $  %s\nBitcoin değeri : TL %s",
    "kripto" : "%s değeri : $ %s\n%s değeri : TL %s",
    "doviz" : "%s/TL : %s",
    "roller" : "**%s | Server Rolleri:** ```%s```",
    "rolverHata" : "Rol verilirken hata oluştu (Bunun nedeni yetkimin olmaması olabilir!)",
    "rolverHataYetkiYok" : "**Buna yetkin yok!**",
    "server1" : "**Server Adi :** %s \n**Server ID :** %s \n**Server Sahibi :** %s(%s)\n**Kullanici Sayisi :** %d\n**Server Bolgesi :** %s\n**Server Yaratilma Tarihi :** %s",
    "self" : "%ssin!",
    "senceEvet1" : "Maalesef evet...",
    "senceEvet2" : "Evet! Kesinlikle",
    "senceHayir1" : "Hayır, bu doğru olamaz",
    "senceHayir2" : "Maalesef hayır...",
    "firlatYazi" : "Yazı geldi!",
    "firlatTura" : "Tura geldi!",
    "omurcek" : ":spider: ::)",
    "kedi1" : "https://cdn.discordapp.com/attachments/455819920140271626/456190563360702484/3.jpg",
    "kedi2" : "https://cdn.discordapp.com/attachments/455821524285259778/456190685301833738/4.jpg",
    "kedi3" : "https://cdn.discordapp.com/attachments/455821524285259778/456190723620864011/1.jpg",
    "kedi4" : "https://cdn.discordapp.com/attachments/455821524285259778/456190866554617857/2.jpg",
    "bot1" : "https://p.fod4.com/p/media/1cd2f27638/aPtE2U3sSnEkyjeDodvg_r3.gif",
    "bot2" : "https://media.giphy.com/media/10XpbAw59H1mog/giphy.gif",
    "bot3" : "https://media1.tenor.com/images/c771433f71582c244de8b3e7d6c8e241/tenor.gif",
    "bot4" : "https://media2.giphy.com/media/EizPK3InQbrNK/giphy.gif"
}