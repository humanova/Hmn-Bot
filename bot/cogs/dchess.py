# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
import discord
import requests
from utils import confparser, permissions, default
from discord.ext import tasks, commands
from io import BytesIO
import time

API_URL = "https://bruh.uno/dchess/api"

chess_dict_tr = {
    "mate": "Mat",
    "outoftime": "Süre bitti",
    "draw": "Berabere",
    "black": "Siyah",
    "white": "Beyaz"
}


class DChess(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.games = []

        self.check_concurrent_games.start()

    def cog_unload(self):
        self.check_concurrent_games.cancel()

    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    async def send_create_match_request(self, host: discord.Member, guest: discord.Member, guild: discord.Guild):
        content = {"user_id": host.id,
                   "user_nick": str(host),
                   "opponent_id": guest.id,
                   "opponent_nick": str(guest),
                   "guild_id": guild.id}
        try:
            r = requests.post(f"{API_URL}/create_match", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_update_match_request(self, match_id: str, result: str, white_id :str, black_id: str):
        content = {"match_id": match_id,
                   "match_result": result,
                   "white_id": white_id,
                   "black_id": black_id}
        try:
            r = requests.post(f"{API_URL}/update_match", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_get_match_request(self, match_id: str):
        content = { "match_id": match_id }
        try:
            r = requests.post(f"{API_URL}/get_match", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_get_player_request(self, player_id):
        content = { "player_id": player_id }
        try:
            r = requests.post(f"{API_URL}/get_player", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    # returns png obj
    async def send_get_match_preview_request(self, match_id: str, move):
        try:
            r = requests.get(f"{API_URL}/get_match_preview/{match_id}/{move}.png", timeout=4.0)
            return BytesIO(r.content)
        except Exception as e:
            print(e)

    @tasks.loop(seconds=0.1)
    async def check_concurrent_games(self):
        if len(self.games) > 0:
            for game in self.games:
                game_data = await self.send_get_match_request(game["match_id"])
                if not game["white_data"] and game['white_id']:
                    game["white_data"] = await self.send_get_player_request(player_id=game["white_id"])
                if not game["black_data"] and game['black_id']:
                    game["black_data"] = await self.send_get_player_request(player_id=game["black_id"])

                if game_data["success"] == False:
                    if time.time() - game["timestamp"] > 180:
                        try:
                            game["msg"].channel.send(f"Oyun iptal edildi. <@{game['host'].id}>")
                            game["msg"].delete()
                            self.games.remove(game)
                        except Exception as e:
                            print(e)

                if game_data["success"] == True:
                    status = game_data["match"]["status"]
                    moves = game_data["match"]["moves"]
                    move_count = len(moves.split(" "))

                    game["moves"] = moves
                    preview_url = f"{API_URL}/get_match_preview/{game['match_id']}/{len(moves)}"
                    white_player = f"<@{game['white_id']}> ({game['white_data']['player']['elo']})" if game['white_id'] else "Bilinmiyor"
                    black_player = f"<@{game['black_id']}> ({game['black_data']['player']['elo']})" if game['black_id'] else "Bilinmiyor"

                    embed = discord.Embed(title=f":chess_pawn: {game['host'].name} vs {game['guest'].name}",
                                          color=0x00ffff)
                    embed.add_field(name="⚪Beyaz", value=white_player, inline=True)
                    embed.add_field(name="⚫Siyah", value=black_player, inline=True)
                    if status == "started":
                        if move_count > game["move_count"]:
                            embed.add_field(name="Durum", value="Devam ediyor", inline=False)
                            embed.add_field(name="URL", value=game["match_url"], inline=True)
                            embed.add_field(name="Hamleler", value=moves, inline=False)
                            embed.set_image(url=preview_url)

                            await game["msg"].edit(embed=embed)

                    elif status == "mate" or status == "outoftime" or status == "draw":
                        status_tr = chess_dict_tr[status]
                        embed.add_field(name="Durum", value=status_tr, inline=False)
                        if not status == "draw":
                            winner = game_data["match"]["winner"]
                            winner_player = f"<@{game[f'{winner}_id']}>" if game[f'{winner}_id'] else chess_dict_tr[winner]
                            embed.add_field(name="Kazanan", value=winner_player, inline=True)
                        embed.add_field(name="URL", value=game["match_url"], inline=False)
                        embed.add_field(name="Hamleler", value=moves, inline=True)
                        embed.set_image(url=preview_url)

                        await game["msg"].edit(embed=embed)
                        self.games.remove(game)
                    game["move_count"] = move_count

    @commands.command()
    @commands.guild_only()
    @commands.check(permissions.is_owner)
    async def chess(self, ctx, member: discord.Member):

        match = await self.send_create_match_request(host=ctx.author, guest=member, guild=ctx.guild)
        #print(match)
        #if match["success"]:
        #    print("successfully created match")
        match_id = match["db_match"]["id"]
        match_url = f"https://lichess.org/{match_id}"

        dm_embed = discord.Embed(title=":chess_pawn: Oyun Daveti", color=0x00ffff)
        dm_embed.add_field(name="Rakip", value=f"<@{ctx.author.id}>", inline=True)
        dm_embed.add_field(name="Guild", value=f"{ctx.guild.name}", inline=True)
        dm_embed.add_field(name="URL", value=f"{match_url}", inline=False)

        await member.send(embed=dm_embed)
        await ctx.author.send(embed=dm_embed)

        embed = discord.Embed(title=":chess_pawn: Oyun Daveti", color=0x00ffff)
        embed.add_field(name="Rakip", value=f"<@{ctx.author.id}>", inline=True)
        embed.add_field(name="Guild", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name="URL", value=f"Özel mesaj olarak gönderildi.", inline=False)
        embed.set_footer(text="Oyun başladıktan sonra renginizi reaction bırakarak belirtin!")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⚪')
        await msg.add_reaction('⚫')

        self.games.append({"msg": msg,
                           "match_id": match_id,
                           "match_url": match_url,
                           "host": ctx.author,
                           "guest": member,
                           "white_data": None,
                           "black_data": None,
                           "timestamp": time.time(),
                           "move_count": 0,
                           "moves": None,
                           "white_id": None,
                           "black_id": None})

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        for g in self.games:
            if user.id == g["host"].id or user.id == g["guest"].id:
                if reaction.message.id == g["msg"].id:
                    if user.id == g["host"].id:
                        if reaction.emoji == "⚪":
                            g["white_id"] = user.id
                        elif reaction.emoji == '⚫':
                            g["black_id"] = user.id
                    else:
                        if reaction.emoji == "⚪":
                            g["white_id"] = user.id
                        elif reaction.emoji == '⚫':
                            g["black_id"] = user.id

                    if g["white_id"] is not None and g["black_id"] is not None:
                        if not g["white_id"] == g["black_id"]:
                            match = await self.send_update_match_request(match_id=g["match_id"], result="unfinished",
                                                                         white_id=g["white_id"], black_id=g["black_id"])
                            #if match["success"]:
                            #    print("successfully updated match")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        for g in self.games:
            if user.id == g["host"].id or user.id == g["guest"].id:
                if reaction.message.id == g["msg"].id:
                    if user.id == g["host"].id:
                        if reaction.emoji == "⚪":
                            g["white_id"] = None
                        elif reaction.emoji == '⚫':
                            g["black_id"] = None
                    else:
                        if reaction.emoji == "⚪":
                            g["white_id"] = None
                        elif reaction.emoji == '⚫':
                            g["black_id"] = None

def setup(bot):
    bot.add_cog(DChess(bot))