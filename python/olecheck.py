#!/usr/bin/python3

import argparse
import olefile
import OleFileIO_PL
import os
import sys

def walkdir(dir):
	for cur, _dirs, files in os.walk(dir):
		file = ''
		head, tail = os.path.split(cur)
		while head:
			file +=os.path.split(file)
		return file




def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-d', '--dir', help='directory to search files')
	parser.add_argument('-f', '--file', help='individual file to scan')
	parser.add_argument('-o', '--output', help='file to write results')
	parser.add_argument('-v', '--verbose', help='show verbose output', action='store_true')

	# parse arguments
	args = parser.parse_args()
	file = args.file
	ole = olefile.OleFileIO(file)
	meta = ole.get_metadata()

	if args.dir:
		file = walkdir(args.dir)

	if not ole:
		print('nofile')
	else:
		print(ole.listdir(streams=False, storages=True))
		if ole.exixts('macros/vba'):
			print('[!] ' + file + ' has macros')
		else:
			print('[-] ' + file + ' No macros')

if __name__ == '__main__':
	main()