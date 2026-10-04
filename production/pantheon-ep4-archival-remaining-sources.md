# Pantheon Ep.4 — The Forgotten Ones — Remaining Archival Photo Sources

How this was done: this sandbox's network egress blocks direct fetches to
upload.wikimedia.org, Wikipedia, museum sites, etc. (confirmed: direct
curl gets "CONNECT tunnel failed, 403"). The Firecrawl MCP tool
(`mcp__Firecrawl__firecrawl_scrape` / `firecrawl_search`) reaches these
sites through its own proxy, so every beat below was researched by
reading the relevant Wikipedia/Commons page, following its `og:image` or
file-page link to a real `upload.wikimedia.org/...` file, and then
**independently re-fetching that exact URL** with `firecrawl_scrape`
(no `formats`) to confirm `metadata.statusCode: 200` and
`metadata.contentType` starting with `image/`. Every URL listed below
was verified this way — none are guessed. I cannot download the bytes
into this sandbox, so matching is judged from the file's own page
title/description/category (and, where Firecrawl returned one, its
auto-generated image caption), not a direct visual look — flagged below
wherever that matters.

License notes come from the Commons file page's own credit line
("Author, License, via Wikimedia Commons") where I fetched it; a few
beats only had time to confirm the image resolves and its Wikipedia
context, not that credit line, and are marked `CHECK — unclear` rather
than guessed.

## B001 — Jebel Barkal
Narration: "There is a monument beside the Nile, at the foot of a sacred mountain."
Source: Jebel Barkal (Gebel Barkal), the sacred mountain at Napata, northern Sudan
URL: https://upload.wikimedia.org/wikipedia/commons/4/4e/Gebel_Barkal.jpg
License: CC BY-SA 4.0 / 3.0 / 2.5 / 2.0 / 1.0 + GFDL (self-published, uploader LassiHU)
Match quality: Strong — the exact mountain named in the guidance, this is the `og:image` on the Wikipedia "Jebel Barkal" article.

## B005 — Victory Stele of Piye, first line with translation
Narration: "The story was left standing, as though the stone itself refused to forget what the living had decided to."
Source: Stele of Piye, first line of the inscription with its French translation (after Emmanuel de Rougé's 1876 edition)
URL: https://upload.wikimedia.org/wikipedia/commons/a/af/Stele_of_Piye_%28translation_of_first_line%29.jpg
License: Public Domain (19th-century publication; PD-old)
Match quality: Good — a genuine inscription extract from the real stele, distinct from B002's full-stela photo and B043's homage-register crop already in the shot list. Not a tight physical-register crop so much as a text excerpt plate, hence Good rather than Strong.

## B009 — Sphinx of Taharqo
Narration: "Within one generation, his family held the Two Lands together and ruled the largest Nile empire since the age of Ramesses."
Source: Sphinx of Taharqo, British Museum
URL: https://upload.wikimedia.org/wikipedia/commons/c/c0/Sphinx_of_Taharqo.jpg
License: CC BY-SA 4.0 (and compatible older CC-BY-SA versions), photographer Prioryman
Match quality: Strong — the exact object named in the guidance.

## B014 — Victory stele of Thutmose III, Jebel Barkal
Narration: "Egyptian temples rose on Kushite soil."
Source: Victory stele of Thutmose III, from the temple of Amun at Jebel Barkal, Museum of Fine Arts Boston (23.733)
URL: https://upload.wikimedia.org/wikipedia/commons/7/7a/Victory_stele_of_Thutmose_III.jpg
License: CC BY 3.0, photographer Marcus Cyron
Match quality: Strong — exact object and MFA accession number named in the guidance.

## B015 — Tomb of Huy: Nubians bringing tribute
Narration: "Egyptian kings carved their boasts about trampling the south, and Kush paid in gold, in ivory, in ebony, and in soldiers."
Source: "Nubian Tribute Presented to King Tutankhamun," Tomb of Amenhotep-Huy (TT40) — facsimile painting by Charles K. Wilkinson, Metropolitan Museum of Art
URL: https://upload.wikimedia.org/wikipedia/commons/6/65/Nubian_Tribute_Presented_to_King_Tutankhamun%2C_Tomb_of_Huy_MET_DT221112.jpg
License: CC0 / Public Domain (Met Museum open-access donation)
Match quality: Strong — exactly the facsimile painting the guidance asked for.

## B025 — Stela of Tefnakht (Athens)
Narration: "He chose the wrong year, and he chose the wrong neighbor."
Source: Stela of Tefnakht, National Archaeological Museum, Athens (detail, photo by T. Efthimiadis)
URL: https://upload.wikimedia.org/wikipedia/commons/e/ed/Tefnakht_Athens_stela_%28T._Efthimiadis%29_det.jpg
License: CHECK — unclear (this is the `og:image` on Wikipedia's "Tefnakht" article and resolves fine; I did not separately confirm the Commons file page's licence tag)
Match quality: Strong — exact object named in the guidance, found directly via the Tefnakht Wikipedia page. (This was flagged as one of the harder ones to find; it turned up cleanly.)

## B031 — Victory Stele of Piye, complete inscription
Narration: "His orders to his commanders survive on the stone, and they read like the orders of a man who cared how a war was won."
Source: Stele of Piye, complete (plate from Auguste Mariette, 1872)
URL: https://upload.wikimedia.org/wikipedia/commons/a/a5/Stele_of_Piye_%28complete%29.jpg
License: Public Domain (PD-old-100-expired)
Match quality: Good — shows the full inscribed stele (all the lines of text) rather than a tight single-line crop, but it is the real inscription and is a different plate from B002/B005/B043's other Piye-stele crops already in the list.

## B033 — Victory Stele of Piye: Nimlot's submission
Narration: "Then a king named Nimlot of Hermopolis, who had been Piye's ally, abandoned him and joined Tefnakht."
Source: Drawing of the upper register of the Victory Stele — Piye receiving Nimlot (with horse and sistrum) and the other Delta rulers (Auguste Mariette, 1872)
URL: https://upload.wikimedia.org/wikipedia/commons/e/eb/Stele_Piye_submission_Mariette.jpg
License: Public Domain (PD-old-100-expired)
Match quality: Strong — the file's own description explicitly names Nimlot holding the horse and sistrum, matching the guidance exactly.

## B046 — Amenirdis I (Medinet Habu)
Narration: "He made his sister Amenirdis the God's Wife of Amun at Thebes, which tied the great temples of the south to his family."
Source: Depiction of Amenirdis I from her chapel at Medinet Habu
URL: https://upload.wikimedia.org/wikipedia/commons/5/59/Ch_Am_I_Med_Habou_082005.jpg
License: CHECK — unclear (this is the `og:image` on Wikipedia's "Amenirdis I" article and resolves fine; the Commons file-page credit line was not separately pulled)
Match quality: SUBSTITUTE — a genuine period depiction of Amenirdis I, but from her chapel at Medinet Habu, not the alabaster statue in a Cairo museum case named in the guidance. No Commons file specifically labeled as that Cairo alabaster statue turned up in this search.

## B048 — Pyramids of El-Kurru
Narration: "When he died, he was buried beneath a pyramid, a tomb style Egypt itself had abandoned centuries before, and eight of his horses were buried beside him."
Source: Main pyramid at El-Kurru, royal cemetery, northern Sudan
URL: https://upload.wikimedia.org/wikipedia/commons/5/50/Al-Kurru%2Cmain_pyramid.jpg
License: CC BY 3.0, photographer Bertramz
Match quality: Strong — exact site named in the guidance.

## B052 — Statue of Taharqa (Sudan National Museum)
Narration: "Then came Taharqa."
Source: Standing statue of Taharqa, National Museum of Sudan, Khartoum
URL: https://upload.wikimedia.org/wikipedia/commons/8/80/SNMTaharqo.jpg
License: CC BY-SA 4.0, photographer Clemens Schmillen
Match quality: Strong — a real statue of Taharqa, exactly what the guidance asked for.

## B055 — Relief: Taharqa followed by Queen Abar (Lepsius drawing)
Narration: "I mention this because it reminds you that these were people, not statues."
Source: "Taharqa followed by his mother Queen Abar," Jebel Barkal room C (Karl Richard Lepsius, *Denkmäler aus Aegypten und Aethiopien*, 1849–1859)
URL: https://upload.wikimedia.org/wikipedia/commons/7/7f/Abar.jpg
License: Public Domain (PD-old, 19th-century Lepsius plate)
Match quality: Strong — exactly the Lepsius-era drawing of Taharqa and Abar the guidance asked for; this was one flagged as potentially hard to find, and it turned up cleanly.

## B057 — Kiosk of Taharqa, Karnak
Narration: "He restored temples at Karnak, and built new ones at Kawa and at Jebel Barkal."
Source: Kiosk (colonnade) of Taharqa, Karnak Temple
URL: https://upload.wikimedia.org/wikipedia/commons/7/7b/Taharqa%27s_kiosk._Karnak_Temple.jpg
License: CC BY-SA 4.0, uploader EditorfromMars
Match quality: Strong — exact structure named in the guidance.

## B059 — Pyramid of Taharqa at Nuri
Narration: "He built a pyramid at Nuri, the largest in all of Nubia."
Source: Pyramid of Taharqa, Nuri pyramid field, Sudan
URL: https://upload.wikimedia.org/wikipedia/commons/7/71/Pyramid_of_Taharqa_at_Nuri.jpg
License: CC BY-SA 4.0, uploader Dodo1717
Match quality: Strong — exact monument named in the guidance.

## B060 — Lachish relief, British Museum
Narration: "And his name survives even in the Hebrew Bible, as a king of Kush who marched out to fight the Assyrians."
Source: Lachish reliefs — Assyrian siege of Lachish, British Museum
URL: https://upload.wikimedia.org/wikipedia/commons/d/d8/Lachish_Relief%2C_British_Museum_6.jpg
License: CC BY-SA 4.0, photographer Mike Peel
Match quality: Strong — exact object/collection named in the guidance.

## B063 — Medinet Habu: Sea Peoples relief (sourced fresh — see note)
Narration: "I had watched Egypt survive the Hyksos. I had watched it survive the Libyans, and the Sea Peoples."
Source: Medinet Habu, mortuary temple of Ramesses III — Peleset/Sherden (Sea Peoples) prisoner relief, north-east wall
URL: https://upload.wikimedia.org/wikipedia/commons/7/7a/02010_Sea_People%2C_Medinet_Habu_Ramses_III._Tempel_Nordostwand_cropped.jpg
License: CC BY-SA 4.0, uploader Oltau
Match quality: Strong, **but flagged**: the shot list's own guidance says "reuse from Episode 1." I checked both `pantheon-ep1-archival-sources.md` and `pantheon-ep1-shot-list-final.json` — Episode 1 (about the Younger Dryas impact / Göbekli Tepe) never sourced or used any Medinet Habu or Sea Peoples image; there is nothing there to reuse. I sourced this fresh instead rather than fabricating a reuse that doesn't exist.

## B067 — Esarhaddon's Sam'al victory stele
Narration: "Members of the royal family were taken captive."
Source: Victory stele of Esarhaddon from Sam'al (Zincirli) — detail of a kneeling Egyptian prince, Pergamon Museum, Berlin
URL: https://upload.wikimedia.org/wikipedia/commons/e/e4/Detail._Sam%27al_stele_of_Esarhaddon%2C_671_BCE%2C_Pergamon_Museum.jpg
License: CHECK — unclear (this is the `og:image` on Wikipedia's "Esarhaddon" article and resolves fine; the Commons file-page credit line was not separately pulled)
Match quality: Strong — exact object named in the guidance (Esarhaddon's Sam'al stele, prince of Egypt kneeling captive).

## B070 — Ashurbanipal relief, British Museum
Narration: "His son Ashurbanipal finished the work, and drove Taharqa out of Egypt for good."
Source: Ashurbanipal wall relief, 7th century BC, from Nineveh, British Museum
URL: https://upload.wikimedia.org/wikipedia/commons/7/71/Ashurbanipal_wall_relief%2C_7th_century_BC%2C_from_Nineveh%2C_the_British_Museum.jpg
License: CC BY-SA 4.0, photographer Osama Shukir Muhammed Amin FRCP(Glasg)
Match quality: Strong — exact object and collection named in the guidance.

## B072 — Statue of Tantamani, Louvre
Narration: "His nephew Tantamani took the crown."
Source: Reconstructed/3D-printed copy of a Kushite royal statue (identified as Tantamani) on display at the Louvre
URL: https://upload.wikimedia.org/wikipedia/commons/d/de/Tantamani%2C_Louvre_Museum.jpg
License: CC BY 2.0, photographer Jean-Pierre Dalbéra
Match quality: Good/Substitute — genuinely at the Louvre and labeled Tantamani, matching the guidance's own phrase "(colour reconstruction)," but the Commons category identifies it as one of a set of modern reconstructed/3D-printed copies of Kushite royal statues found at Dukki-Gel, not a photograph of an ancient original. Flagging so this can be swapped if a photo of the genuine ancient statue turns up.

## B077 — Rassam cylinder (Ashurbanipal, capture of Thebes)
Narration: "An Assyrian inscription boasts that the king lifted his spear against Egypt and Kush and showed his power."
Source: Rassam cylinder — Ashurbanipal's Second Campaign in Egypt (19th-century plate/translation, George Smith)
URL: https://upload.wikimedia.org/wikipedia/commons/6/63/Ashurbanipal%27s_Second_Campaign_in_Egypt_%28Rassam_cylinder%29.jpg
License: Public Domain (PD-old, 19th-century publication)
Match quality: Strong — exact text/object named in the guidance (the Rassam cylinder's account of the capture of Thebes).

## B079 — Psamtik I (statue)
Narration: "In Egypt, an Assyrian ally from Sais named Psamtik founded a new dynasty. The twenty-fifth dynasty was over."
Source: Bust from a statue of Psamtik I, Metropolitan Museum of Art (EGX.358)
URL: https://upload.wikimedia.org/wikipedia/commons/4/4f/Bust_from_Statue_of_a_King_MET_EGX.358.jpeg
License: CHECK — unclear (this is the `og:image` on Wikipedia's "Psamtik I" article and resolves fine; the Commons file-page credit line was not separately pulled, though MET donations are usually CC0)
Match quality: Strong — exactly the statue/relief of Psamtik I the guidance asked for.

## B082 — Erased cartouche / damnatio memoriae (substitute)
Narration: "Figures were scraped from temple carvings."
Source: "Horus and Thot purifying Hatshepsut," Red Chapel of Hatshepsut, Karnak — the figure of Hatshepsut chiseled away by her stepson Thutmose III
URL: https://upload.wikimedia.org/wikipedia/commons/1/1c/Horus_and_Thot_purifying_Hatshepsut_%28chiseled_away_by_her_stepson_Thutmose_III%29..._%2836101001330%29.jpg
License: CC BY-SA 2.0, photographer Bernard Dupont
Match quality: SUBSTITUTE — a real, clear photo of genuine ancient erasure damage (a figure scraped from a relief), exactly the kind of image the narration describes, but it is Hatshepsut's erasure by Thutmose III, not a Kushite king's. No photo of a specifically Kushite erased figure turned up in this search; this is offered as the honest close substitute the task anticipated.

## B088 — Pyramids of Meroe, aerial view
Narration: "There were pyramids, small and steep and graceful, hundreds of them across the kingdom."
Source: Aerial view of the Nubian pyramids at Meroe (2001)
URL: https://upload.wikimedia.org/wikipedia/commons/5/53/Sudan_Meroe_Pyramids_2001.JPG
License: CC BY-SA 1.0 (photographer B N Chagny, image owner Francis Geius)
Match quality: Strong — the file's own description says "Aerial view of the Nubian pyramids at Meroe," and it is categorized under "Aerial photographs of Sudan."

## B089 — Lion Temple of Apedemak, Naqa
Narration: "There were temples to Apedemak, a lion-headed war god you will not find in Egypt."
Source: Lion Temple relief, Naqa — Natakamani and Amanitore approaching Apedemak (engraving from Frédéric Cailliaud's *Voyage à Méroé*, 1826–1827)
URL: https://upload.wikimedia.org/wikipedia/commons/3/31/Lion_temple_relief%2C_Naga_%28Sudan%29.jpg
License: Public Domain (PD-old-70-expired, Cailliaud)
Match quality: Strong — exact temple and deity named in the guidance, though delivered as a 19th-century engraving of the relief rather than a modern photograph.

## B094 — Strabo, Geography (manuscript page)
Narration: "The Greek geographer Strabo sneered that she was mannish and blind in one eye."
Source: Strabo, *Geographica*, 14th-century Venice manuscript (Gr. XI,6)
URL: https://upload.wikimedia.org/wikipedia/commons/0/03/Strabo%2C_Geographica%2C_Venice%2C_Gr._XI%2C6.jpg
License: Public Domain (PD-Art, PD-old-100-expired)
Match quality: Strong — a genuine manuscript page of Strabo's Geography, as the guidance asked for (it is a 14th-century copy, not Strabo's own 1st-century original, which does not survive).

## B096 — Bronze head of Augustus from Meroe
Narration: "Her warriors had also taken the bronze head of a statue of Augustus."
Source: Bronze head from an over-life-sized statue of Augustus, found buried at Meroe, British Museum
URL: https://upload.wikimedia.org/wikipedia/commons/d/d5/Bronze_head_from_an_over-life-sized_statue_of_Augustus.jpg
License: CC BY-SA 2.0, photographer Carole Raddato
Match quality: Strong — exact object named in the guidance.

## B098 — Excavations at Meroe, 1910 (Garstang)
Narration: "It lay there until nineteen ten, when archaeologists found it."
Source: Plate from John Garstang, *Meroë, the City of the Ethiopians: being an account of a first season's excavations on the site, 1909–1910* (Oxford, 1911)
URL: https://upload.wikimedia.org/wikipedia/commons/a/a1/Mero%C3%AB%2C_the_City_of_the_Ethiopians_-_being_an_account_of_a_first_season%27s_excavations_on_the_site%2C_1909-1910_%281911%29_%2814578449067%29.jpg
License: Public Domain (PD-old-100-expired, Internet Archive Book Images / Flickr Commons)
Match quality: Strong — this is literally a page from Garstang's own 1911 excavation report, exactly the source named in the guidance.

## B104 — Ancient Greek world map showing Aethiopia
Narration: "And the Greeks and Romans who came after knew Kush only as a distant land at the edge of the world."
Source: "The World according to Herodotus" — reconstruction map (base data from an 1895 publication, redrawn/vectorized by a Wikimedia contributor in 2012)
URL: https://upload.wikimedia.org/wikipedia/commons/0/05/Herodotus_World_Map.jpg
License: Public Domain (released by the uploader, "Cush")
Match quality: Good — the map explicitly labels "Æthiopes" and "Mare Æthiopicum" at its southern/eastern edge, matching the narration precisely, and it sits in Commons' "Maps of Herodotus's world" category. It is a modern redraw sourced from an 1895 original rather than a literal antique print, so I'm not calling it Strong, but it is a faithful reconstruction, not an invented modern infographic.

## B105 — Meroitic inscription
Narration: "But Kush wrote itself, too. In a script that has never been fully deciphered."
Source: Sandstone block with Meroitic hieroglyphs (3 vertical columns, probably referring to Amun), from Meroe, Petrie Museum of Egyptian Archaeology, London
URL: https://upload.wikimedia.org/wikipedia/commons/0/06/Detail_of_a_sandstone_showing_meroitic_hieroglyphs_in_3_vertical_columns%2C_probably_referring_to_Amun._From_Meroe._Meroitic_period._The_Petrie_Museum_of_Egyptian_Archaeology%2C_London.jpg
License: CC BY-SA 4.0, photographer Osama Shukir Muhammed Amin FRCP(Glasg)
Match quality: Strong — a genuine Meroitic inscription on stone, exactly as the guidance asked for.

## B109 — Erased cartouche, macro (substitute)
Narration: "Where Egypt cut away a king's name, it left a hole in the exact shape of the king. Scholars have been reading those holes for generations."
Source: Situla with the erased cartouche of Akhenaten, Walters Art Museum (48.456)
URL: https://upload.wikimedia.org/wikipedia/commons/5/57/Egyptian_-_Situla_with_Erased_Cartouche_of_Akhenaten_-_Walters_48456_-_Profile.jpg
License: Public Domain (Walters Art Museum open content; also dual-licensed CC BY-SA 3.0/GFDL)
Match quality: Good/Substitute — a real, clear macro of a genuinely erased ancient Egyptian cartouche, matching the narration's "hole in the exact shape of the king." It is on a portable ritual vessel (a situla) rather than a wall, and the erasure is Akhenaten's (Amarna-period damnatio memoriae), not a Kushite king's — flagged per the task's own guidance that any clear genuinely-erased royal cartouche is an acceptable substitute here.

---

## Summary

- **Strong matches (exact object/site named in the guidance, found and verified): 23** — B001, B009, B014, B015, B025, B033, B046 is actually a substitute (see below), B048, B052, B055, B057, B059, B060, B063, B067, B070, B077, B079, B089, B094 (borderline strong), B096, B098, B105.
- **Good matches (real, on-topic, but not a perfect fit to the exact crop/object named): 5** — B005, B031, B072, B104, B109.
- **Flagged substitutes (real artifact, but not the specific one named in the guidance): 3** — B046 (Medinet Habu depiction instead of the Cairo alabaster statue), B082 (Hatshepsut's erasure instead of a Kushite one), B109 (Akhenaten's erasure, on a situla, instead of a wall).
- **Genuinely unresolved: 0.** Every one of the 30 beats got a real, verified, directly-resolving image URL — including the three flagged as hardest in the brief (B025 Tefnakht stela, B055 Lepsius Taharqa/Abar relief, B089 Lion Temple of Naqa), which all turned up clean, on-target sources.
- **B063 note:** the brief says "reuse from Episode 1," but Episode 1's own archival-sources doc and final shot list were checked and contain no Medinet Habu / Sea Peoples asset — there was nothing to reuse, so this one was sourced fresh instead.
- **Licence CHECK (resolves fine, but the Commons credit line wasn't separately pulled): 4** — B025, B046, B067, B079.
