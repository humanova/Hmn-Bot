# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import discord
from utils import confparser, default
from discord.ext import commands
import psutil
from datetime import datetime
import os

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.process = psutil.Process(os.getpid())

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, *, user:discord.Member = None):
        """ Etiketlenen kullanıcının avatarını gönderir """
        if user is None:
            user = ctx.author
        await ctx.send(f"{user.avatar_url_as(size=1024)}")

    @commands.command(aliases=['roller'])
    @commands.guild_only()
    async def roles(self, ctx):
        """ Suncucu rollerini listeler """
        roles = ""

        for role in ctx.guild.roles:
            roles += f"{role.name}\n"

        embed = discord.Embed(title=" ", color=0x001a40)
        embed.add_field(name= "Roller", value=f"```{roles}```")
        await ctx.send(embed= embed)

    @commands.command()
    @commands.guild_only()
    async def server(self, ctx):
        """ Suncucu bilgilerini gönderir """
        tch_count = 0
        vch_count = 0
        for chan in ctx.guild.channels:
            if chan.type == discord.ChannelType.text:
                tch_count += 1
            else:
                vch_count += 1

        if ctx.invoked_subcommand is None:
            bot_count = sum(1 for member in ctx.guild.members if member.bot)

        embed = discord.Embed()
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner_url_as(format="png"))

        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        embed.add_field(name="Sahibi", value=f"{str(ctx.guild.owner)}", inline=True)
        embed.add_field(name="Bölge", value=ctx.guild.region, inline=True)
        embed.add_field(name="Yazı Kanalı", value=str(tch_count), inline=True)
        embed.add_field(name="Ses Kanalı", value=str(vch_count), inline=True)
        embed.add_field(name="Kullanıcı", value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Rol", value=str(len(ctx.guild.roles)), inline=True)
        embed.add_field(name="İnsan", value=(ctx.guild.member_count-bot_count), inline=True)
        embed.add_field(name="Bot", value=bot_count, inline=True)
        embed.set_footer(text=f"ID: {ctx.guild.id} | Created at•{default.date(ctx.guild.created_at)}")
        await ctx.send(embed=embed)

    @commands.command(aliases=['developer, geliştirici'])
    async def dev(self, ctx):
        """ Geliştirici bilgilerini gönderir """
        embed = discord.Embed(title=" ", color=0x75df00)
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Geliştirici", value=f"<@{self.config.owners[0]}>", inline=False)
        embed.add_field(name="GitHub", value="https://github.com/humanova", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def destek(self, ctx):
        """ Destek sunucusu daveti gönderir """
        embed = discord.Embed(title=" ", description="**[Davet](https://discord.gg/XBebmFF)**", color=0x75df00)
        embed.set_author(name="Hmn-Bot Destek", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['stats', 'bilgi'])
    async def info(self, ctx):
        """ Bot bilgilerini gönderir """
        #ram_usage = self.process.memory_full_info().rss / 1024 ** 2
        embed_color = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embed_color = ctx.me.top_role.colour

        user_count = len(self.bot.users)
        avgmembers = user_count / len(self.bot.guilds)

        embed = discord.Embed(colour=embed_color)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Son restart", value=default.timeago(datetime.now() - self.bot.boot_time), inline=False)
        embed.add_field(name="Server Sayısı", value=f"{len(ctx.bot.guilds)}", inline=False)
        embed.add_field(name="Kullanıcı Sayısı", value=f"{user_count}", inline=False)
        embed.add_field(
            name=f"Geliştirici",
            value=f"{str(self.bot.get_user(self.config.owners[0]))}",
            inline=True)
        #embed.add_field(name="Bellek kullanımı", value=f"{ram_usage:.2f} MB", inline=True)

        await ctx.send(content=f"**{ctx.bot.user}** | **{self.config.version}**", embed=embed)

    @commands.command(aliases=['yardim'], hidden=True)
    async def help(self, ctx):
        help_cmd = self.bot.get_command('yardım')
        ctx.command = help_cmd
        await self.bot.invoke(ctx)

def setup(bot):
    bot.add_cog(Info(bot))