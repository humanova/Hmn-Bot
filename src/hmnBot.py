
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
import threading
import asyncio
import time
from datetime import datetime

import dbl  #discordbotlist.org api bot istatistikleri icin

#kendi importlarim
import havaDurumu as hava
import botStrings as yazi
import dovizIslem as doviz
import copypasta
import zaman
import ceviri
import meme
import music
import botEval as hmnEval
import memeRenderer as mrender


################################

token = os.environ['PP_BOT_TOKEN']
dbl_token = os.environ['DBL_TOKEN']

Client = discord.Client()
client = commands.Bot(command_prefix = "!")

version = "hmnBot v0.3.4\n11/11/18"
myID = "213262071050141696"
barisID = "190836437917237248"
botID = "455819835486502933"
logChannelID = "470853011233570817"

uyari_disi = [botID,myID]
kizginKaraliste = ["460563755772936212"]

# ======================== LOGLAMA ========================= #

log_num = 0
temel_log = "\n[TEMEL]\n"
komut_log = "\n[KOMUT LOGLARI]\n```"
online_server_log = "\n[ONLINE SERVERLAR]\n```"


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


def onlineServerLog():
    global online_server_log
    servers = list(client.servers)

    for i in range(len(servers)):
        online_server_log += servers[i-1].name + "\n"

    
async def bot_logla():

    while not client.is_closed:

        dblpy = dbl.Client(client, dbl_token)

        temelLog()
        onlineServerLog()
        
        global log_num
        global temel_log
        global komut_log
        global online_server_log 

        log_num += 1
        
        tarih = str(datetime.now())
        log_baslangic = "\nLOG[" + str(log_num) + "] : " + tarih + "\n"
        log_son = str(log_baslangic) + str(temel_log) + str(online_server_log) + "```" +str(komut_log)

        try:
            a = 0
            string = log_son
            for chunk in [string[i:i+1982] for i in range(0, len(string), 1982)]:
                if a == 0 : await client.send_message(discord.Object(id=logChannelID), chunk + "```")
                else : await client.send_message(discord.Object(id=logChannelID), "```" + chunk + "```")
                a += 1

        except:
            await client.send_message(discord.Object(id=logChannelID), log_son + "```")
        
        #discordbotlist.org istatistikleri gonder
        try:
            await dblpy.post_server_count()
            print('server sayisi gonderildi : ({})'.format(len(client.servers)))
        except Exception as e:
            print('server sayisi gonderilirken hata olustu : \n{}: {}'.format(type(e).__name__, e))

        temel_log = "\n[TEMEL]\n"
        komut_log = "\n[KOMUT LOGLARI]\n```"
        online_server_log = "\n[ONLINE SERVERLAR]\n```"

        await asyncio.sleep(1800) 


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



# ===================== LOGLAMA BITIS ====================== #


def is_float(string):
  try:
    return float(string) and '.' in string 
  except ValueError:  
    return False


@client.event
async def on_ready():
    print("Bot hazir!\n")
    print("%s adiyla giris yapildi" % (client.user.name))
    await bot_logla()
    await client.change_presence(game=discord.Game(name=yazi.bot_game["despacito"]))

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
        if message.content.upper() == "!VERSION"  or message.content.upper() == "!VERSIYON"  or message.content.upper() == "!SÜRÜM" or message.content.upper() == "!SURUM":
            global komut_log

            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            embed=discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=client.user.name + " Versiyonu", icon_url=client.user.avatar_url)
            embed.add_field(name="Version : ", value=version, inline=False)
            await client.send_message(message.channel,embed=embed)
            #await client.send_message(message.channel, "**%s**" % (version))


        #!gelistirici,!developer
        if message.content.upper() == "!DEV" or message.content.upper() == "!GELISTIRICI" or message.content == "!geliştirici":
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            msg = message.content.split(" ")

            if len(msg) == 2:
                komut = msg[1]
                try:
                    await client.send_message(message.channel, yazi.komutYardim[komut])
                except:
                    return
            else:
                await client.send_message(message.channel, yazi.komut["yardim"])
            

        #!statu,!stats
        if message.content.upper() == "!STATS" or message.content.upper() == "!STATÜ" or message.content.upper() == "!STATU":
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            embed=discord.Embed(title=" ",description="**[Davet](https://discord.gg/XBebmFF)**", color=0x75df00)
            embed.set_author(name="Hmn-Bot Destek", icon_url=client.user.avatar_url)
            await client.send_message(message.channel,embed=embed)
        
        #!temizle
        if message.content.upper().startswith("!TEMIZLE"):

            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
                            return

                    except:
                        flag = False
                        return
                    
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


        #!durt,!ping
        if message.content.upper().startswith('!PING') or message.content.upper().startswith("!DÜRT") or message.content.upper().startswith("!DURT"):
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:            
                contents = message.content.split(" ")

                try:
                    if contents[1]: 
                        userID = message.author.id
                        member = message.server.get_member_named(contents[1])
                        if not userID == member.id:
                            await client.send_message(message.channel, yazi.komut["durt"] % (member.id,userID))
                        else:
                            await client.send_message(message.channel, yazi.komut["durt2"] % (userID))
                except:
                    return    


        #!davet,invite
        if message.content.upper() == "!DAVET" or message.content.upper() == "!INVITE":
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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


        #!!say (sadece benim id'm)
        if message.content.upper().startswith("!SAY"):
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
           
            if message.author.id == myID:
                args = message.content.split(" ")
                try:
                    if args[1]:
                        try:
                            await client.delete_message(message)
                        except discord.errors.NotFound:
                            return
                        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))
                except:
                    return
                        
            else:
                await client.send_message(message.channel,"**Buna yetkin yok!**")

        '''
        #!cevir , ffff99
        if message.content.upper().startswith("!CEVIR") or message.content.upper().startswith("!ÇEVIR"):
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
                    return
        '''

        #!oyla,!vote
        if message.content.upper().startswith("!VOTE") or message.content.upper().startswith("!OYLA"):
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:   

                userID = message.author.id
                msg = message.content.split(" ")

                try:
                    if msg[1]:
                        msg = await client.send_message(message.channel, yazi.komut["oyla"] % (userID," ".join(msg[1:])))
                        await client.add_reaction(msg,'👍')
                        await client.add_reaction(msg,'👎')
                except:
                    return
                
                
        #!google,!ara 
        if message.content.upper().startswith("!GOOGLE") or message.content.upper().startswith("!ARA"):
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
          
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
                        return

        #!lmgtfy
        if message.content.upper().startswith("!LMGTFY"):
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
           
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
            except:
                return
        
        #!hava
        if message.content.upper().startswith("!HAVA"):
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
                    return

        #!bitcoin,!btc
        if message.content.upper() == "!BITCOIN" or message.content.upper() == "!BTC":
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:               
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
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:               
                msg = message.content.split(" ")

                try:
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
                except:
                    return


        #!doviz kur
        if message.content.upper().startswith("!DÖVIZ") or message.content.upper().startswith("!DOVIZ"):
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:          
                msg = message.content.split(" ")

                try:
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
                            if kur == "AYLIK SUPPORTER":
                                embed.add_field(name="Indirimli", value="~" + doviz.supporterDiscount(adet,kur_degeri), inline=False)
                            embed.set_footer(text="💰 Kaynak : 1forge.com")
                            await client.send_message(message.channel,embed=embed)
                            # await client.send_message(message.channel, yazi.komut["doviz"] % (kur,kur_degeri))

                except:
                    return

        #!oyun
        if message.content.upper().startswith("!OYUN "):

            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:             
                sikayet = message.content.split(" ")

                try:
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
                
                except:
                    return


        #!server,!serverstats
        if message.content.upper() == "!SERVER":
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

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
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
        
            ilk_msg = await client.send_message(message.channel, "Şarkı aranıyor...") 

            flag = True
            msg = message.content.split(" ")
            msg = " ".join(msg[1:])

            '''
            try:
                if msg[0:]:
                    if "-" in msg:
                        sarki = msg[0:msg.find('-')]
                        artist = msg[msg.find('-') + 1:]

                    else:
                        sarki = msg[0:]
                        artist = ""
                else:
                    flag = False
            except:
                flag = False
                return
            '''

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
            
            server_flag = True

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"

            if not server_flag:

                msg = message.content.split(" ")
                
                try:
                    subreddit = msg[1]
                except:
                    return

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
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
        
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
            except:
                return


        #!ben,!self
        if message.content.upper().startswith("!SELF") or message.content.upper().startswith("!BEN"):
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"
            
            if not '@everyone' in message.content:
                if not '@here' in message.content:
                    msg = message.content.split(" ")

                    try:
                        if msg[1]:
                            await client.send_message(message.channel, yazi.komut["self"] % (" ".join(msg[1:])))
                    except:
                        return


        #!sence
        if message.content.upper().startswith("!SENCE"):
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"


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
            
            server_flag = False

            if not message.server == None: 
                server_flag = False
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @" + message.server.name + "            " + message.content + "\n"
            else:
                if server_flag == True:
                    await client.send_message(message.channel, "Bu komut sadece bir serverda kullanılabilir")
                komut_log += "[" + message.author.name + "#" + message.author.discriminator + "] @DM            " + message.content + "\n"


            gelen = random.randint(1,100)
            if gelen % 2 == 1:
                await client.send_message(message.channel, yazi.komut["firlatYazi"])
            if gelen % 2 == 0:
                await client.send_message(message.channel, yazi.komut["firlatTura"])


        #herkesi etiketleyenlere kizgin
        if message.mention_everyone:
            if not message.server.id in kizginKaraliste:
                await client.add_reaction(message,"😡")


        #++========================== OZEL ============================++#

        #!eval 
        if message.content.startswith("!eval"):
            if message.author.id == myID:
                msg = message.content.split(" ")
                if len(msg) >= 2:
                    
                    command = msg[1:]
                    ret, out = hmnEval.EvalHmnBot(command)
                    client.send_message(message.channel, out)

        #!mrender
        if message.content.startswith("!mrender"):
            if message.author.id == myID:

                msg = message.content.split(" ")
                if len(msg) >= 3:
                    
                    if msg[1] == 'rm':
                        check = mrender.ClearOutVideos()
                        client.send_message(message.channel, "`rm mrender/outs/*.*` Temizleme sonucu : " + check)
                    
                    else:
                        vid_template = msg[1]
                        vid_text = msg[2: ]

                        out_file = mrender.RenderMeme(vid_template, vid_text)
                        client.send_file(message.channel, out_file, content = msg[2:])


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
                            return 
                except:
                    return

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

            pasta = copypasta.pasta_al(yazi.komut["112_pasta2"])

            await client.send_message(message.channel, pasta)





client.run(token)



