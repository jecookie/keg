#!/bin/bash

files="minute_save.txt hour_save.txt"

exe="rsync -ua"
dest='jessecooke@thecooke.com:/home/jessecooke/b.thecooke.com/'
src=/home/pi/kegbot/moisture

pushd $src

echo "$exe  $files $dest"
$exe $files $dest

