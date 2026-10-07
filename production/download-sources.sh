#!/bin/bash
# Downloads chosen YouTube sources into footage/ as <key>.mp4 (<=1080p). Footage is gitignored.
mkdir -p footage
while read -r key id; do
  [ -f "footage/$key.mp4" ] && continue
  yt-dlp --no-warnings -q -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]" --merge-output-format mp4 \
    -o "footage/$key.%(ext)s" "https://www.youtube.com/watch?v=$id" 2>&1 | tail -2 || echo "FAIL $key"
done <<'LIST'
dd_born_again 7xALolZzhSM
dd_s2_trailer U1MqJBVn8Rk
dd_s2_teaser sBVjIlTjoIk
dd_netflix_s1 jAy6NJ_D5vU
dd_netflix_s3 n83s6NO1NE0
defenders jYvHxEEgrPA
punisher_s2 jrLhP5sK2wI
trueblood_s1 3Wk3HSiX-vQ
escape_room 6dSKUoV0SNI
escape_room2 KlfUbZJVInA
god_of_war hfJ4Km46A-0
critrole_twiggy exv7cxs4JBg
queen_of_ring -g6-VuXktNM
woll_interview_critqal hShoaJa3beU
woll_interview_et aAL7KgQu9pw
woll_nycc_dnd ItNH91X92D0
cast_rt AUmUgYPk-IY
scardapane_collider m4TNkooOlJ4
scardapane_marvel EtA-25hBiXc
LIST
