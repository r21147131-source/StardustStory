# Build the full cut on your own machine (Windows / macOS / Linux)

`ernie-build.py` joins your two voiceovers, lays title cards / labels / grain / letterbox over footage and
photos, and writes `output/ernie-reyes-jr.mp4`. A scene uses a clip or photo if one named for its slot is in
`production/media/`; otherwise it renders a title card. Nothing downloads from inside the script.

## 1. Install (once)

Windows (PowerShell):

    winget install Python.Python.3.12
    winget install Gyan.FFmpeg
    winget install OpenJS.NodeJS.LTS
    pip install pillow "yt-dlp[default]"

macOS: `brew install python ffmpeg node` then `pip3 install pillow "yt-dlp[default]"`.
Linux: your package manager for python3, ffmpeg, nodejs, then the same pip line.

Font (optional but recommended): download Inter from https://rsms.me/inter/ and unzip it. Set
`ERNIE_FONTS` to the folder holding `Inter-Bold.otf`, `InterDisplay-Black.otf` etc. Without it the script
falls back to Segoe UI / Arial / DejaVu and the look changes slightly.

## 2. Get the project

    git clone -b claude/amazing-bohr-jsyaed https://github.com/r21147131-source/StardustStory.git
    cd StardustStory

## 3. Put the media in `production/media/`

- **Footage:** run `production\download-clips.ps1` (Windows) or `bash production/download-clips.sh`
  from an empty working folder. It creates `ernie-clips/` with `s07.mp4 ... s42.mp4`. Copy those into
  `production/media/`. If YouTube asks you to sign in, put a `cookies.txt` next to the script.
- **Your own clips:** `s02.m4v` and `s06.m4v` (the files you sent) go in the same folder.
- **Photos** (Wikimedia Commons): save as `ernie_jr.jpg`, `bruce.jpg`, `chan.jpg`, `jcvd.jpg`, `rock.jpg`.
  PowerShell:

      cd production\media
      $ua = "StardustStoryVideo/1.0 (you@example.com)"
      iwr -UserAgent $ua -OutFile ernie_jr.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Ernie_Reyes_Jr.jpg"
      iwr -UserAgent $ua -OutFile bruce.jpg    "https://commons.wikimedia.org/wiki/Special:FilePath/Bruce_Lee_as_Chen_Zhen_(4x5_cropped).jpg"
      iwr -UserAgent $ua -OutFile chan.jpg     "https://commons.wikimedia.org/wiki/Special:FilePath/Jackie_Chan.jpg"
      iwr -UserAgent $ua -OutFile jcvd.jpg     "https://commons.wikimedia.org/wiki/Special:FilePath/Jean-Claude_Van_Damme_at_Brussels_Comic_Con_2023_DSC19480_Kiri_DxO.jpg"
      iwr -UserAgent $ua -OutFile rock.jpg     "https://commons.wikimedia.org/wiki/Special:FilePath/Dwayne_The_Rock_Johnson_2009_street_portrait.jpg"

  Commons rate-limits quickly: if you get an error, wait a minute and retry. Credits: `photo-credits.md`.

## Shortcut (Windows): steps 3 and 4 in one command

    powershell -ExecutionPolicy Bypass -File .\production\build-full.ps1 -Clips C:\path\to\ernie-clips -Own C:\path\to\s02-and-s06-folder -Vo1 C:\path\part1.mp3 -Vo2 C:\path\part2.mp3

It copies your clips into `production\media`, fetches the five photos, and runs the build.

## 4. Build

Windows (PowerShell), from the repo root:

    $env:ERNIE_VO1 = "C:\path\to\CapCut_TTS_Bill_D20260713_T081806.mp3"
    $env:ERNIE_VO2 = "C:\path\to\CapCut_TTS_Bill_D20260713_T082752.mp3"
    $env:ERNIE_FONTS = "C:\path\to\inter\folder"      # optional
    python production\ernie-build.py

macOS / Linux:

    ERNIE_VO1=/path/part1.mp3 ERNIE_VO2=/path/part2.mp3 python3 production/ernie-build.py

Output: `output/ernie-reyes-jr.mp4` (1080p, 17:17, about 100 MB with clips). It takes 30-40 minutes.

## Useful options

| Option | What it does |
|---|---|
| `--only s10,s18` | re-render just those scenes (stored in the work folder) |
| `--only s10 --assemble` | stitch the already-rendered scenes + audio without re-rendering |
| `--res 1280x720` | render smaller (faster) |
| `ERNIE_CLIPFREE=1` + `ERNIE_MEDIA=<folder with only your clips and photos>` | the version with no third-party film footage |
| `ERNIE_WORK`, `ERNIE_OUT` | scratch folder / output file |
| `--vo1`, `--vo2` | voiceover paths (same as the env variables) |

## Changing what a scene shows

Edit the tables near the top of `ernie-build.py`: `SLOT_SRC` (reuse another slot's clip at a start time),
`SLOT_OPTS` (start offset, crop to hide a watermark), `PHOTO_FIRST` (photo instead of clip), `MONTAGE`
(the quick-cut openings), and the scene list `SC` (headlines, labels). Slot names are in `ernie-media-links.md`.

## Rights

Trailers and film clips are copyrighted. Using them in a commentary video may be fair use, but that is your
call, and a platform may still claim or remove the video. The clip-free build avoids that.
