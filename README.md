# Stardust Story

## Automated edit pipeline

`build.py` is a reusable Python + ffmpeg pipeline that turns a script +
voiceover into a fully edited, graded episode for the Stardust Story
YouTube channel (cinematic Hollywood career documentaries, e.g. the
"Golden Four" series). See `pipeline/` for the eight build steps
(alignment, entity detection, asset resolution, EDL + review gate,
cinematic look, series elements, audio mix, render).

```
pip install -r requirements.txt
python build.py --script script/joseph_quinn.md --audio audio/narration.mp3 \
    --series "GOLDEN FOUR" --ep 2
# review build/edl_preview.html, then:
python build.py --script script/joseph_quinn.md --audio audio/narration.mp3 \
    --series "GOLDEN FOUR" --ep 2 --render
```

Required inputs (each directory has a README explaining its exact
contents): `script/<slug>.md`, `audio/narration.mp3`, an intro bumper in
`assets/intro/`, per-title folders in `footage/movies/`, score beds in
`music/`, and a `TMDB_API_KEY` in `.env` (copy `.env.example`).

Outputs land in `output/` (`<slug>_final.mp4`, `<slug>_chapters.txt`) and
`build/` (`missing_footage.md`, `decisions.md`, `credits.txt` — all
gitignored, regenerated per run).

## Earlier one-off renders

### Timberland Story — video production

"How a Poor Russian Boy Created Timberland" — a narrated documentary-style
YouTube video built from the user's own script and voiceover recording.

#### Status

Assembly pivoted from a local Remotion render to vidIQ's server-side
`vidiq_compose` tool. This session's network egress policy blocks direct
downloads from arbitrary external hosts (stock footage CDNs, etc.), so a
local Remotion/ffmpeg render couldn't pull in the required B-roll and
AI-generated clips. `vidiq_compose` renders entirely server-side from
hosted URLs, which avoids that constraint.

Because `vidiq_compose` caps output at 240s per call, the ~9:53 video is
split into 3 segments (`production/compose-segments.json`), rendered
separately, then stitched into one final file.

#### Files

- `production/script.txt` — full narration script, split by section.
- `production/shot-list.json` — the ~44-shot list with timecodes, source
  type (B-roll vs. AI-generated), source URL, and on-screen duration,
  reconciled to match the voiceover's exact length.
- `production/compose-segments.json` — the shot list split into 3
  sub-240s segments for `vidiq_compose`.
- `public/voiceover.m4a` — the user-provided voiceover recording.
