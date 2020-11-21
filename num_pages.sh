#!/bin/sh
for f in *.pdf; do 
	pages=$(pdfinfo $f | grep Pages | rev | cut -d' ' -f 1 | rev)
	echo "$f $pages"
done