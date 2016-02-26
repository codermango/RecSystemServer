# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import wordpunct_tokenize

class TitlePreprocessor(object):

	def number_removal(self, title):
		return [unicode(word) for word in title if not word.isdigit()]

	def stop_word_removal(self, title_stemmed):
		stop_words = set(stopwords.words("english"))
		stop_words.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}', '-', '&', '/'])
		stop_words.update(['movi', 'film', 'best', 'good', 'see', 'watch', 'seen', 'favorit', 'favourit', 'dvd', 'ray', 'top', 'tv', 'list', 'watchlist', 'great', 'must', 'dvds', 'want', 've'])
		return [i for i in title_stemmed if i not in stop_words]

	def stemming(self, title):
		stemmer = SnowballStemmer("english")
		#title = title.decode('utf-8')
		return [stemmer.stem(word.lower()) for word in wordpunct_tokenize(title)]

	def get_n_grams(self, title):
		return self.number_removal(self.stop_word_removal(self.stemming(title)))


if __name__ == "__main__":
	TP = TitlePreprocessor()
	title = "the NOT-so-great-but-still-enjoyable list of gay-themed movies made in 1958 with apples airports"
	print TP.get_n_grams(title)
