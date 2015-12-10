#!/usr/bin/env python
#coding:utf-8
import tornado.web
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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

        client = MongoClient('192.168.1.87')
        db = client.vionlabs
        col = db.tmdb_content

        keyword = self.__get_holiday_keyword_dict(date)

        # if day == "20150911":
        #     keyword = 'terror'
        # elif day == '20151210':
        #     keyword = 'nobel prize'
        # elif day == '20150204':
        #     keyword = 'cancer'

        docs = col.find({'tmdbKeyword.name': {'$exists': 'true', '$in': [keyword]}}, {'imdbID': 1, '_id': 0})

        result_dict = {}
        movieid_list = []
        for doc in docs:
            movieid_list.append(doc['imdbID'])

        result_dict['specday_movies'] = movieid_list
        result_dict['day_keyword'] = keyword
        client.close()

        self.write(result_dict)