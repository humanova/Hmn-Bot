# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# a cog to mess with a friend, nothing serious :)
import discord
from discord.ext import commands, tasks
from utils import confparser, strings, default, permissions
import time

TRACKED_ACT_NAME = None
TRACKED_ACT_START_MSG = None
TRACKED_ACT_END_MSG = None


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

        self.tracked_member = None
        self.tracking_channel = None
        self.is_started = False

        self.tracked_act_status = False
        self.act_start_time = None

    def cog_unload(self):
        self.tracker_task_loop.cancel()

    @tasks.loop(minutes=1)
    async def tracker_task_loop(self):
        self.is_started = True
        if TRACKED_ACT_NAME in [act.name for act in self.tracked_member.activities]:
            if not self.tracked_act_status:
                await self.tracking_channel.send(TRACKED_ACT_START_MSG)
                self.tracked_act_status = True
                self.act_start_time = time.time()
        elif self.tracked_act_status:
            await self.tracking_channel.send(TRACKED_ACT_END_MSG + f" (yaklasik {int((time.time() - self.act_start_time)/60)} dakika oynadin)")
            self.tracked_act_status = False

    @commands.command()
    @commands.check(permissions.is_owner)
    async def track(self, ctx, mem: discord.Member):
        if self.is_started:
            self.tracker_task_loop.stop()
        self.tracked_member = mem
        self.tracking_channel = ctx
        self.tracker_task_loop.start()

        await ctx.send(f"tracking started : {str(mem)}")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def trackstop(self, ctx):
        if self.is_started:
            self.tracker_task_loop.cancel()
            await ctx.send(f"tracking stopped  : {str(self.tracked_member)}")
        else:
            await ctx.send(f"couldn't stop tracking")


def setup(bot):
    bot.add_cog(Tracker(bot))