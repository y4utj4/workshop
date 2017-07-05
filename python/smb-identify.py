#!/usr/bin/python3

import argparse
import socket
import sys


def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-i', '--infile', help='input file for script to process')
	parser.add_argument('-o', '--outfile', help='file to write output')
	parser.add_argument('-H', '--host', help='single host to scan')
	parser.add_argument('-v', '--verbose', help='show verbose output', action='store_true')
	# add additional arguments here

	# parse arguments
	args = parser.parse_args()
	host = args.host
	
	win_smb = 445
	lin_smb = 139
	ports = {21,22,23,25,80,88,115,139,389,445,445,3389,8080,8443}

	s = socket.socket()

	for port in ports:
		try:
			con = s.connect((host, port))
			print('[+]', port,' open.')
			
		except socket.error as e:	
			pass	
	
if __name__ == '__main__':
	main()