import requests
import json
from array import *
from datetime import datetime, timezone, timedelta

from tabulate import tabulate
import ohiapi
      
ohi_api_key = "a0aa809b3b4e7ba9a33bfbaa46b27cb3"
def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

def isexpired(now, end):
    diff = (now - end).total_seconds()
    if diff > 0:
        return True
    else:
        return False

def Test():
    content = {"api_key": ohi_api_key}
    r = requests.post("https://ohi-api.herokuapp.com/api/v1/users", timeout=5.0, json=content)
    data = r.json()
    a = 0
    Users = [[0 for x in range(3)] for y in range(len(data['data']))] 
    for user in data['data']:
        Users[a][0] = user["username"]
        Users[a][1] = user["account_type"]

        timestamp = user["sub_end_timestamp"]
        now = datetime.now()
        end_date = datetime.fromtimestamp(int(timestamp))
        if not isexpired(now, end_date):
            diff = days_hours_minutes(end_date - now)
            Users[a][2] = f"{diff[0]}g {diff[1]}s {diff[2]}dk"
        else:
            Users[a][2] = "bitti"

        a += 1
        
    table = tabulate(Users, ["username", "acc_type", "kalan_sure"], tablefmt="orgtbl")
    return table

#print(ohiapi.RegisterRequest("test5", "test5", "test5@hotmail.com"))

print(ohiapi.ChangeUserSubTimeRequest("test5", "15"))
print(ohiapi.GetUsersRequest())

#print tabulate([["value1", "value2"], ["value3", "value4"]], ["column 1", "column 2"], tablefmt="grid")