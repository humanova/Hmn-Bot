import music
  
message = "!soz Human Rag"
msg = message.split(" ")
msg = " ".join(msg[1:])

try:
    if msg[0:]:
        if "-" in msg:
            sarki = msg[0:msg.find('-')]
            artist = msg[msg.find('-') + 1:]

        else:
            sarki = msg[0:]
            artist = ""
    else:
        flag = False
except:
    flag = False
  
music.sozParse("","Human - Rag")