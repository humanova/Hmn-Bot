import discord
from . import confparser
from discord.ext import commands

owners = confparser.get("config.json").owners


def is_owner(ctx):
    return ctx.author.id in owners


async def check_permissions(ctx, perms, *, check=all):
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)


async def check_priv(ctx, member):
    try:
        if member == ctx.author:
            return await ctx.send(f"Kendine **{ctx.command.name}** komutunu uygulayamazsın.")
        if member.id == ctx.bot.user.id:
            return await ctx.send(":monkey:")

        if ctx.author.id == ctx.guild.owner.id:
            return False

        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.send(f":monkey:")
            else:
                pass
        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"Sunucu sahibine **{ctx.command.name}** komutunu uygulayamazsın.")
        if ctx.author.top_role == member.top_role:
            return await ctx.send(f"Senle aynı yetkiye sahip birine **{ctx.command.name}** komutunu uygulayamazsın.")
        if ctx.author.top_role < member.top_role:
            return await ctx.send(f"Senle daha yüksek yetkiye sahip birine **{ctx.command.name}** komutunu uygulayamazsın.")
    except Exception:
        pass

def can_send(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).send_messages


def can_embed(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).embed_links


def can_upload(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).attach_files


def can_react(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions


def is_nsfw(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw()