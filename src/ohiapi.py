# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import json
import requests

ohi_api_key = os.environ['OHI_TOKEN']

def SendRegisterRequest(username, password, email):
    content = {"username" : username, "email" : email ,"password" : password, "api_key": ohi_api_key}
    r = requests.post("https://ohi-api.herokuapp.com/api/v1/register", timeout=2.0, json=content)
    data = r.json()
    response = json.dumps(data)
    return response

def SendLoginRequest(username, password):
    content = {"username" : username, "password" : password}
    r = requests.post("https://ohi-api.herokuapp.com/api/v1/login", timeout=2.0, json=content)
    data = r.json()
    response = json.dumps(data)
    return response

def SendGetUsersRequest():
    content = {"api_key": ohi_api_key}
    r = requests.post("https://ohi-api.herokuapp.com/api/v1/users", timeout=2.0, json=content)
    data = r.json()
    response = json.dumps(data)
    return response