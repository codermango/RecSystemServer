#!/usr/bin/env python
#coding:utf-8
import tornado.web
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


DB_HOST = '192.168.1.87'
DB_PORT = 27017
DB_NAME = 'vionlabs'
DB_COLLECTION = 'tmdb_content'

class HolidayKeywordHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        client = MongoClient(DB_HOST)
        db = client[DB_NAME]
        col = db[DB_COLLECTION]

        holiday_keyword_dict = {}
        with open('/home/mark/Projects/Docker/RecSystemServer/data/holiday_keywords.txt') as holiday_keywords_file:
            for line in holiday_keywords_file:
                date_line = line[:8].strip()
                keywords = line[8:].strip().lower()
                if ' ' in keywords:
                    continue
                holiday_keyword_dict[date_line] = keywords

        self.write(holiday_keyword_dict)