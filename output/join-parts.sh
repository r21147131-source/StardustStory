#!/bin/sh
for i in 0 1 2 3 4; do echo "file ernie-reyes-jr-clips-1080p-part$i.mp4"; done > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy ernie-reyes-jr-1080p.mp4 && rm list.txt
