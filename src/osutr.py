import os
import codecs

log_path = os.environ['OSUTR_PATH']

def GetChat(lines):

    chat = ""
    with codecs.open(log_path, "r", "utf-8") as f:
        data = f.readlines()
    
    try:
        chat = "".join(data[-lines:])
    except Exception as e:
        print(f"error while getting chat log : {e}")

    chat = chat.replace("`", "")  

    return chat