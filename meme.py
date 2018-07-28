
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot reddit meme command

import random
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import json

def memeParse(subreddit):

    subURL = subredditAlgila(subreddit)

    if not subURL == "hata":
        memeStickied = "true"

        while memeStickied == "true":
    
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
        url = "https://www.reddit.com/r/dankmemes.json?count=15"
        return url

    elif subreddit ==  "memeeconomy":
        url = "https://www.reddit.com/r/MemeEconomy.json?count=15"
        return url

    elif subreddit ==  "deepfriedmemes":
        url = "https://www.reddit.com/r/DeepFriedMemes.json?count=15"
        return url

    elif subreddit ==  "me_irl":
        url = "https://www.reddit.com/r/me_irl.json?count=15"
        return url

    elif subreddit ==  "meirl":
        url = "https://www.reddit.com/r/meirl.json?count=15"
        return url

    elif subreddit ==  "memes":
        url = "https://www.reddit.com/r/memes.json?count=15"
        return url

    elif subreddit ==  "animemes":
        url = "https://www.reddit.com/r/Animemes.json?count=15"
        return url

    elif subreddit ==  "okbuddyretard":
        url = "https://www.reddit.com/r/okbuddyretard.json?count=15"
        return url

    elif subreddit ==  "anime_irl":
        url = "https://www.reddit.com/r/anime_irl.json?count=15"
        return url
    
    elif subreddit == "ihavesex":
        url = "https://www.reddit.com/r/ihavesex.json?count=15"
        return url

    elif subreddit == "surrealmemes":
        url = "https://www.reddit.com/r/surrealmemes.json?count=15"
        return url
    
    elif subreddit == "memes_of_the_dank":
        url = "https://www.reddit.com/r/memes_of_the_dank.json?count=15"
        return url
    
    elif subreddit == "offensivememes":
        url = "https://www.reddit.com/r/offensivememes.json?count=15"
        return url

    elif subreddit ==  "coaxedintoasnafu":
        url = "https://www.reddit.com/r/coaxedintoasnafu.json?count=15"
        return url

    elif subreddit ==  "notgayporn":
        url = "https://www.reddit.com/r/notgayporn.json?count=15"
        return url

    elif subreddit ==  "turkeyjerky":
        url = "https://www.reddit.com/r/turkeyjerky.json?count=15"
        return url

    elif subreddit ==  "blackpeopletwitter":
        url = "https://www.reddit.com/r/BlackPeopleTwitter.json?count=15"
        return url

    elif subreddit ==  "2meirl4meirl":
        url = "https://www.reddit.com/r/2meirl4meirl.json?count=15"
        return url

    else:
        url = "hata"
        return url