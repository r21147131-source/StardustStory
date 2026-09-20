# Pantheon Ep.1 — Real Archival Source Candidates

Found via web search. This sandbox's network egress policy blocks every
media host tested (Pexels, Pixabay, Wikimedia, Unsplash all return 403) —
same limitation noted in this repo's README for the Timberland project —
so these are **candidate sources with page URLs, not resolved direct-file
URLs**, and nothing has been downloaded or verified here. Open each page
link to confirm licensing and grab the actual file (or hand this list to a
local session that can reach these hosts).

Prefer the Wikimedia Commons / USGS / public-domain items below over
generic stock — they're the real, freely-licensed thing the script is
actually describing, not a stand-in.

---

### S01 & S26 — Ice core extraction / Younger Dryas Boundary line (cold open + closing)
- ["Camp Century" ice core drilling](https://commons.wikimedia.org/wiki/Category:Camp_Century) — US Army CRREL, Greenland, 1960s core extraction
- Lonnie Thompson ice core sample photo, Byrd Polar Research Center (Wikimedia Commons — search "ice core sample Thompson")
- [File:An ice core segment.jpg](https://commons.wikimedia.org/wiki/File:An_ice_core_segment.jpg) — GISP2, visible annual layers, good generic "there is a thin line" visual
- [Category:Ice cores](https://commons.wikimedia.org/wiki/Category:Ice_cores) — browse for more

### S04 — Mammoth tusks, dire wolf skulls, ground sloth bones (museum displays)
- [File:Woolly mammoth tusk, World Museum Liverpool.JPG](https://commons.wikimedia.org/wiki/File:Woolly_mammoth_tusk,_World_Museum_Liverpool.JPG)
- [File:Dire wolf skulls La Brea display.jpeg](https://commons.wikimedia.org/wiki/File:Dire_wolf_skulls_La_Brea_display.jpeg) — CC BY-SA 3.0
- [File:Dire Wolf Skulls La Brea 2005-08-01.JPG](https://commons.wikimedia.org/wiki/File:Dire_Wolf_Skulls_La_Brea_2005-08-01.JPG) — CC BY-SA 2.5, the famous orange-lit wall of ~400 skulls
- [File:Smithsonian woolly mammoth.jpg](https://commons.wikimedia.org/wiki/File:Smithsonian_woolly_mammoth.jpg)

### S07 — Younger Dryas Boundary layer (ice core cross-section)
Hardest one to source literally — no single public photo is specifically
labeled "YDB layer." Best real stand-in:
- [File:An ice core segment.jpg](https://commons.wikimedia.org/wiki/File:An_ice_core_segment.jpg) — GISP2 core showing distinct annual/ash layers (illustrates the concept even though it's not the literal YDB core)
- Figures in [NOAA NCEI's Younger Dryas PDF](https://www.ncei.noaa.gov/sites/default/files/2021-11/3%20The%20Younger%20Dryas%20-FINAL%20NOV%20(1).pdf) may have a usable diagram — check the PDF directly
- Fallback: use the motion-graphic diagram (already spec'd in `pantheon-ep1-visual-prompts.md`) instead of a photo for this beat

### S10 — Impact craters (Barringer, Wolf Creek)
- [File:Barringer Crater aerial photo by USGS.jpg](https://commons.wikimedia.org/wiki/File:Barringer_Crater_aerial_photo_by_USGS.jpg) — public domain, USGS
- [Category:Aerial photographs of Barringer Crater](https://commons.wikimedia.org/wiki/Category:Aerial_photographs_of_Barringer_Crater) — more options
- Wolfe Creek meteorite crater.jpg — search [Category:Wolfe Creek Meteorite Crater National Park](https://commons.wikimedia.org/wiki/Category:Wolfe_Creek_Meteorite_Crater_National_Park)

### S13 — Extinction-era museum displays
- Reuse [Dire Wolf Skulls La Brea](https://commons.wikimedia.org/wiki/File:Dire_Wolf_Skulls_La_Brea_2005-08-01.JPG) or search Commons for "Smilodon skeleton Page Museum" (saber-toothed cat mounts, same collection)
- [Paleobiota of the La Brea Tar Pits](https://en.wikipedia.org/wiki/Paleobiota_of_the_La_Brea_Tar_Pits) — Wikipedia article links to several specimen photos

### S17 — Archaeological excavation / abandoned pre-impact settlement
- [Category:Clovis culture](https://commons.wikimedia.org/wiki/Category:Clovis_culture) — Bull Brook site artifacts (Robbins Museum), reconstructed Clovis spear
- Gault site, Topper site, East Wenatchee Clovis Site — search each by name on Commons for excavation photos

### S20 — Ancient texts: cuneiform, hieroglyphics, cave paintings
- [File:The Flood Tablet or Tablet XI of the Epic of Gilgamesh...jpg](https://commons.wikimedia.org/wiki/File:The_Flood_Tablet_or_Tablet_XI_of_the_Epic_of_Gilgamesh,_currently_housed_in_the_British_Museum_in_London.jpg) — CC BY-SA 4.0, British Museum. **Strong pick**: this is the exact tablet the script's own narration references ("the Sumerians spoke of the great flood").
- [Category:Hieroglyphs of Egypt](https://commons.wikimedia.org/wiki/Category:Hieroglyphs_of_Egypt) — e.g. "Detail from White Chapel of Senusret I.jpg"
- [File:LascauxStier.jpg](https://commons.wikimedia.org/wiki/File:LascauxStier.jpg) (Bull of Lascaux, PD) / [File:Lascaux2.jpg](https://commons.wikimedia.org/wiki/File:Lascaux2.jpg) — cave paintings, public domain

### S23 — Göbekli Tepe
- [Category on Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:G%C3%B6bekli_Tepe) — main excavation area, Building D, T-shaped pillars, CC BY-SA 4.0
- [World History Encyclopedia — T-shaped Pillars image](https://www.worldhistory.org/image/13198/t-shaped-pillars-at-gobekli-tepe/) — check its own license terms separately (not Commons)

---

## Next step

This sandbox can't fetch these to verify/download. Two ways forward:
1. Open the links above yourself, grab the files, and send them the same
   way you sent the AI clips (drag-and-drop upload) — I'll slot them into
   `pantheon-ep1-shot-list-final.json` as they land, same as before.
2. If a local Claude Code session (with normal internet access) is
   available, hand it this file — it can fetch, download, and even push
   directly into the repo's `public/pantheon-ep1-clips/` folder.
