#!/usr/bin/python3
from urllib.parse import urlparse
import urllib.request

def url_checker(url):
	parsed_url = urlparse(url)	
	if not parsed_url.scheme == None:
		secure_url = "https://" + url
		try:
			urllib.request.urlopen(secure_url)
			return secure_url
		except:
			url = "http://" + url
			urllib.request.urlopen(url)
			return url
		else:
			print ('your site sucks')
			return 0
			

def main():
	url = "web-sniffer.net"

	is_valid = url_checker(url)
	print (is_valid)


if __name__ == '__main__':
	main()
