# Pantheon Ep.2 — Göbekli Tepe — Production Status

## DONE

1. **Script** — done. `pantheon-ep2-gobekli-tepe-script.md`. 8 parts,
   ~1,517 words of narration, same "The God" narrator voice as Ep.1,
   direct narrative bridge from Ep.1's closing.
2. **Draft shot list** — done, word-count estimated (~639s target,
   matching Ep.1's runtime almost exactly). `pantheon-ep2-shot-list.json`.
   30 cues: 11 archival, 10 graphics, 9 AI (Veo-style).
3. **Visual production brief** — done. `pantheon-ep2-visual-prompts.md` —
   full AI shot prompts, motion graphics spec, archival search terms.
4. **Voiceover** — done. `public/pantheon-ep2-voiceover.mp3`, 614.87s
   (10:15).
5. **Final shot list** — done, reconciled to the real voiceover.
   `pantheon-ep2-shot-list-final.json` (629.88s total: 614.87s VO +
   15s fixed logo/citation tail). `pantheon-ep2-allocate.py` is the
   reconciliation script. S22 (the burial sequence, originally 51.93s —
   over the 45s single-shot ceiling) split into S22a/S22b sub-clips,
   ~25.97s each, same pattern as Ep.1's long cues.

6. **AI clips — all 10 of 10 cues covered.** You supplied 12 user-generated
   clips (Grok), sorted into `public/pantheon-ep2-clips/` (1 duplicate
   discarded — byte-identical to an already-saved S13 take):
   - **S03** (cold open aerial enclosure) — 1 clip, 4.54s (short of the
     8.08s needed — will repeat/loop at assembly)
   - **S05** (hunter band at dusk) — 1 clip, 5.5s (short of 18.62s —
     will repeat/loop)
   - **S08** (Schmidt recognition) — 1 clip, 10.04s (short of 22.66s —
     will repeat/loop)
   - **S13** (stone-pillar hauling) — 3 alternate takes, 10.04s each —
     full coverage, will split the 25.52s across all 3 (~8.5s each)
   - **S17** (night feast) — 1 clip, 10.04s (short of 21.88s — will
     repeat/loop). Strong match — firelit carved pillars, drummers,
     large seated gathering.
   - **S22a / S22b** (deliberate burial, 2 sub-clips) — 1 clip each,
     10.04s — short of 25.97s each, will repeat/loop
   - **S25** (time-lapse camp-to-settlement) — 1 clip, 10.04s — full
     coverage, will trim to 8.97s
   - **S27** (modern sunset closing) — 1 clip, 10.04s (short of
     26.31s — will repeat/loop). Excellent match — real aerial of the
     actual site at sunset, protective canopy visible, exactly as
     specced.
   - **S20** (Vulture Stone push-in) — 1 clip, 10.04s (short of
     32.02s — will repeat/loop). Excellent match — vulture, glowing
     disc, scorpions, bird row along the top edge, slow push-in exactly
     as specced.

   Note: S03 and S05 came from a single 10s source clip that had two
   distinct scenes back to back — I split it in two and re-encoded
   (the first `-c copy` attempt silently dropped the video stream on
   one half, caught it via a frame-extraction check and fixed it).

7. **Archival photos — 10 of 11 cues covered.** Different approach from
   Ep.1: found real, working image URLs via web search (World History
   Encyclopedia's photo archive) and verified each one resolves to an
   actual `image/jpeg` via a server-side fetch (`vidiq_compose` fetches
   scene sources server-side too, so these hotlinked URLs work directly
   without needing to download/commit files, unlike Ep.1). Full list
   and match-quality notes in `pantheon-ep2-archival-sources.md`. 4 of
   the 10 are flagged as substitutes (not an exact match to the cue,
   but the best real photo found) rather than presented as perfect.

## WAITING ON YOU

8. **1 archival photo still unresolved: S24** (wild vs. domesticated
   einkorn wheat). A Wikimedia Commons file exists but that host is
   blocked from this sandbox and a mirror-site attempt failed. Options
   in the archival-sources doc: supply a photo yourself, or let it
   become a graphic instead.

## NOT STARTED YET

9. **Motion graphics** — 9 Remotion components to build in
   `src/graphics/` (prefix `EP2_`), reusing `src/theme.ts` and the Ep.1
   `S30_LogoCard`/`S31_CitationCrawl` patterns. Durations locked, ready
   to build.
10. **Assembly** — via `vidiq_compose`, same 3-segment pattern as Ep.1
   (629.88s total / 240s cap per call = 3 segments). Can run once S24
   is settled (or run now with S24 using a graphic fallback).

## Credit budget note

Current vidIQ balance (as of this status): 120 credits (69 renewable +
51 add-on, renewable resets 2026-10-29). AI clip generation and
`vidiq_compose` renders will draw on this — worth checking balance again
before the generation pass once the shot list is locked, since 9 AI
clips + multi-segment composes is a meaningful chunk of a 120-credit
budget depending on model/resolution choices.
