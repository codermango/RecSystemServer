#!/usr/bin/env python
#coding:utf-8
import sys
import tornado.web
from pymongo import MongoClient
from cb_recommender.recommender import SimilarityRecommender

reload(sys)
sys.setdefaultencoding('utf-8')

class AllMoviesHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        client = MongoClient('localhost')
        db = client.VionelMovies
        col = db.BoxerMovies

        docs = col.find({}, {'imdbId': 1, '_id': 0})
        result_dict = {}
        movieid_list = []
        for doc in docs:
            movieid_list.append(doc['imdbId'])

        result_dict['all_movies'] = movieid_list
        client.close()

        self.write(result_dict)

