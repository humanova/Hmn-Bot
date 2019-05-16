
# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from datetime import datetime, timedelta

def GetTime():
    now = datetime.now()
    tr_timezone = 3
    tr_time = now + timedelta(hours=tr_timezone)
    return f"{tr_time.hour}:{tr_time.minute}"

def GetDate():
    now = datetime.now()
    tr_timezone = 3
    tr_time = now + timedelta(hours=tr_timezone)
    return f"{tr_time.hour}:{tr_time.minute}"


