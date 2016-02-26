#!/usr/bin/env python
#coding:utf-8
import sys
import json
import tornado.web
from themeword_handler import *


class ThemeSearchHandler(tornado.web.RequestHandler):
    def get(self, word, x, y):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        print word, x, y
        tp = TitlePreprocessor()
        twe = ThemewordExtractor()
        query = tp.stemming(word)
        query = " ".join(query)
        result = twe.search_and_get_movie(query)
        self.write(json.dumps(result))

class ThemeNumSearchHandler(tornado.web.RequestHandler):
    def get(self, ngnum, fromnum, tonum):
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET")

        tp = TitlePreprocessor()
        twe = ThemewordExtractor()
        result = twe.get_top_ngrams_movies(ngnum, fromnum, tonum)
        self.write(json.dumps(result))
