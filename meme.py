
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot reddit meme command

import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def memeParse(subreddit):

    if subreddit == "dankmemes":
        memeURL = "https://www.reddit.com/r/dankmemes.json"

    else :
        imgURL = "hata"
        return imgURL


    data = urlopen(Request(memeURL, headers={'User-Agent': 'Mozilla'})).read()
    page = data.json()

    imgURL = random.choice(page["data"]["children"])["data"]["url"]

    return imgURL



    