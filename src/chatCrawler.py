import codecs
import requests

API_URL = "http://173.249.51.133:5000/osuTR-API/v1/get_messages"
LOG_PATH = "../log/osutr-log.txt"

def RequestChatLog(url = API_URL):

    request_content = {"lineIndex": "1"}
    try:
        r = requests.post(API_URL, timeout = 10.0, json=request_content)
        data = r.json()

        if data['success'] == True:
            return data['messages']
        else:
            print("chat API returned false")
            return None
    except Exception as e:
        print("error while requesting chat : " , e)
        return None

def GetMessages():
    
    msgs = RequestChatLog()
    if not msgs == None:
        file = codecs.open(LOG_PATH, "w+", "utf-8")
        for msg in msgs:
            file.write(msg)

        return LOG_PATH
    else:
        return None