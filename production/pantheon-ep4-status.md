# Pantheon Ep.4 — "The Forgotten Ones" (Kush / 25th Dynasty) — Status

**Episode complete end to end:** script → voiceover → shot list → AI clips →
archival photos → motion graphics → assembly → delivery.

1. **Script** — `pantheon-ep4-kush-script.md`. 7 parts, 111 narration beats
   (57 AI, 34 archival, 20 motion graphic).
2. **Shot list** — `pantheon-ep4-shot-list.json` (source of truth, edited
   incrementally as assets were matched) and `pantheon-ep4-shot-list-final.json`
   (voiceover-reconciled timing, see below).
3. **AI clips — all 57 cues / 71 individual clip slots covered.** User-supplied
   (Veo-generated from prompts in `pantheon-ep4-visual-prompts.md`), sorted
   into `public/pantheon-ep4-clips/`. Full match-quality notes in
   `pantheon-ep4-sources.md`. Two beats (B023, B040) kept a secondary
   alternate take flagged as a slightly looser match; everything else is a
   strong or exact match.
4. **Archival photos — all 34 beats covered.** Mix of user-uploaded photos
   (most, with user-confirmed labels for several) and 20 pulled directly
   from Wikimedia Commons once the environment's network policy was opened
   to that domain mid-session. Full list and confidence notes in
   `pantheon-ep4-sources.md`. 6 beats (B002, B003, B014 alternate, B048,
   B052, B060) remain flagged as tentative/unconfirmed identifications —
   worth a second look before a future re-cut, not blocking for this one.
5. **Motion graphics — all 20 of 20 built and rendered.** New Remotion
   components in `src/graphics/` (`EP4_` prefix), registered in
   `src/Root.tsx`, rendered via the local Playwright headless-shell pipeline
   (`remotion.config.ts`). A layout bug in `EP4_B102_KingListScroll` (names
   rendering on one line instead of stacking) was caught on visual review
   and fixed before committing.
6. **Voiceover reconciliation — done.** User supplied the real recording
   (`public/pantheon-ep4-voiceover.mp3`, 759.43s). `pantheon-ep4-allocate.py`
   scaled every beat's provisional 150wpm narration estimate by 0.97164x
   and wrote `pantheon-ep4-shot-list-final.json` (759.48s total, matching
   target to within 0.05s). All 20 motion graphics were re-rendered at their
   corrected frame counts.
7. **Assembly — done, via local ffmpeg** (same path as Ep.2; `vidiq_compose`
   was ruled out — only 18 credits left, needs ~200+ for a multi-segment job
   at this length):
   - `pantheon-ep4-build-scenes.py` derives a 140-scene plan
     (`pantheon-ep4-scenes.json`) from the final shot list: multi-take AI
     beats split evenly across their clips, short clips loop to fill their
     allotted time, long clips trim from a non-literal start point, B049
     (a narration-less cutaway nested inside B048's line) borrows 4s from
     B048's window instead of getting a zero-length scene.
   - `pantheon-ep4-render-segments.sh` renders all 140 scenes to normalized
     1920×1080/30fps clips (images held static, video scaled/cropped/
     trimmed/looped as needed) into `output/ep4-segments/` (gitignored,
     intermediate only) — validated against 3 representative scenes before
     running the full batch.
   - Concatenated with `ffmpeg -f concat -c copy`. The stream-copy concat
     corrupted only the throwaway silent-audio track's duration metadata
     (confirmed via decode-based playback check — the video stream itself
     was correct at 759.17s); the real voiceover was muxed on fresh
     afterward, so this never affected the deliverable.
   - **Result:** `output/pantheon-ep4-final.mp4` — 759.20s (12:39),
     1920×1080, audio healthy (-20.0dB mean, -1.9dB max, not silent).
     Verified at 7 timestamps spanning the full runtime (cold open,
     Karnak colonnade, Piye praying, column-raising construction, Napata
     map graphic, Augustus bronze head, cartouche-grid graphic) — all land
     on the correct content.

## Delivery

- **Original full-quality file** (329MB) uploaded to CreativeClaw storage
  (real PUT upload, not inline base64 — Google Drive's only available tool
  here requires embedding the whole file as base64 in one call, which isn't
  workable at this size) and hosted at a durable public URL:
  `https://cdn.creativeclaw.co/u/a4eaf4ab/videos/db79e426-d4f1-423f-9efc-745b0afaa54c.mp4`
- **Compressed full-quality version** committed to the repo:
  `output/pantheon-ep4-full-compressed.mp4` — two-pass H.264 (811k/973k
  maxrate/1947k bufsize, preset slow, 128k AAC audio), 88.6MB, 1920×1080,
  759.20s. Same compression recipe pattern as Ep.1/Ep.2, under GitHub's
  100MB push limit.

## Known non-blocking flags

- B002, B003, B014 (alternate photo), B048, B052, B060 — archival photo
  matches that are plausible but not independently confirmed as the exact
  objects/sites named in the brief. Worth a second look before a future
  re-cut.
- B082, B109 — deliberate substitutes for damnatio-memoriae beats where no
  Kushite-specific example was found (Hatshepsut erasure, Akhenaten-erased
  situla). Real erasure examples, same concept, different subject — not
  what the literal guidance named.
- B023, B040 — AI clips kept a secondary alternate take alongside the
  primary match, flagged as slightly looser fits worth a second look.

## If revisiting this episode

- To change an asset: edit `pantheon-ep4-shot-list.json` (the live source
  of truth), re-run `pantheon-ep4-allocate.py` if timing needs to shift,
  then `pantheon-ep4-build-scenes.py` and `pantheon-ep4-render-segments.sh`
  to rebuild just the affected scene(s) — no need to re-render everything.
- The 140-scene intermediate clips in `output/ep4-segments/` are gitignored
  and not committed; re-run the render script to regenerate them.
