#!/usr/bin/env python
#coding:utf-8
import sys
sys.path.append('/Users/Mark/Projects/work/vionel-recommendations/')
import tornado.web
from cb_recommender.recommender import SimilarityRecommender

reload(sys)
sys.setdefaultencoding('utf-8')


DB_HOST = 'localhost'
DB_PORT = 27017
DB_NAME = 'VionelDB'
DB_COLLECTION = 'BoxerMovies'

class SimilarMoviesHandler(tornado.web.RequestHandler):
    def get(self, movieid, recnum):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")
        sr = SimilarityRecommender('movie', DB_NAME, DB_COLLECTION, DB_HOST, DB_PORT)
        result_dict = sr.recommend(movieid, int(recnum))
        self.write(result_dict)