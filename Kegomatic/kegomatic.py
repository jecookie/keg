#!/usr/bin/python
import os
import time
import math
import logging
import RPi.GPIO as GPIO
import datetime
from flowmeter import *
from adabot import *
from subprocess import call
#from seekrits import *

LITERS_IN_A_KEG = 18

#boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_UP)

view_mode = 'normal'

# set up the flow meters
fm = FlowMeter('imp', ["beer"])
fm2 = FlowMeter('imp', ["seltzer"])

# Beer, on Pin 23.
def doAClick(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if fm.enabled == True:
    fm.update(currentTime)

# Root Beer, on Pin 24.
def doAClick2(channel):
  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
  if fm2.enabled == True:
    fm2.update(currentTime)

def updatePage(f1, f2):
	#Find and replace OZ1 with last pour
	call("cp /home/pi/kegbot/beer_www/rightBeerOunces.html /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	call("sed -i 's/OZ1/This Pour      :" + f1.getFormattedThisPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	call("sed -i 's/OZ2/Before that    :" + f1.getFormattedLastPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	call("sed -i 's/OZ3/And Before That:" + f1.getFormattedLasterPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	
	#This calculation is in Liters
	percent_left = round(1 - (f1.totalPour / LITERS_IN_A_KEG) * 100)	
	call("sed -i 's/RM1/" + str(percent_left) + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	
def updateSave(f1, f2):	
	with open("keg_save_file.txt","w") at fout:
		fout.writelines(f1.thisPour+"\n")
		fout.writelines(f1.lastPour+"\n")
		fout.writelines(f1.lasterPour+"\n")
		fout.writelines(f1.totalPour+"\n")
		file.close()
		
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print "File written at "+st+"\n"
	
    
GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) # Beer, on Pin 23
GPIO.add_event_detect(24, GPIO.RISING, callback=doAClick2, bouncetime=20) # Seltzer, on Pin 24

#TODO: Load saves from a file

# main loop
while True:

  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
 
  view_mode = 'normal'
    
  # reset flow meter after each pour (2 secs of inactivity)
  if (fm.thisPour >= 0.05 and currentTime - fm.lastClick > 2000):
		# Update the webpage
		updatePage(fm, fm2)
		#Update the savefile
		updateSave(fm,fm2)
		fm.clear()
		
    
  #if (fm2.thisPour <= 0.23 and currentTime - fm2.lastClick > 2000):
    #fm2.clear()
		# Update the webpage
		#updatePage(fm, fm2)
		#Update the savefile
		#updateSave(fm,fm2)

  
  
  #GPIO.cleanup()
