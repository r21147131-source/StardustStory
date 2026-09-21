# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## DONE — episode assembled and delivered

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done, reconciled to the real voiceover.
   `pantheon-ep1-shot-list-final.json` (639.31s vs 639.27s VO, 0.04s off).
3. **Voiceover** — done. `public/pantheon-ep1-voiceover.mp3` (10:39).
4. **All 9 script AI shots + S04/S13 fallback** — done. 32 clips in
   `public/pantheon-ep1-clips/`.
5. **Motion graphics (12: 11 + logo card)** — done. Real Remotion/React
   components in `src/graphics/`, rendered to video.
6. **Archival footage (9 cues)** — done. Real photos in
   `public/pantheon-ep1-archival/` (ice core, craters, cave art,
   Gilgamesh tablet, Göbekli Tepe, museum specimens).
7. **Assembly/render** — **done**, via `vidiq_compose` (3 segments,
   stitched with ffmpeg). See below.

## Final assembly

Built `production/pantheon-ep1-compose-segment-{1,2,3}.json` — a 57-scene
plan derived from the shot list, using each source's `raw.githubusercontent.com`
URL (this repo is public, so no separate hosting step was needed). Multi-beat
cues (S15, S22, S13, S04, S10, S20, S01, S07, S26, S17, S27) split their
duration across sub-clips in narration order; redundant-alternate cues
picked one representative clip; S18's single clip repeats 3x (no native
video loop in the tool); S32 (credits) reuses 8 clips already used
elsewhere; S29 (fade) folded into S30's `dip_to_black` transition.

Submitted all 3 segments to `vidiq_compose` (~213s each, under its 240s
cap), downloaded the rendered outputs, and concatenated with `ffmpeg -c copy`
(same codec/resolution/fps across all three, so no re-encode needed).

**Result:** `output/pantheon-ep1-final.mp4` — 639.55s (10:39), 1920×1080,
audio intact throughout, verified at multiple checkpoints including both
segment splices (clean, no artifacts beyond one expected single-frame black
flash exactly at a splice point).

### Delivery

The final file (574MB) and the 3 raw segments (163-263MB each) all exceed
GitHub's 100MB push limit, so they're **not** committed to this repo —
gitignored instead (see `.gitignore`). They were delivered directly to the
user:
- A compressed 480p preview (~20MB) sent via chat.
- Direct S3 download links to the 3 full-quality 1080p segments (signed
  URLs, valid ~12h from render time — **expired by now** if this is read
  later; re-render via the segment JSON files to get fresh links).

To reproduce or re-render: the 3 segment JSON files in `production/` are
ready to resubmit to `vidiq_compose` as-is. To rebuild the segment plan
from scratch (e.g. after swapping an asset), see
`/tmp` scratch scripts referenced in the commit history, or rewrite
using the same logic: split `pantheon-ep1-shot-list-final.json` into
≤240s chunks, map each `src` entry to its `raw.githubusercontent.com`
URL, and set each segment's `voiceover.trimStartSeconds` to the
cumulative offset.

## Known non-blocking flags

- `S08a-airbursts-over-ice-NEEDS-FIX.mp4` (in `pantheon-ep1-clips/`) has a
  fabricated "ARCHIVE FOOTAGE: NOV 14, 2023" timestamp burned in — **not
  used** in the final assembly (clean alternates covered S08 instead).
- `FLAGGED-likely-AI-generated-DO-NOT-USE-AS-ARCHIVAL.jpg` (in
  `pantheon-ep1-archival/`) — an implausible underground industrial
  complex image, inconsistent with the other genuine archival photos —
  **not used**.
- `EXTRA-modern-arctic-base-unassigned.webp` — spare b-roll, unused, no
  particular cue match.

## If revisiting this episode

- Re-render is straightforward: resubmit the 3 segment JSONs to
  `vidiq_compose`, download, concatenate with `ffmpeg -c copy`.
- To change an asset: edit `pantheon-ep1-shot-list-final.json`, regenerate
  the affected segment JSON's scene entry, resubmit just that segment.
- The full per-shot asset map (which files cover which cue) lives in
  `pantheon-ep1-shot-list-final.json` and the segment JSON files.
