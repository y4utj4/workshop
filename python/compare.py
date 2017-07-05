#! /usr/bin/python3
import argparse
import datetime
import difflib
import os.path
import socket
import sys
import webbrowser

def compare(args):
	newfile = args.infile
	oldfile = args.previous_scan
	outfile = args.htmlfile

	oldfile_create = "Orig File Created: %s" % str(args.previous_scan) 
	nowtime_html = '<h3 style="font-style:italic;">' + str(datetime.datetime.now()) + '</h3>'
	header = """<style>
			  body{text-align:center; background:#EEE; width:80%; margin:0 auto;}
			  table{margin:0 auto; width:auto;}
			  td tr {padding:0px;}
			  .heading{width:80%; margin-left:400px;}
			  .clear{clear:both}
			  </style>
			  <div class="heading">
			  <img src="http://www.bridgestone.com/etc/images/logos/bridgestone-logo-set-en.png" style="float:left; margin-top:10px;" />
			  <h1 style="float:left; width:50%;">Host Discovery and Comparison</h1>
			  </div>
			  <div class="clear"</clear>"""	
	diff = difflib.HtmlDiff()
	d = diff.make_file(open(oldfile).readlines(), open(newfile).readlines(), fromdesc=oldfile_create, todesc="Newest Scan", context=True, numlines=0)
	
	with open(outfile, 'w+') as doc:
		doc.write(header)
		doc.write(nowtime_html)
		doc.write(d)
	try:
		webbrowser.open(outfile)
	except:
		return
	return

def main():
	sys.setrecursionlimit(50000)
	parser = argparse.ArgumentParser(description='Compares two host discovery scans')
	parser.add_argument('-i', '--infile', help='new scan')
	parser.add_argument('-p', '--previous_scan', help='previous discovery results to compare')
	parser.add_argument('-H', '--htmlfile', help='HTML filename to export the differences between scans')
	args = parser.parse_args()

	compare(args)

if __name__ == '__main__':
	main()
