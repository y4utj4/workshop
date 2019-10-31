#!/usr/bin/python3

import argparse
import sys
import requests

def lookup(url):
	try:
		r = requests.get(url, timeout=1)
		print("[>] URL: ", url, " connected")
		try:
			parse_headers(r, url)
		except:
			print('[-] Could not check headers')
	except:
		pass
	return

def parse_headers(r, url):
	missing_headers = []
	secure_headers = ("X-Frame-Options", 
		"X-XSS-Protection" , 
		"x-content-type-options",
#		"Content-Type",
#		"Server",
#		"X-Powered-By",
#		"X-AspNet-Version",
		"Access-Control-Allow-Origin",
#		"Content-Security-Policy",
		'HTTP-Strict-Transport-Security'
		)
	
	for i in secure_headers:
		try:
			print('\t [+]' + str(i) + ':' + r.headers.get(i))
		except:
			missing_headers.append(i)
			pass
	print('[!]', url, " is missing headers:")
	print('\t[-]','\n\t[-] '.join(map(str,missing_headers)))
	
def make_url(host, ports):
	http_ports = ('80', '587','2480', '4567', '5000', 
		'5104', '5800', '5985', '7001','8008', '8042', 
		'8080', '8088', '8222', '8280', '8281', '8530', 
		'8887', '9080', '9981', '11371', '12046', '16080')
	https_ports = ('443','832', '981', '1311', '4444', 
		'4445', '5986', '7000','7002',  '8443', '8243',
		'8333', '8531', '8888', '9443', '12043', '12443', '18091', '18092' )

	for port in ports:
		if port in http_ports:
			url = 'http://' + host + ':' + port
			url.rstrip()
			lookup(url)
		if port in https_ports:
			url = 'https://' + host + port
			url.rstrip()
			lookup(url)

def main():
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-s', '--system', help='IP or Domain to test')
	parser.add_argument('-i', '--infile', help='Input file of systems to test')
	parser.add_argument('-o', '--outfile', help="File to write failures to")
	parser.add_argument('-p', '--ports', help='ports to test')

	args = parser.parse_args()
	host = args.system
	infile = args.infile
	outfile = args.outfile

	if not args.ports:
		port = "80"
	else:
		port = args.ports
	ports = port.split(',')

	if host:
		make_url(str(host), ports)
		
	if infile:
		with open(infile, 'r') as f:
			for line in f:
				make_url(str(line).strip('\n'), ports)
				
if __name__ == '__main__':
	main()