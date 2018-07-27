
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot reddit meme command

import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json

def memeParse(subreddit):

    imgURL = "giris"

    while imgURL == "https://www.polltab.com" or imgURL == "https://i.imgur.com/qNGc9uX.png" or imgURL == "giris":
        if subreddit == "dankmemes":
            memeURL = "https://www.reddit.com/r/dankmemes.json?count=20"

        else :
            imgURL = "hata"
            break


        data = urlopen(Request(memeURL, headers={'User-Agent': 'Mozilla'})).read()
        page = json.loads(data.decode('utf-8'))

        meme = random.choice(page["data"]["children"])

        imgURL = meme["data"]["url"]
        memeAuthor = meme["data"]["author"]
        memeTitle = meme["data"]["title"]
        permaLink = "https://reddit.com" + meme["data"]["permalink"]
        memeUpvote = meme["data"]["ups"]

    return imgURL,memeAuthor,memeTitle,permaLink,memeUpvote



    