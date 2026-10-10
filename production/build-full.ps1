# One-command build of the full cut on Windows (PowerShell). Run from the repo root:
#
#   powershell -ExecutionPolicy Bypass -File .\production\build-full.ps1 `
#       -Clips  C:\path\to\ernie-clips `
#       -Own    C:\path\to\folder-with-s02.m4v-and-s06.m4v `
#       -Vo1    C:\path\to\CapCut_TTS_Bill_D20260713_T081806.mp3 `
#       -Vo2    C:\path\to\CapCut_TTS_Bill_D20260713_T082752.mp3 `
#       [-Fonts C:\path\to\inter\folder]
#
# Needs python, pillow, ffmpeg on PATH (see production\PORTABLE.md). Output: output\ernie-reyes-jr.mp4 (1080p).
param(
  [Parameter(Mandatory)] [string]$Clips,
  [Parameter(Mandatory)] [string]$Own,
  [Parameter(Mandatory)] [string]$Vo1,
  [Parameter(Mandatory)] [string]$Vo2,
  [string]$Fonts
)
$ErrorActionPreference = "Stop"
$media = Join-Path $PSScriptRoot "media"
New-Item -ItemType Directory -Force $media | Out-Null

# 1. footage + your own clips
$n = 0
Get-ChildItem $Clips -Filter "s*.mp4" | ForEach-Object { Copy-Item $_.FullName $media -Force; $n++ }
foreach ($f in "s02.m4v", "s06.m4v") {
  $p = Join-Path $Own $f
  if (Test-Path $p) { Copy-Item $p $media -Force; $n++ } else { Write-Warning "missing $f in $Own" }
}
Write-Host "copied $n media files into $media"

# 2. photos from Wikimedia Commons (skipped if already there)
$ua = "StardustStoryVideo/1.0 (build-full.ps1)"
$photos = @{
  "ernie_jr.jpg" = "Ernie_Reyes_Jr.jpg"
  "bruce.jpg"    = "Bruce_Lee_as_Chen_Zhen_(4x5_cropped).jpg"
  "chan.jpg"     = "Jackie_Chan.jpg"
  "jcvd.jpg"     = "Jean-Claude_Van_Damme_at_Brussels_Comic_Con_2023_DSC19480_Kiri_DxO.jpg"
  "rock.jpg"     = "Dwayne_The_Rock_Johnson_2009_street_portrait.jpg"
}
foreach ($k in $photos.Keys) {
  $dst = Join-Path $media $k
  if ((Test-Path $dst) -and (Get-Item $dst).Length -gt 20000) { continue }
  for ($i = 1; $i -le 6; $i++) {
    try { Invoke-WebRequest -UserAgent $ua -OutFile $dst "https://commons.wikimedia.org/wiki/Special:FilePath/$($photos[$k])"; break }
    catch { Write-Host "retry $k ($i)"; Start-Sleep -Seconds (20 * $i) }
  }
}

# 3. build
$env:ERNIE_VO1 = $Vo1; $env:ERNIE_VO2 = $Vo2
if ($Fonts) { $env:ERNIE_FONTS = $Fonts }
Remove-Item Env:ERNIE_CLIPFREE, Env:ERNIE_MEDIA -ErrorAction SilentlyContinue
python (Join-Path $PSScriptRoot "ernie-build.py")
Write-Host "`nDone: output\ernie-reyes-jr.mp4"
