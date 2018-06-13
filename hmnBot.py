#	NOTLAR
#   google,lmgtfy ozel karakterler!
#   !sikayet (bana ya da server sahibine) yazilacak


import os
import random
import discord
import aiohttp
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time

Client = discord.Client()
client = commands.Bot(command_prefix = "!")


version = "v0.1.4a\n14/06/18"
myID = "213262071050141696"
botID = "455819835486502933"

uyarilar = ["EMIR","HUMAN","HUMANOVAN","HUMANOVA","HUMANOV","HUMANDESU"]
uyari_disi = [botID,myID]


komutlarYazi =  "\n\n\n" +"**[Komutlar]**\n"
eglenceYazi =   "```\n**-Eğlence-**\n```"
genelYazi =     "```\n**-Genel-**\n```"
yonetimYazi =   "\n\n**-Yönetim-**\n```"

surumYazi =            "     !sürüm,!version              (versiyonum!)\n"
statusYazi =           "     !statü,!stats                (istatisiklerim!)\n"
serverYazi =           "     !server,!serverstats         (server bilgileri!)\n"
rollerYazi =           "     !roller,roles                (serverdaki roller!)\n"          
rolverYazi =           "     !rolver                      (etiketlenen kullanicilara rol ver!)\n"
gelistiriciYazi =      "     !geliştirici,!developer      (beni yazan kişi!)\n"
senceYazi =            "     !sence                       (bota soru sor!)\n"
googleYazi =           "     !google,!ara                 (google'da ara!)\n"
lmgtfyYazi =           "     !lmgtfy                      (birisine googlelamayı öğret!)\n"
btcYazi =              "     !bitcoin,!btc                (anlık bitcoin kuru!)\n" 
dovizYazi =            "     !doviz                       (anlık doviz kurlari!)\n"
selfYazi =             "     !ben,!self                   (kendi kendini öv!)\n"
oylaYazi =             "     !oyla,!vote                  (oylama baslat!)\n"
pingYazi =             "     !dürt,!ping                  (birisini dürt!)\n"
firlatYazi =           "     !firlat,!flip                (yazı mı, tura mı!)\n"
#omurcekYazi =          "     ömürcek                      (neden olmasın ki!)"
#sayYazi =              "     !söyle,!say                  (bir seyler yaz!)\n"

helpYazisiBitis= "```:spider::spider::spider::spider::spider::spider::spider::spider::spider:"

helpYazisi =   komutlarYazi + yonetimYazi + rolverYazi
helpYazisi +=  genelYazi +  pingYazi + oylaYazi + googleYazi + lmgtfyYazi + btcYazi + dovizYazi + serverYazi + rollerYazi + statusYazi + gelistiriciYazi + surumYazi
helpYazisi +=  eglenceYazi + senceYazi + firlatYazi + selfYazi + helpYazisiBitis



def serverSayisi():
    i = 0
    for server in client.servers:
        i = i + 1
    return i

def channelSayisi():
    i = 0
    for server in client.servers:
        for channel in server.channels:
            i = i + 1
    return i

def kullaniciSayisi():
    i = 0
    for server in client.servers:
        for member in server.members:
            i = i + 1     
    return i

def DovizParse(kur):
    if kur.upper() == "USD" or kur == "DOLAR" or kur == "DOLLAR" or kur == "AMERIKAN":
        kur = "usd"

    elif kur.upper() == "EUR" or kur.upper() == "EURO" or kur.upper() == "AVRO" or kur.upper() == "AVRUPA":
        kur = "eur"

    elif kur.upper() == "CAD" or kur.upper() == "KANADA": 
        kur = "cad"

    elif kur.upper() == "AUD" or kur.upper() == "AVUSTRALYA":
        kur = "aud"

    elif kur.upper() == "GBP" or kur.upper() == "POUND" or kur.upper() == "STERLIN" or kur.upper() == "STERLING":
        kur = "gbp"

    elif kur.upper() == "EUR" or kur.upper() == "EURO" or kur.upper() == "AVRO":
        kur = "eur"

    elif kur.upper() == "SAR" or kur.upper() == "SAUDI" or kur.upper() == "ARABISTAN":
        kur = "sar"

    elif kur.upper() == "JPY" or kur.upper() == "JAPON" or kur.upper() == "YEN":
        kur = "jpy"
    
    elif kur.upper() == "CNY" or kur.upper() == "ÇIN" or kur.upper() == "RENMINBI":
        kur = "cny"

    elif kur.upper() == "PKR" or kur.upper() == "PAKISTAN":
        kur = "pkr"
    
    elif kur.upper() == "BGN" or kur.upper() == "BULGAR" or kur.upper() == "BULGARISTAN":
        kur = "bgn"

    elif kur.upper() == "IRR" or kur.upper() == "IRAN":
        kur = "irr"

    elif kur.upper() == "RUB" or kur.upper() == "RUBLE" or kur.upper() == "RUS" or kur.upper() == "RUSYA":
        kur = "rub"

    elif kur.upper() == "RON" or kur.upper() == "ROMANYA" or kur.upper() == "RUMEN":
        kur = "ron"

    elif kur.upper() == "NOK" or kur.upper() == "ROMANYA" or kur.upper() == "RUMEN":
        kur = "nok"

    elif kur.upper() == "KWD" or kur.upper() == "KUVEYT" or kur.upper() == "KUWAITI":
        kur = "kwd"

    elif kur.upper() == "SEK" or kur.upper() == "SWE" or kur.upper() == "ISVEÇ":
        kur = "sek"

    elif kur.upper() == "CHF" or kur.upper() == "SWI" or kur.upper() == "ISVIÇRE":
        kur = "sek"

    elif kur.upper() == "DKK" or kur.upper() == "DANIMARKA" or kur.upper() == "DAN":
        kur = "dkk"

    kurURL = "http://tr.investing.com/currencies/" + kur + "-try"

    if kur.upper() == "BTC-TRY":
        kurURL = 'https://tr.investing.com/crypto/bitcoin/btc-try'
    elif kur.upper() == "BTC-USD":
        kurURL = 'https://tr.investing.com/crypto/bitcoin/btc-usd'

    data = urlopen(Request(kurURL, headers={'User-Agent': 'Mozilla'})).read()
    parse = BeautifulSoup(data,'html.parser')

    for doviz in parse.find_all('span', id="last_last"):
        liste = list(doviz)
    
    liste = str(liste)
    for char in "[']":
        liste = liste.replace(char,'')

    kur_degeri = liste
    return kur.upper(),kur_degeri


@client.event
async def on_ready():
    print("Bot hazir!")
    await client.change_presence(game=discord.Game(name="lookin' at r/dankmemes"))

@client.event
async def on_server_join(server):
    client.start_private_message(server.author)
    userID = server.author.id 
    await client.send_message(server.author, "Merhaba <@%s>!\n Sana ve Serverdaki **%d** kullanıcıya yardımcı olmak için hazırım! Tek yapman gereken !help yazarak komutlarımı öğrenmek." % (userID,server.member_count))


@client.event
async def on_message(message):

    #bana seslenilme
    contents = message.content.split(" ")
    userID = message.author.id
    for word in contents:
        if word.upper() in uyarilar:
            if not message.author.id in uyari_disi:
                await client.send_message(message.channel, "**<@%s>,  <@%s> sana seslendi!**" % (myID,userID))


    #++========================== GENEL============================++#

    #!surum,!version,!versiyon
    if message.content.upper().startswith("!VERSION") or message.content.upper().startswith("!VERSIYON") or message.content.upper().startswith("!SÜRÜM") or message.content.upper().startswith("!SURUM"):
        await client.send_message(message.channel, "**%s**" % (version))

    #!gelistirici,!developer
    if message.content.upper().startswith("!DEVELOPER") or message.content.upper().startswith("!GELISTIRICI") or message.content.startswith("!geliştirici"):
        userID = message.author.id
        await client.send_message(message.channel, "Merhaba <@%s>, Emir Erbasan tarafından geliştiriliyorum.\n\n  Discord : <@%s> \n  GitHub : https://github.com/humanova\n  Steam : http://steamcommunity.com/id/humanovan" % (userID,myID))

    #!help,!yardim
    if message.content.upper().startswith("!HELP") or message.content.upper().startswith("!YARDIM") or message.content.startswith("!yardim"):
        await client.send_message(message.channel, helpYazisi)
        
    #!statu,!stats
    if message.content.upper().startswith("!STATS") or message.content.upper().startswith("!STATÜ") or message.content.upper().startswith("!STATU"):
        servers = serverSayisi()
        users = kullaniciSayisi()
        channels = channelSayisi()
        await client.send_message(message.channel, "%d Serverda,\n%d Kullaniciya,\n%d Kanala hizmet veriyorum!"% (servers,users,channels))

    #!durt,!ping
    if message.content.upper().startswith('!PING') or message.content.upper().startswith("!DÜRT") or message.content.upper().startswith("!DURT"):
        userID = message.author.id
        contents = message.content.split(" ")
        member = message.server.get_member_named(contents[1])
        if not userID == member.id:
            await client.send_message(message.channel, "<@%s>,  <@%s> seni dürttü!" % (member.id,userID))
        else:
            await client.send_message(message.channel, "<@%s> Kendi kendini dürttün!" % (userID))
    
    #!soyle,!say (sadece benim id'm)
    if message.content.upper().startswith("!SAY") or message.content.upper().startswith("!SOYLE") or message.content.upper().startswith("!SÖYLE"):
        if message.author.id == myID:
            args = message.content.split(" ")
            try:
                await client.delete_message(message)
            except discord.errors.NotFound:
                return

            await client.send_message(message.channel, "%s" % (" ".join(args[1:])))
        else:
            await client.send_message(message.channel,"**Buna yetkin yok!**")

    #!oyla,!vote
    if message.content.upper().startswith("!VOTE") or message.content.upper().startswith("!OYLA"):
        userID = message.author.id
        msg = message.content.split(" ")
        msg = await client.send_message(message.channel, '<@%s> bir oylama başlattı!\n\n"**%s**" ' % (userID," ".join(msg[1:])))
        await client.add_reaction(msg,'👍')
        await client.add_reaction(msg,'👎')
    
    #!google,!ara (NOT! ozel karakterler desteklenmiyor!)
    if message.content.upper().startswith("!GOOGLE") or message.content.upper().startswith("!ARA"):
        searchQ = "https://google.com/search?q="
        msg = message.content.split(" ")
        
        for word in range(1,len(msg)):
            if not word == len(msg) - 1:
                searchQ += msg[word] + "+"
            else:
                searchQ += msg[word]

        await client.send_message(message.channel, "%s" % (searchQ))

    #!lmgtfy (NOT! ozel karakterler desteklenmiyor!)
    if message.content.upper().startswith("!LMGTFY"):
        searchQ = "http://lmgtfy.com/?q="
        msg = message.content.split(" ")
        
        for word in range(1,len(msg)):
            if not word == len(msg) - 1:
                searchQ += msg[word] + "+"
            else:
                searchQ += msg[word]

        await client.send_message(message.channel, "%s" % (searchQ))

    
    #!bitcoin,!btc  (dolarKuru eksik)
    if message.content.upper().startswith("!BITCOIN") or message.content.upper().startswith("!BTC"):
        a,btc_tl = DovizParse("BTC-TRY")
        a,btc_usd = DovizParse("BTC-USD")
        
    
        await client.send_message(message.channel, "Bitcoin değeri : $     %s\nBitcoin değeri : TL   %s" % (btc_usd,btc_tl))
    
    
    #!doviz kur
    if message.content.upper().startswith("!DÖVIZ") or message.content.upper().startswith("!DOVIZ"):
        msg = message.content.split(" ")
        kur = msg[1]
        kur,kur_degeri = DovizParse(kur)

        await client.send_message(message.channel, "%s/TL : %s" % (kur,kur_degeri))
       
    
        

    #!roller,!roles
    if message.content.upper().startswith("!ROLLER") or message.content.upper().startswith("!ROLES"):
        currServer = message.server.name
        roles = message.server.role_hierarchy
        roller = ""
        for role in roles:
            roller += role.name + "\n"
        
        await client.send_message(message.channel, "**%s | Server Rolleri:** ```%s```" % (currServer,roller))
        
    #!rolver (sadece sahipler)
    if message.content.upper().startswith("!ROLVER"):
        if message.server.owner.id == message.author.id:
            users = message.mentions
            roles = message.role_mentions
            try:
                client.add_roles(users,roles)
            except discord.errors.NotFound:
                await client.send_message(message.channel, "Rol verilirken hata oluştu (Bunun nedeni yetkim olmaması olabilir!)")
                return
        else:
            await client.send_message(message.channel, "**Buna yetkin yok!**")


    #!server,!serverstats
    if message.content.upper().startswith("!SERVERSTATS") or message.content.upper().startswith("!SERVER"):
        serverName = message.server.name
        serverID = message.server.id
        serverOwner = message.server.owner.name
        serverOwnerN = message.server.owner.nick
        serverMemCount = message.server.member_count
        serverRegion = message.server.region
        roles = message.server.role_hierarchy
        serverDate = message.server.created_at
        
        roller = ""
        for role in roles:
            roller += role.name + "\n"

        await client.send_message(message.channel, "**Server Adi :** %s \n**Server ID :** %s \n**Server Sahibi :** %s(%s)\n**Kullanici Sayisi :** %d\n**Server Bolgesi :** %s\n**Server Yaratilma Tarihi :** %s" % (serverName,serverID,serverOwner,serverOwnerN,serverMemCount,serverRegion,serverDate))
        await client.send_message(message.channel, "**Server Rolleri:** ```%s```" % (roller))
        

    #++========================== EGLENCE ============================++#

   #!ben,!self
    if message.content.upper().startswith("!SELF") or message.content.upper().startswith("!BEN"):
        msg = message.content.split(" ")
        await client.send_message(message.channel, "%ssin!" % (" ".join(msg[1:])))

    #!sence
    if message.content.upper().startswith("!SENCE"):
        option = random.randint(1,4)
        if option == 1 :
            await client.send_message(message.channel, "Maalesef evet...")
        if option == 2 :
            await client.send_message(message.channel, "Evet! Kesinlikle")
        if option == 3:
            await client.send_message(message.channel, "Hayır, bu doğru olamaz")
        if option == 4:
            await client.send_message(message.channel, "Maalesef hayır...")

    #!firlat,!flip
    if message.content.upper().startswith("!FIRLAT") or message.content.startswith("!fırlat") or message.content.upper().startswith("!FLIP"):
        gelen = random.randint(1,100)
        if gelen % 2 == 1:
            await client.send_message(message.channel, "Yazi geldi!")
        if gelen % 2 == 2:
            await client.send_message(message.channel, "Tura geldi!")

    #herkesi etiketleyenlere kizgin
    if message.mention_everyone:
        await client.add_reaction(message,"😡")

    #omurcek ozel
    if message.content.upper().startswith("OMURCEK") or message.content.upper().startswith("ÖMÜRCEK"):
        await client.send_message(message.channel, ":spider: ::)")

    ############ OZEL #############
    #no more hiding "send nudes" msg (anti selindesu)
    if "nude" in message.content:
        await client.add_reaction(message,"🇳")
        await client.add_reaction(message,"🇺")
        await client.add_reaction(message,"🇩")
        await client.add_reaction(message,"🇪")
        await client.add_reaction(message,"🇸")

    #crazy cries 
    if "crazy cries" in message.content:
        op = random.randint(1,4)

        if op == 1:
            await client.send_message(message.channel, "https://cdn.discordapp.com/attachments/455819920140271626/456190563360702484/3.jpg")
        if op == 2:
            await client.send_message(message.channel, "https://cdn.discordapp.com/attachments/455821524285259778/456190685301833738/4.jpg")
        if op == 3:
            await client.send_message(message.channel, "https://cdn.discordapp.com/attachments/455821524285259778/456190723620864011/1.jpg")
        if op ==4:
            await client.send_message(message.channel, "https://cdn.discordapp.com/attachments/455821524285259778/456190866554617857/2.jpg")


'''
    #server sahibini dogrula
    if message.author.id == message.server.owner.id:
        try:
            await client.add_reaction(message,"✅")
        except discord.errors.NotFound:
            return
    
    if message.author.id == myID:
        await client.add_reaction(message,"🇩")
        await client.add_reaction(message,"🇦")
        await client.add_reaction(message,"🇲")
        await client.add_reaction(message,"🇳")
'''


token = os.environ['BOT_TOKEN']
client.run(token)

