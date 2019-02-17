# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import json
import requests
from datetime import datetime,timedelta
from tabulate import tabulate

#ohi_api_key = os.environ['OHI_TOKEN']
ohi_api_key = "a0aa809b3b4e7ba9a33bfbaa46b27cb3"

def time_diff_to_timestamp(timestamp):
    now = datetime.now()
    end_date = datetime.fromtimestamp(int(timestamp))
    if not isexpired(now, end_date):
        diff = days_hours_minutes(end_date - now)
        return diff
    else:
        return None

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def isexpired(now, end):
    diff = (now - end).total_seconds()
    if diff > 0:
        return True
    else:
        return False
        

def RegisterRequest(username, password, email):
    content = {"username" : username, "email" : email ,"password" : password, "api_key": ohi_api_key}
    try:
        r = requests.post("https://ohi-api.herokuapp.com/api/v1/register", timeout=4.0, json=content)
        data = r.json()
        response = json.dumps(data)
        return response
    except Exception as e:
        return e

def LoginRequest(username, password):
    content = {"username" : username, "password" : password}
    try:
        r = requests.post("https://ohi-api.herokuapp.com/api/v1/login", timeout=4.0, json=content)
        data = r.json()
        response = json.dumps(data)
        return response
    except Exception as e:
        return e

def GetXUsersRequest():
    content = {"api_key": ohi_api_key}
    try:
        r = requests.post("https://ohi-api.herokuapp.com/api/v1/users", timeout=4.0, json=content)
        data = r.json()
        response = json.dumps(data)
        return response
    except Exception as e:
        return e

def GetUsersRequest():
    content = {"api_key": ohi_api_key}
    try:
        r = requests.post("https://ohi-api.herokuapp.com/api/v1/users", timeout=4.0, json=content)
        data = r.json()
        a = 0
        Users = [[0 for x in range(3)] for y in range(len(data['data']))] 
        for user in data['data']:
            Users[a][0] = user["username"]
            Users[a][1] = user["account_type"]

            timestamp = user["sub_end_timestamp"]
            diff = time_diff_to_timestamp(timestamp)
            if not diff == None:
                Users[a][2] = f"{diff[0]}g {diff[1]}s {diff[2]}dk"
            else:
                Users[a][2] = "bitti"
            a += 1

        table = tabulate(Users, ["username", "acc_type", "kalan_sure"], tablefmt="orgtbl")
        return table
    except Exception as e:
        return e

def ChangeUserSubTimeRequest(username, hour_addition):
    content = {"api_key": ohi_api_key, "username": username, "hour_addition": hour_addition}
    try:
        r = requests.post("https://ohi-api.herokuapp.com/api/v1/change_sub_time", timeout=4.0, json=content)
        data = r.json()
        
        result = ""
        if data['success'] == True:
            result = "Sure eklendi : "
            new_timestamp = data['new_timestamp']
            diff = time_diff_to_timestamp(new_timestamp)
            new_remaining_time = f"{diff[0]}g {diff[1]}s {diff[2]}dk"
            result += f"yeni bitis tarihi : {datetime.fromtimestamp(int(new_timestamp))} , kalan sure : {new_remaining_time}"  
                
        return result
    except Exception as e:
        return e