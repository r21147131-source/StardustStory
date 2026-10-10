# Download the footage for the Ernie Reyes Jr. cut (Windows PowerShell version).
#
#   1. Install yt-dlp, ffmpeg and Node.js (or Deno); open PowerShell in this folder.
#   2. If YouTube asks you to sign in, save your cookies as cookies.txt next to this script.
#   3. Run:   powershell -ExecutionPolicy Bypass -File .\download-clips.ps1
#             powershell -ExecutionPolicy Bypass -File .\download-clips.ps1 s10 s18   (only these slots)
#   4. Upload the ernie-clips folder (or a zip of it) back to Claude.
param([string[]]$Slots)
$out = "ernie-clips"; New-Item -ItemType Directory -Force $out | Out-Null
$cook = @(); if (Test-Path cookies.txt) { $cook = @("--cookies", "cookies.txt") }
$fmt = "bv*[height<=1080]+ba/b[height<=1080]/b"
# slot, start(sec), length(sec), url
$clips = @(
  @("s02", 10, 30, "https://www.youtube.com/watch?v=UlLWmFpEouI")  # Surf Ninjas trailer (early 90s)
  @("s06", 60, 30, "https://www.youtube.com/watch?v=rjUhnpjbDMQ")  # Ernie Sr. + West Coast Demo Team
  @("s07", 60, 30, "https://www.youtube.com/watch?v=I0YGSMq0wSQ")  # demo w/ Sr. & Jr., 1990
  @("s08", 30, 30, "https://www.youtube.com/watch?v=oifngY5UhPI")  # demo team performance
  @("s09", 20, 30, "https://www.youtube.com/watch?v=5RGju9NuoOU")  # Enter the Dragon trailer
  @("s10", 5, 30, "https://www.youtube.com/watch?v=Z7Crt4S1IZM")  # The Last Dragon trailer
  @("s11", 10, 30, "https://www.youtube.com/watch?v=LWfEL_zAA78")  # Red Sonja trailer
  @("s12", 100, 30, "https://www.youtube.com/watch?v=FkZFmpVKnFY")  # Ernie Jr. action highlights
  @("s13", 200, 30, "https://www.youtube.com/watch?v=FkZFmpVKnFY")  # more highlights
  @("s14", 5, 30, "https://www.youtube.com/watch?v=FMJPwRWaZBI")  # TMNT (1990) trailer
  @("s15", 10, 30, "https://www.youtube.com/watch?v=3y9C_P7dG6s")  # TMNT 4K trailer
  @("s16", 40, 30, "https://www.youtube.com/watch?v=3y9C_P7dG6s")  # TMNT trailer, later part
  @("s17", 10, 30, "https://www.youtube.com/watch?v=T6sjDuhZKCQ")  # TMNT original trailer
  @("s18", 5, 30, "https://www.youtube.com/watch?v=al9jfY7zOBY")  # TMNT II trailer
  @("s19", 5, 30, "https://www.youtube.com/watch?v=7ycjTzPPdIc")  # Keno intro pizza scene
  @("s20", 10, 30, "https://www.youtube.com/watch?v=1ulJwDjpD30")  # TMNT II 4K trailer
  @("s21", 20, 30, "https://www.youtube.com/watch?v=0vidhKXSlYs")  # "Pizza Boy" clip
  @("s22", 10, 30, "https://www.youtube.com/watch?v=UlLWmFpEouI")  # Surf Ninjas trailer
  @("s23", 5, 30, "https://www.youtube.com/watch?v=khoiWMnQw6o")  # Surf Ninjas VHS trailer
  @("s24", 5, 30, "https://www.youtube.com/watch?v=bCZ1CIQ64YQ")  # Bloodsport trailer (Van Damme)
  @("s25", 300, 30, "https://www.youtube.com/watch?v=FkZFmpVKnFY")  # Ernie Jr. interview
  @("s26", 420, 30, "https://www.youtube.com/watch?v=FkZFmpVKnFY")  # interview
  @("s27", 540, 30, "https://www.youtube.com/watch?v=FkZFmpVKnFY")  # interview
  @("s28", 20, 30, "https://www.youtube.com/watch?v=bf61mm7ClbQ")  # Ernie Jr. on fight scenes
  @("s29", 120, 30, "https://www.youtube.com/watch?v=bf61mm7ClbQ")  # interview
  @("s30", 200, 30, "https://www.youtube.com/watch?v=bf61mm7ClbQ")  # interview
  @("s31", 10, 30, "https://www.youtube.com/watch?v=XmUOlVAuGeo")  # The Rundown fight scene
  @("s32", 60, 30, "https://www.youtube.com/watch?v=AYSVCFfgSu0")  # Rock vs. Manito
  @("s33", 30, 30, "https://www.youtube.com/watch?v=R2CPfA5eFa4")  # The Rundown trailer
  @("s34", 90, 30, "https://www.youtube.com/watch?v=R2CPfA5eFa4")  # The Rundown trailer, later part
  @("s35", 0, 30, "https://www.youtube.com/watch?v=IipH4uShx34")  # Ernie Jr. needs a kidney (news)
  @("s36", 0, 30, "https://www.youtube.com/watch?v=mgmdy4Ygzyc")  # Ernie Jr. on his health
  @("s37", 30, 30, "https://www.youtube.com/watch?v=mgmdy4Ygzyc")  # kidney recovery
  @("s38", 600, 30, "https://www.youtube.com/watch?v=BRmuJrG7uHg")  # long interview
  @("s39", 1200, 30, "https://www.youtube.com/watch?v=BRmuJrG7uHg")  # long interview
  @("s40", 1800, 30, "https://www.youtube.com/watch?v=BRmuJrG7uHg")  # long interview
  @("s41", 300, 30, "https://www.youtube.com/watch?v=iR-VrtGdkiQ")  # Art of Action episode
  @("s42", 900, 30, "https://www.youtube.com/watch?v=iR-VrtGdkiQ")  # Art of Action episode
)
foreach ($c in $clips) {
  $slot, $start, $len, $url = $c
  if ($Slots -and ($Slots -notcontains $slot)) { continue }
  if (Test-Path "$out\$slot.mp4") { Write-Host "skip $slot (exists)"; continue }
  $end = $start + $len
  Write-Host "== $slot  $url  [${start}s-${end}s]"
  & yt-dlp @cook --extractor-args "youtube:player_client=web_safari" -f $fmt --merge-output-format mp4 `
      --download-sections "*$start-$end" --force-keyframes-at-cuts -o "$out\$slot.%(ext)s" $url
  if ($LASTEXITCODE -ne 0) { Write-Host "!! $slot failed" }
}
Write-Host "`nDone. Upload the '$out' folder (or zip it)."
