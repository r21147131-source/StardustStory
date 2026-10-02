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

## WAITING ON YOU

6. **Archival photos** — this sandbox can't fetch Wikimedia/press-archive
   images directly (network policy, same as Ep.1). I'll research and
   list candidate sources; you'll need to paste/upload the actual files,
   same as Ep.1's workflow. Search terms are in the visual-prompts doc.

## NOT STARTED YET

7. **AI (Veo-style) clip generation** — 9 shots (now 10 cues with the
   S22 split), prompts ready, durations locked. Next step once we
   decide how to spend the credit budget.
8. **Motion graphics** — 9 Remotion components to build in
   `src/graphics/` (prefix `EP2_`), reusing `src/theme.ts` and the Ep.1
   `S30_LogoCard`/`S31_CitationCrawl` patterns. Durations locked, ready
   to build.
9. **Assembly** — via `vidiq_compose`, same 3-segment pattern as Ep.1
   (629.88s total / 240s cap per call = 3 segments).

## Credit budget note

Current vidIQ balance (as of this status): 120 credits (69 renewable +
51 add-on, renewable resets 2026-10-29). AI clip generation and
`vidiq_compose` renders will draw on this — worth checking balance again
before the generation pass once the shot list is locked, since 9 AI
clips + multi-segment composes is a meaningful chunk of a 120-credit
budget depending on model/resolution choices.
