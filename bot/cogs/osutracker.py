# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import discord
from discord.ext import commands, tasks
from utils import confparser, strings, default, permissions
from osuapi import OsuApi, ReqConnector
import datetime
import json
import os

class OsuTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

        self.api = OsuApi(key=self.config.osu_token, connector=ReqConnector())
        self.last_check_datetime = datetime.datetime.utcnow()
        self.tracking_channel = None
        self.tracked_users = self.get_tracked_users()

        self.tracker_task_loop.start()

    def cog_unload(self):
        self.tracker_task_loop.cancel()

    @tasks.loop(seconds=30)
    async def tracker_task_loop(self):
        for user in self.tracked_users:
            scores = self.api.get_user_best(user['name'], limit=20)
            for s in [s for s in scores if s.date > self.last_check_datetime]:
                bmap = self.api.get_beatmaps(beatmap_id=s.beatmap_id)[0]
                msg = f"{user['nick']} abım {bmap.title} - {bmap.version} mapınde {int(round(s.pp))} pp play yapmıs\n" \
                      f"helal abım <@{user['discord'].id}>\n".lower().replace('i', 'ı')
                await self.tracking_channel.send(msg)
        self.last_check_datetime = datetime.datetime.utcnow()

    def get_tracked_users(self):
        with open("tracked_users.json", "r") as f:
            data = json.load(f) if not json.load(f) == {} else None
        users = []
        if data:
            for u in data['users']:
                users.append({"name": u['name'], "discord": self.bot.get_user(id=u['discord_id']), "nick": u['nick']})
        return users

    def add_to_tracked_users_file(self, osu_username, discord_id, nick):
        with open("tracked_users.json", "w") as f:
            data = json.load(f)
            if data == {}:
                data = {"users": [{"name": osu_username, "discord_id": discord_id, "nick": nick}]}
            else:
                data['users'].append({"name": osu_username, "discord_id": discord_id, "nick": nick})
                data.update()
            print(data)
            json.dump(data, f)

    @commands.command()
    @commands.check(permissions.is_owner)
    async def osutrack(self, ctx, mem: discord.Member, osu_username, nick):
        if osu_username not in [u['name'] for u in self.tracked_users]:
            try:
                osu_id = self.api.get_user(osu_username)[0].user_id
                self.tracked_users.append({"name": osu_username, "nick": nick, "discord": mem})
                self.add_to_tracked_users_file(osu_username, discord_id=mem.id, nick=nick)
                await ctx.send(f"tracking started : {str(mem)}, osu id : {osu_id}")
            except:
                await ctx.send(f"couldn't start tracking")
        else:
            await ctx.send(f"already tracking : {str(mem)}")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def setch(self, ctx):
        self.tracking_channel = ctx
        await ctx.send(f"ok")

def setup(bot):
    bot.add_cog(OsuTracker(bot))