# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# moderation related commands
# mostly from : github.com/Rapptz/RoboDanny

import discord
from utils import confparser, permissions, default
from discord.ext import commands

def responsible(target, reason):
    responsible = f"[ {target} ]"
    if reason is None:
        return f"{responsible} no reason given..."
    return f"{responsible} {reason}"

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m.id


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
            await ctx.send(embed=embed)
        except Exception as e:
            default.print_error(ctx, e)

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """ Etiketlenen kullanıcıyı sunucudan atar """
        if await permissions.check_priv(ctx, member):
            return

        try:
            await member.kick(reason=responsible(ctx.author, reason))
            await ctx.send(f"{str(member)} sunucudan **atıldı**.")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def ban(self, ctx, member: MemberID, *, reason: str = None):
        """ ID'si girilen kullanıcıyı sunucudan yasaklar """
        m = ctx.guild.get_member(member)
        if m is not None and await permissions.check_priv(ctx, m):
            return

        try:
            await ctx.guild.ban(discord.Object(id=member), reason=responsible(ctx.author, reason))
            await ctx.send(f"{str(member)} sunucudan **yasaklandı**.")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(ban_members=True)
    async def unban(self, ctx, member: MemberID, *, reason: str = None):
        """ ID'si girilen kullanıcının yasağını kaldırır """
        try:
            await ctx.guild.unban(discord.Object(id=member), reason=responsible(ctx.author, reason))
            await ctx.send(f"{str(member)} kullanıcısının yasağı kaldırıldı.")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = None):
        """ ID'si girilen kullanıcıyı susturur (Muted rolü) """
        if await permissions.check_priv(ctx, member):
            return

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("Bu sunucuda 'Muted' rolü yok.")

        try:
            await member.add_roles(muted_role, reason=responsible(ctx.author, reason))
            await ctx.send(f"{str(member)} **susturuldu**.")
        except:
            pass

    @commands.command()
    @commands.guild_only()
    @permissions.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member, *, reason: str = None):
        """ ID'si girilen kullanıcının Muted rolünü siler """
        if await permissions.check_priv(ctx, member):
            return

        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)

        if not muted_role:
            return await ctx.send("Bu sunucuda 'Muted' rolü yok.")

        try:
            await member.remove_roles(muted_role, reason=responsible(ctx.author, reason))
            await ctx.send(f"{str(member)} kullanıcısının susturulması kaldırıldı.")
        except:
            pass


def setup(bot):
    bot.add_cog(Admin(bot))