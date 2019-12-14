# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from discord.ext import commands
from discord.ext.commands import AutoShardedBot
import sys
import traceback
from utils import permissions
from datetime import datetime

init_extensions = ['cogs.utility', 'cogs.owner', 'cogs.info', 'cogs.admin', 'cogs.fun', 'cogs.meme', 'cogs.currency']

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

        for ext in init_extensions:
            self.load_extension(ext)

        self.boot_time = datetime.now()

    async def on_ready(self):
        print(f"Ready : {self.user.name} -- {self.user.id}")

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
        else:
            print(f'{error}', file=sys.stderr)