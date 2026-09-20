# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## Pipeline (mirrors the Timberland / Golden Four pattern in this repo)

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done. `pantheon-ep1-shot-list.json` (estimated timing)
   → `pantheon-ep1-shot-list-final.json` (**reconciled to the real
   voiceover**, see below) — 32 cues: 9 AI, 9 archival, 11 graphic, 1
   transition, 1 brand, 1 mixed montage.
3. **Voiceover** — **done.** `public/pantheon-ep1-voiceover.mp3`,
   **639.27s (10:39)**, measured via `mutagen` (`ffprobe` isn't installed
   in this environment). `pantheon-ep1-allocate.py` has been run against it
   — `pantheon-ep1-shot-list-final.json` now totals 639.23s, a 0.04s match.
4. **AI video shots (9)** — **you say these are generated**, in
   `C:\Users\roman\pantheon\Sep20-18_38`. This cloud session can't see that
   folder directly (see below — need the files themselves, or URLs, to wire
   them into the shot list).

   ⚠️ **4 of the 9 AI cues need more screen time than one native Veo
   generation (~10s) provides**, now that they're scaled to the real VO:
   | Shot | Cue | Needs | Over by |
   |---|---|---|---|
   | S15 | Environmental transformation montage | 35.7s | +25.7s |
   | S22 | Myth-witness reconstruction montage | 29.9s | +19.9s |
   | S18 | Desperate hunter group in changing landscape | 24.7s | +14.7s |
   | S27 | Modern landscape fade | 14.9s | +4.9s |

   Each needs one of: loop the generated clip, hold on a freeze frame at
   the end, generate 2-3 variant clips and cut between them, or cut in
   archival/graphic B-roll to cover the gap. S15 and S22 are already
   montages by design, so generating them as 2-3 separate sub-clips (one
   per beat) rather than one continuous shot is probably the cleanest fix.
5. **Motion graphics (9)** — **pending.** Not AI-video; build in After
   Effects or Remotion per the spec sheet in `pantheon-ep1-visual-prompts.md`.
6. **Archival footage (9 cues)** — **pending.** Source from stock/archival
   libraries using the search terms in `pantheon-ep1-visual-prompts.md`.
7. **Assembly/render** — **pending**, blocked on getting the assets from
   #4-6 into this session (or the reverse — this repo pulled down locally
   and assembled there). Once shots have real hosted URLs (or local files,
   if rendering with Remotion instead of `vidiq_compose`), fill `src` in
   `pantheon-ep1-shot-list-final.json` and compose, following the same
   segmenting approach as `production/compose-segments.json` if using
   `vidiq_compose` (240s cap per call — this episode needs 3 segments at
   ~10:39 total).

## Blocker: getting the local visuals into this session

You said the visuals are done in `C:\Users\roman\pantheon\Sep20-18_38` —
this cloud session has no access to that Windows folder, the same
limitation as before. To move forward, one of:
- **Upload the 9 AI clips + graphics here**, the same way you just sent the
  voiceover — I'll pull durations, wire them into
  `pantheon-ep1-shot-list-final.json`, and drive the compose step.
- **Host them somewhere with a URL** (the repo, cloud storage, etc.) and
  send the links — `vidiq_compose` needs hosted URLs anyway, so this is
  the more direct path to final render regardless.
- **Assemble locally** — if the local Claude Code session in that folder
  also has this repo cloned, it can run `pantheon-ep1-allocate.py`
  (already updated with the real 639.27s total) and drive the render with
  local ffmpeg/Remotion directly, no upload needed.

## What this session can pick up next

- The 9 AI clips (or their URLs) → wire into the final shot list and start
  compose.
- The 9 motion graphics once built.
- The 9 archival clips once sourced.
- A decision on render path: `vidiq_compose` (server-side, matches
  Timberland's approach — needs hosted URLs, 3 segments at this length)
  vs. local Remotion render (this repo has the `remotion` dependency, but
  needs local compute + ffmpeg since this cloud session's network egress
  is limited for pulling arbitrary asset URLs).
