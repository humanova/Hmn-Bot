# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot reddit meme command

import random
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json
import praw
import botStrings

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

    for sub in botStrings.memeSubreddits:
        if sub in subreddit:
            data_url = "https://reddit.com/r/" + subreddit
            return data_url
    
    return "hata"