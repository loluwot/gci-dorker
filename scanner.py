import requests as req
import re
from urllib import parse
import sys
import argparse

parser = argparse.ArgumentParser(description='Search engine dorker.')
parser.add_argument("--search", "-s", help="search/dork term to use")
parser.add_argument("--engine", "-e", help="engine to use")
parser.add_argument("--page", "-p", help="number of pages to return")
args = parser.parse_args()

#variables that change between search engines
url_str = ""
dork = ""
page = 1
page_str = ""
regex = ""
google = False

if args.search:
	dork = args.search
else:
	print("No search term given.")
	exit()
if args.page:
	page = int(args.page)
if args.engine.lower() == "google":
	url_str = 'https://www.google.com/search?q=' + dork + '&start='
	regex = '<a href="(\/url\?[A-Za-z0-9&%\+\,/:;=?@#_\-\.]*)">'
	google = True
elif args.engine.lower() == "bing":
	url_str = 'https://www.bing.com/search?q=' + dork + '&first='
	regex = '<a href="[^\/]([A-Za-z0-9&%\+\,/:;=?@#_\-\.()]*)'
else:
	print("Search engine not bing or google.")
	exit()

results = ""
for i in range(page):
	results += req.get(url_str + str(i*10)).text
	
urls = re.findall(regex, results)#finds all urls in text by searching with regex, removes last url if google
if google:
	urls = urls[:-1]
parsed_urls = list(dict.fromkeys([parse.unquote(s) for s in urls])) #decodes from url encoding format and removes duplicates.

if google:
	parsed_urls = [parse.unquote(s.split('/url?q=')[1].split('&amp;')[0]) for s in urls] #parses urls by removing unnecessary sections
print ("------URLs------")
for url in parsed_urls:
	print(url)
print ("----------------")
print ("Number of URLs: " + str(len(parsed_urls)))