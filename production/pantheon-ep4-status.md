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

## Post-cut revisions (first assembled cut → user feedback)

The first assembled cut had three real problems, flagged by the user after
watching it:

1. **Archival stills were hard-cropped.** The original per-scene ffmpeg
   filter (`scale=increase,crop=1920:1080`) forced every still to fill
   16:9 by cropping the overflow — for the many portrait-oriented photos
   (some as extreme as 0.38:1), that meant losing 50-80% of the image's
   vertical extent. Fixed: each still is now composited full-content
   (a blurred, darkened copy of itself scaled to fill as the backdrop,
   the unmodified image centered and fit on top — no cropping) plus a
   slow Ken Burns zoom. All 36 image segments re-rendered.
2. **Stills had no motion** — a plain static hold for their full
   duration. Fixed by the same change above (zoompan-driven slow
   zoom-in). Note: zoompan's `d` parameter must be the *total output
   frame count*, not `1` — with `d=1` the filter silently produces a
   perfectly static image despite looking correct in the command.
3. **The 11 Nile-valley map graphics (MG1/MG2/MG4/MG5/MG8) used an
   entirely invented river/city layout**, not real geography. Fixed:
   sourced a real public-domain Nile basin map (Wikimedia Commons
   "River Nile map.svg", Hel-hama, CC BY-SA 3.0), rasterized it via
   headless Chromium at 3x scale, pixel-sampled the actual city-dot and
   river-bend positions (Cairo/Luxor/Aswan/Khartoum dots, the real
   4th-Cataract bend for Napata/Jebel Barkal), recolored to the
   Pantheon palette (`public/pantheon-ep4-assets/nile-real-map.png`),
   and recalibrated `CITY_POS`/`RIVER_PATH`/`BORDER_Y` in
   `src/graphics/ep4-map-data.ts` against those real coordinates. New
   shared `Ep4RealMapBackground` component renders it behind each
   graphic's existing animated SVG overlay. All 11 map components
   updated and re-rendered.

Full video reassembled afterward (re-concat + re-mux voiceover +
re-compress) — see updated numbers below.

## Name cards (lower-third credential cards)

User request: show an on-screen name/title card the first time each
historical figure is named in the narration. Implementation:

1. **17 people identified** across the script (kings, queens, and the
   non-royal figures Strabo and Manetho), each with a name, role/title,
   and the scene index + frame offset of their first mention —
   `production/pantheon-ep4-names.json`. One scene (25, the Alara→Kashta
   map) needed two cards in sequence.
2. **`src/graphics/Ep4NameCard.tsx`** — a single reusable Remotion
   composition (`EP4-NameCard`, 110 frames / 3.67s), parameterized per
   person via `--props` at render time instead of registering 17 separate
   compositions. Slides in from the left (10 frames), holds, slides out
   (16 frames) — position-based only, never CSS `opacity`, which would
   blend with the chroma-key backdrop (see next point).
3. **Chroma-key compositing, not real alpha.** This sandbox's Remotion
   webm/vp8 alpha export (`--codec=vp8 --pixel-format=yuva420p`) did not
   actually produce transparency when tested (ffprobe still reported
   yuv420p). Worked around by rendering each card against solid
   `#00FF00` and keying it out at assembly time with ffmpeg's `colorkey`
   filter (`similarity=0.38:blend=0.15` — tuned up slightly from an
   initial 0.35/0.08 pass, which left a 1-pixel compression-blurred
   green fringe visible along the card's hard edge against near-black
   scenes).
4. **`production/pantheon-ep4-render-namecards.py`** renders the 17
   unique cards to `output/ep4-namecards/` (gitignored, intermediate).
   **`production/pantheon-ep4-apply-namecards.py`** composites them onto
   their target scenes in `output/ep4-segments/`, in place, using
   `overlay=0:0:eof_action=pass` — the default `eof_action=repeat` was
   found to freeze a card's last frame (mid-slide-out, still a partial
   sliver on screen) as a permanent overlay for the rest of the scene
   once the card's own clip ended, which only showed up once a scene ran
   longer than a card's 3.67s. For the dual-card scene, the second card
   is prepended with `tpad=start_duration=...:color=0x00FF00` so both
   cards composite in one pass on their shared timeline.
5. Two short archival-photo scenes (TAHARQA at 1.17s, TANTAMANI at
   2.33s) are shorter than the card's full animation — the card still
   slides in and reads clearly (confirmed by frame extraction) before
   the scene cuts away; accepted as a reasonable truncation rather than
   re-timing those beats.

Full video reassembled afterward (re-concat + re-mux voiceover +
re-compress) — see updated numbers below.

## Delivery

- **Original full-quality file** (759.37s, 1920×1080, ~339MB) uploaded to
  CreativeClaw storage (real PUT upload, not inline base64 — Google
  Drive's only available tool here requires embedding the whole file as
  base64 in one call, which isn't workable at this size) and hosted at a
  durable public URL:
  `https://cdn.creativeclaw.co/u/a4eaf4ab/videos/df03a531-08e5-4306-b249-9c9e810fa083.mp4`
  (the earlier pre-revision upload was deleted from storage).
- **Compressed full-quality version** committed to the repo:
  `output/pantheon-ep4-full-compressed.mp4` — two-pass H.264 (811k/973k
  maxrate/1947k bufsize, preset slow, 128k AAC audio), ~89MB, 1920×1080,
  759.36s. Same compression recipe pattern as Ep.1/Ep.2, under GitHub's
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
