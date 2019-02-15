# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import json
import requests

def SendRegisterRequest(username, password, email):
    content = {"username" : username, "email" : email ,"password" : password}
    r = requests.post("https://ohi-api.herokuapp.com/api/v1/register", timeout=2.0, json=content)
    data = r.json()
    response = json.dumps(data)
    return response