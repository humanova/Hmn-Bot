import os
from utils import permissions
from discord.ext.commands import AutoShardedBot
from datetime import datetime

class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)

        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                fn = file[:-3]
                self.load_extension(f"cogs.{fn}")

        self.boot_time = datetime.now()

    async def on_ready(self):
        print(f"Ready : {self.user.name} -- {self.user.id}")

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)