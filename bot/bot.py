import os
from utils import permissions
from discord.ext.commands import AutoShardedBot
from datetime import datetime

init_extensions = ['cogs.utility', 'cogs.owner', 'cogs.info', 'cogs.admin', 'cogs.fun', 'cogs.currency']

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