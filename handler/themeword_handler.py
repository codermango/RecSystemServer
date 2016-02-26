import redis
import sys
from pymongo import MongoClient
from text_preprocess import TitlePreprocessor

REDIS_HOST = '192.168.1.60'
PORT = 6379

MONGO_HOST = '192.168.1.67'
MONGO_PORT = 27017
mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)


class ThemewordExtractor(object):
    def __init__(self, host=REDIS_HOST, port=PORT, db=0):
        self.r = redis.StrictRedis(host ,port=port, db=db)

    # function gets top n-grams sorted by number of movies in them
    def get_top_ngrams(self, n, range_low, range_high):
        return self.r.zrevrange("{0}-grams".format(n), range_low, range_high, "WITHSCORES")

    def get_ngram_movie_num(self, n, ngram):
        return self.r.zscore("{0}-grams".format(n), ngram)

    # this method is not used at all, TODO  remove or revise the search and get movie
    def search_ngrams(self,query_string):
        return self.r.keys("ng*{0}*".format(query_string))
    def get_top_ngrams_movies(self, n, range_low, range_high):
        top_ngrams = self.r.zrevrange("{0}-grams".format(n), range_low, range_high)
        print top_ngrams
        list_ngrams = ["ng-{0}:".format(n)+ngram for ngram in top_ngrams]
        print list_ngrams
        result_list = []
        list_of_usr_lists = [self.get_ngram_usr_lists(ngram) for ngram in list_ngrams]
        all_ngram_usr_lists = list(set(reduce(lambda x,y: x+y, list_of_usr_lists)))
        all_ngram_dict = self.query_list_title_with_ngram(all_ngram_usr_lists)
        for ngram in list_ngrams:
            n, key = ngram.split(":")[0][-1], ngram.split(":")[1]
            num_movie = self.get_ngram_movie_num(n,key)
            usr_lists = self.get_ngram_usr_lists(ngram)
            ngram_usr_list_dict = {}
            ngram_movies = set()
            for ele in usr_lists:
                ngram_usr_list_dict[ele] = all_ngram_dict[ele]["title"]
                ngram_movies.update(set(all_ngram_dict[ele]["movies"]))
            single_ngram_dict = {}
            single_ngram_dict["ngram"] = ngram
            single_ngram_dict["usr_lists"] = ngram_usr_list_dict
            single_ngram_dict["usr_lists_number"] = len(ngram_usr_list_dict)
            single_ngram_dict["movie_number"] = num_movie
#            single_ngram_dict["ngrams_movies"] = list(ngram_movies)
            result_list.append(single_ngram_dict)
        return result_list

    # input any string as a search query and get back all the n-grams for it
    def search_and_get_movie(self, query_string):
        list_ngrams = self.r.keys("ng*{0}*".format(query_string))
        print list_ngrams
        result_list = []
        list_of_usr_lists = [self.get_ngram_usr_lists(ngram) for ngram in list_ngrams]
        if not list_of_usr_lists:
            return []
        all_ngram_usr_lists = list(set(reduce(lambda x,y: x+y, list_of_usr_lists)))
        print all_ngram_usr_lists
        all_ngram_dict = self.query_list_title_with_ngram(all_ngram_usr_lists)
        for ngram in list_ngrams:
            n, key = ngram.split(":")[0][-1], ngram.split(":")[1]
            num_movie = self.get_ngram_movie_num(n,key)
            usr_lists = self.get_ngram_usr_lists(ngram)
            ngram_usr_list_dict = {}
            ngram_movies = set()
            for ele in usr_lists:
                ngram_usr_list_dict[ele] = all_ngram_dict[ele]["title"]
                ngram_movies.update(set(all_ngram_dict[ele]["movies"]))
            single_ngram_dict = {}
            single_ngram_dict["ngram"] = ngram
            single_ngram_dict["usr_lists"] = ngram_usr_list_dict
            single_ngram_dict["usr_lists_number"] = len(ngram_usr_list_dict)
            single_ngram_dict["movie_number"] = num_movie
#            single_ngram_dict["ngrams_movies"] = list(ngram_movies)
            result_list.append(single_ngram_dict)
        return result_list

    def get_ngram_usr_lists(self, ngram):
        return self.r.zrange(ngram, 0, -1)

    # returns all the movies given a list of usr list id
    # mongo query, time matters
    def query_movies_with_usr_list(self, usr_lists):
        ngram_movies = set()
        for res in mongo_client.user_lists.boxer.aggregate(
                pipeline=[
                    {"$match":{"imdbID": {"$in": list(usr_lists)}}},
                    {"$group":{"_id": "$imdbID", "movies":{"$push":"$movie_list_id"}}}
                    ],
                allowDiskUse=True
            ):
            ngram_movies.update(res["movies"][0])
        return ngram_movies

    # returns all the usr list titles for a given ngram
    # mongo query, time matters
    def query_list_title_with_ngram(self, usr_lists):
        ngram_list_titles = {}
        for res in mongo_client.user_lists.boxer.aggregate(
                pipeline=[
                    {"$match":{"imdbID": {"$in":usr_lists}}},
                    {"$group":{"_id": "$imdbID", "title":{"$push":"$title"}, "movies":{"$push": "$movie_list_id"}}}
                    ],
                allowDiskUse=True
            ):
            ngram_list_titles[res["_id"]] = {}
            ngram_list_titles[res["_id"]]["title"] = res["title"][0]
            ngram_list_titles[res["_id"]]["movies"] = res["movies"][0]
        return ngram_list_titles

    def merge_ngrams(self, keyword_name, ngram_list):
        keyword_json = {}
        keyword_json["name"] = keyword_name
        usr_lists = [self.get_ngram_usr_lists(ngram) for ngram in ngram_list]
        all_usr_lists = list(set(reduce(lambda x,y: x+y , usr_lists)))
        all_keyword_movies = self.query_movies_with_usr_list(all_usr_lists)
        keyword_json["usr_lists"] = all_usr_lists
        keyword_json["movies"] = all_keyword_movies

    # TODO unfinished filter operation
    def filter_ngrams(self, keyword_name, nagram_list):
        keyword_json = {}
        keyword_json["name"] = keyword_name
        usr_lists = [self.get_ngram_usr_lists(ngram) for ngram in ngram_list]
        filtered_sets = reduce(lambda x,y :set(x).intersection(y), usr_lists)

if __name__ == "__main__":
    tp = TitlePreprocessor()
    twe = ThemewordExtractor()
    query = tp.stemming(sys.argv[1])
    query = " ".join(query)
    print query
    result = twe.search_and_get_movie(query)
#    print twe.get_top_ngrams(3,0,100)
#    twe.merge_ngrams("gay", ["ng-2:gay theme", "ng-2:gay love"])
#    print result
    # print twe.get_top_ngrams_movies(2,1,10)
