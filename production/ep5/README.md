# Ep5 production notes

- `tmdb-images.json`: TMDB image paths collected through Firecrawl (the sandbox
  can't reach TMDB directly). URL = `https://image.tmdb.org/t/p/w1280/<path>.jpg`
  (use `w780` for posters and profile photos). 20 sources, 101 images.
  - Profile photos are portrait: use `layout: "fit"` in vidiq_compose.
  - `doomsday`: the film is unreleased, so check its images are official art, not fan edits.
- Segment cut points, placed on natural pauses in the audio (s): 0, 222.23, 412.12, 608.98, 794.20, 1007.18.
- Interview clips (vidIQ trim of YouTube): these come out at only 256x144, so use them as small inset windows only.
  - IGN, Hall H Doom reveal (okIjPJG9dz4, 0–120s → 66.8s clip)
  - EPK clip of Pascal at the First Steps premiere (Iab-JLbOV4Q, 0–60s; watermark in the first ~6s)
  - IMAX four-cast interview (Z4CxHxYbYnA, 20–200s)
  Their signed URLs expire, so trim again before rendering.

## Voiceover (re-recorded 2026-09-28)
`public/golden-four-ep5-voiceover.mp3` is now the user's re-recording of the fact-checked
script (`production/golden-four-ep5-recording-script.txt`, = v1.1 without headings), 14:34.
The original recording (which read the unrevised draft) is in git history only.

## Render
- `align_vo.py` → `sent_times.json`: sentence start times, found by snapping each sentence
  break to a detected pause (ffmpeg silencedetect -35dB/0.18s) with a DP on sentence length.
  No transcript needed; section breaks all land on 0.8–2.6s pauses.
- `build_compose.py sent_times.json - OUTDIR` writes `compose-seg{1..5}.json` (cuts at
  0, 202.03, 342.01, 568.14, 804.03, 873.64). Pass a clips.json instead of `-` to add the
  interview insets (freshly signed vidIQ trim URLs; skipped otherwise).
- `render_local.py WORKDIR OUT.mp4` renders with ffmpeg only (no Python packages).
  Set `FFMPEG=` to a build with libx264 + libfreetype (BtbN's linux64-gpl static build works).
  Needs `image.tmdb.org` and `videos.pexels.com`. `--preview --only N` for a quick test.
