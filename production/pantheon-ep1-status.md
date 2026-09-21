# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## Pipeline (mirrors the Timberland / Golden Four pattern in this repo)

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done, reconciled to the real voiceover.
   `pantheon-ep1-shot-list-final.json` (639.23s vs 639.27s VO, 0.04s off).
3. **Voiceover** — **done.** `public/pantheon-ep1-voiceover.mp3` (10:39).
4. **AI video shots (9)** — **7 of 9 covered**, 20 clips received and
   organized in `public/pantheon-ep1-clips/`. See table below.
5. **Motion graphics (11)** — **done.** Built as real Remotion/React
   components (`src/graphics/`), rendered to video, and wired into the
   shot list. See below — this turned out to be 11 cues, not 9 (two extra
   graphic beats were in the script body but not the production notes list).
6. **Archival footage (8 cues)** — **pending.** Real source candidates
   researched in `pantheon-ep1-archival-sources.md`; nothing downloaded yet
   (this sandbox can't reach any image/archive host — see that file for why).
7. **Assembly/render** — **pending**, blocked on S15, S22, the 8 archival
   photos, and a render-path decision.

## Motion graphics — now real, rendered code

Built the whole set as a small Remotion project instead of just specs,
since Remotion was already a dependency and needs no network access to
render (registry.npmjs.org is allowed; only the media/asset hosts are
blocked). Found the pre-installed Playwright Chromium headless shell at
`/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`
and pointed Remotion's renderer at it, since Remotion's own Chrome download
host (`remotion.media`) is blocked like everything else.

| Cue | Graphic | Duration | File |
|---|---|---|---|
| S02 | Timeline axis, clock spinning back to 12,800 BCE | 15.6s | `S02-TimelineAxis.mp4` |
| S06 | Ice sheet extent / habitable zones / population dots | 4.5s | `S06-IceSheetMap.mp4` |
| S09 | Impact hypothesis diagram (fragments → airbursts) | 16.9s | `S09-ImpactDiagram.mp4` |
| S11 | Extinction rate chart, species dropping out | 29.9s | `S11-ExtinctionChart.mp4` |
| S14 | Climate temperature plunge, YD period highlighted | 33.1s | `S14-ClimatePlunge.mp4` |
| S16 | AMOC disruption diagram | 4.5s | `S16-AMOCDiagram.mp4` |
| S19 | Population density map, before/after | 7.8s | `S19-PopulationMap.mp4` |
| S21 | Global myth text montage, 5 cultures | 45.5s | `S21-MythMontage.mp4` |
| S25 | Neolithic transition timeline | 17.6s | `S25-NeolithicTimeline.mp4` |
| S28 | Closing stat cards (4 facts) | 37.7s | `S28-StatCards.mp4` |
| S31 | Source citation crawl | 26.7s | `S31-CitationCrawl.mp4` |

All in `public/pantheon-ep1-motion-graphics/`, 1920×1080, 30fps, durations
matched exactly to the voiceover-reconciled shot list. Source in
`src/graphics/*.tsx`, shared palette/type in `src/theme.ts`, registered in
`src/Root.tsx`. To re-render or tweak:
```
npm install
npx remotion render src/index.ts <CompositionId> out/name.mp4 \
  --browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```
(the `--browser-executable` flag is only needed in this sandbox; a normal
dev machine with Remotion's own Chrome download working won't need it.)

Maps are stylized/schematic abstractions (a soft continent-like blob), not
real cartographic geometry — no geo data was fetchable, and it reads fine
as a documentary-graphic style choice. Everything else is genuine chart/
diagram/typography animation, not placeholder.

## AI shots — coverage table

| Shot | Cue | Needs | Clips received | Status |
|---|---|---|---|---|
| S03 Shot 1 | Night sky meteor streak | 4.5s | 2 (mammoths/bison watching meteor shower) | ✅ covered |
| S05 Shot 2 | Hunters with mammoth herd | 4.5s | 4 (hunters+herd, 2× herd-only, dawn steppe) | ✅ covered, well over-provisioned |
| S08 Shot 3 | Impact event sequence | 4.5s | 4 (comet entering atmosphere, shockwave×2, airburst) | ✅ covered — **use the 3 clean clips, not `S08a`** (see flag below) |
| S12 Shot 4 | Post-impact devastated landscape | 4.5s | 2 (burned ash landscape, scorched tundra + mammoth carcass) | ✅ covered |
| S15 Shot 5 | Environmental transformation montage | **35.7s** | 0 | ❌ **missing** — prompt split into 4 sub-clips (5a-5d) in `pantheon-ep1-visual-prompts.md` |
| S18 Shot 6 | Desperate hunter group | **24.7s** | 1 (woman + child, 8s) | ⚠️ **short by ~16.7s** — 3 more sub-clip prompts (6b-6d) written |
| S22 Shot 9 | Myth-witness reconstruction montage | **29.9s** | 0 | ❌ **missing** — prompt split into 5 sub-clips (9a-9e), one per culture |
| S24 Shot 7 | Neolithic settlement / Göbekli Tepe | 4.5s | 2 (farmer + village, crop rows / grain field) | ✅ covered |
| S27 Shot 8 | Modern landscape fade | 14.9s | 3 (farmland→city, two angles) | ✅ covered, comfortably fills the runtime |

## ⚠️ Fake archival timestamp on S08a — do not use

`S08a-airbursts-over-ice-NEEDS-FIX.mp4` has a fabricated "ARCHIVE FOOTAGE:
NOV 14, 2023" timestamp burned in. 3 clean replacement clips cover the
same beat instead (`S08b`, `S08c`, `S08d`), so S08 is fully coverable
without it. Left in `public/pantheon-ep1-clips/` for reference only.

## Archival footage — still nothing downloaded

Researched real candidates (Wikimedia Commons, USGS, British Museum) in
`pantheon-ep1-archival-sources.md`, but this sandbox cannot reach any
image/archive host to actually fetch them (tested extensively — see that
file and the conversation history). Options: you download and upload here
(same as the AI clips), or a local Claude Code session with normal network
access fetches and pushes them to the repo directly.

## What's still needed

- **S15** (environmental transformation montage) — 0 clips, 4 sub-prompts ready.
- **S22** (myth-witness montage) — 0 clips, 5 sub-prompts ready.
- **More material for S18** — currently 8s of 24.7s needed, 3 sub-prompts ready.
- **8 archival photos** — sources researched, nothing fetched yet.
- **Render path decision**: `vidiq_compose` (needs hosted URLs — these
  files are currently only local to this session/repo) vs. local Remotion
  render (now proven working in this repo for the graphics layer — the
  same setup could composite the whole episode if ffmpeg/Remotion handles
  the AI clips + voiceover too).

Send S15, S22, S18 coverage, or archival photos whenever ready — I'll keep
wiring things in as they land.
