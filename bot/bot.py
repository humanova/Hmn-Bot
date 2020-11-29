# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import sys
import traceback
import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot, DefaultHelpCommand
from utils import permissions
from datetime import datetime

init_extensions = ['cogs.utility',
                   'cogs.owner',
                   'cogs.info',
                   'cogs.admin',
                   'cogs.fun',
                   'cogs.meme',
                   'cogs.currency',
                   'cogs.weather',
                   'cogs.mrender',
                   'cogs.tracker',
                   'cogs.osutracker'
                   #'cogs.dchess'
                   ]

help_cmd_attrs = {'name': 'yardım',
                 'help': 'Bu mesajı gösterir.'}


# override !help command
class HelpFormat(DefaultHelpCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_attrs=help_cmd_attrs, **kwargs)

    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    def get_ending_note(self):
        return "!yardım <komut> yazarak bir komut hakkında daha fazla bilgi al."

    async def send_pages(self, no_pm: bool = False):
        try:
            if permissions.can_react(self.context):
                await self.context.message.add_reaction(chr(0x2709))
        except discord.Forbidden:
            pass

        try:
            destination = self.get_destination(no_pm=no_pm)
            for page in self.paginator.pages:
                await destination.send(page)
        except discord.Forbidden:
            destination = self.get_destination(no_pm=True)
            for page in self.paginator.pages:
                await destination.send(page)


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, help_command=HelpFormat(), **kwargs)
        self.loop.create_task(self.ready())

        for ext in init_extensions:
            self.load_extension(ext)

        self.boot_time = datetime.now()

    async def ready(self):
        await self.wait_until_ready()
        print(f"Ready : {self.user.name} -- {self.user.id}")
        print(f"Shards : {self.shard_count}")
        await self.change_presence(status=discord.Status.online, activity=discord.Game("!help"))


    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('Bu komutu sadece bir sunucuda kullanabilirsiniz.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Bu komut devredışı.')
        elif isinstance(error, commands.CommandInvokeError):
            print(error)
            print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
            traceback.print_tb(error.original.__traceback__)
            print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            print(f'{error}', file=sys.stderr)