#!/usr/bin/python3
import olefile
import OleFileIO_PL

def main():
	ole = olefile.OleFileIO('./test.xls', write_mode=True)
	meta = ole.get_metadata()

	if not ole:
		print ('nofile')
	else:
		print('file')
		print(ole.listdir(streams=False, storages=True))
		if ole.exists('macros/vba'):
			print ('this doc has macros')
		else:
			print ('no macros')
		print ("Author: ", meta.author)


if __name__ == "__main__":
	main()