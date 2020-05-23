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
from discord_argparse import ArgumentConverter, RequiredArgument, OptionalArgument

font_file = f"../mrender/fonts/impact.ttf"
param_converter = ArgumentConverter(
    src=OptionalArgument(
        str,
        doc="source flag (youtube = y, other = n)",
        default="n"
    ),
    fontsize=OptionalArgument(
        int,
        doc="font size",
        default=100
    ),
    speed=OptionalArgument(
        float,
        doc="new video speed",
        default = 1.0
    )
)

class MRender(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def render(self, inputs, outputs):
        try:
            ff = ffmpy.FFmpeg(
                inputs=inputs,
                outputs=outputs
            ).run()
            return ff
        except Exception as e:
            print(f"Error in MRender.render() : {e}")
            return None

    @commands.command()
    @commands.guild_only()
    @commands.check(permissions.is_owner)
    async def mr(self, ctx, url:str, upper_text:str, lower_text:str, *, params:param_converter=param_converter.defaults()):
        source = params['src']
        font_size = params['fontsize']
        speed = params['speed']

        filename = "ytvideo" if source == "y" else os.path.basename(urlparse(url).path)
        dl_path = f"../mrender/"
        dl_filename = f"{int(time.time())}_{filename}"
        dl_file_path = f"{dl_path}{dl_filename}"
        out_file_path = f"{dl_path}{int(time.time())}_{filename}_out.mp4"

        upper_text = upper_text.replace("_", " ")
        lower_text = lower_text.replace("_", " ")
        try:
            if source == "n":
                subprocess.call(['python', 'utils/download.py', url, dl_file_path])
            elif source == "y":
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

            self.render(inputs={dl_file_path: None}, outputs={out_file_path: out_args})

            if not speed == 1.0:
                out_file_path_s = f"{out_file_path[:-4]}_s.mp4"
                out_args = ["-loglevel", "warning",
                            "-g", "300",
                            "-preset", "veryfast",
                            "-filter_complex", f"[0:v]setpts={1 / speed}*PTS[v];[0:a]atempo={speed}[a]",
                            "-map", "[v]",
                            "-map", "[a]"]
                self.render(inputs={out_file_path: None}, outputs={out_file_path_s: out_args})
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