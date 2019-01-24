#!/usr/bin/python3

import argparse
import datetime
import difflib
import os.path
import socket
import sys
import webbrowser

from multiprocessing import Process, Queue

try:
	import netaddr
except ImportError:
	print('[-] You need to install the "netaddr" module.  Get it with "pip install netaddr".')
	sys.exit(0)

def get_ips_from_range(ipRange):
	if '/' in ipRange:
		try:
			cidrIPs = netaddr.IPNetwork(ipRange)
		except netaddr.core.AddrFormatError:
			print('[-] Invalid IP cidr specified: ' + ipRange)
			sys.exit(0)
		return cidrIPs
	elif '-' in ipRange:
		# build ending IP from range
		dashRange = ipRange
		startIP, endIP = dashRange.split('-')
		# convert to cidr notation
		try:
			cidrIPs = netaddr.iprange_to_cidrs(startIP, endIP)[0]
		except netaddr.core.AddrFormatError:
			print('[-] Invalid IP range specified: ' + ipRange)
			sys.exit(0)
		return cidrIPs
	else:
		print('Something went wrong. Check your input ' + ipRange + " caused an error")
		sys.exit(0)

def send_to_lookup(q, verbose, outfile, timeout, hosts):
#	outfile = open(outfile, 'w')
	for ip in hosts:
		try:
			ip = str(ip)
			proc = Process(target=dns_reverse_lookup, args=(ip, verbose, q))
			proc.start()
			line = q.get()
			results = []
			if line != None:
#				outfile.write(line + '\n')
				results.append(line)
			proc.join(timeout)
			if proc.is_alive():
				print('[!] Lookup timeout exceeded for: ' + ip)
				proc.terminate()
				proc.join()
		except KeyboardInterrupt:
			print('\n[!] Kill signal detected, shutting down.')
			proc.terminate()
			proc.join()
			break
#	outfile.close()
	return

def dns_reverse_lookup(ip, verbose, q):
	try:
		host = socket.gethostbyaddr(ip)
		line = ip + ' - ' + host[0]
		print(line)
		q.put(line)
	except:
		if verbose:
			print('[-] Could not resolve: ' + ip)
			q.put(None)

def compare_results(outfile, htmlfile, prev_scan):
	sys.setrecursionlimit(50000)
	now = datetime.datetime.now()
	newfile = outfile
	outfile = htmlfile + now.strftime('%d-%b-%Y_%H:%M:%S') + '.html'
	oldfile = prev_scan
	oldfile_header = "Orig File: %s" % oldfile
	newfile_header = "New File: %s" % outfile
	nowtime_html = '<h3 style="font-style:italic;">' + now.strftime('%d-%b-%Y_%H:%M:%S') + '</h3>'
	header = """<style>
			  body{text-align:center; background:#EEE; width:80%; margin:0 auto;}
			  table{margin:0 auto; width:auto;}
			  td tr {padding:0px;}
			  .heading{width:80%; margin-left:400px;}
			  .clear{clear:both}
			  </style>
			  <div class="heading">
			  <h1 style="float:left; width:50%;">Key Bank <br />Host Discovery and Comparison</h1>
			  </div>
			  <div class="clear"</clear>"""

	diff = difflib.HtmlDiff()
	d = diff.make_file(open(oldfile).readlines(), open(newfile).readlines(), fromdesc=oldfile_header, todesc=newfile_header, context=True, numlines=0)
	with open(outfile, 'w+') as doc:
		doc.write(header)
		doc.write(nowtime_html)
		doc.write(d)
		doc.close()
		print ('\n[+] HTML report has been sucessfully written to: ', htmlfile)
		try:
			webbrowser.open(outfile)
		except:
			return
	return

def main():
	#Set up arguments
	parser = argparse.ArgumentParser(description='Host discovery scan using ICMP Ping requests with previous scan comparison.')
	parser.add_argument('-r', '--range', help='IP range to check. i.e. 192.168.1.0/24 or 192.168.1.0-255', default=None)
	parser.add_argument('-i', '--infile', help='file to read scope from. Preferably used when multiple ranges are needed')
	parser.add_argument('-p', '--previous_scan', help='previous discovery results to compare')
	parser.add_argument('-o', '--outfile', help='filename to export results from discovery', required=True)
	parser.add_argument('-H', '--htmlfile', help='HTML filename to export the differences between scans')
	parser.add_argument('-t', '--timeout', help='time in seconds to wait for lookup to complete, default is 5.', default=2)
	parser.add_argument('-v', '--verbose', help='show verbose output', action='store_true')
	args = parser.parse_args()

#Declaring Variables
	timeout = int(args.timeout)
	outfile = False
	infile = False
	ipRange = False
	verbose = False
	q = Queue()
	

# Conditional Variables
	if args.range:
		ipRange = args.range
	elif args.infile:
		infile = True
	else:
		print('[!] input values are required, please enter a range or specify a file')

	if not args.outfile:
		print('[!] an outfile must be specified to send the results of the discovery scan')
		return 0
	else:
		now = datetime.datetime.now()
		outfile = args.outfile + '_'+ now.strftime('%d-%b-%Y_%H:%M:%S')
		print('[+] writing files to: ', outfile)

	if args.htmlfile and not outfile and not args.previous_scan:
		print('[!] in order to compare results, you must specify a previous scan, outfile and an htmlfile file')
	elif args.htmlfile and not args.previous_scan:
		print('[!] in order to compare results, you must specify a file to compare against')
	else:
		htmlfile = args.htmlfile
		prev_scan = args.previous_scan

	if args.verbose:
		verbose = True

# Do things
	if ipRange:
		outfile = open(outfile, 'w')
		ip = get_ips_from_range(ipRange)
		results = send_to_lookup(q, verbose, outfile, timeout, ip)
		if results != None:
			outfile.write(results)
			print(results)
		else:
			pass
			
	elif infile:
		outfile = open(outfile, 'w')
		with open(args.infile, 'r') as f:
			for line in f:
				host = line.strip('\n')
				if '-' in host or '/' in host:
					host = get_ips_from_range(host)
					results = send_to_lookup(q, verbose, outfile, timeout, host)

				else:
					dns_reverse_lookup(host, verbose, outfile, q)
			f.close()	
	else:
		return 0

	
	if htmlfile:
		try:
			compare_results(outfile, htmlfile, prev_scan)
		except:
			print('\n[-] could not complete the comparison')

	outfile.close()
	print('[+] Done, happy hunting!')

if __name__ == '__main__':
	main()
