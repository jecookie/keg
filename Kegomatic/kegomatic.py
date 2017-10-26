#!/usr/bin/python
import os
import time
import math
import logging
import RPi.GPIO as GPIO
import time
from flowmeter import *
from os import system
#from seekrits import *

import signal
import sys
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        GPIO.cleanup()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


LITERS_IN_A_KEG = 18

#boardRevision = GPIO.RPI_REVISION
GPIO.setmode(GPIO.BCM) # use real GPIO numbering
GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_UP)


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
	system("cp /home/pi/kegbot/beer_www/rightBeerOunces.html /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	system("sed -i 's/OZ1/" + f1.getFormattedThisPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	system("sed -i 's/OZ2/" + f1.getFormattedLastPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	system("sed -i 's/OZ3/" + f1.getFormattedLasterPour() + "/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	
	#This calculation is in Liters
	percent_left = round((1 - (f1.totalPour / LITERS_IN_A_KEG)) * 100,0)	
	system("sed -i 's/RM1/" + str(percent_left) + "%/' /home/pi/kegbot/beer_www/rightBeerOuncesNow.html")
	
def updateSave(f1, f2):	
	with open("keg_save_file.txt","w") as fout:
		fout.writelines(str(f1.thisPour)+"\n")
		fout.writelines(str(f1.lastPour)+"\n")
		fout.writelines(str(f1.lasterPour)+"\n")
		fout.writelines(str(f1.totalPour)+"\n")
		fout.close()
		
                print time.ctime() + ": This pour "+f1.getFormattedThisPour() +"\n"
	
def loadFromSave(f1, f2):
    if(os.path.isfile("keg_save_file.txt")):
        with open("keg_save_file.txt","r") as fin:
                f1.thisPour = float(fin.readline().strip())
                f1.lastPour = float(fin.readline().strip())
                f1.lasterPour = float(fin.readline().strip())
                f1.totalPour = float(fin.readline().strip())
                fin.close()
        print "Loaded defaults from file\n";
	   

GPIO.add_event_detect(23, GPIO.RISING, callback=doAClick, bouncetime=20) # Beer, on Pin 23
GPIO.add_event_detect(24, GPIO.RISING, callback=doAClick2, bouncetime=20) # Seltzer, on Pin 24

#Load saves from a file
loadFromSave(fm, fm2)


#Test the functions now
# Update the webpage
updatePage(fm, fm2)
#Update the savefile
updateSave(fm,fm2)
fm.clear()
#GPIO.cleanup()
#sys.exit(0)



# main loop
while True:

  currentTime = int(time.time() * FlowMeter.MS_IN_A_SECOND)
 
    
  # reset flow meter after each pour (2 secs of inactivity)
  if (fm.thisPour >= 0.05 and currentTime - fm.lastClick > 2000):
		# Update the webpage
		updatePage(fm, fm2)
		#Update the savefile
		updateSave(fm,fm2)
		fm.clear()

#  print str(fm.thisPour*fm.OUNCES_IN_A_LITER) + "\n"
  time.sleep(1)
		
    
  #if (fm2.thisPour <= 0.23 and currentTime - fm2.lastClick > 2000):
    #fm2.clear()
		# Update the webpage
		#updatePage(fm, fm2)
		#Update the savefile
		#updateSave(fm,fm2)

  
  
  #GPIO.cleanup()
