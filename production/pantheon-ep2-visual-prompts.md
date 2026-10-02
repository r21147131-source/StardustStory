# Pantheon Ep.2 — Göbekli Tepe — Visual Production Brief

Companion to `pantheon-ep2-gobekli-tepe-script.md` and
`pantheon-ep2-shot-list.json`. Durations below are word-count estimates
and will be rescaled once the real voiceover is in (same pipeline as
Ep.1: `pantheon-ep1-allocate.py`).

**Style base for every AI prompt:** "Cinematic, archaeological accuracy,
naturalistic lighting, Pre-Pottery Neolithic Anatolia, c. 9600 BCE, no
modern objects, no anachronistic tools or clothing, warm ochre and
limestone-tan palette, documentary realism, not fantasy or stylized."

---

## AI (Veo-style) Shot Prompts — 9 shots

### S03 — Cold open: circular enclosure, golden hour (8.2s)
Wide aerial-leaning establishing shot, golden-hour light, a circular
megalithic enclosure of T-shaped limestone pillars partially built, a
dozen small human figures working among them — hauling stone, lashing
rope, lifting with wooden levers. Dust hangs in angled light. Camera
slowly cranes/pushes in. No modern tools, no metal. Awe-inspiring scale,
documentary-realistic, not CGI-glossy.

### S05 — Hunter-gatherer band at dusk (18.9s)
A small band of eight to twelve Pre-Pottery Neolithic hunter-gatherers —
simple leather/woven garments, no metal, carrying spears and gathering
baskets — moving in single file through tall golden grassland at dusk. A
gazelle herd grazes in the middle distance. Low warm sun, long shadows,
wind moving the grass. Naturalistic, unhurried pacing, like a nature
documentary reconstruction.

### S08 — Schmidt's recognition (23.0s)
Documentary-reconstruction style: a lone figure (archaeologist, 1990s
field clothing — khaki, boots, no modern phone/tech visible) kneels on a
sunbaked, rocky hillside scattered with broken limestone fragments,
brushing dust from a curved stone edge, a slow dawning recognition on
their face as they realize what they're looking at. Harsh midday
Anatolian sun, dry scrubland, modest excavation tools (brush, trowel)
nearby.

### S13 — Mass stone-hauling (25.9s)
Wide-to-medium cinematic shot: forty to sixty Pre-Pottery Neolithic
people hauling an enormous T-shaped limestone pillar lying on a wooden
sledge, thick ropes, coordinated rhythmic pulling, some pushing with
wooden levers, dust rising from dry ground, overseers calling rhythm.
Bright midday sun, open quarry landscape with exposed bedrock in
background. Convey immense physical scale and coordinated effort without
visible modern equipment.

### S17 — Night feast (22.2s)
Night scene: a large gathering (fifty-plus people) seated and standing
around multiple bonfires near the stone enclosure, firelight flickering
across carved animal reliefs on nearby pillars, people eating, some
drumming on simple hide drums, clay/stone vessels being passed. Warm
amber firelight against deep blue night sky, stars visible, smoke
drifting. Communal, celebratory, ritualistic mood — not chaotic.

### S20 — Vulture Stone push-in (32.5s)
Slow, deliberate push-in on a large carved limestone pillar face showing
a vulture with outstretched wing beneath a circular disc shape, a
headless human figure, scorpions, and a row of birds along the top edge.
Firelight flickers across the carving from off-screen torches, the
circular disc catches the light as if faintly luminous. Reverent,
mysterious tone — this is the episode's most ambiguous/contested visual,
keep it suggestive rather than literal (no overt "comet" VFX, just light
and shadow implying significance).

### S22 — Deliberate burial, two sub-clips (52.7s total — split ~26.4s / 26.4s in narration order)
**S22a:** People carrying woven baskets heaped with rubble, broken stone,
and soil, pouring the fill methodically into the base of a stone
enclosure around a standing T-pillar, working in an unhurried, almost
ceremonial rhythm. Daylight, dusty, quiet concentration rather than
labor-camp urgency.
**S22b:** Continuation — the fill now rising higher around several
pillars, only the carved upper shoulders and heads still exposed above
the packed rubble, a few figures pressing the last soil into place by
hand. Same lighting/location continuity as S22a.

### S25 — Time-lapse transformation (9.1s)
Short time-lapse-style sequence (can be a single continuous dissolve
rather than true time-lapse VFX): a simple hunter-gatherer camp of hide
tents near the hill gradually giving way to small mudbrick structures
with cultivated field rows and penned animals appearing in the
background. Keep the transition subtle and grounded — this is a 9-second
bridge shot, not the episode's centerpiece.

### S27 — Modern sunset wide shot, closing (26.7s)
Wide shot of the excavated Göbekli Tepe hillside today at sunset — the
circular stone enclosures visible under their protective canopy
structure, golden light catching the tops of the T-pillars, the modern
Anatolian landscape beyond. Quiet, contemplative, present-day (can
include a discreet modern conservation canopy/walkway to signal "today"
without it dominating the frame).

---

## Motion Graphics — 10 graphics (build in Remotion, reuse `src/theme.ts`)

Same component pattern as Ep.1 (`src/graphics/S02_TimelineAxis.tsx`
etc.) — new components live in `src/graphics/` prefixed `EP2_`, new
`Composition` entries added to `src/Root.tsx`. Durations = `ceil(est_dur
* 30)` frames, rescale once VO lands.

1. **S02 — Bridge timeline** (25.5s): axis sliding from 10,800 BCE to
   9600 BCE, visually continuing Ep.1's `S02_TimelineAxis` style so it
   reads as the same device picking up where Ep.1 left off.
2. **S06 — Taş Tepeler map** (15.2s): Fertile Crescent outline, three
   site markers (Göbekli Tepe, Karahan Tepe, Nevalı Çori) pinning in
   sequence.
3. **S10 — Comparative timeline** (19.8s): Göbekli Tepe vs. Stonehenge
   vs. Great Pyramid vs. invention of writing/wheel/pottery, horizontal
   bars extending from a shared zero point.
4. **S11 — Inverted-sequence bars** (39.1s): stacked bar chart, Göbekli
   Tepe far left, long gap, then agriculture/cities/writing clustering
   much later — the visual argument for "temple before farming."
5. **S15 — Labor-convergence diagram** (28.8s): scattered band icons on
   a map converging on one central point, radiating lines.
6. **S19 — Vulture Stone overlay** (30.0s): the carving (from S18's
   archival photo) with semi-transparent constellation-line annotations
   overlaid, clearly labeled "Proposed interpretation — contested" in
   persistent on-screen text (do not let this read as settled fact).
7. **S23 — Agriculture spread map** (26.3s): radiating gradient/arrows
   expanding outward from the Taş Tepeler region across the Fertile
   Crescent.
8. **S24 — Einkorn domestication comparison** (27.59s): converted from
   an archival photo cue (no fetchable specimen photo found). Two-panel
   side-by-side comparison: left panel "WILD EINKORN" with an
   illustrated seed head and a highlighted, animated breakpoint on the
   stem labeled "brittle rachis — shatters, scatters seed"; right panel
   "DOMESTICATED EINKORN" with an intact seed head labeled "non-brittle
   rachis — ear stays intact." A small locator label reads "Karacadağ
   Mountains, SE Turkey." Keep it simple and diagrammatic (closer to
   S11's bar-chart register than a literal illustration) — the point is
   the mechanism (why non-shattering grain is harvestable), not botanical
   realism.
9. **S28 — Closing stat card** (13.2s): same stat-card format as Ep.1's
   closing graphic — four lines (dates, enclosure count, predates-list,
   einkorn note).
10. **S30 — Citation crawl** (10.0s): reuse Ep.1's `S31_CitationCrawl`
   component with Ep.2's source list.

Plus **S29 — Logo card** (5.0s): reuse `S30_LogoCard.tsx` verbatim,
swap "EPISODE ONE" → "EPISODE TWO".

---

## Archival Search Terms (for real-photo sourcing)

Direct fetch of Wikimedia/museum/press-archive images isn't possible
from this sandbox (network policy) — same constraint as Ep.1. Research
candidate source pages by these terms, then the user supplies the actual
image files the same way as Ep.1 (paste/upload into chat).

| Shot | Search terms |
|---|---|
| S01 | "Göbekli Tepe aerial photograph", "Göbekli Tepe site overview" |
| S04 | "Fertile Crescent landscape photograph", "southeastern Turkey wild einkorn field" |
| S07 | "Klaus Schmidt Göbekli Tepe excavation 1994", "Göbekli Tepe early trench photograph" |
| S09 | "Göbekli Tepe excavation progress photographs DAI", "Göbekli Tepe enclosure uncovering" |
| S12 | "Göbekli Tepe pillar animal relief fox boar snake vulture scorpion crane" |
| S14 | "Göbekli Tepe Pillar 18 arms belt", "Göbekli Tepe Pillar 31 central pillar" |
| S16 | "Göbekli Tepe stone vessel trough", "Göbekli Tepe fermentation residue vessel" |
| S18 | "Göbekli Tepe Pillar 43 Vulture Stone photograph" |
| S21 | "Göbekli Tepe backfill cross-section excavation", "Göbekli Tepe enclosure D C B A stratigraphy" |
| S26 | "Göbekli Tepe modern site photograph tourists canopy" |

(S24 was converted to a motion graphic — see the graphics section above — after no fetchable einkorn specimen photo could be sourced; see `pantheon-ep2-archival-sources.md`.)

---

## Credits roll reuse

Pull from Ep.1's already-sourced archival/AI clips for a brief visual
callback in the end-credits montage (same pattern as Ep.1's S32),
specifically the Göbekli Tepe archival photo already in
`public/pantheon-ep1-archival/S23a-gobekli-tepe-excavation.jpg` — ties
the two episodes together visually.
