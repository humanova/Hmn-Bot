
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
            memeURL = "https://www.reddit.com/r/dankmemes.json"

        else :
            imgURL = "hata"
            return imgURL


        data = urlopen(Request(memeURL, headers={'User-Agent': 'Mozilla'})).read()
        page = json.loads(data.decode('utf-8'))

        imgURL = random.choice(page["data"]["children"])["data"]["url"]


    return imgURL



    