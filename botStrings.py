
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#  hmnBot Yazilari


bot_game = {
    "meme" : "lookin' at r/dankmemes",
    "knack" : "Knack 2 Baby",
    "mario" : "Super Mario Bros. 2",
    "despacito" : "Despacito 2",
    "sotarks" : "Sotarks Map",
    "respect" : "Pressing F Simulator 2018"
}

memeSubreddits = [
    "+ dankmemes",
    "+ memeeconomy",
    "+ deepfriedmemes",
    "+ me_irl",
    "+ meirl",
    "+ memes",
    "+ animemes",
    "+ okbuddyretard",
    "+ anime_irl",
    "+ coaxedintoasnafu",
    "+ notgayporn",
    "+ turkeyjerky"
]

memeSubs = "\n".join(memeSubreddits[:])

yardim = {
    "komutlar" :    "```asciidoc\n== Hmn-Bot Komutları ==\n\n",
    "eglence" :     "\n[EGLENCE]\n",
    "genel" :       "\n[GENEL]\n",
    "yonetim" :     "[YONETIM]\n",
    "bitis" :       "```",
    "surum" :       "!sürüm,!version    :: bot sürümünü gösterir\n",
    "statu" :       "!statü,!stats      :: bot istatistiklerini gösterir\n",
    "server" :      "!server            :: server bilgilierini gösterir\n",
    "temizle":      "!temizle           :: kanaldaki son x mesajı temizler\n",
    "hava" :        "!hava              :: istenilen şehirdeki hava durumunu gösterir\n",
    "roller" :      "!roller            :: serverdaki rolleri listeler\n",
    "rolver" :      "!rolver            :: etiketlenen kullanıcılara rol verir\n",
    "gelistirici" : "!dev,!geliştirici  :: geliştirici bilgilerini gösterir\n",
    "sence" :       "!sence             :: evet-hayır sorularına cevap verir\n",
    "google" :      "!google,!ara       :: google'da arama linki oluşturur\n",
    "meme" :        "!meme              :: seçilen subredditten rastgele bir meme gönderir\n",
    "davet" :       "!davet,!invite     :: bulunulan kanal için x adet davet linki oluşturur\n",
    "lmgtfy" :      "!lmgtfy            :: lmgtfy ile arama linki oluşturur\n",
    "btc" :         "!bitcoin,!btc      :: bitcoin kurunu gösterir\n" ,
    "kripto" :      "!kripto,!crypto    :: istenilen kripto para kurunu gösterir\n",
    "doviz" :       "!döviz             :: istenilen döviz kurunu gösterir\n",
    "self" :        "!ben,!self         :: yazdıklarınız ile sizi över\n",
    "ceviri":       "!cevir             :: dilden dile çeviri yapar\n",
    "oyla" :        "!oyla,!vote        :: bir oylama başlatır\n",
    "yardim" :      "!yardim,help       :: bir komut hakkında yardımı gösterir (!yardım <komut>)\n",
    "leet" :        "!leet,!l33t        :: yazılarınızı h4v4l1 yapar\n",
    "durt" :        "!dürt,!ping        :: tam ismi girilen birini dürter\n",
    "firlat" :      "!fırlat,!flip      :: bozuk para fırlatır\n",
    "sikayet" :     "!şikayet           :: server sahibine şikayet yollar\n",
    "karakter" :    "\nNot: Türkçe komutları türkçe karakter kullanmadan da çalıştırabilirsiniz.\n(!sürüm == !surum, !döviz usd == !doviz usd)"
}

komutYardim = {
    "durt" :        "```asciidoc\n== !dürt komutu ==\n\nAçıklama : Tam ismini yazdığın birini dürter\n\nÖrnek : !durt Hmn-Bot | !ping Hmn-Bot```",
    "dürt" :        "```asciidoc\n== !dürt komutu ==\n\nAçıklama : Tam ismini yazdığın birini dürter\n\nÖrnek : !durt Hmn-Bot | !ping Hmn-Bot```",
    "ping" :        "```asciidoc\n== !ping komutu ==\n\nAçıklama : Tam ismini yazdığın birini dürter\n\nÖrnek : !ping Hmn-Bot | !durt Hmn-Bot```",
    "surum" :       "```asciidoc\n== !sürüm komutu ==\n\nAçıklama : Bot sürümünü gösterir\n\nÖrnek : !surum | !version```",
    "version" :     "```asciidoc\n== !sürüm komutu ==\n\nAçıklama : Bot sürümünü gösterir\n\nÖrnek : !surum | !version```",
    "statu" :       "```asciidoc\n== !statu komutu ==\n\nAçıklama : Botun istatistiklerini gösterir\n\nÖrnek : !statu | !stats```",
    "stats" :       "```asciidoc\n== !statu komutu ==\n\nAçıklama : Botun istatistiklerini gösterir\n\nÖrnek : !statu | !stats```",
    "server" :      "```asciidoc\n== !server komutu ==\n\nAçıklama : Bulunulan serverın bilgilerini gösterir\n\nÖrnek : !durt Hmn-Bot | !ping Hmn-Bot```",
    "temizle":      "```asciidoc\n== !temizle komutu ==\n\nAçıklama : Belirtilen miktarda mesajı kanaldan siler\n\nÖrnek : !temizle 10```",
    "hava" :        "```asciidoc\n== !hava komutu ==\n\nAçıklama : Belirtilen şehirdeki hava durumunu gösterir\n\nÖrnek : !hava Istanbul | !hava Berlin```",
    "roller" :      "```asciidoc\n== !roller komutu ==\n\nAçıklama : Bulunulan serverdaki rolleri listeler\n\nÖrnek : !roller```",
    "rolver" :      "```asciidoc\n== !rolver komutu ==\n\nAçıklama : Etiketlenen kullanıcıya etiketlenen rolü verir\n\nÖrnek : !rolver @Hmn-Bot @Bot```",
    "gelistirici" : "```asciidoc\n== !geliştirici komutu ==\n\nAçıklama : Geliştirici bilgilerini gösterir\n\nÖrnek : !geliştirici | !dev```",
    "geliştirici" : "```asciidoc\n== !geliştirici komutu ==\n\nAçıklama : Geliştirici bilgilerini gösterir\n\nÖrnek : !geliştirici | !dev```",
    "dev" :         "```asciidoc\n== !dev komutu ==\n\nAçıklama : Geliştirici bilgilerini gösterir\n\nÖrnek : !geliştirici | !dev```",
    "sence" :       "```asciidoc\n== !sence komutu ==\n\nAçıklama : Bir evet-hayır sorusunu cevaplar\n\nÖrnek : !sence Bugün yağmur yağar mı?```",
    "google" :      "```asciidoc\n== !google komutu ==\n\nAçıklama : Girilen kelimelerle arama linki oluşturur\n\nÖrnek : !google Reverse Engineering nedir? | !ara Dennis Ritchie```",
    "ara" :         "```asciidoc\n== !ara komutu ==\n\nAçıklama : Girilen kelimelerle arama linki oluşturur\n\nÖrnek : !google Reverse Engineering nedir? | !ara Dennis Ritchie```",
    "meme" :        "```asciidoc\n== !meme komutu ==\n\nAçıklama : Girilen subredditten rastgele bir meme gönderir\nDesteklenen Subredditler : \n\n" + memeSubs +"\n\nÖrnek : !meme dankmemes | !meme turkeyjerky```",
    "davet" :       "```asciidoc\n== !davet komutu ==\n\nAçıklama : Bulunulan kanal için x kullanımlık davet linki oluşturur\n\nÖrnek : !davet 10```",
    "invite" :      "```asciidoc\n== !invite komutu ==\n\nAçıklama : Bulunulan kanal için x kullanımlık davet linki oluşturur\n\nÖrnek : !davet 10```",
    "lmgtfy" :      "```asciidoc\n== !lmgtfy komutu ==\n\nAçıklama : Girilen kelimelerle lmgtfy linki oluşturur\n\nÖrnek : !lmgtfy How to use Google```",
    "btc" :         "```asciidoc\n== !btc komutu ==\n\nAçıklama : Bitcoin kurunu gösterir\n\nÖrnek : !bitcoin | !btc```",
    "bitcoin" :     "```asciidoc\n== !bitcoin komutu ==\n\nAçıklama : Bitcoin kurunu gösterir\n\nÖrnek : !bitcoin | !btc```",
    "kripto" :      "```asciidoc\n== !kripto komutu ==\n\nAçıklama : Girilen kripto para kurunu gösterir\n\nÖrnek : !kripto monero | !kripto xmr```",
    "crypto" :      "```asciidoc\n== !kripto komutu ==\n\nAçıklama : Girilen kripto para kurunu gösterir\n\nÖrnek : !kripto monero | !kripto xmr```",
    "doviz" :       "```asciidoc\n== !döviz komutu ==\n\nAçıklama : Girilen döviz kurunu gösterir\n\nÖrnek : !döviz dolar 20 | !döviz euro```",
    "döviz" :       "```asciidoc\n== !döviz komutu ==\n\nAçıklama : Girilen döviz kurunu gösterir\n\nÖrnek : !döviz dolar 20 | !döviz usd```",
    "self" :        "```asciidoc\n== !self komutu ==\n\nAçıklama : Yazdıklarınla seni över(biraz gereksiz sanki :D)\n\nÖrnek : !ben Müthiş```",
    "ben" :         "```asciidoc\n== !ben komutu ==\n\nAçıklama : Yazdıklarınla seni över(biraz gereksiz sanki :D)\n\nÖrnek : !ben Müthiş```",
    "cevir":        "```asciidoc\n== !çeviri komutu ==\n\nAçıklama : İstenilen dilden istenilen dile çeviri yapar\n\n\nÖrnek : !cevir -fr -en J'aime mon vie (bu durumda fransızcadan ingilizceye çeviri yapar)\n\nÖrnek : !cevir -en Konnichiwa (bu durumda algılanan dilden(japonca) ingilizceye çeviri yapar\n\nÖrnek : !cevir Conscious (bu durumda algılanan dilden (ingilizce) türkçe'ye çeviri yapar```",
    "çevir":        "```asciidoc\n== !çeviri komutu ==\n\nAçıklama : İstenilen dilden istenilen dile çeviri yapar\n\nÖrnek : !cevir -fr -en J'aime mon vie (bu durumda fransızcadan ingilizceye çeviri yapar)\n\nÖrnek : !cevir -en Konnichiwa (bu durumda algılanan dilden(japonca) ingilizceye çeviri yapar\n\nÖrnek : !cevir Conscious (bu durumda algılanan dilden (ingilizce) türkçe'ye çeviri yapar```",
    "oyla" :        "```asciidoc\n== !oyla komutu ==\n\nAçıklama : Girilen bir durum için oylama başlatır\n\nÖrnek : !oyla Servera yeni kanal eklemeli miyim?```",
    "vote" :        "```asciidoc\n== !oyla komutu ==\n\nAçıklama : Girilen bir durum için oylama başlatır\n\nÖrnek : !oyla Servera yeni kanal eklemeli miyim?```",
    "leet" :        "```asciidoc\n== !leet komutu ==\n\nAçıklama : Yazdıklarınızı leet alfabesine uyarlar\n\nÖrnek : !leet Selam```",
    "l33t" :        "```asciidoc\n== !leet komutu ==\n\nAçıklama : Yazdıklarınızı leet alfabesine uyarlar\n\nÖrnek : !leet Selam```",
    "firlat" :      "```asciidoc\n== !fırlat komutu ==\n\nAçıklama : Bir bozuk para fırlatır\n\nÖrnek : !fırlat | !flip```",
    "flip" :        "```asciidoc\n== !flip komutu ==\n\nAçıklama : Bir bozuk para fırlatır\n\nÖrnek : !fırlat | !flip```",
    "sikayet" :     "```asciidoc\n== !şikayet komutu ==\n\nAçıklama : Server sahibine şikayet gönderir\n\nÖrnek : !sikayet Kanalda spam yapılıyor```",
    "şikayet" :     "```asciidoc\n== !şikayet komutu ==\n\nAçıklama : Server sahibine şikayet gönderir\n\nÖrnek : !sikayet Kanalda spam yapılıyor```",
    "yardim" :      "```asciidoc\n== !yardim komutu ==\n\nAçıklama : Bu komutu kullanmayı zaten biliyorsun :D\n\nÖrnek : !yardim cevir```",
    "yardım" :      "```asciidoc\n== !yardim komutu ==\n\nAçıklama : Bu komutu kullanmayı zaten biliyorsun :D\n\nÖrnek : !yardim cevir```",
    "help" :      "```asciidoc\n== !help komutu ==\n\nAçıklama : Bu komutu kullanmayı zaten biliyorsun :D\n\nÖrnek : !help cevir```"
}


komut = {
    "yardim" : yardim["komutlar"] + yardim["yonetim"] + yardim["sikayet"] + yardim["rolver"] + yardim["temizle"]+ yardim["genel"] + yardim["yardim"] + yardim["durt"] + yardim["oyla"] + yardim["ceviri"] + yardim["google"] + yardim["lmgtfy"] + yardim["doviz"] + yardim["kripto"] + yardim["btc"] + yardim["davet"] + yardim["server"] + yardim["roller"] +  yardim["gelistirici"]  +yardim["statu"] + yardim["surum"] + yardim["eglence"] + yardim["meme"] + yardim["sence"] + yardim["leet"] + yardim["self"] + yardim["bitis"] + yardim["karakter"],
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
    "deadserver" : "https://media.discordapp.net/attachments/406172843580063784/463424761318473729/LegitimateWrongBengaltiger.png",
    "kedi1" : "https://cdn.discordapp.com/attachments/455819920140271626/456190563360702484/3.jpg",
    "kedi2" : "https://cdn.discordapp.com/attachments/455821524285259778/456190685301833738/4.jpg",
    "kedi3" : "https://cdn.discordapp.com/attachments/455821524285259778/456190723620864011/1.jpg",
    "kedi4" : "https://cdn.discordapp.com/attachments/455821524285259778/456190866554617857/2.jpg",
    "bot1" : "https://p.fod4.com/p/media/1cd2f27638/aPtE2U3sSnEkyjeDodvg_r3.gif",
    "bot2" : "https://media.giphy.com/media/10XpbAw59H1mog/giphy.gif",
    "bot3" : "https://media1.tenor.com/images/c771433f71582c244de8b3e7d6c8e241/tenor.gif",
    "bot4" : "https://media2.giphy.com/media/EizPK3InQbrNK/giphy.gif",
    "kripto-cizgi" : "-------------------------------"
}

