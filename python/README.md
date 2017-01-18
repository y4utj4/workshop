## Python Scripts / Tools

This is essentially a collection of python scripts I've been working on in order to better understand the python languate while creating something useful that anyone can use. Scripts are mainly network/infosec related, but see below for a description of each tool. 


## Tools
* **blink1-color.py** - a quick python script to flash colors on the blink1 usb light
	* requires blink1
* **blink-weather.py** - using an api, pulls the weather for your location, tells you the temperature and depending on the temp, flashes a color on the blink1 usb light
	* requires blink1 and an api from weather underground
* **CheckSumCheck.py** - checks the MD5 sum between two files
* **jinja_scriptor.py** - creates a directory tree and starting files for a jinja/flask site
	* requires jinja2 and flask to be installed
* **pyDirBuster.py** - Using a wordlist, attempts to find directories of a web application and reports status, and headers of available pages
	* requires ssl, urllib.request
* **resolve_range.py** - using either a single ip, cidr, range, or file, grabs hostnames for associated IP addresses
* **pyDirBuster_v2.py** - Using a wordlist, attempts to find directories of a web application and reports status, and headers of available pages.
	* requires aiohttp, asyncio

## Acknowledgements
Thanks to zero_steiner for the guidance and help when I'm stuck. 