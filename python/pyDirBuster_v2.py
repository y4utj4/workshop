#!/usr/bin/python3
# Author: Jeremy Schoeneman
# Thanks to: Coldfusion39 for the help!!
""" 
pyDirBuster is a python version of DirBuster which brute forces webdirectories. 
You'll need your own directory wordlist. 
"""

import aiohttp
import argparse
import asyncio
import signal

@asyncio.coroutine
def get_status(site, verbose, outfile, sem):
	# Analyzes the previous status and prints out results
	with (yield from sem):
		response = yield from aiohttp.request('GET', site, compress=True)

	if response.status == 200:
		if verbose:
			print("[+] FOUND: {0}: {1}".format(site, response.status))
		if outfile:
			outfile.write("{0}: {1}".format(site, response.status) + '\n')
	elif 300 < response.status < 308:
		if verbose:
			print("[!] Web Redirect: {0}: {1}".format(site, response.status))	
		if outfile:
			outfile.write("{0}: {1}".format(site, response.status) + '\n')
	elif response.status == 401:
		if verbose:
			print("[!] Authorization Required: {0}: {1}".format(site, response.status))
		if outfile:
			outfile.write("{0}: {1}".format(site, response.status) + '\n')
	elif response.status == 403:
		if verbose:
			print("[!] Forbidden: {0}: {1}".format(site, response.status))
		if outfile:
			outfile.write("{0}: {1}".format(site, response.status) + '\n')
	elif response.status == 404:
		if verbose:
			print("[-] Not Found: {0}: {1}".format(site, response.status))
	elif response.status == 503:
		if verbose:
			print("[-] Service Unavailable: {0}: {1}".format(site, response.status))
	else:
		if verbose:
			print("[?] Unknown Response: {0}: {1}".format(site, response.status))
	
	yield from response.release()

def signal_handler():
	print('Stopping all tasks')
	for task in asyncio.Task.all_tasks():
		task.cancel()

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-u', '--url', help='URL to look up')
	parser.add_argument('-w', '--wordlist', help='directory listing')
	parser.add_argument('-o', '--outfile', help='file to write output')
	parser.add_argument('-v', '--verbose', help='prints results to screen', action='store_true')

	# Assigning args
	args = parser.parse_args()
	outfile = 0
	if args.outfile:
		outfile = open(args.outfile, 'w')
	url = args.url
	verbose = args.verbose
	directories = open(args.wordlist, 'r')

	# Assigning loop and connection
	sem = asyncio.Semaphore(1000)
	loop = asyncio.get_event_loop()
	loop.add_signal_handler(signal.SIGINT, signal_handler)

	f = asyncio.wait([get_status(url + directory.rstrip('\n'), verbose, outfile, sem) for directory in directories])
	try:
		
		loop.run_until_complete(f)
	except asyncio.CancelledError:
		print('Tasks were canceled')

if __name__ == '__main__':
	main()
