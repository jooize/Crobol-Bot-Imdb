#!/usr/bin/env python

import sys
import argparse
import imdb

# movie must be an IMDb Movie object
def get_genre_string(movie):
	genre_string = movie['genre'][0]
	for genre in movie['genre'][1:]:
		genre_string += " | " + genre
	return genre_string

def get_rating_string(movie, encoding="ASCII"):
	rating_string = str(movie['rating'])
	if encoding == "Unicode":
		# \u2605 is BLACK STAR
		rating_string += u" \u2605"
	else:
		rating_string += " stars"
	return rating_string

def get_url_string(imdb_access, movie, dash="ASCII"):
	# Replace akas.imdb.com with imdb.com (will redirect to www.imdb.com)
	imdb_url = imdb_access.get_imdbURL(movie).replace('http://akas.', 'http://', 1)
	if dash == "Quotation dash":
		# \u2015 is HORIZONTAL BAR
		dash_string = u"\u2015"
	elif dash == "Em dash":
		# \u2014 is EM DASH
		dash_string = u"\u2014"
	else:
		dash_string = "--"
	url_string = dash_string + imdb_url
	return url_string

def get_title_string(movie):
	return movie['long imdb canonical title']

def i():
	parser = argparse.ArgumentParser(description='Get information about movies or series from IMDb.')
	parser.add_argument("title", nargs="+", help="Movie or TV serie")
	parser.add_argument("--url", help="Print URL to IMDb page", action="store_true")
	parser.add_argument("--no-genre", dest="genre", help="Don't show genre", action="store_false", default=True)
	parser.add_argument("--no-rating", dest="rating", help="Don't show rating", action="store_false", default=True)
	args = parser.parse_args()

	imdb_access = imdb.IMDb()
	movie_args = ""
	for arg in args.title:
		movie_args += arg + " "
	search_result = imdb_access.search_movie(movie_args)
	movie = search_result[0]
	imdb_access.update(movie)

	print_string = get_title_string(movie)

	if args.rating:
		print_string += " " + get_rating_string(movie, "Unicode")

	if args.genre:
		print_string += "  " + get_genre_string(movie)

	if args.url:
		print_string += get_url_string(imdb_access, movie, "Quotation dash")

	print print_string

if __name__  == "__main__":
	i()

