
# 2018 Emir Erbasan (humanova)
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

    if subreddit == "dankmemes":
        url = "https://www.reddit.com/r/dankmemes.json?limit=10"
        return url

    elif subreddit ==  "memeeconomy":
        url = "https://www.reddit.com/r/MemeEconomy.json?limit=10"
        return url

    elif subreddit ==  "deepfriedmemes":
        url = "https://www.reddit.com/r/DeepFriedMemes.json?limit=10"
        return url

    elif subreddit ==  "me_irl":
        url = "https://www.reddit.com/r/me_irl.json?limit=10"
        return url

    elif subreddit ==  "meirl":
        url = "https://www.reddit.com/r/meirl.json?limit=10"
        return url

    elif subreddit ==  "memes":
        url = "https://www.reddit.com/r/memes.json?limit=10"
        return url

    elif subreddit ==  "animemes":
        url = "https://www.reddit.com/r/Animemes.json?limit=10"
        return url

    elif subreddit ==  "okbuddyretard":
        url = "https://www.reddit.com/r/okbuddyretard.json?limit=10"
        return url

    elif subreddit ==  "anime_irl":
        url = "https://www.reddit.com/r/anime_irl.json?limit=10"
        return url
    
    elif subreddit == "ihavesex":
        url = "https://www.reddit.com/r/ihavesex.json?limit=10"
        return url

    elif subreddit == "surrealmemes":
        url = "https://www.reddit.com/r/surrealmemes.json?limit=10"
        return url
    
    elif subreddit == "memes_of_the_dank":
        url = "https://www.reddit.com/r/memes_of_the_dank.json?limit=10"
        return url
    
    elif subreddit == "offensivememes":
        url = "https://www.reddit.com/r/offensivememes.json?limit=10"
        return url

    elif subreddit ==  "coaxedintoasnafu":
        url = "https://www.reddit.com/r/coaxedintoasnafu.json?limit=10"
        return url

    elif subreddit ==  "notgayporn":
        url = "https://www.reddit.com/r/notgayporn.json?limit=10"
        return url

    elif subreddit ==  "turkeyjerky":
        url = "https://www.reddit.com/r/turkeyjerky.json?limit=10"
        return url

    elif subreddit ==  "blackpeopletwitter":
        url = "https://www.reddit.com/r/BlackPeopleTwitter.json?limit=10"
        return url

    elif subreddit ==  "2meirl4meirl":
        url = "https://www.reddit.com/r/2meirl4meirl.json?limit=10"
        return url

    elif subreddit == "dank_meme":
        url = "https://www.reddit.com/r/dank_meme.json?limit=10"
        return url

    elif subreddit == "edgymemes":
        url = "https://www.reddit.com/r/edgymemes.json?limit=10"
        return url

    elif subreddit == "wholesomememes":
        url = "https://www.reddit.com/r/wholesomememes.json?limit=10"
        return url
    
    elif subreddit == "historymemes":
        url = "https://www.reddit.com/r/HistoryMemes.json?limit=10"
        return

    elif subreddit == "ligma":
        url = "https://www.reddit.com/r/ligma.json?limit=10"
        return url

    else:
        url = "hata"
        return url