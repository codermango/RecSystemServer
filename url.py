#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.index import IndexHandler
from handler.similar_movies import SimilarMoviesHandler

url = [
    (r'/', IndexHandler),
    (r'/similar_movies/(\w+)/(\d+)', SimilarMoviesHandler)
]