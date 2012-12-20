#!/usr/bin/env python

import sys
import argparse
import imdb

def main(argv):
	parser = argparse.ArgumentParser(description='IMDb stuff.')
	parser.add_argument("title", nargs="+", help="Movie or TV serie")
	parser.add_argument("--url", help="Print URL to IMDb page", action="store_true")
	args = parser.parse_args()

	imdb_access = imdb.IMDb()
	movie_args = ""
	for arg in args.title:
		movie_args += arg + " "
	search_result = imdb_access.search_movie(movie_args)
	movie = search_result[0]
	imdb_access.update(movie)
	# \u2605 is Black Star
	print_string = movie['long imdb canonical title'] + " " + str(movie['rating']) + u" \u2605"
	genre_string = movie['genre'][0]
	for genre in movie['genre'][1:]:
		genre_string += " | " + genre
	print_string += "  " + genre_string
	if args.url:
		# Replace akas.imdb.com with imdb.com (will redirect to www.imdb.com)
		imdb_url = imdb_access.get_imdbURL(movie).replace('http://akas.', 'http://', 1)
		# \u2015 is HORIZONTAL BAR, quotation dash. Use "--" if ASCII is required.
		print_string += u" \u2015 " + imdb_url
	print print_string

if __name__ == "__main__":
	main(sys.argv[1:])

