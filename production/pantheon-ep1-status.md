# Pantheon Ep.1 — Younger Dryas Impact — Production Status

## Pipeline (mirrors the Timberland / Golden Four pattern in this repo)

1. **Script** — done. `pantheon-ep1-younger-dryas-script.md`
2. **Shot list** — done, reconciled to the real voiceover.
   `pantheon-ep1-shot-list-final.json` (639.23s vs 639.27s VO, 0.04s off).
3. **Voiceover** — **done.** `public/pantheon-ep1-voiceover.mp3` (10:39).
4. **AI video shots (9 script + 2 fallback for S04/S13)** — **7 of 9
   script shots covered**, 20 clips in `public/pantheon-ep1-clips/`.
   S15/S22 still need generation; S04/S13 switched to AI fallback (see
   below) since their real photos couldn't transfer.
5. **Motion graphics (11)** — **done.** Real Remotion/React components,
   rendered to video, wired into the shot list.
6. **Archival footage (9 cues)** — **7 of 9 covered** with real photos
   (S01, S07, S10, S20, S23, S26 + reused ice-core shots). S04/S13
   switched to AI generation (see below) after their real photos twice
   arrived without a usable file path.
7. **Assembly/render** — **pending**, blocked on S15/S22/S04/S13
   generation and a render-path decision.

## AI shots — coverage table

| Shot | Cue | Needs | Status |
|---|---|---|---|
| S03 Shot 1 | Night sky meteor streak | 4.5s | ✅ covered |
| S05 Shot 2 | Hunters with mammoth herd | 4.5s | ✅ covered, over-provisioned |
| S08 Shot 3 | Impact event sequence | 4.5s | ✅ covered — use the 3 clean clips, not `S08a` (flagged, fake timestamp) |
| S12 Shot 4 | Post-impact devastated landscape | 4.5s | ✅ covered |
| S15 Shot 5 | Environmental transformation montage | **35.7s** | ❌ missing — 4 sub-prompts (5a-5d) ready |
| S18 Shot 6 | Desperate hunter group | **24.7s** | ⚠️ 1 clip (8s), short by ~16.7s — 3 more sub-prompts (6b-6d) ready |
| S22 Shot 9 | Myth-witness montage | **29.9s** | ❌ missing — 5 sub-prompts (9a-9e) ready |
| S24 Shot 7 | Neolithic settlement | 4.5s | ✅ covered |
| S27 Shot 8 | Modern landscape fade | 14.9s | ✅ covered |
| **S04 Shot 10 (new)** | Mammoth/dire-wolf museum specimens | **43.5s** | ❌ missing — 4 sub-prompts (10a-10d) ready, AI fallback |
| **S13 Shot 11 (new)** | Extinction-era displays/reconstructions | **29.9s** | ❌ missing — reuses 10b-10d + 2 more (11a-11b), AI fallback |

All prompts for S15/S18/S22/S04-fallback/S13-fallback are in
`pantheon-ep1-visual-prompts.md` and `pantheon-ep1-local-handoff.md`.

## Archival footage — 7 of 9 covered with real photos

| Cue | Content | Files |
|---|---|---|
| S01 | Ice core extraction | `S01a` parka+core, `S01b` night drilling rig |
| S07 | YD boundary layer (stand-in) | `S07a` blue ice wall, `S07b` core barrel close-up |
| S10 | Impact craters | `S10a/b` Wolfe Creek, `S10c/d` Barringer aerial |
| S20 | Ancient texts | `S20a` Lascaux horse, `S20b` Gilgamesh Flood Tablet |
| S23 | Göbekli Tepe | `S23a` excavation site |
| S26 | Ice core (closing) | `S26a` sunny core segment, `S26b` vintage tunnel |
| S04/S13 | Mammoth/dire-wolf specimens | **switched to AI** — real photos arrived twice without a file path and couldn't be transferred; see Shots 10/11 above |

All in `public/pantheon-ep1-archival/`. One extra file flagged and NOT
used: `FLAGGED-likely-AI-generated-DO-NOT-USE-AS-ARCHIVAL.jpg` (implausible
underground industrial complex, inconsistent with the other genuine
photos). One unassigned extra: `EXTRA-modern-arctic-base-unassigned.webp`.

## Motion graphics — real, rendered code

Built as a small Remotion project (already a repo dependency, no network
needed to render — `registry.npmjs.org` is allowed even though media hosts
aren't). Rendered with the sandbox's pre-installed Playwright Chromium
headless shell since Remotion's own Chrome download host is blocked.

| Cue | Graphic | Duration | File |
|---|---|---|---|
| S02 | Timeline axis → 12,800 BCE | 15.6s | `S02-TimelineAxis.mp4` |
| S06 | Ice sheet extent / population | 4.5s | `S06-IceSheetMap.mp4` |
| S09 | Impact hypothesis diagram | 16.9s | `S09-ImpactDiagram.mp4` |
| S11 | Extinction rate chart | 29.9s | `S11-ExtinctionChart.mp4` |
| S14 | Climate temperature plunge | 33.1s | `S14-ClimatePlunge.mp4` |
| S16 | AMOC disruption diagram | 4.5s | `S16-AMOCDiagram.mp4` |
| S19 | Population density map | 7.8s | `S19-PopulationMap.mp4` |
| S21 | Global myth text montage | 45.5s | `S21-MythMontage.mp4` |
| S25 | Neolithic transition timeline | 17.6s | `S25-NeolithicTimeline.mp4` |
| S28 | Closing stat cards | 37.7s | `S28-StatCards.mp4` |
| S31 | Source citation crawl | 26.7s | `S31-CitationCrawl.mp4` |

All in `public/pantheon-ep1-motion-graphics/`, 1920×1080, 30fps. Source in
`src/graphics/*.tsx`. To re-render:
```
npm install
npx remotion render src/index.ts <CompositionId> out/name.mp4 \
  --browser-executable=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
```

## What's still needed

- **S15** — 0 clips, prompts ready.
- **S22** — 0 clips, prompts ready.
- **S04/S13** — 0 clips, AI-fallback prompts ready (real photos didn't transfer).
- **More material for S18** — 8s of 24.7s needed.
- **Render path decision**: `vidiq_compose` (needs hosted URLs) vs. local
  Remotion render (proven working here for graphics — could handle the
  full composite if it can pull in the AI clips + voiceover too).

Send generated clips whenever ready — I'll keep wiring them in.
