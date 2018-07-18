
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#	NOTLAR

#  Fikir sunanlar ve gelistirirken emegi gecenler :
#  112'nin Yaz Turnuvasi Sunucusu, 112servis, barisuraz, selindesu ve digerleri!


import os,sys
import random
import discord
import aiohttp
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time

#kendi importlarim
import havaDurumu as hava
import botStrings as yazi
import dovizIslem as doviz
import zaman
import ceviri
################################

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

version = "hmnBot v0.2.6\n18/07/18"
myID = "213262071050141696"
botID = "455819835486502933"


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

def is_float(string):
  try:
    return float(string) and '.' in string 
  except ValueError:  
    return False


@client.event
async def on_ready():
    print("Bot hazir!\n")
    print("%s adiyla giris yapildi" % (client.user.name))
    await client.change_presence(game=discord.Game(name=yazi.bot_game["knack"]))

@client.event
async def on_server_join(server):
    client.start_private_message(server.owner)
    ownerName = server.owner.name 
    await client.send_message(server.owner, yazi.komut["join_sahip"] % (ownerName,server.member_count))


@client.event
async def on_message(message):

    if not message.author.bot == 1:
        
        #++========================== GENEL============================++#

        #!surum,!version,!versiyon
        if message.content.upper().startswith("!VERSION") or message.content.upper().startswith("!VERSIYON") or message.content.upper().startswith("!SÜRÜM") or message.content.upper().startswith("!SURUM"):
            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name + " Versiyonu", icon_url=client.user.avatar_url)
            embed.add_field(name="Version : ", value=version, inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, "**%s**" % (version))


        #!gelistirici,!developer
        if message.content.upper().startswith("!DEV") or message.content.upper().startswith("!GELISTIRICI") or message.content.startswith("!geliştirici"):
            userID = message.author.id
            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name + " Geliştirici", icon_url=client.user.avatar_url)
            embed.add_field(name='------------------------------------------------------------------------------', value="Merhaba <@%s>, <@%s> tarafından geliştiriliyorum!" % (userID,myID), inline=False)
            embed.add_field(name="GitHub", value = "https://github.com/humanova", inline=False)
            embed.add_field(name="Steam", value = "http://steamcommunity.com/id/humanovan", inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, yazi.komut["gelistirici"] % (userID,myID))


        #!help,!yardim
        if message.content.upper().startswith("!HELP") or message.content.upper().startswith("!YARDIM") or message.content.startswith("!yardim"):
            #embed=discord.Embed(title=" ", color=0xce6c6f)
            #embed.set_author(name=client.user.name + " Yardım", icon_url=client.user.avatar_url)
            #embed.add_field(name="", value=yazi.komut["yardim"], inline=False)
            #await client.send_message(message.channel,embed=embed)
            await client.send_message(message.channel, yazi.komut["yardim"])
            

        #!statu,!stats
        if message.content.upper().startswith("!STATS") or message.content.upper().startswith("!STATÜ") or message.content.upper().startswith("!STATU"):
            servers = serverSayisi()
            users = kullaniciSayisi()
            channels = channelSayisi()
            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name + " Istatistikleri", icon_url=client.user.avatar_url)
            embed.add_field(name="Server Sayısı : ", value=servers, inline=False)
            embed.add_field(name="Kullanıcı Sayısı :" , value=users, inline=False)
            embed.add_field(name="Kanal Sayısı :" , value=channels, inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, yazi.komut["statu"] % (servers,users,channels))


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
        

        #!davet,invite
        if message.content.upper().startswith("!DAVET") or message.content.upper().startswith("!INVITE"):
            msg = message.content.split(" ")
            kul_sayisi = 1
            if len(msg)>1:
                if msg[1].isdigit():
                    kul_sayisi = int(msg[1])

            try:
                davet = await client.create_invite(message.channel,max_uses=kul_sayisi)
            except discord.errors.NotFound:
                await client.send_message(message.channel,"Yetkim yok!")

            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=message.channel.name + " Kanal Daveti", icon_url=client.user.avatar_url)
            embed.add_field(name="%d kullanımlık davet linki : " % (kul_sayisi), value=davet.url, inline=False)
            await client.send_message(message.channel,embed=embed)


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

        #!cevir , ffff99
        if message.content.upper().startswith("!CEVIR"):
            raw_msg = message.content.split(" ")
            if raw_msg[1]:
                raw_msg = raw_msg[1:len(raw_msg)]
                son_msg = ""

                
                if raw_msg[0].startswith("-") and raw_msg[1].startswith("-"):
                    currDil = raw_msg[0].replace("-","")
                    hedefDil = raw_msg[1].replace("-","")
                    
                    
                    msg = raw_msg[2:len(raw_msg)]

                elif raw_msg[0].startswith("-") and raw_msg[1].startswith("-") == 0:
                    currDil = "auto"
                    hedefDil = raw_msg[0].replace("-","")
                    
                    msg = raw_msg[1:len(raw_msg)]
                    
                else :
                    msg = raw_msg
                    currDil = "auto"
                    hedefDil = "tr"
                    
                son_msg = " ".join(msg)
                metin,currDil,hedefDil,oran = ceviri.Cevir(currDil,hedefDil,son_msg)
                
                embed=discord.Embed(title=" ", color=0x75df00)
                embed.set_author(name="Google Çeviri", icon_url=client.user.avatar_url)
                embed.add_field(name="["+currDil+" -> "+hedefDil+"]", value=metin, inline=False)
                embed.set_footer(text=oran)
                await client.send_message(message.channel,embed=embed)

        #!oyla,!vote
        if message.content.upper().startswith("!VOTE") or message.content.upper().startswith("!OYLA"):
            userID = message.author.id
            msg = message.content.split(" ")
            if msg[1]:
                msg = await client.send_message(message.channel, yazi.komut["oyla"] % (userID," ".join(msg[1:])))
                await client.add_reaction(msg,'👍')
                await client.add_reaction(msg,'👎')
            

        #!google,!ara 
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


        #!lmgtfy
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

        
        #!hava
        if message.content.upper().startswith("!HAVA"):
            msg = message.content.split(" ")
            if msg[1]:
                sehir,durum = hava.havaParse(msg[1])
                yer,sicaklik,nem_orani,ruzgar_hizi,gun_dogumu,gun_batimi,durum_ikon_url = hava.havaParseOWM(msg[1])

                if not sehir == "hata":
                    embed=discord.Embed(title=" ", color=0x00ffff)
                    #embed.set_author(name="Hava Durumu", icon_url=client.user.avatar_url)
                    embed.set_thumbnail(url=durum_ikon_url)
                    embed.add_field(name=":earth_africa: Yer", value=yer, inline=True)
                    embed.add_field(name=":thermometer: Sıcaklık" , value=str(sicaklik) + "°C", inline=True)
                    embed.add_field(name=":droplet: Nem" , value=str(nem_orani)+"%", inline=True)
                    embed.add_field(name=":dash: Rüzgar Hızı" , value=str(ruzgar_hizi)+" m/s", inline=True)
                    embed.add_field(name=":sunrise: Gün Doğumu" , value=gun_dogumu, inline=True)
                    embed.add_field(name=":city_sunset: Gün Batımı" , value=gun_batimi, inline=True)
                    embed.add_field(name="Durum :" , value=durum, inline=False)
                    embed.set_footer(text="🔆 Kaynak : openweathermap.org ve mgm.gov.tr")
                    #print(sehir + tarih + durum + maks + minn + peryot)
                    await client.send_message(message.channel,embed=embed)
        

        #!bitcoin,!btc
        if message.content.upper().startswith("!BITCOIN") or message.content.upper().startswith("!BTC"):
            a,btc_tl = doviz.DovizParse("BTC-TRY",1)
            a,btc_usd = doviz.DovizParse("BTC-USD",1)
            
            embed=discord.Embed(title=" ", color=0x2079ff)
            embed.set_author(name="Bitcoin Kuru", icon_url=client.user.avatar_url)
            embed.add_field(name="1 BTC" + "/USD", value=btc_usd, inline=True)
            embed.add_field(name="1 BTC" + "/TL" , value=btc_tl, inline=True)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, yazi.komut["bitcoin"] % (btc_usd,btc_tl))
        
        #!kripto
        if message.content.upper().startswith("!KRIPTO") or message.content.upper().startswith("!CRYPTO"):
            msg = message.content.split(" ")
            if msg[1]:
                
                if msg[1].upper().startswith("FETOCU") or msg[1].upper().startswith("FETÖCÜ"):
                    await client.send_message(message.channel,"https://media.giphy.com/media/RYjnzPS8u0jAs/giphy.gif")

                try:
                    if msg[2]:
                        if not msg[2] == "0":
                            if is_float(msg[2]):
                                adet = float(msg[2])

                            elif msg[2].isnumeric():
                                adet = msg[2]
                            
                            else:
                                adet = 1
                        else:
                            adet = 1
                except:
                    adet = 1

                kur = msg[1]
                kurUSD,deger_USD,kur_degisim,grafik_link = doviz.KriptoParse(kur,"usd",adet)
                a,dolar_degeri = doviz.DovizParse("USD",1)
                kurTL,deger_TL = kurUSD,(float(deger_USD) * float(dolar_degeri))

                deger_USD = round(float(deger_USD) * float(adet),2)
                deger_TL = round(float(deger_TL) * float(adet),2)
                kur_degisim = round(float(kur_degisim),2)


                if not kurUSD == "hata":
                    embed=discord.Embed(title=" ", color=0x2079ff)
                    embed.set_author(name="Kripto Kurları [" + kur.upper() +"]", icon_url=client.user.avatar_url)
                    embed.add_field(name=str(adet) + " " + kurUSD + "/USD", value= str(deger_USD), inline=True)
                    embed.add_field(name=str(adet) + " " + kurTL + "/TL" , value=str(deger_TL), inline=True)

                    if not str(kur_degisim).startswith("-"):
                        embed.add_field(name="Günlük Değişim",value=":arrow_up_small: " + str(kur_degisim) + "%", inline=True)
                    else:
                        embed.add_field(name="Günlük Değişim",value=":arrow_down_small: " + str(kur_degisim) + "%", inline=True)

                    embed.add_field(name="Son 7 günlük grafik", value=yazi.komut["kripto-cizgi"], inline=True)
                    embed.set_image(url=grafik_link)
                    embed.set_footer(text="💎 Kaynak : coinmarketcap.com")
                    await client.send_message(message.channel,embed=embed)
                    #await client.send_message(message.channel, yazi.komut["kripto"] % (kurUSD,deger_USD,kurTL,deger_TL))
           
        #!doviz kur
        if message.content.upper().startswith("!DÖVIZ") or message.content.upper().startswith("!DOVIZ"):
            msg = message.content.split(" ")
            if msg[1]:
                kur = msg[1]

                try:
                    if msg[2]:
                        if not msg[2] == "0":
                            if is_float(msg[2]):
                                adet = float(msg[2])

                            elif msg[2].isnumeric():
                                adet = msg[2]
                            
                            else:
                                adet = 1
                        else:
                            adet = 1
                except:
                    adet = 1

                kur,kur_degeri = doviz.DovizParse(kur,adet)
                if not kur == "hata":
                    embed=discord.Embed(title=" ", color=0x2b80ff)
                    embed.set_author(name="Döviz Kurları", icon_url=client.user.avatar_url)
                    embed.add_field(name=str(adet) + " " + kur + "/TL", value=kur_degeri, inline=True)
                    embed.set_footer(text="💰 Kaynak : xe.com")
                    await client.send_message(message.channel,embed=embed)
                    # await client.send_message(message.channel, yazi.komut["doviz"] % (kur,kur_degeri))
        

        #!roller,!roles
        if message.content.upper().startswith("!ROLLER") or message.content.upper().startswith("!ROLES"):
            currServer = message.server.name
            roles = message.server.role_hierarchy
            roller = ""
            for role in roles:
                roller += role.name + "\n"
            
            embed=discord.Embed(title=" ", color=0x001a40)
            embed.set_author(name=currServer + " Rolleri", icon_url=client.user.avatar_url)
            embed.add_field(name="Roller", value="```"+roller+"```", inline=True)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, yazi.komut["roller"] % (currServer,roller))
            
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
                tarih = zaman.tamTarih() + " (UTC+3)"
                
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
            serverMemCount = str(message.server.member_count)
            serverRegion = str(message.server.region)
            serverDate = str(message.server.created_at)
            serverKanal = 0
            serverRol = 0
            
            for i in message.server.channels:
                serverKanal += 1

            for i in message.server.roles:
                serverRol +=1

            embed=discord.Embed(title=" ", color=0xff6600)
            embed.set_author(name="Server Bilgileri", icon_url=client.user.avatar_url)
            embed.add_field(name="Server Adı :", value=serverName + "  (ID : " + serverID +")", inline=False)
            embed.add_field(name="Server Sahibi :", value=serverOwner+"(" + str(serverOwnerN) + ")", inline=False)
            embed.add_field(name="Kullanıcı Sayısı :", value=serverMemCount, inline=False)
            embed.add_field(name="Kanal Sayısı : ",value=serverKanal, inline=False)
            embed.add_field(name="Rol Sayısı : ",value=serverRol, inline=False)
            embed.add_field(name="Server Bölgesi :", value=serverRegion, inline=False)
            embed.add_field(name="Server Yaratılma Tarihi(UTC) : ", value=serverDate, inline=False)
            await client.send_message(message.channel,embed=embed)

            #await client.send_message(message.channel, yazi.komut["server1"] % (serverName,serverID,serverOwner,serverOwnerN,serverMemCount,serverRegion,serverDate))
            
        if message.content.upper().startswith("!SRVRS"):
            if message.author.id == myID:
                liste = ""
                server_listesi = list(client.servers)

                for a in range(len(server_listesi)):
                    liste += server_listesi[a-1].name + "\n"

                embed=discord.Embed(title=" ", color=0x75df00)
                embed.set_author(name="Aktif Serverlar", icon_url=client.user.avatar_url)
                embed.add_field(name="Liste", value=server_listesi, inline=False)
            else:
                await client.send_message(message.channel,"Buna yetkin yok.")

        #++========================== EGLENCE ============================++#


        #!leet,!l33t
        if message.content.upper().startswith("!LEET") or message.content.upper().startswith("!L33T"):
            msg = message.content
            if msg[6]:
                msg = msg[6:]
                msg = msg.replace('e','3')
                msg = msg.replace('a','4')
                msg = msg.replace('i','1')
                msg = msg.replace('ı','1')
                msg = msg.replace('s','5')
                msg = msg.replace('o','0')
                    
                await client.send_message(message.channel,msg)

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
            if gelen % 2 == 0:
                await client.send_message(message.channel, yazi.komut["firlatTura"])


        #herkesi etiketleyenlere kizgin
        if message.mention_everyone:
            await client.add_reaction(message,"😡")


        #++========================== OZEL ============================++#
        
        #oyun degisme
        if message.content.upper().startswith("!OYUN"):
            if message.author.id == myID:
                msg = message.content.split(" ")

                try:
                    if msg[1]:
                        try:
                            await client.change_presence(game=discord.Game(name=yazi.bot_game[msg[1]]))
                        except:
                            await client.send_message(message.channel,"Hata olustu")
                            return 
                except:
                    return

            else:
                await client.send_mesage(message.channel, "Yetkin yok!")

        
        #buglubot
        if "buglubot" in message.content:
            op = random.randint(1,4)

            if op == 1:
                await client.send_message(message.channel, yazi.komut["bot1"])
            if op == 2:
                await client.send_message(message.channel, yazi.komut["bot2"])
            if op == 3:
                await client.send_message(message.channel, yazi.komut["bot3"])
            if op == 4:
                await client.send_message(message.channel, yazi.komut["bot4"])

        #dead server - ded server (MESAJI EKLE)
        if "DEAD SERVER" in message.content.upper() or "DED SERVER" in message.content.upper() or "DEADSERVER" in message.content.upper():
            await client.send_message(message.channel, yazi.komut["deadserver"])

        #omurcek
        if message.content.upper().startswith("OMURCEK") or message.content.upper().startswith("ÖMÜRCEK"):
            await client.send_message(message.channel, yazi.komut["omurcek"])
        
        #send nudes
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
            if op == 4:
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



