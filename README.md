# Timberland Story — video production

"How a Poor Russian Boy Created Timberland" — a narrated documentary-style
YouTube video built from the user's own script and voiceover recording.

## Status

Assembly pivoted from a local Remotion render to vidIQ's server-side
`vidiq_compose` tool. This session's network egress policy blocks direct
downloads from arbitrary external hosts (stock footage CDNs, etc.), so a
local Remotion/ffmpeg render couldn't pull in the required B-roll and
AI-generated clips. `vidiq_compose` renders entirely server-side from
hosted URLs, which avoids that constraint.

Because `vidiq_compose` caps output at 240s per call, the ~9:53 video is
split into 3 segments (`production/compose-segments.json`), rendered
separately, then stitched into one final file.

## Files

- `production/script.txt` — full narration script, split by section.
- `production/shot-list.json` — the ~44-shot list with timecodes, source
  type (B-roll vs. AI-generated), source URL, and on-screen duration,
  reconciled to match the voiceover's exact length.
- `production/compose-segments.json` — the shot list split into 3
  sub-240s segments for `vidiq_compose`.
- `public/voiceover.m4a` — the user-provided voiceover recording.

## Consumed — Episode 1: Daniel Day-Lewis

- `public/consumed-ep1-daniel-day-lewis-voiceover.mp3`: the user's voiceover (10:25).
- `production/consumed-ep1-script.md`: the narration script, by section.
- `production/consumed-ep1-align.py` → `consumed-ep1-sentences.json`: sentence start times,
  found by snapping sentence breaks to pauses in the voiceover (ported from Ep5; no transcript).
- `production/consumed-ep1-edit.py` → `consumed-ep1-edl.json`: the edit, one cue per mention.
  A named film gets its TMDB poster and then trailer footage. A named person gets their TMDB
  photo and a caption. Gaps get interview clips, TMDB stills and Pexels B-roll. Trailers and
  interviews are YouTube trims made with `vidiq_edit_media`. They come back at about 256x144,
  so they play framed over a blurred copy of themselves. Rendered locally with ffmpeg.
- `production/consumed-ep1-build.py`: the earlier B-roll-only cut. It also downloads the Pexels
  clips the edit uses (`render/consumed-ep1/src/`).
- `production/consumed-ep1-credits.md`: sources and attribution for the YouTube description.
- `output/consumed-ep1/daniel-day-lewis-consumed-720p.mp4`: the final render at 720p. The 1080p master is 181MB, over GitHub's file limit, so it stays out of the repo.
