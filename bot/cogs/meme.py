# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import random
import praw

import discord
from utils import confparser, default, strings
from discord.ext import commands

class Meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.reddit = praw.Reddit(client_id='zAMDWabp1WMohA',
                                     client_secret=self.config.reddit_token,
                                     password=self.config.reddit_password,
                                     user_agent='Hmn-Bot',
                                     username='humanovan')

    def parse_meme(self, subreddit):
        is_valid_sub = self.check_subreddit(subreddit)

        if is_valid_sub:
            hot_posts = [post for post in self.reddit.subreddit(subreddit).hot(limit=10)]

            post = random.choice(hot_posts)
            # stickied post check
            while post.stickied:
                post = random.choice(hot_posts)

            post_data = {
                "img_url"       : post.url,
                "author"        : post.author.name,
                "title"         : post.title,
                "permalink"     : "https://reddit.com" + post.permalink,
                "upvote_count"  : post.ups,
                "is_stickied"   : post.stickied
            }
            return post_data
        else:
            return None

    def check_subreddit(self, subreddit):
        if subreddit in strings.meme_subreddits:
            return True
        return False

    @commands.command()
    async def meme(self, ctx, subreddit: str):
        """ Belirtilen subredditten bir meme gönderir 
        
            Gecerli subredditler:
                - dankmemes,
                - memeeconomy,
                - deepfriedmemes,
                - surrealmemes,
                - offensivememes,
                - 2meirl4meirl,
                - blackpeopletwitter,
                - okbuddyretard,
                - coaxedintoasnafu,
                - bikinibottomtwitter,
                - bonehurtingjuice,
                - iamverysmart,
                - me_irl,
                - meirl,
                - memes,
                - animemes,
                - suddenlygay,
                - ihavesex,
                - wholesomememes,
                - historymemes,
                - softwaregore,
                - turkeyjerky
        """
        meme_data = self.parse_meme(subreddit.lower())
        if meme_data is not None:
            embed = discord.Embed(title=" ", description=f"**[{meme_data['title']}]({meme_data['permalink']})**", color=0xFF0000)
            embed.set_author(name=f"r/{subreddit}", icon_url=strings.komut["redditico"])
            embed.set_footer(text=f"👍 {meme_data['upvote_count']} | Yaratıcı : u/{meme_data['author']}")
            embed.set_image(url=meme_data['img_url'])
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=" ", description=strings.komut["memeHata"], color=0xFF0000)
            embed.set_author(name="Hmn-Bot Yardım", icon_url=strings.komut["redditico"])
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Meme(bot))