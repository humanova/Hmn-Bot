﻿
# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#	NOTLAR

#  Fikir sunanlar ve gelistirirken emegi gecenler :
#  112'nin Yaz Turnuvasi Sunucusu, 112servis, barisuraz, selindesu ve digerleri!

import asyncio
import os
import random
import re
import sys
import threading
import time
from datetime import datetime
import json
import io
import codecs

#import env_set
#env_set.setEnv()

import aiohttp
import botEval as hmnEval
import botStrings as yazi
import ceviri
import copypasta

import database as db
# discordbotlist.org api bot istatistikleri icin
import dbl  
import discord
import dovizIslem as doviz
import havaDurumu as hava
import meme
import memeRenderer as mrender
import music
import ohiapi
import zaman
import faceDet

from discord.ext import commands
from discord.ext.commands import Bot

################################

token = os.environ['PP_BOT_TOKEN']
dbl_token = os.environ['DBL_TOKEN']


b_database = db.DB()
Client = discord.Client()
client = commands.Bot(command_prefix = "!")

version = "hmnBot v0.4.6\n10/08/19"

myID = "213262071050141696"
barisID = "608001852700622855"
botID = "455819835486502933"

logChannelID = "470853011233570817"
hideoutID = "405492399595323393"
USDLogID = "572432834581626902"

######

# ======================== LOGLAMA ========================= #

log_num = 0
temel_log = "\n[TEMEL]\n"
komut_log = "\n[KOMUT LOGLARI]\n```"

def logUsersToText():

    file = codecs.open("../log/users.txt", "w+", "utf-8")
    servers = client.servers

    for srvr in servers:
        print(f"Logging server : {srvr.name}")
        file.write(f"## {srvr.name} -- {srvr.member_count} users\n")
        for mem in srvr.members:
            file.write(f"{mem.name}#{mem.discriminator}\n")
    file.close()

async def checkServer(message, server_flag):
    global komut_log
    if not message.server == None: 
        komut_log += "[" + getUserName(message.author) + "] @" + message.server.name + "            " + message.content + "\n"
        return False
    elif message.server == None and server_flag == True:
        await client.send_message(message.channel, "Bu komut sadece bir sunucuda kullanılabilir.")
        komut_log += "[SERVER COMMAND][" + getUserName(message.author) + "] @DM            " + message.content + "\n"
        return True
    else: 
        komut_log += "[" + getUserName(message.author) + "] @DM            " + message.content + "\n"
        return False

def temelLog():
    global temel_log
    temel_log += "Online Server Sayisi : " + str(serverSayisi()) + "\n"
    temel_log += "Online Kullanici Sayisi : " + str(kullaniciSayisi()) + "\n"
    temel_log += "Online Kanal Sayisi : " + str(channelSayisi()) + "\n"

    
def onlineServer():
    servers = list(client.servers)
    
    temp_liste = ""

    for i in range(len(servers)):
        temp_liste += servers[i-1].name + "\n"

    return temp_liste

def logUSDEmbed():
    res = doviz.DovizParse("USD")
    kur = "USD"
    kur_degeri = res['kur_buy']
    embed=discord.Embed(title=" ", color=0x2b80ff)
    embed.set_author(name="Saatlik USD/TL", icon_url=client.user.avatar_url)
    embed.add_field(name="Kur", value=kur_degeri, inline=True)
    embed.add_field(name="Günlük Değişim", value=f"{res['kur_change']} (%{res['kur_change_percentage']})", inline=True)
    embed.set_footer(text=f"💰 Kaynak : canlidoviz.com | {res['kur_time']}")
    return embed

async def bot_logla():

    while not client.is_closed:

        dblpy = dbl.Client(client, dbl_token)

        temelLog()
        
        global log_num
        global temel_log
        global komut_log

        log_num += 1
        
        tarih = str(datetime.now())
        log_baslangic = "\nLOG[" + str(log_num) + "] : " + tarih + "\n"
        if not len(komut_log) == 20:
            log_son = str(log_baslangic) + str(temel_log) + str(komut_log)
        else:
            log_son = str(log_baslangic) + str(temel_log)
        
        if len(log_son) > 2000:
            a = 0
            string = log_son
            for chunk in [string[i:i+1982] for i in range(0, len(string), 1982)]:
                if a == 0 : await client.send_message(discord.Object(id=logChannelID), chunk + "```")
                else : await client.send_message(discord.Object(id=logChannelID), "```" + chunk + "```")
                a += 1
                
        else:
            if not len(komut_log) == 20:
                await client.send_message(discord.Object(id=logChannelID), log_son + "```")
            else:
                await client.send_message(discord.Object(id=logChannelID), log_son)
        
        #discordbotlist.org istatistikleri gonder
        try:
            await dblpy.post_server_count()
            print('server sayisi gonderildi : ({})'.format(len(client.servers)))
        except Exception as e:
            print('server sayisi gonderilirken hata olustu : \n{}: {}'.format(type(e).__name__, e))
        
        if zaman.IsWeekDay():
            embed = logUSDEmbed()
            await client.send_message(discord.Object(id=USDLogID), embed=embed)
        
        temel_log = "\n[TEMEL]\n"
        komut_log = "\n[KOMUT LOGLARI]\n```"

        await asyncio.sleep(3600) 


def serverSayisi():

    servers = list(client.servers)
    return len(servers)

def channelSayisi():

    i = 0
    for server in client.servers:
        for channel in server.channels:
            i += 1
            
    return i

def kullaniciSayisi():

    i = 0
    for server in client.servers:
        for member in server.members:
            i = i + 1     
    return i

def getUserName(user):
    return str(user.name) + "#" + str(user.discriminator)

# ===================== LOGLAMA BITIS ====================== #


def is_float(string):
  try:
    return float(string) and '.' in string 
  except ValueError:  
    return False


@client.event
async def on_ready():
    b_database.Connect()
    if b_database.is_connected:
        try:
            b_database.InitDatabase()
        except:
            print("Error while initializing the database, it may be initialized already...")

    print("Bot hazir!\n")
    print("%s adiyla giris yapildi" % (client.user.name))
    logUsersToText()
    await bot_logla()

@client.event
async def on_server_join(server):
    client.start_private_message(server.owner)
    ownerName = server.owner.name 
    await client.send_message(server.owner, yazi.komut["join_sahip"] % (ownerName,server.member_count))


@client.event
async def on_message(message):
    global komut_log
    if not message.author.bot == 1:
    
        #++========================== GENEL============================++#

        #!surum,!version,!versiyon
        if message.content.upper() == "!VERSION"  or message.content.upper() == "!VERSIYON"  or message.content.upper() == "!SÜRÜM" or message.content.upper() == "!SURUM":
            await checkServer(message, False)

            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name + " Versiyonu", icon_url=client.user.avatar_url)
            embed.add_field(name="Version : ", value=version, inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, "**%s**" % (version))


        #!gelistirici,!developer
        if message.content.upper() == "!DEV" or message.content.upper() == "!GELISTIRICI" or message.content == "!geliştirici":
            await checkServer(message, False)

            userID = message.author.id
            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
            embed.add_field(name="Geliştirici", value=f"<@{myID}>", inline=False)
            embed.add_field(name="GitHub", value = "https://github.com/humanova", inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, yazi.komut["gelistirici"] % (userID,myID))

        #!help,!yardim
        if message.content.upper().startswith("!HELP") or message.content.upper().startswith("!YARDIM") or message.content.startswith("!yardim"):
            await checkServer(message, False)

            msg = message.content.split(" ")

            if len(msg) == 2:
                komut = msg[1]
                try:
                    await client.send_message(message.channel, yazi.komutYardim[komut])
                except:
                    pass
            else:
                await client.send_message(message.channel, yazi.komut["yardim"])
            

        #!stats
        if message.content.upper() == "!STATS":
            await checkServer(message, False)

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

        
        #!destek
        if message.content.upper() == "!DESTEK":
            await checkServer(message, False)

            embed=discord.Embed(title=" ",description="**[Davet](https://discord.gg/XBebmFF)**", color=0x75df00)
            embed.set_author(name="Hmn-Bot Destek", icon_url=client.user.avatar_url)
            await client.send_message(message.channel,embed=embed)
        
        #!temizle
        if message.content.upper().startswith("!TEMIZLE"):

            server_flag = await checkServer(message, True)

            if not server_flag:

                if message.author.server_permissions.manage_messages:
                    flag = True
                    botYetki = "var"
                    msg = message.content.split(" ")

                    try:
                        if msg[1].isdigit():
                            msg_sayisi = msg[1]
                            
                        else:
                            flag = False
                            pass

                    except:
                        flag = False
                        pass
                    
                    if not flag == False:
                        msg_sayisi = int(msg_sayisi) 

                        if msg_sayisi > 0 and msg_sayisi < 100:
                            mgs = []
                            
                            async for x in client.logs_from(message.channel, limit = msg_sayisi + 1):
                                mgs.append(x)
                            
                            try:
                                await client.delete_messages(mgs)
                            except:
                                await client.send_message(message.channel,"Buna yetkim yok")
                                botYetki = "yok"

                            if not botYetki == "yok":
                                embed=discord.Embed(title=" " , color=0x75df00)
                                embed.set_author(name="Temizlik",icon_url=client.user.avatar_url)
                                embed.add_field(name="Tamamlandı", value=str(msg_sayisi) + " mesaj silindi", inline=False)
                                await client.send_message(message.channel, embed=embed)

                        else :
                            await client.send_message(message.channel,"Aynı anda 1 - 99 arasında mesaj silebilirim.")

                    else:
                        embed=discord.Embed(title=" ",description = yazi.komut["temizlikHata"], color=0xFF0000)
                        embed.set_author(name="Hmn-Bot Yardım", icon_url=client.user.avatar_url)
                        await client.send_message(message.channel,embed=embed)
                
                else:
                    await client.send_message(message.channel,"Buna yetkiniz yok!")

        #!davet,invite
        if message.content.upper() == "!DAVET" or message.content.upper() == "!INVITE":
            
            server_flag = await checkServer(message, True)

            if not server_flag:    

                msg = message.content.split(" ")
                kul_sayisi = 1
                if len(msg)>1:
                    if msg[1].isdigit():
                        kul_sayisi = int(msg[1])

                try:
                    davet = await client.create_invite(message.channel,max_uses=kul_sayisi)
                except:
                    await client.send_message(message.channel,"Yetkim yok!")

                embed=discord.Embed(title=" ", color=0x75df00)
                embed.set_author(name=message.channel.name + " Kanal Daveti", icon_url=client.user.avatar_url)
                embed.add_field(name="%d kullanımlık davet linki : " % (kul_sayisi), value=davet.url, inline=False)
                await client.send_message(message.channel,embed=embed)


        #!say
        if message.content.upper().startswith("!SAY"):
            
            server_flag = await checkServer(message, False)
           
            if message.author.id == myID:
                args = message.content.split(" ")
                try:
                    if args[1]:
                        try:
                            await client.delete_message(message)
                        except discord.errors.NotFound:
                            pass
                        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))
                except:
                    pass
                        
            else:
                await client.send_message(message.channel,"**Buna yetkin yok!**")

        
        #!cevir 
        if message.content.upper().startswith("!CEVIR") or message.content.upper().startswith("!ÇEVIR"):
            
            server_flag = await checkServer(message, True)

            if not server_flag:   

                raw_msg = message.content.split(" ")
                try:
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

                except:
                    pass
        

        #!oyla,!vote
        if message.content.upper().startswith("!VOTE") or message.content.upper().startswith("!OYLA"):
            
            server_flag = await checkServer(message, True)

            if not server_flag:   

                userID = message.author.id
                msg = message.content.split(" ")

                try:
                    if msg[1]:
                        msg = await client.send_message(message.channel, yazi.komut["oyla"] % (userID," ".join(msg[1:])))
                        await client.add_reaction(msg,'👍')
                        await client.add_reaction(msg,'👎')
                except:
                    pass
                
                
        #!google,!ara 
        if message.content.upper().startswith("!GOOGLE") or message.content.upper().startswith("!ARA"):
            
            server_flag = await checkServer(message, True)
          
            searchQ = "https://google.com/search?q="
            if not '@everyone' in message.content:
                if not '@here' in message.content:
                    msg = message.content.split(" ")

                    try:
                        if msg[1]:
                            for word in range(1,len(msg)):
                                if not word == len(msg) - 1:
                                    searchQ += msg[word] + "+"
                                else:
                                    searchQ += msg[word]

                            await client.send_message(message.channel, "%s" % (searchQ))
                    except:
                        pass

        #!lmgtfy
        if message.content.upper().startswith("!LMGTFY"):
            
            server_flag = await checkServer(message, True)
           
            searchQ = "http://lmgtfy.com/?q="
            msg = message.content.split(" ")

            try:
                if msg[1]:
                    for word in range(1,len(msg)):
                        if not word == len(msg) - 1:
                            searchQ += msg[word] + "+"
                        else:
                            searchQ += msg[word]

                    await client.send_message(message.channel, "%s" % (searchQ))
            except: pass
        
        #!hava
        if message.content.upper().startswith("!HAVA"):
            
            server_flag = await checkServer(message, True)

            if not server_flag:   

                msg = message.content.split(" ")

                try:
                    if msg[1]:
                        sehir,durum = hava.havaParse(" ".join(msg[1:]))
                        yer,sicaklik,nem_orani,ruzgar_hizi,gun_dogumu,gun_batimi,durum_ikon_url = hava.havaParseOWM(" ".join(msg[1:]))

                        if not yer == "hata":
                            embed=discord.Embed(title=" ", color=0x00ffff)
                            #embed.set_author(name="Hava Durumu", icon_url=client.user.avatar_url)
                            embed.set_thumbnail(url=durum_ikon_url)
                            embed.add_field(name=":earth_africa: Yer", value=yer, inline=True)
                            embed.add_field(name=":thermometer: Sıcaklık" , value=str(sicaklik) + "°C", inline=True)
                            embed.add_field(name=":droplet: Nem" , value=str(nem_orani)+"%", inline=True)
                            embed.add_field(name=":dash: Rüzgar Hızı" , value=str(ruzgar_hizi)+" m/s", inline=True)
                            embed.add_field(name=":sunrise: Gün Doğumu" , value=gun_dogumu + " (utc+3)", inline=True)
                            embed.add_field(name=":city_sunset: Gün Batımı" , value=gun_batimi + " (utc+3)", inline=True)

                        if not sehir == "hata":
                            embed.add_field(name="Durum :" , value=durum, inline=False)

                        embed.set_footer(text="🔆 Kaynak : openweathermap.org ve mgm.gov.tr")
                        #print(sehir + tarih + durum + maks + minn + peryot)
                        await client.send_message(message.channel,embed=embed)

                except:
                    pass

        #!bitcoin,!btc
        if message.content.upper() == "!BITCOIN" or message.content.upper() == "!BTC":
            
            server_flag = await checkServer(message, True)

            if not server_flag:               
                res = doviz.DovizParse("BTC")
                
                embed=discord.Embed(title=" ", color=0xf7931a)
                embed.set_author(name="Bitcoin Kuru", icon_url=client.user.avatar_url)
                embed.add_field(name="1 BTC" + "/USD", value=res['kur_buy_usd'], inline=True)
                embed.add_field(name="1 BTC" + "/TL" , value=res['kur_buy_tl'], inline=True)
                embed.set_footer(text="💎 Kaynak : coindesk.com")
                await client.send_message(message.channel,embed=embed)
            
        #!kripto
        if message.content.upper().startswith("!KRIPTO") or message.content.upper().startswith("!CRYPTO"):
            
            server_flag = await checkServer(message, True)
            if not server_flag:               
                msg = message.content.split(" ")
                kur = None
                adet = None
                if len(msg) == 2:
                    kur = msg[1]
                    adet = 1
                elif len(msg) == 3:
                    kur = msg[1]
                    if not msg[2] == "0":
                        if is_float(msg[2]):
                            adet = float(msg[2])
                        elif msg[2].isnumeric():
                            adet = int(msg[2])
                        else:
                            adet = 1
                    else:
                        adet = 1
                else: 
                    pass
                res = doviz.KriptoParse(kur,"usd",adet)
                if not res == None:
                    kurUSD = res[0]
                    deger_USD = res[1]
                    kur_degisim = res[2]
                    grafik_link = res[3]

                    res = doviz.DovizParse("USD")
                    kurTL,deger_TL = kurUSD,(float(deger_USD) * float(res['kur_buy']))

                    deger_USD = round(float(deger_USD) * float(adet),2)
                    deger_TL = round(float(deger_TL) * float(adet),2)
                    kur_degisim = round(float(kur_degisim),2)


                    if not kurUSD == None:
                        embed=discord.Embed(title=" ", color=0xf7931a)
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


        #!doviz kur
        if message.content.upper().startswith("!DÖVIZ") or message.content.upper().startswith("!DOVIZ"):
            
            server_flag = await checkServer(message, True)

            if not server_flag:          
                msg = message.content.split(" ")
                kur = None
                adet = None
                if len(msg) == 2:
                    kur = msg[1]
                    adet = 1
                elif len(msg) == 3:
                    kur = msg[1]
                    if not msg[2] == "0":
                        if is_float(msg[2]):
                            adet = float(msg[2])
                        elif msg[2].isnumeric():
                            adet = int(msg[2])
                        else:
                            adet = 1
                    else:
                        adet = 1
                else: 
                    pass

                res = doviz.DovizParse(kur, adet)    
                if not res == None:
                    embed=discord.Embed(title=" ", color= doviz.getEmbedColor(res['kur_adi']))
                    embed.set_author(name="Döviz Kurları", icon_url=client.user.avatar_url)
                    embed.set_footer(text=f"💰 Kaynak : canlidoviz.com | {res['kur_time']}")

                    if not res['kur_adi'] == "ALTIN":
                        embed.add_field(name=f"{str(adet)} {res['kur_adi']}/TL", value=res['kur_buy'], inline=True)

                    if res['kur_adi'] == "AYLIK SUPPORTER":
                        embed.add_field(name="Indirimli", value=f"~{res['discount']}", inline=False)

                    elif res['kur_adi'] == "ALTIN":
                        for i in range(len(res) - 2):
                            altin_adi = list(res)[i+2]
                            altin_degeri = res[list(res)[i+2]]
                            embed.add_field(name=altin_adi, value=f"{altin_degeri}", inline=False)

                    if res['kur_adi'] == "AYLIK NITRO" or res['kur_adi'] == "AYLIK SUPPORTER" or res['kur_adi'] =="ALTIN":
                        await client.send_message(message.channel, embed=embed)

                    else:
                        embed.add_field(name="Günlük Değişim", value=f"{res['kur_change']} (%{res['kur_change_percentage']})", inline=True)
                        await client.send_message(message.channel, embed=embed)
                    

        #!xdoviz
        if message.content.upper().startswith("!XDÖVIZ") or message.content.upper().startswith("!XDOVIZ"):
            
            server_flag = await checkServer(message, True)
            
            if not server_flag:          
                msg = message.content.split(" ")
                kur = None
                if len(msg) == 2:
                    kur = msg[1]
                else:
                    pass
                res = doviz.DovizParse(kur, is_detailed =True)
                if not res == None:
                    await client.send_message(message.channel, f"```json\n{json.dumps(res, indent = 4)}```")

        #!oyun
        if message.content.upper().startswith("!OYUN "):

            server_flag = await checkServer(message, True)

            if not server_flag: 

                server = message.server
                members = server.members
                oyuncu_sayisi = 0

                msg = message.content.split(" ")
                oyun = " ".join(msg[1:])
                oyuncuListe = "```asciidoc\n== Kim '" + oyun +"' oynuyor ==\n\n"

                embed=discord.Embed(title=" ", color=0x001a40)
                embed.set_author(name="Kim Oynuyor", icon_url=client.user.avatar_url)

                if len(oyun) < 4:
                    embed=discord.Embed(title=" ",description = yazi.komut["oyunHata"], color=0xFF0000)
                    await client.send_message(message.channel,embed=embed)
            
                else:
                    for member in members:
                        if not member.game == None:
                            if oyun.upper() in str(member.game).upper() or oyun.upper() == str(member.game).upper():
                                oyuncuListe += " + " + member.name + "#" + str(member.discriminator) + "  - " + str(member.game) + "\n"
                                oyuncu_sayisi += 1

                    oyuncuListe += "```"
                    
                    if oyuncu_sayisi > 0:
                        embed.add_field(name="Oyun",value=oyun, inline=False)
                        embed.add_field(name="Oyuncu Sayısı : ",value=str(oyuncu_sayisi), inline=False)
                        await client.send_message(message.channel,embed=embed)
                        await client.send_message(message.channel,oyuncuListe)
                    else:
                        embed=discord.Embed(title=" ",description = yazi.komut["oyunHata2"] % ("'" + oyun + "'"), color=0xFF0000)
                        await client.send_message(message.channel,embed=embed)


        #!roller,!roles
        if message.content.upper() == "!ROLLER" or message.content.upper() == "!ROLES":
            
            server_flag = await checkServer(message, True)

            if not server_flag: 

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
            
            server_flag = await checkServer(message, True)

            if not server_flag:             
                sikayet = message.content.split(" ")

                try:
                    if sikayet[1]:
                        owner = message.server.owner
                        sikayetci = getUserName(message.author)
                        sikayetci_nick = message.author.display_name
                        serverAdi = message.server.name
                        kanalAdi = message.channel.name
                        tarih = zaman.GetTime() + " (UTC+3)"
                        
                        try:
                            client.start_private_message(owner)
                            await client.send_message(owner, yazi.komut['sikayet_admin'] % (tarih,serverAdi,kanalAdi,sikayetci,sikayetci_nick," ".join(sikayet[1:])))
                            await client.send_message(message.channel, yazi.komut['sikayet_kullanici'])
                            try:
                                await client.delete_message(message)
                            except discord.errors.NotFound: pass

                        except discord.errors.NotFound:
                            await client.send_message(message.channel, yazi.komut['sikayet_hata'])
                
                except:
                    pass


        #!server,!serverstats
        if message.content.upper() == "!SERVER":
            
            server_flag = await checkServer(message, True)

            if not server_flag: 
                serverName = message.server.name
                serverID = message.server.id
                serverIconURL = message.server.icon_url
                serverOwner = message.server.owner.name + "#" + str(message.server.owner.discriminator)
                serverOwnerN = message.server.owner.nick
                serverMemCount = str(message.server.member_count)
                serverRegion = str(message.server.region)
                serverDate = str(message.server.created_at)[:-10]
                serverKanal = 0
                serverRol = 0
                
                for i in message.server.channels:
                    serverKanal += 1

                for i in message.server.roles:
                    serverRol +=1

                embed=discord.Embed(title=" ", color=0xff6600)
                embed.set_thumbnail(url=serverIconURL)
                embed.set_author(name=serverName, url=serverIconURL)
                embed.add_field(name="Sahibi :", value=serverOwner+"(" + str(serverOwnerN) + ")", inline=True)
                embed.add_field(name="Server Bölgesi :", value=serverRegion, inline=True)
                embed.add_field(name="Kullanıcı :", value=serverMemCount, inline=True)
                embed.add_field(name="Kanal : ",value=serverKanal, inline=True)
                embed.add_field(name="Rol : ",value=serverRol, inline=True)
                embed.add_field(name="Yaratılma Tarihi(UTC) : ", value=serverDate, inline=True)
                embed.set_footer(text="Server ID : " + serverID)
                await client.send_message(message.channel,embed=embed)

                #await client.send_message(message.channel, yazi.komut["server1"] % (serverName,serverID,serverOwner,serverOwnerN,serverMemCount,serverRegion,serverDate))

        #++========================== EGLENCE ============================++#

        #!soz,!lyrics
        if message.content.upper().startswith("!SOZ") or message.content.upper().startswith("!SÖZ") or message.content.upper().startswith("!LYRICS"):
            
            await checkServer(message, False)
        
            ilk_msg = await client.send_message(message.channel, "Şarkı aranıyor...") 

            flag = True
            msg = message.content.split(" ")
            msg = " ".join(msg[1:])

            try:
                if msg[0:]:
                    sarki = msg[0:]
                    artist = ""
            except:
                flag = False

            if not flag == False:
                
                sozler,sarki_adi,sarki_artist,sarki_url = music.sozParse(artist,sarki)

                if not sozler == "hata":
                    kisa_ad = sarki_artist + " - " + sarki_adi + " Sözleri" 
                    soz_son = yazi.komut["lyrics"] % (kisa_ad,sozler)

                    string = soz_son
                
                    a = 0
                    try:
                        for chunk in [string[i:i+1982] for i in range(0, len(string), 1982)]:
                            
                            if a == 3:
                                await client.send_message(message.channel, "```asciidoc\n== Sözler 3 mesajı aştığı için kısaltıldı... ==\nTamamı için : " + sarki_url + "```")
                                break
                            elif a == 0:
                                await client.edit_message(ilk_msg,chunk + "```")
                            else:
                                await client.send_message(message.channel,"```asciidoc\n" + chunk + "```")
                            a += 1


                    except:
                        await client.edit_message(ilk_msg,soz_son)
                
                else:
                    await client.edit_message(ilk_msg,"`" + sarki +"` bulunamadı... :(")
                
                #embed=discord.Embed(title=" ", description=sarki_adi + " - " + sarki_artist, color=0x75df00)
                #embed.set_author(name="Hmn-Bot Lyrics", icon_url=client.user.avatar_url)
                #embed.add_field(name="Şarkı Sözleri ", value=sozler, inline=False)

        #!meme
        if message.content.upper().startswith("!MEME"):
            
            server_flag = await checkServer(message, True)

            if not server_flag:

                msg = message.content.split(" ")
                
                try:
                    subreddit = msg[1]
                except:
                    pass

                try:
                    is_top = msg[2]
                    if is_top == "top" : is_top = True
                    else: is_top = False
                except:
                    is_top = False

                memeURL,yazar,baslik,link,upvote = meme.memeParse(subreddit.lower(),is_top)

                if not memeURL == "hata":

                    embed=discord.Embed(title=" ",description = "**["+baslik+"]"+"("+link+")**", color=0xFF0000)
                    embed.set_author(name="r/" + subreddit, icon_url=yazi.komut["redditico"])
                    embed.set_footer(text= "👍 " + str(upvote) + " | Yaratıcı : u/" + yazar)
                    embed.set_image(url = memeURL)

                    await client.send_message(message.channel,embed=embed)
                
                else:
                    embed=discord.Embed(title=" ",description = yazi.komut["memeHata"], color=0xFF0000)
                    embed.set_author(name="Hmn-Bot Yardım", icon_url=yazi.komut["redditico"])
                    await client.send_message(message.channel,embed=embed)

        #!leet,!l33t
        if message.content.upper().startswith("!LEET") or message.content.upper().startswith("!L33T"):
            
            await checkServer(message, False)    
            msg = message.content

            try:
                if msg[6]:
                    msg = msg[6:]
                    msg = msg.replace('e','3')
                    msg = msg.replace('a','4')
                    msg = msg.replace('i','1')
                    msg = msg.replace('ı','1')
                    msg = msg.replace('s','5')
                    msg = msg.replace('o','0')
                        
                    await client.send_message(message.channel,msg)
            except: pass

        #!avatar
        if message.content.upper().startswith("!AVATAR"):
            
            await checkServer(message, False)
            
            try:
                user = message.mentions[0]
            except:
                try:
                    msg = message.content.split(" ")
                    user = message.server.get_member_named(msg[1])
                except:
                    user = None

            if not user == None:
                await client.send_message(message.channel, str(user.avatar_url))
            

        #!sence
        if message.content.upper().startswith("!SENCE"):
            
            server_flag = await checkServer(message, False)

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
        if message.content.upper() == "!FIRLAT" or message.content == "!fırlat" or message.content.upper() == "!FLIP":
            
            await checkServer(message, False)

            gelen = random.randint(1,100)
            if gelen % 2 == 1:
                await client.send_message(message.channel, yazi.komut["firlatYazi"])
            if gelen % 2 == 0:
                await client.send_message(message.channel, yazi.komut["firlatTura"])

        #!censor
        if message.content.upper().startswith("!CENSOR"):
            msg = message.content.split(" ")
            print(message.embeds)

            if len(msg) == 2:
                url = msg[1]
                threshold = 0.5

                success, blur_img, img_bytearr = faceDet.blurFaces(url, threshold, is_url=True)
                if success:
                    await client.send_file(message.channel, fp=img_bytearr, filename = "blurred_img.png")

            elif len(msg) == 3:
                url = msg[1]
                threshold = float(msg[2])

                success, blur_img, img_bytearr = faceDet.blurFaces(url, threshold, is_url=True)
                if success:
                    await client.send_file(message.channel, fp=img_bytearr, filename = "blurred_img.png")
        #!faces
        if message.content.upper().startswith("!FACES"):
            msg = message.content.split(" ")

            if len(msg) == 2:
                url = msg[1]
                threshold = 0.5

                faces, bboxes, img = faceDet.cropFaces(url, threshold, is_url=True)
                if len(faces) > 0:
                    for face in faces:
                        await client.send_file(message.channel, fp=face[1], filename = "face.png")

            if len(msg) == 3:
                url = msg[1]
                threshold = float(msg[2])

                faces, bboxes, img = faceDet.cropFaces(url, threshold, is_url=True)
                if len(faces) > 0:
                    for face in faces:
                        await client.send_file(message.channel, fp=face[1], filename = "face.png")
        #++========================== OZEL ============================++#
        #ohi-api
        if message.content.startswith('!ohiapi') and message.author.id == myID:
            msg = message.content.split(" ")
            response = ''
            if msg[1] == 'register':
                response = ohiapi.RegisterRequest(msg[2],msg[3],msg[4])
                await client.send_message(message.channel, f'```{response}```')
            
            elif msg[1] == 'login':
                response = ohiapi.LoginRequest(msg[2],msg[3])
                await client.send_message(message.channel, f'```{response}```')

            elif msg[1] == 'xusers':
                response = ohiapi.GetXUsersRequest()
                a = 0
                for chunk in [string[i:i+1990] for i in range(0, len(response), 1990)]: #2000 dc char limit, 6 tanesi kod tagleri (```)
                    if a == 0 : await client.send_message(message.channel, "```" + chunk + "```")
                    else : await client.send_message(message.channel, "```" + chunk + "```")
                    a += 1
                
            elif msg[1] == 'users':
                table = ohiapi.GetUsersRequest()
                await client.send_message(message.channel, f'```{table}```')
            
            elif msg[1] == 'addtime':
                username = msg[2]
                time = msg[3]
                response = ohiapi.ChangeUserSubTimeRequest(username, time)
                await client.send_message(message.channel, f'```{response}```')

            elif msg[1] == 'addtimeall':
                time = msg[2]
                response = ohiapi.ChangeAllSubTimeRequest(time)
                await client.send_message(message.channel, f'```{response}```')

        #n word check (hideout server)
        if 'N' in message.content.upper() and message.server.id == hideoutID:
            n_word = yazi.n_word_list[0]
            n_what_msg = ''
            if message.content == '!n':
                word_c = b_database.GetWord(n_word).word_count
                last_user = b_database.GetWord(n_word).user_name
                last_message = b_database.GetWord(n_word).last_msg

                await client.send_message(message.channel, f'`Toplamda {word_c} kez n word kullanildi`\nEn son ({last_user}) -> "{last_message}"')
            if message.content == '!nwhat':
                last_message = b_database.GetWord(n_word).last_msg
                await client.send_message(message.channel, f'{last_message}')

            msg = message.content.upper()

            for c_word in yazi.n_word_list:
                if c_word in msg:
                    try:
                        await client.add_reaction(message, "\U0001F6E1")
                        await client.send_message(discord.Object(id=540828135583645718), f'```n word detected : {message.author.name} -> {message.content} @ {message.channel.name}```\n`total count : {b_database.GetWord(n_word).word_count}`')
                        n_what_word = c_word
                        a = re.search(r'({})'.format(n_what_word), msg)
                        n_what_msg = message.content[:a.start()] + '||' + message.content[a.start(): a.end()] + '||' + message.content[a.end():]
                        b_database.CountWord(n_word, n_what_msg, getUserName(message.author))
                    except Exception as e:
                        print(f'error while checking n word(detected) - > {e}')
                    break

        #!eval 
        if message.content.startswith("!eval"):
            if message.author.id == myID or message.author.id == barisID:
                msg = message.content.split(" ")
                if len(msg) >= 2:
                    
                    command = msg[1:]
                    try:
                        ret, out = hmnEval.EvalHmnBot(command)
                        await client.send_message(message.channel, out)

                    except Exception as e: print(e)

        #!mrender
        if message.content.startswith("!mrender"):
            await checkServer(message, False)
            perm_user = b_database.GetPermUser(message.author.id)
            if not perm_user == None:

                    video = b_database.GetVideo(message.content)
                    if not video == None:
                        await client.send_message(message.channel, str(video.url))
                    
                    else:
                        msg = message.content.split(" ")
                        if len(msg) >= 2:
                            shortcut_flag = False
                            
                            if msg[1] == 'giveperm' and message.author.id == myID:
                                user = message.mentions[0]
                                user_nick = getUserName(user)
                                try:
                                    b_database.AddPermUser(str(user.id), user_nick, str(message.server.id))
                                    await client.send_message(message.channel, f"`{user.id}` VideoPermUser'a eklendi")

                                except:
                                    await client.send_message(message.channel, f"`{user.id}` VideoPermUser'a eklenemedi...")

                            if msg[1] == 'rm' and message.author.id == myID:
                                check = mrender.ClearOutVideos()
                                await client.send_message(message.channel, "`rm mrender/outs/*`\n Temizleme sonucu : " + str(check))
                            
                            else:
                                font_size = '96'
                                vid_template = msg[1]
                                text_start = 2

                                #!mrender template -f 10 ...
                                if '-f' in msg:
                                    font_size_index = msg.index('-f') + 1
                                    font_size = msg[font_size_index]
                                    text_start += 2
                                #!mrender template -s short ...
                                if '-s' in msg and message.author.id == myID:
                                    shortcut_flag = True
                                    shortcut_index = msg.index('-s') + 1
                                    shortcut = msg[shortcut_index]
                                    text_start += 2

                                vid_text = msg[text_start:]

                                try:
                                    await client.send_typing(message.channel)
                                    out_file, err_msg = mrender.RenderMeme(vid_template, font_size, vid_text)
                                    if err_msg == None:    
                                        snd_msg = await client.send_file(message.channel, str(out_file), content = " ".join(vid_text))
                                        vid_url = str(snd_msg.attachments[0]['url'])
                                        user_name = getUserName(user)
                                        #print(f"new vid row : :  {str(message.content)} | {vid_url} | {user_name}")
                                        if not shortcut_flag:
                                            b_database.AddVideo(str(message.content), vid_url, user_name)
                                        else:
                                            b_database.AddVideo('!mrender ' + str(shortcut), vid_url, user_name)
                                    else:
                                        await client.send_message(message.channel, f"Video olusturulurken hata meydana geldi : {err_msg}")

                                except Exception as e: 
                                    print(e)

        #oyun degisme
        if message.content.upper().startswith("!OYUNDEGIS"):
                        
            if message.author.id == myID:
                msg = message.content.split(" ")

                try:
                    if msg[1]:
                        try:
                            await client.change_presence(game=discord.Game(name=yazi.bot_game[msg[1]]))
                        except:
                            await client.send_message(message.channel,"Hata olustu")
                            pass
                except:
                    pass

            else:
                await client.send_mesage(message.channel, "Yetkin yok!")

        
        #!srvrs
        if message.content == "!srvrs" and message.author.id == myID:

            await client.send_message(message.channel,"Server sayisi : " + str(serverSayisi()) + "\n" + "```asciidoc\n" + onlineServer() + "```")

        #!srvrs2
        if message.content == "!srvrs2" and message.author.id == myID:

            servers = list(client.servers)
            temp_liste = ""

            for i in range(len(servers)):
                temp_liste += servers[i-1].name + " -- " + str(servers[i-1].member_count) + " kullanici\n"
            
            await client.send_message(message.channel,"Server sayisi : " + str(serverSayisi()) + "\n" + "```asciidoc\n" + temp_liste + "```")

        #!logla
        if message.content == "!logla" and message.author.id == myID:

            await bot_logla()

        #112
        if message.content == "!112":

            await checkServer(message, False)
            pasta = copypasta.pasta_al(yazi.komut["112_pasta2"])
            await client.send_message(message.channel, pasta)

@client.event
async def on_message_edit(old_msg, message):
    if not message.author.bot == 1:
        #n word check (hideout server)
        if 'N' in message.content.upper() and message.server.id == hideoutID:
            n_word = yazi.n_word_list[0]
            n_what_msg = ''
            if message.content == '!n':
                word_c = b_database.GetWord(n_word).word_count
                last_user = b_database.GetWord(n_word).user_name
                last_message = b_database.GetWord(n_word).last_msg

                await client.send_message(message.channel, f'`Toplamda {word_c} kez n word kullanildi`\nEn son ({last_user}) -> "{last_message}"')
            if message.content == '!nwhat':
                last_message = b_database.GetWord(n_word).last_msg
                await client.send_message(message.channel, f'{last_message}')

            msg = message.content.upper()

            for c_word in yazi.n_word_list:
                if c_word in msg:
                    try:
                        await client.add_reaction(message, "\U0001F6E1")
                        await client.send_message(discord.Object(id=540828135583645718), f'```n word detected : {message.author.name} -> {message.content} @ {message.channel.name}```\n`total count : {b_database.GetWord(n_word).word_count}`')
                        n_what_word = c_word
                        a = re.search(r'({})'.format(n_what_word), msg)
                        n_what_msg = message.content[:a.start()] + '||' + message.content[a.start(): a.end()] + '||' + message.content[a.end():]
                        b_database.CountWord(n_word, n_what_msg, getUserName(message.author))
                    except Exception as e:
                        print(f'error while checking n word(detected) - > {e}')
                    break

client.run(token)
