#!/bin/sh
for f in *.pdf; do 
	pdfinfo -js $f
done