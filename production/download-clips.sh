#!/usr/bin/env bash
# Download the footage for the Ernie Reyes Jr. cut, one ~30 s clip per scene slot.
#
# Run this on YOUR machine (YouTube blocks the cloud sandbox), then upload the
# whole  ernie-clips/  folder (or a zip of it) back to Claude.  Files are named
# s10.mp4, s11.mp4 ... exactly as the build script expects.
#
# Needs: yt-dlp (latest: yt-dlp -U) + ffmpeg + a JavaScript runtime (Node or Deno) --
# without one, yt-dlp warns "n challenge solving failed" and offers only thumbnails.   Optional: a cookies file next to this script
# (cookies.txt, Netscape format) if YouTube asks you to sign in.
#
#   bash download-clips.sh            # all slots
#   bash download-clips.sh s10 s18    # only these slots
set -u
OUT=ernie-clips; mkdir -p "$OUT"
COOK=(); [ -f cookies.txt ] && COOK=(--cookies cookies.txt)
FMT='bv*[height<=1080]+ba/b[height<=1080]/b'

#  slot  start(sec)  length(sec)  url                                             # what
CLIPS=$(cat <<'EOF'
s02   10   30  https://www.youtube.com/watch?v=UlLWmFpEouI   # Surf Ninjas trailer (early 90s)
s06   60   30  https://www.youtube.com/watch?v=rjUhnpjbDMQ   # Ernie Sr. + West Coast Demo Team
s07   60   30  https://www.youtube.com/watch?v=I0YGSMq0wSQ   # demo w/ Sr. & Jr., 1990
s08   30   30  https://www.youtube.com/watch?v=oifngY5UhPI   # demo team performance
s09   20   30  https://www.youtube.com/watch?v=5RGju9NuoOU   # Enter the Dragon trailer
s10    5   30  https://www.youtube.com/watch?v=Z7Crt4S1IZM   # The Last Dragon trailer
s11   10   30  https://www.youtube.com/watch?v=LWfEL_zAA78   # Red Sonja trailer
s12   30   30  https://www.youtube.com/watch?v=CcEbxUJi7uA   # Ernie Jr. action highlights
s13  120   30  https://www.youtube.com/watch?v=CcEbxUJi7uA   # more highlights
s14    5   30  https://www.youtube.com/watch?v=FMJPwRWaZBI   # TMNT (1990) trailer
s15   10   30  https://www.youtube.com/watch?v=3y9C_P7dG6s   # TMNT 4K trailer
s16   40   30  https://www.youtube.com/watch?v=3y9C_P7dG6s   # TMNT trailer, later part
s17   10   30  https://www.youtube.com/watch?v=T6sjDuhZKCQ   # TMNT original trailer
s18    5   30  https://www.youtube.com/watch?v=al9jfY7zOBY   # TMNT II trailer
s19    5   30  https://www.youtube.com/watch?v=7ycjTzPPdIc   # Keno intro pizza scene
s20   10   30  https://www.youtube.com/watch?v=1ulJwDjpD30   # TMNT II 4K trailer
s21   20   30  https://www.youtube.com/watch?v=0vidhKXSlYs   # "Pizza Boy" clip
s22   10   30  https://www.youtube.com/watch?v=UlLWmFpEouI   # Surf Ninjas trailer
s23    5   30  https://www.youtube.com/watch?v=khoiWMnQw6o   # Surf Ninjas VHS trailer
s24    5   30  https://www.youtube.com/watch?v=bCZ1CIQ64YQ   # Bloodsport trailer (Van Damme)
s25  300   30  https://www.youtube.com/watch?v=FkZFmpVKnFY   # Ernie Jr. interview
s26  420   30  https://www.youtube.com/watch?v=FkZFmpVKnFY   # interview
s27  540   30  https://www.youtube.com/watch?v=FkZFmpVKnFY   # interview
s28   20   30  https://www.youtube.com/watch?v=bf61mm7ClbQ   # Ernie Jr. on fight scenes
s29  120   30  https://www.youtube.com/watch?v=bf61mm7ClbQ   # interview
s30  200   30  https://www.youtube.com/watch?v=bf61mm7ClbQ   # interview
s31   10   30  https://www.youtube.com/watch?v=XmUOlVAuGeo   # The Rundown fight scene
s32   60   30  https://www.youtube.com/watch?v=AYSVCFfgSu0   # Rock vs. Manito
s33   30   30  https://www.youtube.com/watch?v=R2CPfA5eFa4   # The Rundown trailer
s34   90   30  https://www.youtube.com/watch?v=R2CPfA5eFa4   # The Rundown trailer, later part
s35    0   30  https://www.youtube.com/watch?v=IipH4uShx34   # Ernie Jr. needs a kidney (news)
s36    0   30  https://www.youtube.com/watch?v=mgmdy4Ygzyc   # Ernie Jr. on his health
s37   30   30  https://www.youtube.com/watch?v=mgmdy4Ygzyc   # kidney recovery
s38  600   30  https://www.youtube.com/watch?v=BRmuJrG7uHg   # long interview
s39 1200   30  https://www.youtube.com/watch?v=BRmuJrG7uHg   # long interview
s40 1800   30  https://www.youtube.com/watch?v=BRmuJrG7uHg   # long interview
s41  300   30  https://www.youtube.com/watch?v=iR-VrtGdkiQ   # Art of Action episode
s42  900   30  https://www.youtube.com/watch?v=iR-VrtGdkiQ   # Art of Action episode
EOF
)

want=("$@")
while read -r slot start len url _; do
  [ -z "${slot:-}" ] && continue
  if [ ${#want[@]} -gt 0 ] && [[ ! " ${want[*]} " =~ " $slot " ]]; then continue; fi
  [ -f "$OUT/$slot.mp4" ] && { echo "skip $slot (exists)"; continue; }
  end=$((start + len))
  echo "== $slot  $url  [${start}s-${end}s]"
  yt-dlp "${COOK[@]}" --extractor-args "youtube:player_client=web_safari" \
    -f "$FMT" --merge-output-format mp4 \
    --download-sections "*${start}-${end}" --force-keyframes-at-cuts \
    -o "$OUT/$slot.%(ext)s" "$url" || echo "!! $slot failed"
done <<< "$CLIPS"

echo; echo "Done. Upload the '$OUT' folder (or: zip -r ernie-clips.zip $OUT)."
