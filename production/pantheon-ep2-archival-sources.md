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

## Resolved (10 of 11)

| Shot | URL | Match quality |
|---|---|---|
| S01 | `worldhistory.org/uploads/images/12476.jpg` | Strong — aerial view of Göbekli Tepe and surroundings |
| S04 | `worldhistory.org/uploads/images/12521.jpg` | Substitute — Map of the Fertile Crescent (no landscape/wheat-field photo found) |
| S07 | `worldhistory.org/uploads/images/13198.jpg` | Substitute — general T-pillar/excavation photo, not dated 1994 or showing Schmidt |
| S09 | `worldhistory.org/uploads/images/13199.jpg` | Good — Layer III, Enclosure A, Pillar 2 |
| S12 | `worldhistory.org/uploads/images/12475.jpg` | Strong — Pillar with Sculpture of a Fox |
| S14 | `worldhistory.org/uploads/images/12474.jpg` | Substitute — Pillar 27, Enclosure C (not Pillar 18 specifically) |
| S16 | `worldhistory.org/uploads/images/3847.jpg` | Weak substitute — general temple image, not stone-basin specific |
| S18 | `worldhistory.org/uploads/images/13200.jpg` | Strong — Vulture Stone (Pillar 43), photo by Sue Fleckney |
| S21 | `worldhistory.org/uploads/images/204.jpg` | Substitute — Enclosure F, not a backfill cross-section specifically |
| S26 | `worldhistory.org/uploads/images/3830.jpg` | Good — site under the modern protective covering |

## Unresolved (1 of 11)

**S24** — wild vs. domesticated einkorn wheat specimens. A Wikimedia
Commons file exists (`Usdaeinkorn1.jpg`, USDA/public domain, shows
*Triticum monococcum* spikelets) but `upload.wikimedia.org` is blocked
from this sandbox and a mirror-site fetch attempt failed. Options:
- you supply a photo directly (same as Ep.1's workflow), or
- I keep searching for an alternate reachable source, or
- this cue becomes a graphic instead (a simple side-by-side
  illustration of brittle vs. non-brittle rachis, built in Remotion
  alongside the other motion graphics)

## Reproducing / updating

To swap any of these for a better source: find a direct, reachable
image URL (test it with `mcp__higgsfield__media_import_url` — a
successful `image/jpeg` response confirms it'll work in
`vidiq_compose`), then update that shot's `src` in
`pantheon-ep2-shot-list-final.json`.
