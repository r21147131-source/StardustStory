#!/bin/bash
# Lists top YouTube search hits (title | channel | duration | id) for each source query, for review before download.
while IFS='|' read -r key q; do
  echo "== $key :: $q"
  yt-dlp --no-warnings --skip-download --flat-playlist --print "%(id)s | %(duration_string)s | %(channel)s | %(title)s" "ytsearch4:$q" 2>/dev/null
done <<'LIST'
dd_born_again|Daredevil Born Again official trailer Marvel
dd_s2|Daredevil Born Again season 2 official trailer
dd_netflix|Marvel's Daredevil season 1 official trailer Netflix
dd_s3|Marvel's Daredevil season 3 official trailer Netflix
defenders|Marvel's The Defenders official trailer Netflix
punisher|Marvel's The Punisher season 2 official trailer
trueblood|True Blood season 1 official trailer HBO
escape|Escape Room 2019 official trailer
escape2|Escape Room Tournament of Champions official trailer
gow|God of War 2022 Ragnarok story trailer
critrole|Critical Role Deborah Ann Woll Twiggy
omu|Force Grey Lost City of Omu Deborah Ann Woll
queen|Queen of the Ring official trailer 2024
woll_int|Deborah Ann Woll interview Karen Page Daredevil Born Again
woll_panel|Deborah Ann Woll panel Karen Page girlfriend quote
scard|Dario Scardapane interview Daredevil Born Again Karen Page
LIST
