#!/bin/bash

files="minute_save.txt hour_save.txt moisture_minute.jpg"

exe="rsync -ua"
dest='jessecooke@thecooke.com:/home/jessecooke/b.thecooke.com/'
src=/home/pi/kegbot/moisture


pushd $src

nice -10 octave --no-gui plot_moisture.m 

echo "$exe  $files $dest"
$exe $files $dest

