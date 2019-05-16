
# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot reddit meme command

import random
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json
import praw

redditPassword = os.environ['REDDIT_PASS']
redditToken = os.environ['REDDIT_TOKEN']


reddit = praw.Reddit(client_id='zAMDWabp1WMohA',
                     client_secret=redditToken,
                     password= redditPassword,
                     user_agent='Hmn-Bot',
                     username='humanovan')

def memeParse(subreddit,is_top):

    subURL = subredditAlgila(subreddit)

    if not subURL == "hata":
        memeStickied = True

        if is_top:
            hot_posts = reddit.subreddit(subreddit).hot(limit=4)

            for post in hot_posts:
                if not post.stickied:
                    imgURL = post.url
                    memeAuthor = post.author.name
                    memeTitle = post.title 
                    permaLink = "https://reddit.com" + post.permalink
                    memeUpvote = post.ups
                    memeStickied = post.stickied
                    break

        else:
            
            subURL += ".json?limit=10"

            while memeStickied == True:
        
                data = urlopen(Request(subURL, headers={'User-Agent': 'Mozilla'})).read()
                page = json.loads(data.decode('utf-8'))

                meme = random.choice(page["data"]["children"])

                imgURL = meme["data"]["url"]
                memeAuthor = meme["data"]["author"]
                memeTitle = meme["data"]["title"]
                permaLink = "https://reddit.com" + meme["data"]["permalink"]
                memeUpvote = meme["data"]["ups"]
                memeStickied = meme["data"]["stickied"]

        return imgURL,memeAuthor,memeTitle,permaLink,memeUpvote

    else:
        imgURL = "hata"
        memeAuthor = "hata"
        memeTitle = "hata"
        permaLink = "hata"
        memeUpvote = "hata"
        return imgURL,memeAuthor,memeTitle,permaLink,memeUpvote


def subredditAlgila(subreddit):
    
    subs = {
        "dankmemes"          : "https://www.reddit.com/r/dankmemes",
        "memeeconomy"        : "https://www.reddit.com/r/MemeEconomy",
        "deepfriedmemes"     : "https://www.reddit.com/r/DeepFriedMemes",
        "me_irl"             : "https://www.reddit.com/r/me_irl",
        "meirl"              : "https://www.reddit.com/r/meirl",
        "memes"              : "https://www.reddit.com/r/memes",
        "animemes"           : "https://www.reddit.com/r/Animemes",
        "okbuddyretard"      : "https://www.reddit.com/r/okbuddyretard",
        "anime_irl"          : "https://www.reddit.com/r/anime_irl",
        "ihavesex"           : "https://www.reddit.com/r/ihavesex",
        "surrealmemes"       : "https://www.reddit.com/r/surrealmemes",
        "bikinibottomtwitter": "https://www.reddit.com/r/BikiniBottomTwitter",
        "iamverysmart"       : "https://www.reddit.com/r/iamverysmart",
        "bonehurtingjuice"   : "https://www.reddit.com/r/bonehurtingjuice",
        "memes_of_the_dank"  : "https://www.reddit.com/r/memes_of_the_dank",
        "offensivememes"     : "https://www.reddit.com/r/offensivememes",
        "coaxedintoasnafu"   : "https://www.reddit.com/r/coaxedintoasnafu",
        "notgayporn"         : "https://www.reddit.com/r/notgayporn",
        "suddenlygay"        : "https://www.reddit.com/r/SuddenlyGay",
        "turkeyjerky"        : "https://www.reddit.com/r/turkeyjerky",
        "blackpeopletwitter" : "https://www.reddit.com/r/BlackPeopleTwitter",
        "2meirl4meirl"       : "https://www.reddit.com/r/2meirl4meirl",
        "dank_meme"          : "https://www.reddit.com/r/dank_meme",
        "edgymemes"          : "https://www.reddit.com/r/edgymemes",
        "wholesomememes"     : "https://www.reddit.com/r/wholesomememes",
        "historymemes"       : "https://www.reddit.com/r/HistoryMemes",
        "softwaregore"       : "https://www.reddit.com/r/softwaregore",
        "ligma"              : "https://www.reddit.com/r/ligma"
    }

    try:
        data_url = subs[subreddit]
        return data_url
    except:
        return "hata"