#! /usr/bin/python3

# Defining Colors
# kp_dark_blue = rgb(20, 63, 108)
# kp_light_blue = rgb(111,136,167)
# kp_yellow = rgb(255,195,36)
# kp_red = rgb(197,32,38)
import time
from blink1.blink1 import blink1, ColorCorrect

with blink1() as b1:
	print ("Blinky Blink!")
	b1.fade_to_rgb(100, 149,4,11)
	time.sleep(.2)
	b1.fade_to_rgb(100, 0,0,0)
	time.sleep(.2)
	b1.fade_to_rgb(100, 182,182,182)
	time.sleep(.2)
	b1.fade_to_rgb(100, 0,0,0)
	time.sleep(.2)
	b1.fade_to_rgb(100, 20,63,108)
	time.sleep(.2)
	b1.fade_to_rgb(100, 0,0,0)
	time.sleep(.2)
	b1.fade_to_rgb(100, 255,195,36)
	time.sleep(.2)
	b1.fade_to_rgb(100, 0,0,0)
	time.sleep(.2)
	b1.fade_to_rgb(100, 111,136,167)
	time.sleep(.2)
	b1.fade_to_rgb(100, 0,0,0)
	time.sleep(1)

	print ("<<<<< Welcome to King Phisher >>>>>>")
	b1.fade_to_rgb(10, 20,63,108)
	time.sleep(2)


#	print ("War Room Grey")
#	b1.fade_to_rgb(100, 182,182,182)
#	time.sleep(2)
#
#	print ("King Phisher Blue")
#	b1.fade_to_rgb(100, 20,63,108)
#	time.sleep(2)
#
#	print ("King Phisher Yellow")
#	b1.fade_to_rgb(100, 255,195,36)
#	time.sleep(2)
#
#	print ("King Phisher Light Blue")
#	b1.fade_to_rgb(100, 111,136,167)
#	time.sleep(2)

	
