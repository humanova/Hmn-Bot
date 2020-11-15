# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import discord
from discord.ext import commands, tasks
from utils import confparser, strings, default, permissions
from osuapi import OsuApi, ReqConnector
import datetime


class OsuTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

        self.api = OsuApi(key=self.config.osu_token, connector=ReqConnector())
        self.last_check_datetime = datetime.datetime.utcnow()
        self.tracking_channel = None
        self.is_started = False
        self.tracked_users = []

    def cog_unload(self):
        self.tracker_task_loop.cancel()

    @tasks.loop(minutes=1)
    async def tracker_task_loop(self):
        for user in self.tracked_users:
            scores = self.api.get_user_best(user['name'], limit=30)
            for s in [s for s in scores if s.date > self.last_check_datetime]:
                bmap = self.api.get_beatmaps(beatmap_id=s.beatmap_id)[0]
                msg = f"{user['nick']} abım {bmap.title} - {bmap.version} mapınde {int(round(s.pp))} pp play yapmıs\n" \
                      f"helal abım <@{user['discord'].id}>\n".lower().replace('i', 'ı')
                await self.tracking_channel.send(msg)
        self.last_check_datetime = datetime.datetime.utcnow()

    @commands.command()
    @commands.check(permissions.is_owner)
    async def osutrack(self, ctx, mem: discord.Member, osu_username, nick):
        if osu_username not in [u['name'] for u in self.tracked_users]:
            try:
                osu_id = self.api.get_user(osu_username)[0].user_id
                self.tracked_users.append({"name": osu_username, "nick": nick, "discord": mem})
                await ctx.send(f"tracking started : {str(mem)}, osu id : {osu_id}")
            except:
                await ctx.send(f"couldn't start tracking")
        else:
            await ctx.send(f"already tracking : {str(mem)}")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def startosutracker(self, ctx):
        if not self.is_started:
            self.tracking_channel = ctx
            self.tracker_task_loop.start()
            self.is_started = True
            await ctx.send(f"ok")
        else:
            await ctx.send(f"tracker already started")

def setup(bot):
    bot.add_cog(OsuTracker(bot))