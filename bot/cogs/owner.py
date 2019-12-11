import discord
from utils import confparser, default
from discord.ext import commands

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

    @commands.command()
    async def say(self, ctx, message : str):
        dev_id = self.config.owners[0]
        if ctx.author.id == dev_id:
            try:
                await ctx.delete_message(ctx.message)
                await ctx.send(message)
            except:
                pass

def setup(bot):
    bot.add_cog(Owner(bot))