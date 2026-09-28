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

## Voiceover check (ElevenLabs Scribe transcript, 2026-09-28)
`public/golden-four-ep5-voiceover.mp3` is a recording of the **original**
script (`golden-four-ep5-script.md`), not v1.1. The audio contains these lines, which need fixing:
- s109 "Sue Storm is pregnant during Avengers: Doomsday." (in the film, Franklin is born in First Steps)
- s113 "In The Crown, she was typecast as a young royal." (the role won her a BAFTA)
- s142 "Richard Jewell in Chernobyl." (he wasn't in either)
- s159 "...where Susan Levin never existed..." (Levin is Downey's real wife)
- s169 "He chose Susan." (Tony chose Pepper)
- s184 "...play the thing he escaped in real life, the man who chose power over people."
- s74–s77, s124–s128, s146–s152: the Doomsday plot and dialogue, stated as fact
- s156 "a twist that Marvel Studios has been hinting at" (this is a fan theory)

## Render status (2026-09-28)
- `sent_times.json`: the start time of each script sentence in the voiceover. Built from
  pause detection plus anchors from the Scribe transcript; accurate to about ±2s.
- `build_compose.py sent_times.json clips.json OUTDIR` writes `compose-seg{1..5}.json`, one
  vidiq_compose payload per segment (32–39 scenes each, TMDB stills plus Pexels B-roll,
  interview insets, lower-thirds, title and end card). `clips.json` maps
  imax/rdj/pascal to freshly signed trim URLs. They're not committed because they expire.
- Blocked: vidiq_compose costs **56 credits per segment** (about 280 for the whole video). The account had 38.
- Local render (costs no credits): `pip install imageio-ffmpeg pillow`, then
  `python production/ep5/render_local.py WORKDIR output/golden-four-ep5/the-collision.mp4`
  (WORKDIR holds `compose-seg*.json`). Needs `image.tmdb.org` and `videos.pexels.com`
  reachable. `--placeholders --preview --only N` gives a quick pipeline test.
