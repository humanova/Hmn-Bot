# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import discord
from discord.ext import commands
from utils import confparser, strings, default
from datetime import datetime
import lyricsgenius as genius
import codecs

class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.genius_api = genius.Genius(self.config.genius_token)

    def get_searchq(self, message, is_google = True):
        msg = message.split(" ")
        search_q = "https://google.com/search?q="
        if not is_google:
            search_q = "http://lmgtfy.com/?q="

        for word in range(1, len(msg)):
            if not word == len(msg) - 1:
                search_q += msg[word] + "+"
            else:
                search_q += msg[word]

        return search_q

    def get_lyrics(self, song_name):
        song = self.genius_api.search_song(song_title=song_name, artist_name="")

        if song is not None:
            lyrics = song.save_lyrics(filename="lyrics.txt", format="txt", overwrite="no")

            # backtick(`) injection check
            if '```' not in lyrics and not '```' in song.title and not '```' in song.artist and not '```' in song.url:
                return {"lyrics": lyrics, "title": song.title, "artist": song.artist, "url": song.url}
            else:
                return None
        else:
            return None

    async def send_lyrics(self, ctx, lyrics):
        # send msgs with more than 2000 characters
        # 2000 - format chars = 1985
        for chunk in [lyrics[i:i + 1985] for i in range(0, len(lyrics), 1985)]:
            await ctx.send(f"```asciidoc\n{chunk}```")

    def get_osutr_chat_log(self, line_count):
        chat = str
        with codecs.open(self.config.osutr_log_path, "r", "utf-8") as f:
            data = f.readlines()
        try:
            chat = "".join(data[-line_count:])
        except Exception as e:
            print(f"error while getting chat log : {e}")
        # prevent backtick injection
        chat = chat.replace("`", "")
        return chat

    @commands.command(aliases=['invite', 'inv'])
    @commands.guild_only()
    @commands.has_permissions(create_instant_invite=True)
    @commands.bot_has_permissions(create_instant_invite=True)
    async def davet(self, ctx, inv_count:int = None):
        """ Kanal daveti yaratır """
        if inv_count == None:
            inv_count = 1

        if inv_count > 0:
            inv = await ctx.channel.create_invite(max_uses=inv_count)

            embed = discord.Embed(title=" ", color=0x75df00)
            embed.set_author(name=ctx.channel.name + " Kanal Daveti", icon_url=ctx.guild.icon_url)
            embed.add_field(name=f"{inv_count} kullanımlık davet", value=inv.url, inline=False)

            await ctx.send(embed=embed)

    @commands.command(aliases=['report', 'şikayet'])
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    async def sikayet(self, ctx, *, message:str):
        """ Sunucu sahibine şikayet iletir """
        date = datetime.now()
        report_msg = message
        report_text = strings.komut['sikayet_admin'] % (default.date(date), ctx.guild.name, ctx.channel.name,
                                                        str(ctx.author), ctx.author.display_name, report_msg)
        try:
            await ctx.guild.owner.create_dm()
            await ctx.guild.owner.dm_channel.send(report_text)
            await ctx.message.delete()
            await ctx.send(strings.komut['sikayet_kullanici'])

            report_notify = ctx.send("Şikayet iletildi.")
            await report_notify.delete(delay=3)
        except Exception as e:
            await ctx.send(strings.komut['sikayet_hata'])

            default.print_error(ctx, e)

    @commands.command()
    @commands.guild_only()
    async def oyun(self, ctx, message:str):
        """ Belirtilen oyunu oynayanları listeler """
        if not '```' in message:
            if not len(message) < 4:
                game_name = message
                player_list = f"```asciidoc\n== Kim '{game_name}' oynuyor ==\n\n"
                player_count = 0

                for member in ctx.guild.members:
                    if not len(member.activities) == 0:
                        member_activities = ""
                        for act in member.activities:
                            member_activities += f"{act.name.upper()}"
                        if game_name.upper() in member_activities:
                            if '```' in member.name or '```' in member_activities:
                                continue
                            player_list += f" + {str(member)} - {str(member_activities)}\n"
                            player_count += 1
                player_list += "```"

                embed = discord.Embed(title=" ", color=0x001a40)
                embed.set_author(name="Kim Oynuyor", icon_url=self.bot.user.avatar_url)

                if player_count > 0:
                    embed.add_field(name="Oyun", value=game_name, inline=False)
                    embed.add_field(name="Oyuncu Sayısı : ", value=player_count, inline=False)
                    await ctx.send(embed=embed)
                    await ctx.send(player_list)
                else:
                    embed = discord.Embed(title=" ", description=strings.komut["oyunHata2"] % ("'" + game_name + "'"),
                                          color=0xFF0000)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title=" ", description=strings.komut["oyunHata"], color=0xFF0000)
                await ctx.send(embed=embed)

    @commands.command(aliases=['lyrics', 'söz'])
    async def soz(self, ctx, *, message:str):
        """ Belirtilen şarkının sözlerini gönderir """
        song_name = message
        lyrics_data = self.get_lyrics(song_name=song_name)
        await ctx.send(f"== **{lyrics_data['artist']}** - **{lyrics_data['title']}** Sözleri == ")
        await self.send_lyrics(ctx, lyrics_data['lyrics'])

    @commands.command(aliases=['ara'])
    async def google(self, ctx):
        """ Arama bağlantısı gönderir """
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            await ctx.send(f"{self.get_searchq(ctx.message.content)}")

    @commands.command()
    async def lmgtfy(self, ctx):
        """ lmgtfy arama bağlantısı gönderir """
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            await ctx.send(f"{self.get_searchq(ctx.message.content, True)}")

    @commands.command(aliases=['oyla'])
    @commands.guild_only()
    async def vote(self, ctx, *, message:str):
        """ Evet-hayır oylaması başlatır """
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            msg = await ctx.send(strings.komut["oyla"] % (ctx.author.id, message))
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

    # ======private commands=======
    # =============================
    @commands.command(hidden=True)
    @commands.guild_only()
    async def osutr(self, ctx, msg_count:int=10):
        chat_log = self.get_osutr_chat_log(msg_count)
        await ctx.send(f"```{chat_log}```")

    @commands.command(hidden=True)
    @commands.guild_only()
    async def osutr_dump(self, ctx, msg_count:int=10):
        await ctx.send(file=discord.File(fp=self.config.osutr_log_path, filename="osutr_dump.txt"))

def setup(bot):
    bot.add_cog(Utility(bot))