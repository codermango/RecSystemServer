#!/usr/bin/env python
#coding:utf-8
import sys
import time
# sys.path.append('/home/mark/Projects/work/vionel-recommender/')
import tornado.web
from cb_recommender import simmovie

reload(sys)
sys.setdefaultencoding('utf-8')


class SimilarMoviesHandler(tornado.web.RequestHandler):
    def get(self, movieid, recnum):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        result_dict = simmovie.recommend(movieid, int(recnum))

        self.write(result_dict)