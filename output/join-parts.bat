@echo off
rem Joins the 5 parts into one 1080p file (needs ffmpeg on PATH)
(for %%i in (0 1 2 3 4) do @echo file ernie-reyes-jr-clips-1080p-part%%i.mp4) > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy ernie-reyes-jr-1080p.mp4
del list.txt
pause
