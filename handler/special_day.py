#!/usr/bin/env python
#coding:utf-8
import tornado.web
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpecialDayHandler(tornado.web.RequestHandler):

    def get(self, day):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        client = MongoClient('192.168.1.87')
        db = client.vionlabs
        col = db.tmdb_content

        if day == "0911":
            keyword = 'terror'
        elif day == '1210':
            keyword = 'nobel prize'
        elif day == '0204':
            keyword = 'cancer'

        docs = col.find({'tmdbKeyword.name': {'$exists': 'true', '$in': [keyword]}}, {'imdbID': 1, '_id': 0})

        result_dict = {}
        for doc in docs:
            result_dict[doc['imdbID']] = doc['imdbID']

        self.write(result_dict)