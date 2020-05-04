# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details
import discord
import requests
from utils import confparser, permissions, default, strings
from discord.ext import tasks, commands
from io import BytesIO
import time
from operator import itemgetter
from tabulate import tabulate

API_URL = "https://bruh.uno/dchess/api"

chess_dict_tr = {
    "mate": "Mat",
    "outoftime": "Süre bitti",
    "draw": "Berabere",
    "black": "Siyah",
    "white": "Beyaz",
    "resign": "Çekilme"
}


class DChess(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.games = []

        self.chess_task_loop.start()

    def cog_unload(self):
        self.chess_task_loop.cancel()

    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    def parse_clock_setting(self, clock:str):
        try:
            s = clock.split("+")
            minutes = int(s[0])
            increment = round(int(s[1]))
            if minutes == 0: minutes = 5
            return {"minutes" : minutes, "increment": increment}
        except:
            return None

    async def send_create_match_request(self, host: discord.Member, guest: discord.Member, guild: discord.Guild,
                                        clock:dict=None):
        content = {"user_id": host.id,
                   "user_nick": str(host),
                   "opponent_id": guest.id,
                   "opponent_nick": str(guest),
                   "guild_id": guild.id}
        if clock:
            content.update(clock_minutes = clock['minutes'])
            content.update(clock_increment = clock['increment'])
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

    async def send_update_match_end_request(self, match_id: str):
        content = {"match_id": match_id}
        try:
            r = requests.post(f"{API_URL}/update_match_end", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_get_match_request(self, match_id: str):
        content = { "match_id": match_id}
        try:
            r = requests.post(f"{API_URL}/get_match", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_get_player_request(self, player_id, guild_id=None):
        content = {"player_id": player_id}
        if guild_id:
            content.update(guild_id=guild_id)
        try:
            r = requests.post(f"{API_URL}/get_player", timeout=4.0, json=content)
            response = r.json()
            return response
        except Exception as e:
            print(e)

    async def send_get_guild_request(self, guild_id):
        content = { "guild_id": guild_id}
        try:
            r = requests.post(f"{API_URL}/get_guild", timeout=4.0, json=content)
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

    async def get_player_stat_embed(self, player:discord.Member, guild:discord.Guild):
        pl = await self.send_get_player_request(player.id, guild.id)
        if pl['success']:
            embed = discord.Embed(title="İstatistikler", color=0x00ffff)
            embed.add_field(name="Oyuncu", value=f"<@{player.id}>", inline=True)
            embed.add_field(name="Guild Elo", value=f"{pl['guild_player']['elo']}", inline=True)
            embed.add_field(name="Maç", value=f"{pl['player']['matches']}", inline=False)
            embed.add_field(name="Kazanma", value=f"{pl['player']['wins']}", inline=True)
            embed.add_field(name="Berabere", value=f"{pl['player']['draws']}", inline=True)
            embed.add_field(name="Kaybetme", value=f"{pl['player']['loses']}", inline=True)
            if pl['player']['last_match_id'] != '':
                embed.add_field(name="Son oyun", value=f"https://lichess.org/{pl['player']['last_match_id']}",
                                inline=False)
            return embed
        else:
            embed = discord.Embed(title=" ", description="Oyuncu bulunamadı", color=0xFF0000)
            embed.set_author(name="Satranç", icon_url=strings.komut["chessico"])
            return embed

    @tasks.loop(seconds=1)
    async def chess_task_loop(self):
        if len(self.games) > 0:
            for game in self.games:
                # bad exception handling but yeah
                try:
                    game_data = await self.send_get_match_request(game["match_id"])
                    if not game["white_data"] and game['white_id']:
                        game["white_data"] = await self.send_get_player_request(player_id=game["white_id"])
                    if not game["black_data"] and game['black_id']:
                        game["black_data"] = await self.send_get_player_request(player_id=game["black_id"])

                    if game_data["success"] == False:
                        if time.time() - game["timestamp"] > 180:
                            try:
                                await game["msg"].channel.send(f"Oyun iptal edildi. <@{game['host'].id}>")
                                await game["msg"].delete()
                                self.games.remove(game)
                            except Exception as e:
                                print(e)

                    if game_data["success"] == True:
                        status = game_data["match"]["status"]
                        moves = game_data["match"]["moves"]
                        move_count = len(moves.split(" "))
                        match_type = game["match_type"]
                        match_clock = game["match_clock"]
                        game["moves"] = moves

                        preview_url = f"{API_URL}/get_match_preview/{game['match_id']}/{move_count}"
                        white_player = f"<@{game['white_id']}> ({int(game['white_data']['player']['elo'])})" if game['white_id'] else "Bilinmiyor"
                        black_player = f"<@{game['black_id']}> ({int(game['black_data']['player']['elo'])})" if game['black_id'] else "Bilinmiyor"

                        embed = discord.Embed(title=f":chess_pawn: {game['host'].name} vs {game['guest'].name}",
                                              color=0x00ffff)
                        embed.add_field(name="⚪Beyaz", value=white_player, inline=True)
                        embed.add_field(name="⚫Siyah", value=black_player, inline=True)
                        if match_type:
                            embed.add_field(name="Tür", value=f"{match_type} ({match_clock})", inline=True)
                        if status == "started":
                            if move_count > game["move_count"]:
                                embed.add_field(name="Durum", value="Devam ediyor", inline=False)
                                embed.add_field(name="URL", value=game["match_url"], inline=True)
                                embed.add_field(name="Hamleler", value=moves, inline=False)
                                embed.set_image(url=preview_url)

                                await game["msg"].edit(embed=embed)

                        elif status == "mate" or status == "outoftime" or status == "draw" or status == "resign":
                            m_data = await self.send_update_match_end_request(match_id=game["match_id"])

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
                except Exception as e:
                    print(f"Error in chess task loop : {e}")


    @commands.command()
    @commands.guild_only()
    async def chess(self, ctx, member: discord.Member, clock_setting:str=None):
        match = await self.send_create_match_request(host=ctx.author, guest=member, guild=ctx.guild,
                                                     clock=self.parse_clock_setting(clock_setting))
        #if match["success"]:
        #    print("successfully created match")
        match_id = match["db_match"]["id"]
        match_url = f"https://lichess.org/{match_id}"
        match_type = None
        match_clock = None

        # todo : fix copy-pasting embeds
        dm_embed = discord.Embed(title=":chess_pawn: Oyun Daveti", color=0x00ffff)
        dm_embed.add_field(name="Davet eden", value=f"<@{ctx.author.id}>", inline=True)
        if clock_setting:
            match_type = match['match']['challenge']['speed']
            match_clock = match['match']['challenge']['timeControl']['show']
            dm_embed.add_field(name="Tür", value=f"{match_type} ({match_clock})", inline=True)
        dm_embed.add_field(name="Guild", value=f"{ctx.guild.name}", inline=False)
        dm_embed.add_field(name="URL", value=f"{match_url}", inline=False)

        await member.send(embed=dm_embed)
        await ctx.author.send(embed=dm_embed)

        embed = discord.Embed(title=":chess_pawn: Oyun Daveti", color=0x00ffff)
        embed.add_field(name="Davet eden", value=f"<@{ctx.author.id}>", inline=True)
        if clock_setting:
            embed.add_field(name="Tür", value=f"{match_type} ({match_clock})", inline=True)
        embed.add_field(name="Guild", value=f"{ctx.guild.name}", inline=False)
        embed.add_field(name="URL", value=f"Özel mesaj olarak gönderildi.", inline=False)
        embed.set_footer(text="Oyun başladıktan sonra renginizi reaction bırakarak belirtin!")

        msg = await ctx.send(embed=embed)
        await msg.add_reaction('⚪')
        await msg.add_reaction('⚫')

        self.games.append({"msg": msg,
                           "match_id": match_id,
                           "match_url": match_url,
                           "match_type": match_type,
                           "match_clock": match_clock,
                           "host": ctx.author,
                           "guest": member,
                           "white_data": None,
                           "black_data": None,
                           "timestamp": time.time(),
                           "move_count": 0,
                           "moves": None,
                           "white_id": None,
                           "black_id": None})

    @commands.command()
    @commands.guild_only()
    async def cstats(self, ctx, arg=None):
        if not arg:
            embed = await self.get_player_stat_embed(ctx.author, ctx.guild)
            await ctx.send(embed=embed)
        elif arg:
            if ctx.message.mentions:
                for m in ctx.message.mentions:
                    embed = await self.get_player_stat_embed(m, ctx.guild)
                    await ctx.send(embed=embed)
            elif arg == "guild":
                g = await self.send_get_guild_request(ctx.guild.id)
                if g['success'] and len(g['guild']) > 0:
                    players = g['guild']
                    players = sorted(players, key=itemgetter('elo'), reverse=True)

                    top_players = []
                    for pl in players[:10]:
                        pl_nick = str(ctx.guild.get_member(int(pl['player_id'])))
                        top_players.append([pl_nick, pl['elo']])
                    table_str = tabulate(top_players, headers=["Player", "Guild elo"])
                    await ctx.send(f'```{table_str}```')
                else:
                    embed = discord.Embed(title=" ", description="Guild kaydı bulunamadı", color=0xFF0000)
                    embed.set_author(name="Satranç", icon_url=strings.komut["chessico"])
                    return embed

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