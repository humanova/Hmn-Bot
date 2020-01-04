# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import discord
from discord.ext import commands
import codecs
from utils import confparser, default, permissions, eval

class Owner(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

    @commands.command()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.check(permissions.is_owner)
    async def say(self, ctx, *, message : str):
        try:
            await ctx.delete_message(ctx.message)
            await ctx.send(message)
        except:
            pass

    @commands.command()
    @commands.check(permissions.is_owner)
    async def load(self, ctx, name: str):
        try:
            self.bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Loaded extension **{name}.py**")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def unload(self, ctx, name: str):
        try:
            self.bot.unload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Unloaded extension **{name}.py**")


    @commands.command()
    @commands.check(permissions.is_owner)
    async def reload(self, ctx, name: str):
        try:
            self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.send(f"Reloaded extension **{name}.py**")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def reloadall(self, ctx):
        error_collection = []
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                try:
                    self.bot.reload_extension(f"cogs.{name}")
                except Exception as e:
                    error_collection.append(
                        [file, default.traceback_maker(e, advance=False)]
                    )

        if error_collection:
            output = "\n".join([f"**{g[0]}** ```diff\n- {g[1]}```" for g in error_collection])
            return await ctx.send(output)

        await ctx.send("Successfully reloaded all extensions")

    @commands.command(aliases=['exec', 'eval'])
    @commands.check(permissions.is_owner)
    async def execute(self, ctx, *, cmd: str):
        message = await ctx.send(f"executing {cmd}...")
        output = eval.evaluate_command(cmd)

        await message.edit(content=f"```{output}```")
        await message.add_reaction("👍")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def servers(self, ctx):
        server_list = ""
        for guild in self.bot.guilds:
            server_list += f"{guild.member_count} :: {guild.name}\n"
        await ctx.send(f"```{server_list}```")

    @commands.command()
    @commands.check(permissions.is_owner)
    async def dump_users(self, ctx):
        file = codecs.open(self.config.users_log_path, "w+", "utf-8")

        for g in self.bot.guilds:
            print(f"Logging server : {g.name}")
            file.write(f"==== {g.name} -- {g.member_count} users\n")
            for mem in g.members:
                file.write(f"{str(mem)}\n")
        file.close()

        await ctx.send(file=discord.File(fp=self.config.users_log_path, filename="users_dump.txt"))


def setup(bot):
    bot.add_cog(Owner(bot))