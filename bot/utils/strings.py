# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# strings/dicts related to bot commands

currency_map = {
    "ALTIN": ['ALTIN', 'GOLD'],
    "USD": ['USD', 'DOLAR', 'DOLLAR'],
    "EUR": ['EUR', 'EURO', 'AVRO'],
    "GBP": ['GBP', 'POUND', 'STERLIN'],
    "RUB": ['RUB', 'RUBLE'],
    "JPY": ['JPY', 'YEN'],
    "CAD": ['CAD', 'KANADA'],
    "AUD": ['AUD'],
    "CNY": ['CNY', 'RENMINBI'],
    "SEK": ['SWE'],
    "CHF": ['CHW', 'SWI'],
    "DKK": ['DKK', 'DAN'],
    "SAR": ['SAR', 'RIYAL'],
    "RON": ['RON', 'LEY'],
    "NOK": ['NOK'],
    "BGN": ['BGN'],
    "IRR": ['IRR'],
    "PKR": ['PKR'],
    "KWD": ['KWD'],
    "CSK": ['CSK'],

    # ozel
    "OSU": ['OSU', 'SUPPORTER', 'SUP'],
}

gold_whitelist = [
    'GA',       # gram
    'XAU/USD',  # ons
    'C',        # ceyrek
    'T',        # yarim
    'CMR'       # cumhuriyet
]

crypto_currency_map = {
    "btc": {'currency': 'bitcoin', 'graph_id': '1', 'aliases': ['BTC', 'BITCOIN']},
    "bch": {'currency': 'bitcoin-cash', 'graph_id': '1831', 'aliases': ['BCH', 'BTCCASH', 'BITCOINCASH']},
    "eth": {'currency': 'ethereum', 'graph_id': '1027', 'aliases': ['ETH', 'ETHEREUM']},
    "xrp": {'currency': 'ripple', 'graph_id': '52', 'aliases': ['XRP', 'RIPPLE']},
    "eos": {'currency': 'eos', 'graph_id': '1765', 'aliases': ['EOS']},
    "xmr": {'currency': 'monero', 'graph_id': '328', 'aliases': ['XMR', 'MONERO']},
    "ltc": {'currency': 'litecoin', 'graph_id': '2', 'aliases': ['LTC', 'LITE', 'LITECOIN']},
    "etc": {'currency': 'ethereum-classic', 'graph_id': '1321', 'aliases': ['ETC', 'ETHEREUM CLASSIC']},
    "zec": {'currency': 'zcash', 'graph_id': '1437', 'aliases': ['ZEC', 'ZCASH']},
    "bcn": {'currency': 'bytecoin-bcn', 'graph_id': '372', 'aliases': ['BCN', 'BYTECOIN']},
    "xlm": {'currency': 'stellar', 'graph_id': '512', 'aliases': ['XLM', 'STELLAR']},
    "ada": {'currency': 'cardano', 'graph_id': '2010', 'aliases': ['ADA', 'CARDANO']},
    "miota": {'currency': 'iota', 'graph_id': '1720', 'aliases': ['MIOTA', 'IOTA']},
    "trx": {'currency': 'tron', 'graph_id': '1958', 'aliases': ['TRX', 'TRON']},
    "neo": {'currency': 'neo', 'graph_id': '1376', 'aliases': ['NEO']},
    "nty": {'currency': 'nexty', 'graph_id': '2714', 'aliases': ['NTY', 'NEXTY']},
    "ppc": {'currency': 'peercoin', 'graph_id': '5', 'aliases': ['PPC', 'PEERCOIN']},
}

mgm_city_map = {
    "ISTANBUL": 0,
    "EDIRNE": 1,
    "KOCAELI": 2,
    "IZMIR": 3,
    "AFYONKARAHISAR": 4,
    "DENIZLI": 5,
    "ADANA": 6,
    "ANTALYA": 7,
    "ISPARTA": 8,
    "ANKARA": 9,
    "ESKISEHIR": 10,
    "KONYA": 11,
    "BOLU": 12,
    "ZONGULDAK": 13,
    "KASTAMONU": 14,
    "SAMSUN": 15,
    "TOKAT": 16,
    "TRABZON": 17,
    "ERZURUM": 18,
    "MALATYA": 19,
    "VAN": 20,
    "DIYARBAKIR": 21,
    "GAZIANTEP": 22,
    "SANLIURFA": 23,
    "BURSA": 24,
    "KUTAHYA": 25,
    "NIGDE": 26,
    "KARABUK": 27,
    "ARTVIN": 28,
    "ARDAHAN": 29,
    "KILIS": 30,
    "KARABUK": 31,
}

komut = {
    "sikayet_admin": "[ŞIKAYET]\nTarih : %s\nServer : %s\nKanal : %s\nKullanıcı : %s(%s)\n\nŞikayet : %s",
    "sikayet_kullanici": "Şikayet iletildi!",
    "sikayet_hata": "Şikayet iletilemedi.",
    "oyla": '<@%s> bir oylama başlattı!\n"**%s**"',
    "sence1": "Maalesef evet...",
    "sence2": "Evet! Kesinlikle",
    "sence3": "Hayır, bu doğru olamaz",
    "sence4": "Maalesef hayır...",
    "memeHata": "Subreddit anlaşılamadı. **_!yardim meme_** yazarak geçerli subredditleri görebilirsiniz.",
    "oyunHata": "Girdiğiniz oyun ismi çok kısa. Bu nedenle arama yapamıyorum. :(",
    "oyunHata2": "Sunucuda kimse %s oynamıyor.",
    "redditico": "http://puu.sh/C2Lxd/78e8e9a31b.png",
    "chessico" : "https://pngimage.net/wp-content/uploads/2018/05/chess-knight-png-2.png",
    "112_pasta_url": "https://paste.ee/p/8JKSU",
    "kripto-cizgi": "-------------------------------"
}

meme_subreddits = [
    "dankmemes",
    "memeeconomy",
    "deepfriedmemes",
    "surrealmemes",
    "offensivememes",
    "2meirl4meirl",
    "blackpeopletwitter",
    "okbuddyretard",
    "coaxedintoasnafu",
    "bikinibottomtwitter",
    "bonehurtingjuice",
    "iamverysmart",
    "me_irl",
    "meirl",
    "memes",
    "animemes",
    "suddenlygay",
    "ihavesex",
    "wholesomememes",
    "historymemes",
    "softwaregore",
    "turkeyjerky"
]
