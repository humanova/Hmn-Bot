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

    
