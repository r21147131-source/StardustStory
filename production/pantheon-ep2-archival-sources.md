# Pantheon Ep.2 — Göbekli Tepe — Archival Photo Sources

How this differs from Ep.1: this sandbox's network policy blocks direct
fetches to Wikimedia/museum/press-archive hosts, same as before. But
`vidiq_compose` fetches scene sources server-side, from vidIQ's own
infrastructure — not through this sandbox's restricted egress. So
rather than needing the user to paste/upload image files, these are
**hotlinked directly from their source URLs** and verified resolvable
via `mcp__higgsfield__media_import_url` (which also runs server-side,
confirming each URL is live and returns `image/jpeg` before it's
trusted). Nothing here is committed to the repo as a file — the shot
list's `src` field is the source URL itself, used straight in
`vidiq_compose`'s `scenes[].source`.

Caveat: I can't visually preview these images from this sandbox either,
so matches are judged from the source page's own title/description via
web search, not a direct look. Flagged below wherever that matters.

All images are from World History Encyclopedia (worldhistory.org),
whose content is published under CC BY-NC-SA 4.0 (non-commercial,
share-alike, attribution required) unless the image's own page states
otherwise — the Vulture Stone photo is individually credited to Sue
Fleckney under CC BY-SA 2.0. Credit both in the closing citation crawl.

## Resolved as real photos (10 of 11 archival cues)

3 of these were later upgraded with photos the user supplied directly
(committed to `public/pantheon-ep2-archival/`, not hotlinked) — marked
below.

| Shot | Source | Match quality |
|---|---|---|
| S01 | `worldhistory.org/uploads/images/12476.jpg` | Strong — aerial view of Göbekli Tepe and surroundings |
| S04 | **user-supplied** `S04a-einkorn-wheat-field.jpg` | Strong — real wheat-field photograph (upgraded from a map substitute) |
| S07 | **user-supplied** `S07a-klaus-schmidt-excavation.jpg` | Strong — Klaus Schmidt himself at the site (upgraded from a generic pillar photo) |
| S09 | `worldhistory.org/uploads/images/13199.jpg` | Good — Layer III, Enclosure A, Pillar 2 |
| S12 | **user-supplied** `S12a-animal-relief-closeup.jpg` (primary), `worldhistory.org/uploads/images/12475.jpg` (alternate) | Strong — extreme close-up carving, closer to the cue's "close-up" framing than the alternate |
| S14 | **user-supplied** `S14a-central-pillar-animal-relief.jpg` | Substitute — genuine central-pillar close-up, but the relief is a crouching animal, not Pillar 18's arm/belt motif specifically |
| S16 | `worldhistory.org/uploads/images/3847.jpg` | Weak substitute — general temple image, not stone-basin specific |
| S18 | `worldhistory.org/uploads/images/13200.jpg` | Strong — Vulture Stone (Pillar 43), photo by Sue Fleckney |
| S21 | **user-supplied** `S21a-deep-excavation-stratigraphy.jpg` | Substitute — deep excavated enclosure, strong sense of stratigraphy/depth, but not backfill actively being packed in |
| S26 | `worldhistory.org/uploads/images/3830.jpg` | Good — site under the modern protective covering |

Still flagged as substitutes, open to a better source: **S14** (closer
now, but still not the specific arm/belt motif), **S16** (the one
cue with no real-photo upgrade at all yet), **S21** (closer now, but
not literally backfill in progress). (3 earlier user-supplied
candidates for this batch had visible iStock/Adobe Stock watermarks
baked into the preview — not usable without a licensed version.)

## Extra, unassigned

Three more user-supplied photos didn't match any open cue but are good
material for the end-credits montage, same pattern as Ep.1's
unassigned extras:
- `EXTRA-pillar-base-bird-relief-unassigned.jpg` — a pillar base with a
  row of carved birds
- `EXTRA-blue-hour-boar-pillar-unassigned.webp` — a dramatic blue-hour
  wide shot of a boar-relief pillar
- `EXTRA-shelter-construction-unassigned.jpg` — the protective canopy
  shelter under construction

## Resolved as a graphic (1 of 11)

**S24** — wild vs. domesticated einkorn wheat specimens. No fetchable
photo was found (a Wikimedia Commons file exists but that host is
blocked from this sandbox, and a mirror-site fallback failed), so by
request this cue was converted to the 10th motion graphic instead of an
archival photo: a two-panel wild-vs-domesticated rachis comparison. See
`pantheon-ep2-visual-prompts.md`'s graphics section (item 8) for the
full spec, and `pantheon-ep2-shot-list-final.json` (S24, now
`"type": "graphic"`).

## Reproducing / updating

To swap any of these for a better source: find a direct, reachable
image URL (test it with `mcp__higgsfield__media_import_url` — a
successful `image/jpeg` response confirms it'll work in
`vidiq_compose`), then update that shot's `src` in
`pantheon-ep2-shot-list-final.json`.
