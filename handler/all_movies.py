#!/usr/bin/env python
#coding:utf-8
import sys
import tornado.web
from pymongo import MongoClient


DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = 'VionelDB'
DB_COLLECTION = 'Plejmo'

reload(sys)
sys.setdefaultencoding('utf-8')

class AllMoviesHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        client = MongoClient(DB_HOST, DB_PORT)
        db = client[DB_NAME]
        col = db[DB_COLLECTION]

        docs = col.find({}, {'imdbID': 1, '_id': 0})
        result_dict = {}
        movieid_list = []
        for doc in docs:
            movieid_list.append(doc['imdbID'])

        result_dict['all_movies'] = list(set(movieid_list))
        client.close()

        self.write(result_dict)

