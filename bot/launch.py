import bot
from utils import confparser

config = confparser.get("config.json")

print("Logging in...")
_bot = bot.Bot(command_prefix=config.prefix, prefix=config.prefix, command_attrs=dict(hidden=True))
_bot.run(config.token)