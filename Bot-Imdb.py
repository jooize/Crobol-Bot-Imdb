#!/usr/bin/env python

import sys
import getopt
import imdb

def main(argv):
	imdb_access = imdb.IMDb()

	#args_all = ""
	#for arg in argv:
		#args_all += arg + " "

	#print args_all

	#search_result = imdb_access.search_movie(args_all)
	#print search_result[0]['long imdb canonical title']

	#try:
		#opts, args = getopt.getopt(argv,"h",["tvserie=","movie="])
	#except getopt.GetoptError:
		#print '!imdb --tvserie=Limitless'
		#sys.exit(2)
	#for opt, arg in opts:
		#if opt == '-h':
			#print '!imdb --stuff'
			#sys.exit()
		#elif opt in ("--tvserie"):
			#print "TV Serie: " + arg
		#elif opt in ("--movie"):
			#print "Movie: " + arg

	movie_args = ""
	for arg in argv:
		movie_args += arg + " "
	search_result = imdb_access.search_movie(movie_args)
	movie = search_result[0]
	imdb_access.update(movie)
	print_string = movie['long imdb canonical title'] + " " + str(movie['rating']) + u" \u2605"
	genre_string = "  " + movie['genre'][0]
	for genre in movie['genre'][1:]:
		genre_string += " | " + genre
	print_string += genre_string
	print print_string

if __name__ == "__main__":
	main(sys.argv[1:])

