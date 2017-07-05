#!/usr/bin/python3
import aiohttp
import asyncio

async def fetch(session, url):
	with aiohttp.Timeout(10):
		try:
			async with session.get(url) as response:
				if response.status == 200:
					print('[+] ' + url +': ' + response.reason)
				else:
					print('[-] ' + url + ': ' + response.reason)
				return await response.status
		except OSError as e:
			print('[-] ' + e.strerror)

async def fetch_all(session, urls, loop):
	results = await asyncio.gather(*[fetch(session, url) for url in urls], return_exceptions=True )
	return results

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	conn = aiohttp.TCPConnector(verify_ssl=False)
	# breaks because of the first url
	urls = [
		'https://jschoeneman.com/',
		'http://google.com',
		'http://twitter.com',
		'http://asdfsadfsafsafsafdsf.com',
		'https://y4utj4.com'
	]

	with aiohttp.ClientSession(loop=loop, connector=conn) as session:
		the_results = loop.run_until_complete(fetch_all(session, urls, loop))
