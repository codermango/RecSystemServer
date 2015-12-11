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

class SpecialDayHandler(tornado.web.RequestHandler):

    def __get_holiday_keyword_dict(self, date):
        holiday_keyword_dict = {}
        with open('/home/mark/Projects/Docker/RecSystemServer/data/holiday_keywords.txt') as holiday_keywords_file:
            for line in holiday_keywords_file:
                date_line = line[:8].strip()
                if date_line == date:
                    keywords = line[8:].strip().lower()
                    if ' ' in keywords:
                        continue
                    return keywords


    def get(self, date):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        client = MongoClient(DB_HOST)
        db = client[DB_NAME]
        col = db[DB_COLLECTION]

        keyword = self.__get_holiday_keyword_dict(date)

        docs = col.find({'tmdbKeyword.name': {'$exists': 'true', '$in': [keyword]}}, {'imdbID': 1, '_id': 0})

        result_dict = {}
        movieid_list = []
        for doc in docs:
            movieid_list.append(doc['imdbID'])

        result_dict['specday_movies'] = movieid_list
        result_dict['day_keyword'] = keyword
        client.close()

        self.write(result_dict)