#!/usr/bin/env bash
# Usage: ./download.sh sources.csv   (fill in the url column first)
# Requires: yt-dlp, ffmpeg.  Run on your own machine, only on footage you are licensed to use.
set -euo pipefail
csv="${1:-sources.csv}"
mkdir -p downloads
tail -n +2 "$csv" | python3 -c '
import csv, sys
for r in csv.reader(sys.stdin):
    if len(r) >= 4 and r[3].strip():
        print(r[0] + "\t" + r[3].strip())
' | while IFS=$'\t' read -r id url; do
  yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]" --merge-output-format mp4 \
    --download-archive downloads/archive.txt \
    -o "downloads/${id}_%(title).80s.%(ext)s" "$url"
done
