# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# warning : some shitty rendering code below :)
import os
import discord
import time
import subprocess
from utils import confparser, default, permissions
from discord.ext import commands
from urllib.parse import urlparse
from pytube import YouTube
import ffmpy

font_file = f"../mrender/fonts/impact.ttf"

class MRender(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")

    @commands.command()
    @commands.guild_only()
    @commands.check(permissions.is_owner)
    async def mr(self, ctx, url:str, upper_text:str, lower_text:str, args:str=None, font_size:int=100):
        args = [c for c in args]
        filename = "ytvideo" if args == "y" else os.path.basename(urlparse(url).path)
        dl_path = f"../mrender/"
        dl_filename = f"{int(time.time())}_{filename}"
        dl_file_path = f"{dl_path}{dl_filename}"
        out_file_path = f"{dl_path}{int(time.time())}_{filename}_out.mp4"

        upper_text = upper_text.replace("_", " ")
        lower_text = lower_text.replace("_", " ")
        try:
            if not "y" in args:
                subprocess.call(['python', 'utils/download.py', url, dl_file_path])
            elif "y" in args:
                vid = YouTube(url).streams.get_by_resolution("480p")
                if vid:
                    vid.download(output_path=dl_path, filename=dl_filename)
                else:
                    YouTube(url).streams.get_highest_resolution().download(output_path=dl_path, filename=dl_filename)
                dl_file_path += ".mp4"

            out_args = ["-loglevel", "warning",
                        "-g", "300",
                        "-preset", "veryfast",
                        "-vf", f'drawtext=fontfile={font_file}:text={upper_text}:fontcolor=white:fontsize={font_size}:shadowcolor=black:shadowx=5:shadowy=5:box=0:x=(w-text_w)/2:y=(h-text_h)/8,drawtext=fontfile={font_file}:text={lower_text}:fontcolor=white:fontsize={font_size}:shadowcolor=black:shadowx=5:shadowy=5:box=0:x=(w-text_w)/2:y=(h-text_h)/8*7']

            ff = ffmpy.FFmpeg(
                inputs = {dl_file_path: None},
                outputs = {out_file_path: out_args}
            ).run()
            if "s" in args:
                factor = int(args[args.index('s')+1])
                out_file_path_s = f"{out_file_path[:-4]}_s.mp4"
                out_args = ["-loglevel", "warning",
                            "-g", "300",
                            "-preset", "veryfast",
                            "-filter_complex", f"[0:v]setpts={1 / factor}*PTS[v];[0:a]atempo={factor}[a]",
                            "-map", "[v]",
                            "-map", "[a]"]
                ff = ffmpy.FFmpeg(
                    inputs={out_file_path: None},
                    outputs={out_file_path_s: out_args}
                ).run()
                await ctx.send(file=discord.File(fp=out_file_path_s, filename=f"{filename}_out_s.mp4"))
                os.remove(out_file_path_s)
            else:
                await ctx.send(file=discord.File(fp=out_file_path, filename=f"{filename}_out.mp4"))

            os.remove(dl_file_path)
            os.remove(out_file_path)
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(MRender(bot))