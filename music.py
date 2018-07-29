
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot muzik ve altyazi

import os
import lyricsgenius as genius

token = os.environ['GENIUS_TOKEN']
api = genius.Genius(token)

def sozParse(artist,sarki):

    bulundu_flag = True

    try:
        song = api.search_song(sarki,artist)
    except:        
        bulundu_flag = False

    if bulundu_flag:
        sarkiAdi = song.title
        sarkiArtist = song.artist
        sarkiLink = song.url
        
        lyrics = song.save_lyrics(filename="lyrics_test.txt",format="txt",overwrite="no")
        
        return lyrics,sarkiAdi,sarkiArtist,sarkiLink
    
    else:
        lyrics = "hata"
        sarkiAdi = "hata"
        sarkiArtist = "hata"
        sarkiLink = "hata"

        return lyrics,sarkiAdi,sarkiArtist,sarkiLink



