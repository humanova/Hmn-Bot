# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import bot
from utils import confparser, permissions
config = confparser.get("config.json")


print("Logging in...")
_bot = bot.Bot(command_prefix=config.prefix, prefix=config.prefix, command_attrs=dict(hidden=True))
_bot.run(config.token)