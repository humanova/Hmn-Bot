
# 2018 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

class DB:

    def __init__(self, DATABASE_URL = DATABASE_URL):
        self.db_url = DATABASE_URL
        self.cur = None
        self.is_connected = False
        
    def Connect(self):

        try:
            conn = psycopg2.connect(DATABASE_URL, sslmode = 'require')
            self.is_connected = True
        except:
            print(f"couldn't connec to database, url = {DATABASE_URL}")
            self.is_connected = False
            self.cur = conn.cursor

    def Execute(self, command):

        try:
            self.cur.execute(command)
            rows = self.cur.fetchall()

        except Exception as e :
            print(f"DB Error while executing command :'{command}' -> {e}")
            return None
    
        return rows
