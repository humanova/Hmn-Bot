
# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

#hmnBot sarki sozu

import os
import lyricsgenius as genius

token = os.environ['GENIUS_TOKEN']
api = genius.Genius(token)

def sozParse(artist,sarki):

    song = api.search_song(sarki,artist)

    if not song == None:
        sarkiAdi = song.title
        sarkiArtist = song.artist
        sarkiLink = song.url
        
        lyrics = song.save_lyrics(filename="lyrics_test.txt",format="txt",overwrite="no")
        if not '```' in lyrics: 
            return lyrics,sarkiAdi,sarkiArtist,sarkiLink
        else:
            return None, None, None, None
    
    else:

        return None, None, None, None



