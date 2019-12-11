import random
import discord
import urllib
import secrets
import aiohttp
import re

from io import BytesIO
from discord.ext import commands
from utils import confparser, pasta, strings


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

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

    @commands.command()
    @commands.guild_only()
    async def oyun(self, ctx, message: str):
        if not '```' in message:
            if not len(message) < 4:
                game_name = message
                player_list = "```asciidoc\n== Kim '" + game_name +"' oynuyor ==\n\n"
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


    @commands.command(aliases=['ara'])
    async def google(self, ctx):
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            await ctx.send(f"{self.get_searchq(ctx.message.content)}")

    @commands.command()
    async def lmgtfy(self, ctx, message: str):
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            await ctx.send(f"{self.get_searchq(ctx.message.content, True)}")

    @commands.command(aliases=['oyla'])
    @commands.guild_only()
    async def vote(self, ctx):
        if len(ctx.message.mentions) == 0 and not ctx.message.mention_everyone:
            msg = await ctx.send(strings.komut["oyla"] % (ctx.author.id, ctx.message.content))
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')

    @commands.command()
    async def sence(self, ctx):
        opt = random.randint(1, 4)
        await ctx.send(strings.komut[f"sence{opt}"])

    @commands.command(aliases=['112'])
    async def yuzoniki(self, ctx):
        text = pasta.get_pasta("https://paste.ee/p/tzqyK")
        await ctx.send(text)

    @commands.command(aliases=['fırlat', 'firlat'])
    async def flip(self, ctx):
        coinsides = ['Yazı', 'Tura']
        await ctx.send(f"{ctx.author.name} **{random.choice(coinsides)}** fırlattı!")

def setup(bot):
    bot.add_cog(Fun(bot))