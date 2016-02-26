#!/usr/bin/env python
#coding:utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from handler.all_movies import AllMoviesHandler
from handler.similar_movies import SimilarMoviesHandler
from handler.special_day import SpecialDayHandler
from handler.holiday_keyword import HolidayKeywordHandler
from handler.theme import ThemeSearchHandler, ThemeNumSearchHandler

url = [
    (r'/allmovies/', AllMoviesHandler),
    (r'/rec/(\w+)/(\d+)/', SimilarMoviesHandler),
    (r'/special_day/(\w+)/', SpecialDayHandler),
    (r'/holiday_keyword/', HolidayKeywordHandler),
    (r'/theme/(\w+(%20)*\w*(%20)*\w*)/', ThemeSearchHandler),
    (r'/theme/(\d+)/(\d+)/(\d+)/', ThemeNumSearchHandler)
]