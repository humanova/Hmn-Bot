# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import bot
from utils import confparser, permissions
import discord
from discord.ext.commands import DefaultHelpCommand
config = confparser.get("config.json")

cmd_attrs = {'name': 'yardım',
             'help': 'Bu mesajı gösterir.'}
# override !help command
class HelpFormat(DefaultHelpCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, command_attrs=cmd_attrs, **kwargs)

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

print("Logging in...")
_bot = bot.Bot(command_prefix=config.prefix, prefix=config.prefix, command_attrs=dict(hidden=True), help_command=HelpFormat())
_bot.run(config.token)