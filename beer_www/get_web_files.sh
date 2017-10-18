#!/bin/bash


declare -a files=( leftBeer.jpg leftBeer.html rightBeer.html rightBeer.jpg index.html rightBeerOunces.html AccidentProneBrewing.jpg )

exe=~/kegbot/Dropbox-Uploader/dropbox_uploader.sh

for i in "${files[@]}" 
do
	echo "$exe download 'Stuff/Beer Labels/www/$i' "
	$exe download "Stuff/Beer Labels/www/$i"
	chmod go+r $i
done
