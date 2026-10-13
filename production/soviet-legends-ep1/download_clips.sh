#!/usr/bin/env bash
# Run on your own machine (needs yt-dlp + ffmpeg). Pulls ~7s sections from official uploads
# listed in clips.txt (name|youtube_id|start_seconds) into ./clips/.
# Timestamps are best guesses: check each clip and adjust start_seconds in clips.txt.
set -u
mkdir -p clips && cd clips
LEN="${LEN:-7}"
while IFS='|' read -r name id start; do
  [ -z "$name" ] && continue
  end=$((start+LEN))
  yt-dlp -q --no-warnings -f "bv*[height<=720]/b[height<=720]" \
    --download-sections "*${start}-${end}" --force-keyframes-at-cuts \
    -o "${name}.%(ext)s" "https://www.youtube.com/watch?v=${id}" \
    && echo "ok   $name" || echo "FAIL $name"
done < ../clips.txt
