#!/usr/bin/env python
#coding:utf-8
import sys
sys.path.append('/home/mark/Projects/Docker/vionel-recommender/cb_recommender/')
import tornado.web
from cb_recommender.recommender import SimilarityRecommender

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SimilarMoviesHandler(tornado.web.RequestHandler):
    def get(self, movieid, recnum):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")
        sr = SimilarityRecommender()
        result_dict = sr.recommend(movieid, int(recnum))
        self.write(result_dict)