
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more detail

import meme_test as meme


subreddit = "ligma"


meme_url,meme_author,meme_title,perma_link,meme_upvote = meme.memeParse(subreddit)

print(meme_title + " : " + meme_url)





'''
import music
  

message = "!soz thriller"
flag = True
msg = message.split(" ")
msg = " ".join(msg[1:])


try:
    if msg[0:]:
        sarki = msg[0:]
        artist = ""
except:
    flag = False

if not flag == False:
    
    sozler,sarki_adi,sarki_artist = music.sozParse(artist,sarki)
    print(sozler)
'''
    
