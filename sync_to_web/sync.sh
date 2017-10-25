#!/bin/bash

files="leftBeer.jpg leftBeer.html rightBeer.html rightBeer.jpg index.html rightBeerOunces.html rightBeerOuncesNow.html AccidentProneBrewing.jpg"

exe="rsync -ua"
dest='jessecooke@thecooke.com:/home/jessecooke/b.thecooke.com/'
src=/home/pi/kegbot/beer_www

pushd $src

echo "$exe  $files $dest"
$exe $files $dest

