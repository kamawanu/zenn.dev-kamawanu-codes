#!/bin/bash
for fn in $*
do
    echo file "$fn" 
done > /tmp/files.txt

ffmpeg -f concat -safe 0 -i /tmp/files.txt -c copy -fflags +genpts $( python3 $0.py $* ).mp4 || exit 9
for fn in $*
do
    mv "$fn" "$fn".BAK
done
