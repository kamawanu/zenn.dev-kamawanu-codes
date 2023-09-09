#!/bin/bash
for fn in $*
do
    echo file "$fn" 
done > files.txt

ffmpeg -f concat -safe 0 -i files.txt -c copy -fflags +genpts $( python3 $0.py $* ).mp4
