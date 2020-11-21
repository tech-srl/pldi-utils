#!/bin/sh
for f in *.pdf; do 
	max_image_size=$(pdfimages -list $f | sort -k15 -n -r | head -n 1| rev | cut -d' ' -f 2 | rev | grep -v size)
	[[ ! -z "$max_image_size" ]] && echo "$f $max_image_size"
done