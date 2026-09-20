# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## Pipeline (mirrors the Timberland / Golden Four pattern in this repo)

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done, reconciled to the real voiceover.
   `pantheon-ep1-shot-list-final.json` (639.23s vs 639.27s VO, 0.04s off).
3. **Voiceover** — **done.** `public/pantheon-ep1-voiceover.mp3` (10:39).
4. **AI video shots (9)** — **7 of 9 covered**, 20 clips received and
   organized in `public/pantheon-ep1-clips/`. See table below.
5. **Motion graphics (9)** — **pending.**
6. **Archival footage (9 cues)** — **pending** (several AI clips are
   standing in for archival-type cues, see table).
7. **Assembly/render** — **pending**, blocked on S15, S22, graphics, and
   a render-path decision.

## AI shots — coverage table

| Shot | Cue | Needs | Clips received | Status |
|---|---|---|---|---|
| S03 Shot 1 | Night sky meteor streak | 4.5s | 2 (mammoths/bison watching meteor shower) | ✅ covered |
| S05 Shot 2 | Hunters with mammoth herd | 4.5s | 4 (hunters+herd, 2× herd-only, dawn steppe) | ✅ covered, well over-provisioned |
| S08 Shot 3 | Impact event sequence | 4.5s | 4 (comet entering atmosphere, shockwave×2, airburst) | ✅ covered — **use the 3 clean clips, not `S08a`** (see flag below) |
| S12 Shot 4 | Post-impact devastated landscape | 4.5s | 2 (burned ash landscape, scorched tundra + mammoth carcass) | ✅ covered |
| S15 Shot 5 | Environmental transformation montage | **35.7s** | 0 | ❌ **missing** |
| S18 Shot 6 | Desperate hunter group | **24.7s** | 1 (woman + child, 8s) | ⚠️ **short by ~16.7s** — needs a loop/freeze or 2 more clips |
| S22 Shot 9 | Myth-witness reconstruction montage | **29.9s** | 0 | ❌ **missing** |
| S24 Shot 7 | Neolithic settlement / Göbekli Tepe | 4.5s | 2 (farmer + village, crop rows / grain field) | ✅ covered |
| S27 Shot 8 | Modern landscape fade | 14.9s | 3 (farmland→city, two angles) | ✅ covered, comfortably fills the runtime |

S15 and S22 are exactly the two cues flagged earlier as needing the most
extra screen time (35.7s and 29.9s) — worth prioritizing, and worth
generating as 3-4 short sub-clips each rather than one long one, same
approach that worked well for S05/S08/S27 above.

## ⚠️ Resolved-ish: fake archival timestamp on S08a

`S08a-airbursts-over-ice-NEEDS-FIX.mp4` still has the fabricated
"ARCHIVE FOOTAGE: NOV 14, 2023" timestamp burned in — **do not use it.**
Good news: 3 clean replacement clips arrived for the same beat
(`S08b` comet entering atmosphere, `S08c`/`S08d` shockwave flattening
forest), so S08 is fully coverable without touching `S08a`. Leaving it in
`public/pantheon-ep1-clips/` for reference only, marked in its filename.

## S18 needs more material

Only one 8s clip for a cue that now needs 24.7s of screen time. Options,
cheapest first: hold on a freeze-frame of the last second for ~17s (weakest
visually), loop the clip forward/back, or generate 2-3 more short clips of
the same family/scene from different angles and cut between them (matches
how S05/S08/S27 got covered).

## What's still needed

- **S15** (environmental transformation montage) — 0 clips.
- **S22** (myth-witness montage) — 0 clips.
- **More material for S18** — currently 8s of 24.7s needed.
- **9 motion graphics** (After Effects/Remotion).
- **9 archival clips** — several AI clips are already standing in for
  archival-type cues (S05, S12, S17, S24), which works fine given the
  script's own "reconstructed scene" visual language.
- **Render path decision**: `vidiq_compose` (needs hosted URLs — these
  files are currently only local to this session/repo) vs. local Remotion
  render.

Send S15, S22, and more S18 coverage whenever ready — I'll keep wiring
things in as they land.
