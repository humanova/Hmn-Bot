import random
from discord.ext import commands
from utils import confparser, pasta, strings

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

    @commands.command()
    async def sence(self, ctx):
        """ Evet-hayır sorusuna cevap verir """
        opt = random.randint(1, 4)
        await ctx.send(strings.komut[f"sence{opt}"])

    @commands.command(aliases=['112'], hidden=True)
    async def yuzoniki(self, ctx):
        text = pasta.get_pasta("https://paste.ee/p/tzqyK")
        await ctx.send(text)

    @commands.command(aliases=['fırlat', 'firlat'])
    async def flip(self, ctx):
        """ Yazı-tura """
        coinsides = ['Yazı', 'Tura']
        await ctx.send(f"{ctx.author.name} **{random.choice(coinsides)}** fırlattı!")

    @commands.command(aliases=['l33t'])
    async def leet(self, ctx, message:str):
        """ 1337 """
        msg = message.replace('e', '3')
        msg = msg.replace('a', '4')
        msg = msg.replace('i', '1')
        msg = msg.replace('ı', '1')
        msg = msg.replace('s', '5')
        msg = msg.replace('o', '0')
        ctx.send(msg)

def setup(bot):
    bot.add_cog(Fun(bot))