#!/usr/bin/python3
#!/usr/bin/python3

import argparse
import os
import sys
import xlsxwriter

def main():
	# setup arguments
	parser = argparse.ArgumentParser(description='Put description here')
	parser.add_argument('-m', '--macro', help='macro to pull from')
	parser.add_argument('-o', '--outfile', help='file to write output')
	parser.add_argument('-v', '--verbose', help='show verbose output', action='store_true')
	# add additional arguments here

	# parse arguments
	args = parser.parse_args()
	macro_path = args.macro
	excel_path = args.outfile

	workbook = xlsxwriter.Workbook(excel_path)
	worksheet = workbook.add_worksheet()

	with open(macro_path, 'r') as m:
		macro = m.read()
		print('Inserting macro:')
		print (str(macro))

	worksheet.set_column('A:A', 30)
	workbook.add_vba_project(macro_path)
	worksheet.insert_button('B3', {'macro' : str(macro), 'caption': 'Decrypt your spreadsheet', 'width':80, 'height': 20})
	workbook.close()


	# do some other stuff here

if __name__ == '__main__':
	main()
