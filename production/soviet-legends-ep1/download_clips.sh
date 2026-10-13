#!/usr/bin/env bash
# Run on your own machine (needs yt-dlp + ffmpeg). Pulls ~7s sections from official uploads
# listed in clips.txt (name|youtube_id|start_seconds) into ./clips/.
# Each file is a LEN-second window starting PAD seconds before the guess in clips.txt.
# Watch it, then in scenes.csv write clips/name.mp4@SECONDS to start the render that far into the file.
set -u
mkdir -p clips && cd clips
LEN="${LEN:-60}"   # window length in seconds (wide, so a wrong guess still catches the scene)
PAD="${PAD:-30}"   # seconds subtracted from each start time in clips.txt
while IFS='|' read -r name id start; do
  [ -z "$name" ] && continue
  start=$((start-PAD)); [ "$start" -lt 0 ] && start=0
  end=$((start+LEN))
  yt-dlp -q --no-warnings -f "bv*[height<=720]/b[height<=720]" \
    --download-sections "*${start}-${end}" --force-keyframes-at-cuts \
    -o "${name}.%(ext)s" "https://www.youtube.com/watch?v=${id}" \
    && echo "ok   $name" || echo "FAIL $name"
done < ../clips.txt
