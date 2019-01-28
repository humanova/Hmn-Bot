
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import datetime
from psycopg2 import *
from peewee import * 

DATABASE_NAME = os.environ['DATABASE_NAME']
DATABASE_URL = os.environ['DATABASE_URL']
DATABASE_USER = os.environ['DATABASE_USER']
DATABASE_PASS = os.environ['DATABASE_PASS']
DATABASE_HOST = os.environ['DATABASE_HOST']

db = PostgresqlDatabase(
    DATABASE_NAME,  # Required by Peewee.
    user=DATABASE_USER,  # Will be passed directly to psycopg2.
    password=DATABASE_PASS,  # Ditto.
    host=DATABASE_HOST)  # Ditto.

class BaseModel(Model):
    class Meta:
        database = db

class Video(BaseModel):
    command = CharField(unique=True)
    url = CharField()
    nick = CharField()
    date = DateTimeField()

class VideoPermUser(BaseModel):
    user_id = CharField(unique=True)
    nick = CharField()
    server_id = CharField()
    date = DateTimeField()

class DB:

    def __init__(self):

        self.is_connected = False
    
    def InitDatabase(self):
        try:
            db.create_tables([Video, VideoPermUser])
        except Exception as e:
            print("Couldn't create the tables, it may already exist on the database...")
            print(e)

    def Connect(self):

        try:
            db.connect()
            self.is_connected = True
        except:
            print(f"couldn't connect to database")
            self.is_connected = False

    def AddPermUser(self, user_id, nick, server_id):
        try:
            with db.atomic():
                vid_perm = VideoPermUser.create(
                    user_id= user_id,
                    nick= nick,
                    server_id= server_id,
                    date= datetime.datetime.now(),
                )
                print(f"[DB] Added a new VideoPermUser -> user_id : {user_id}")
                return vid_perm

        except Exception as e:
            print(f'Error while adding perm user : {e}')

    def GetPermUser(self, user_id):
        try:
            perm_user = VideoPermUser.select().where(VideoPermUser.user_id == user_id).get()
        except:
            print(f"[DB] Couldn't find any VideoPermUser attached to this user_id : {user_id}")
            return None
        return perm_user

    def AddVideo(self, command, url, nick):
        try:
            with db.atomic():
                video = Video.create(
                    command= command,
                    url= url,
                    nick= nick,
                    date= datetime.datetime.now(),
                )
                print(f"[DB] Added a new video -> command : {command}")
                return video
        except Exception as e:
            print(f'Error while creating video row : {e}')
        

    def GetVideo(self, cmd):
        try:
            video = Video.select().where(Video.command == cmd).get()
        except:
            print(f"[DB] Couldn't find any video attached to this command : {cmd}")
            return None
        return video