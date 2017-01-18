#!/usr/bin/python3

import argparse
import os
import sys
import urllib.request
import ssl

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-u', '--url', help='URL to look up')
	parser.add_argument('-w', '--wordlist', help='directory listing')
	parser.add_argument('-o', '--outfile', help='file to write output')
	parser.add_argument('-v', '--verbose', help='prints results to screen', action='store_true')

	args = parser.parse_args()
	url = args.url
	if args.outfile:
		outfile = open(args.outfile, 'w')
	verbose = args.verbose
	ssl_check = ssl.create_default_context()
	ssl_check.check_hostname = False
	ssl_check.verify_mode = ssl.CERT_NONE

	with open(args.wordlist, 'r') as f:
		print('[+] Checking ' + str(url) + 'against directories listed in: ' + args.wordlist + '\n')
		for line in f:
			dir = line.strip('\n')
			if verbose:
				print ('Checking: ' + dir)
			uri = url + '/' + dir
			try:
				response = urllib.request.urlopen(uri, context=ssl_check)
				if response:
					if verbose:
						print (response.info())
					if response.getcode() == 200:
						if verbose:
							print ('[+] FOUND: %s ' % (uri) + '\n')
						outfile.write('[+] FOUND: ' + uri + '\n')
			except urllib.error.HTTPError as error:
				if error.code == 401:
					if verbose:
						print ('[!] Authorization Required %s ' % (uri) + '\n')
					outfile.write('[!] Auth Required: ' + uri + '\n')
				elif error.code == 403:
					if verbose:
						print ('[!] Forbidden %s ' % (uri) + '\n')
					outfile.write('[!] Forbidden: ' + uri + '\n')
				elif error.code == 404:
					if verbose:
						print ('[-] Not Found %s' % (uri) + '\n')
				elif error.code == 503:
					if verbose:
						print ('[-] Service Unavailable %s ' % (uri) + '\n')
				else:
					if verbose:
						print ('[?] Unknown' + '\n')
	f.close()
	print ('[+] Check complete. Check your results listed in the file:  ' + args.outfile)
if __name__ == '__main__':
	main()
