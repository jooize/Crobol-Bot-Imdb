#!/usr/bin/env python

import argparse
import imdb

# movie must be an IMDb Movie object
def get_genre_string(movie):
	if movie.has_key('genre'):
		genre_string = movie['genre'][0]
		for genre in movie['genre'][1:]:
			genre_string += " | " + genre
	else:
		genre_string = "No genre"
	return genre_string

def get_rating_string(movie, rating_star="ASCII"):
	if movie.has_key('rating'):
		rating_string = str(movie['rating'])
		if rating_star == "Unicode":
			# \u2605 is BLACK STAR
			rating_string += u" \u2605 "
		else:
			rating_string += " stars "
	else:
		rating_string = ""
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
	url_string = dash_string + " " + imdb_url
	return url_string

def get_title_string(movie, quotes="Double quotation marks"):
	if quotes == "Directional double quotation marks":
		title_string = u"\u201C" + movie['title'] + u"\u201D"
	elif quotes == "None":
		title_string = movie['title'] + " "
	else:
		title_string = '"' + movie['title'] + '"'
	return title_string

# Returns "????" if no year
def get_year_string(movie):
	return str(movie['year'])

def get_runtime_string(movie):
	if movie.has_key('runtime'):
		runtime_string = "(" + str(movie['runtime'][0]) + " min)"
	else:
		runtime_string = "(?? min)"
	return runtime_string

def main():
	parser = argparse.ArgumentParser(usage="%(prog)s [-huAGRY] [--url] title [{title,year} ...]", description='Get information about movies or series from IMDb.')
	parser.add_argument("title", nargs="+", help="Movie or TV serie")
	parser.add_argument("-u", "--url", help="Show URL to IMDb page", action="store_true")
	parser.add_argument("-G", "--no-genre", dest="genre", help="Don't show genre", action="store_false", default=True)
	parser.add_argument("-R", "--no-rating", dest="rating", help="Don't show rating", action="store_false", default=True)
	parser.add_argument("-Y", "--no-year", dest="year", help="Don't show year", action="store_false", default=True)
	parser.add_argument("-A", "--ascii-only", help="Only ASCII, no Unicode", action="store_true")
	#parser.add_argument("-p", "--plot", help="Show plot", action="store_true")
	parser.add_argument("--runtime", help="Show runtime", action="store_true")
	args = parser.parse_args()

	imdb_access = imdb.IMDb()

	title = ""
	for arg in args.title:
		title += arg + " "

	# Search for <title>
	search_result = imdb_access.search_movie(title)

	# First search result, movie or tv serie
	movie = search_result[0]

	# Fetch additional information
	imdb_access.update(movie)

	if args.ascii_only:
		print_string = get_title_string(movie, "Double quotation marks")
	else:
		print_string = get_title_string(movie, "Directional double quotation marks")

	if args.year:
		print_string += " (" + get_year_string(movie) + ")"

	if args.rating:
		if args.ascii_only:
			print_string += " " + get_rating_string(movie)
		else:
			print_string += " " + get_rating_string(movie, "Unicode")

	if args.genre:
		print_string += " " + get_genre_string(movie)

	if args.runtime:
		print_string += " " + get_runtime_string(movie)
	
	if args.url:
		if args.ascii_only:
			print_string += " " + get_url_string(imdb_access, movie)
		else:
			print_string += " " + get_url_string(imdb_access, movie, "Quotation dash")

	print print_string

if __name__  == "__main__":
	main()

