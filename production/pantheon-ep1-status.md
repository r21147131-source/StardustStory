# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## Pipeline (mirrors the Timberland / Golden Four pattern in this repo)

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done (estimated timing). `pantheon-ep1-shot-list.json`
   — 32 cues (9 AI, 9 archival, 11 graphic, 1 transition, 1 brand, 1 mixed
   montage), auto-derived from word counts in the script at ~2.3 words/sec.
   Estimated total: **~7.2 min**. The script's own target is ~10–11 min —
   the gap is expected: this is a words-per-second proxy with no pauses,
   breath, or emphasis, which a real recorded VO always adds back in.
3. **Voiceover** — **pending.** You're recording it. Once done, drop the
   file in `public/` (e.g. `public/pantheon-voiceover.m4a`, matching how
   Timberland and Golden Four store theirs), then:
   ```
   ffprobe -v error -show_entries format=duration -of csv=p=0 public/pantheon-voiceover.m4a
   ```
   Set that number as `TOTAL` in `pantheon-ep1-allocate.py` and run it —
   produces `pantheon-ep1-shot-list-final.json` with durations scaled to
   match the real recording.
4. **AI video shots (9)** — **pending.** You're generating these locally via
   Google Flow in `C:\Users\roman\pantheon\Sep20-18_38`, using the prompts
   in `pantheon-ep1-visual-prompts.md` / `pantheon-ep1-local-handoff.md`.
   Note: a 9th shot (myth-witness montage, Part Six) was found in the script
   body that wasn't in the original 8-shot list — its prompt has been added.
5. **Motion graphics (9)** — **pending.** Not AI-video; build in After
   Effects or Remotion per the spec sheet in the same files.
6. **Archival footage (9 cues)** — **pending.** Source from stock/archival
   libraries using the search terms in `pantheon-ep1-visual-prompts.md`.
7. **Assembly/render** — **pending**, blocked on 3–6 above. Once shots have
   real hosted URLs (or local files, if rendering with Remotion instead of
   `vidiq_compose`), fill `src` in `pantheon-ep1-shot-list-final.json` and
   compose, following the same segmenting approach as
   `production/compose-segments.json` if using `vidiq_compose` (240s cap
   per call — this episode will need 2–3 segments at ~10 min total).

## What this session can pick up next

Once any of the following lands, ping to continue:
- Voiceover file → I'll run the allocation script and produce final timings.
- Generated shot files (with URLs, or told where they are) → I'll wire them
  into the shot list.
- A decision on render path: `vidiq_compose` (server-side, matches
  Timberland's approach — needs hosted URLs) vs. local Remotion render
  (this repo already has the `remotion` dependency, but needs local
  compute + ffmpeg since this cloud session's network egress is limited
  for pulling arbitrary asset URLs).
