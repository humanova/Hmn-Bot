import discord
from utils import confparser, permissions, default
from discord.ext import commands

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(read_message_history=True)
    async def temizle(self, ctx, msg_count:int):
        """ Belirtilen miktarda mesajı siler """
        if not msg_count < 1 and not msg_count > 99:

            msgs = []
            async for message in discord.abc.Messageable.history(ctx.channel, limit=msg_count + 1):
                msgs.append(message)

            try:
                await ctx.channel.delete_messages(msgs)

                embed = discord.Embed(title=" ", color=0x75df00)
                embed.add_field(name="Temizle", value=f"Son **{msg_count}** mesaj silindi.", inline=False)
                delete_notify = await ctx.send(embed=embed)

                await delete_notify.delete(delay=3)
            except Exception as e:
                default.print_error(ctx, e)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def rolver(self, ctx, mem:discord.Member, role:discord.Role):
        """ Etiketlenen kullanıcıya etiketlenen rolü verir """
        try:
            await mem.add_roles(role)

            embed = discord.Embed(title=" ", color=0x75df00)
            embed.add_field(name="Rolver", value=f"<@{mem.id}> kullancısına **{role.name}** rolü verildi.", inline=False)
            delete_notify = await ctx.send(embed=embed)
        except Exception as e:
            default.print_error(ctx, e)



def setup(bot):
    bot.add_cog(Admin(bot))