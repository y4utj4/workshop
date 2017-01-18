#!/usr/bin/python3
import aiohttp
import argparse
import asyncio
import signal
import sys

async def url_connect(client, site):
	# Connects to url, gets status
	async with client.get(site) as response:
		#print ('\n [+] Status: ' + site + ': ' + str(response.status) + '\n')
		site_status = response.status
		return site_status

async def get_status(site, verbose, client):
	# Analyzes the previous status and prints out results
	status = await url_connect(client, site)
	if status == 200:
		print ('[+] FOUND: ' + site + ':' + str(status))
	if status == 401:
		print ('[!] Authorization Required ' + site+ ':' + str(status))
	elif status == 403:
		print ('[!] Forbidden ' + site+ ':' + str(status))
	elif status == 404:
		print ('[-] Not Found ' + site+ ':' + str(status))
	elif status == 503:
		print ('[-] Service Unavailable ' + site+ ':' + str(status))

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
	if args.outfile:
		outfile = open(args.outfile, 'w')
	url = args.url
	verbose = args.verbose
	
	# Assigning loop and connection
	loop = asyncio.get_event_loop()
	loop.add_signal_handler(signal.SIGINT, signal_handler)
	conn = aiohttp.TCPConnector(verify_ssl=False)
	client = aiohttp.ClientSession(loop=loop, connector=conn)
	
	# Do stuff
	with open(args.wordlist, 'r') as f:
		for line in f:
			directory = line.strip('\n')
			site = url+directory
			try:
				loop.run_until_complete(get_status(site,verbose,client))
			except asyncio.CancelledError:
				print('Tasks were canceled')
	
if __name__ == '__main__':
	main()