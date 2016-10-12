#!/usr/bin/env python
import argparse
import hashlib

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='File Checking Script. Uses MD5')
	parser.add_argument('-1', '--origin', help='input file for script to process')
	parser.add_argument('-2', '--second', help='file to write output')
	args = parser.parse_args()

	hasher = hashlib.md5()
	with open (args.origin, 'rb') as afile:
		buf = afile.read()
		hasher.update(buf)
		f1 = hasher.hexdigest()
	print
	print("[+] Original File Hash: " + '\t' + f1)

	if args.second:
		with open(args.second, 'rb') as bfile:
			buf2 = bfile.read()
			hasher.update(buf2)
			f2 = hasher.hexdigest()
		print ("[+] Second File Hash: " + '\t' + '\t' + f2)
		if f1 == f2:
			print
			print ("[+] Your files match!")
		else:
			print
			print ("[-] Your files are different!! Check yo shiz foo!!")

if __name__ == '__main__':
	main()