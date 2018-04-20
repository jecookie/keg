#!/usr/bin/python
from time import sleep
from collections import deque
import serial
import os
import sys
import inspect
import traceback

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def updateMinSave(qs):	
    with open("minute_save.txt","w") as fout:
        for q in qs:
            fout.writelines(str(q)+"\n")
        fout.close()
		
	
def loadMinFromSave(qs):
    if(os.path.isfile("minute_save.txt")):
        with open("minute_save.txt","r") as fin:
            for line in fin:
                try:
                    num = int(line.strip())
                    qs.append(num)
                except ValueError:
                    print "'", line.strip(), "' is not an int", lineno()
            fin.close()
        print "Min: Loaded ",len(qs)," defaults from file\n"

def updateHourSave(qs):	
    with open("hour_save.txt","w") as fout:
        for q in qs:
            fout.writelines(str(q)+"\n")
        fout.close()
		
	
def loadHourFromSave(qs):
    if(os.path.isfile("hour_save.txt")):
        with open("hour_save.txt","r") as fin:
            for line in fin:
                try:
                    num = int(line.strip())
                    qs.append(num)
                except ValueError:
                    print "'", line.strip(), "' is not an int", lineno()
            fin.close()
        print "Hour: Loaded ",len(qs)," defaults from file\n"      


# Establish the connection on a specific port
ser = serial.Serial('/dev/ttyUSB0', 9600) 

minute=deque([]);
hour=deque([]);

min_count=0;

#flush the input
try:
    value=ser.readline() 
    print "-> ", value
    value=ser.readline() 
    print "-> ", value
except:
    print "Unexpected error:", sys.exc_info()[0] 


loadMinFromSave(minute)
loadHourFromSave(hour)

while True:
    try:
        ser.write(b'g')
        value=ser.readline() # Read the newest output 
        print value

        minute.append(value.strip())
        if(len(minute) > 5000):
            minute.popleft()
        updateMinSave(minute)
        print "num mins ",min_count

        if(min_count>=60):
            min_count=0
            l=minute[len(l)-60-1,len(l-1)]
            #Should be average of last hour
            avg_hour=sum(l) / len(l)
            hour.append(avg_hour)
            print "Average this hour is ",avg_hour
            if(len(hour) > 5000):
                hour.popleft()
            updateHourSave(hour)
        min_count += 1
        
    except :
        print "Unexpected error"
        traceback.print_exc()

    sleep(60)


