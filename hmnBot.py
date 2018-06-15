
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#	NOTLAR
#   google,lmgtfy ozel karakterler ekle!

import os
import random
import discord
import aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time

#kendi importlarim
import botStrings as yazi
import dovizIslem as doviz
################################

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

version = "hmnBot v0.1.5a\n14/06/18"
myID = "213262071050141696"
botID = "455819835486502933"

#uyarilar = ["EMIR","HUMAN","HUMANOVAN","HUMANOVA","HUMANOV","HUMANDESU"]
uyari_disi = [botID,myID]


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

@client.event
async def on_ready():
    print("Bot hazir!\n")
    print("%s adiyla giris yapildi" % (client.user.name))
    await client.change_presence(game=discord.Game(name=yazi.bot_game["meme"]))

@client.event
async def on_server_join(server):
    client.start_private_message(server.owner)
    ownerName = server.owner.name 
    await client.send_message(server.owner, yazi.komut["join_sahip"] % (ownerName,server.member_count))


@client.event
async def on_message(message):

    if not message.author.bot == 1:
        
        #bana seslenilme
        if "humandesu" in message.content:
            if not message.author.id in uyari_disi:
                userID = message.author.id
                await client.send_message(message.channel, "**<@%s>,  <@%s> sana seslendi!**" % (myID,userID))
        
        #bu yontem gereksiz yavas (ve diger isleri de yavaslatiyor)
        '''
        contents = message.content.split(" ")
        for word in contents:
            if word.upper() in uyarilar:
                if not message.author.id in uyari_disi:
                    userID = message.author.id
                    await client.send_message(message.channel, "**<@%s>,  <@%s> sana seslendi!**" % (myID,userID))
        '''
        #++========================== GENEL============================++#

        #!surum,!version,!versiyon
        if message.content.upper().startswith("!VERSION") or message.content.upper().startswith("!VERSIYON") or message.content.upper().startswith("!SÜRÜM") or message.content.upper().startswith("!SURUM"):
            await client.send_message(message.channel, "**%s**" % (version))


        #!gelistirici,!developer
        if message.content.upper().startswith("!DEV") or message.content.upper().startswith("!GELISTIRICI") or message.content.startswith("!geliştirici"):
            userID = message.author.id
            await client.send_message(message.channel, yazi.komut["gelistirici"] % (userID,myID))


        #!help,!yardim
        if message.content.upper().startswith("!HELP") or message.content.upper().startswith("!YARDIM") or message.content.startswith("!yardim"):
            await client.send_message(message.channel, yazi.komut["yardim"])
            

        #!statu,!stats
        if message.content.upper().startswith("!STATS") or message.content.upper().startswith("!STATÜ") or message.content.upper().startswith("!STATU"):
            servers = serverSayisi()
            users = kullaniciSayisi()
            channels = channelSayisi()
            await client.send_message(message.channel, yazi.komut["statu"] % (servers,users,channels))


        #!durt,!ping
        if message.content.upper().startswith('!PING') or message.content.upper().startswith("!DÜRT") or message.content.upper().startswith("!DURT"):
            contents = message.content.split(" ")
            if contents[1]:
                userID = message.author.id
                member = message.server.get_member_named(contents[1])
                if not userID == member.id:
                    await client.send_message(message.channel, yazi.komut["durt"] % (member.id,userID))
                else:
                    await client.send_message(message.channel, yazi.komut["durt2"] % (userID))
        

        #!soyle,!say (sadece benim id'm)
        if message.content.upper().startswith("!SAY"):
            if message.author.id == myID:
                args = message.content.split(" ")
                if args[1]:
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
            if msg[1]:
                msg = await client.send_message(message.channel, yazi.komut["oyla"] % (userID," ".join(msg[1:])))
                await client.add_reaction(msg,'👍')
                await client.add_reaction(msg,'👎')
            

        # !google,!ara (NOT! ozel karakterler desteklenmiyor!)
        if message.content.upper().startswith("!GOOGLE") or message.content.upper().startswith("!ARA"):
            searchQ = "https://google.com/search?q="
            msg = message.content.split(" ")
            if msg[1]:
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
            if msg[1]:
                for word in range(1,len(msg)):
                    if not word == len(msg) - 1:
                        searchQ += msg[word] + "+"
                    else:
                        searchQ += msg[word]

                await client.send_message(message.channel, "%s" % (searchQ))


        #!bitcoin,!btc
        if message.content.upper().startswith("!BITCOIN") or message.content.upper().startswith("!BTC"):
            a,btc_tl = doviz.DovizParse("BTC-TRY")
            a,btc_usd = doviz.DovizParse("BTC-USD")
            
        
            await client.send_message(message.channel, yazi.komut["bitcoin"] % (btc_usd,btc_tl))
        

        #!doviz kur
        if message.content.upper().startswith("!DÖVIZ") or message.content.upper().startswith("!DOVIZ"):
            msg = message.content.split(" ")
            if msg[1]:
                kur = msg[1]
                kur,kur_degeri = doviz.DovizParse(kur)
                
                await client.send_message(message.channel, yazi.komut["doviz"] % (kur,kur_degeri))
        

        #!roller,!roles
        if message.content.upper().startswith("!ROLLER") or message.content.upper().startswith("!ROLES"):
            currServer = message.server.name
            roles = message.server.role_hierarchy
            roller = ""
            for role in roles:
                roller += role.name + "\n"
            
            await client.send_message(message.channel, yazi.komut["roller"] % (currServer,roller))
            
        '''
        #!rolver (sadece sahipler)
        if message.content.upper().startswith("!ROLVER"):
            if message.server.owner.id == message.author.id:
                users = message.mentions
                roles = message.role_mentions
                try:
                    client.add_roles(users,roles)
                except discord.errors.NotFound:
                    await client.send_message(message.channel, yazi.komut["rolverHata"])
                    return
            else:
                await client.send_message(message.channel, yazi.komut["rolverHataYetkiYok"])
        '''

        #!sikayet (server sahibine)
        if message.content.upper().startswith("!ŞIKAYET") or message.content.upper().startswith("!SIKAYET"):
            sikayet = message.content.split(" ")
            if sikayet[1]:
                owner = message.server.owner
                sikayetci = message.author.name + "#" + message.author.discriminator
                sikayetci_nick = message.author.display_name
                serverAdi = message.server.name
                kanalAdi = message.channel.name
                tarih = message.timestamp
                
                try:
                    client.start_private_message(owner)
                    await client.send_message(owner, yazi.komut['sikayet_admin'] % (tarih,serverAdi,kanalAdi,sikayetci,sikayetci_nick," ".join(sikayet[1:])))
                    await client.send_message(message.channel, yazi.komut['sikayet_kullanici'])
                    try:
                        await client.delete_message(message)
                    except discord.errors.NotFound:
                        return

                except discord.errors.NotFound:
                    await client.send_message(message.channel, yazi.komut['sikayet_hata'])


        #!server,!serverstats
        if message.content.upper().startswith("!SERVER"):
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

            await client.send_message(message.channel, yazi.komut["server1"] % (serverName,serverID,serverOwner,serverOwnerN,serverMemCount,serverRegion,serverDate))
            await client.send_message(message.channel, yazi.komut["server2"] % (roller))
            

        #++========================== EGLENCE ============================++#

        #!ben,!self
        if message.content.upper().startswith("!SELF") or message.content.upper().startswith("!BEN"):
            msg = message.content.split(" ")
            if msg[1]:
                await client.send_message(message.channel, yazi.komut["self"] % (" ".join(msg[1:])))


        #!sence
        if message.content.upper().startswith("!SENCE"):
            option = random.randint(1,4)
            if option == 1 :
                await client.send_message(message.channel, yazi.komut["senceEvet1"])
            if option == 2 :
                await client.send_message(message.channel, yazi.komut["senceEvet2"])
            if option == 3:
                await client.send_message(message.channel, yazi.komut["senceHayir1"])
            if option == 4:
                await client.send_message(message.channel, yazi.komut["senceHayir2"])


        #!firlat,!flip
        if message.content.upper().startswith("!FIRLAT") or message.content.startswith("!fırlat") or message.content.upper().startswith("!FLIP"):
            gelen = random.randint(1,100)
            if gelen % 2 == 1:
                await client.send_message(message.channel, yazi.komut["firlatYazi"])
            if gelen % 2 == 2:
                await client.send_message(message.channel, yazi.komut["firlatTura"])


        #herkesi etiketleyenlere kizgin
        if message.mention_everyone:
            await client.add_reaction(message,"😡")


        #++========================== OZEL ============================++#
        

        #omurcek ozel
        if message.content.upper().startswith("OMURCEK") or message.content.upper().startswith("ÖMÜRCEK"):
            await client.send_message(message.channel, yazi.komut["omurcek"])
        
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
                await client.send_message(message.channel, yazi.komut["kedi1"])
            if op == 2:
                await client.send_message(message.channel, yazi.komut["kedi2"])
            if op == 3:
                await client.send_message(message.channel, yazi.komut["kedi3"])
            if op ==4:
                await client.send_message(message.channel, yazi.komut["kedi4"])

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


token = os.environ['PP_BOT_TOKEN']
client.run(token)



