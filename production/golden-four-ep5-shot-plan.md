# Golden Four Ep5 "The Collision" — shot plan (draft)

Audio: `public/golden-four-ep5-voiceover.mp3`, about 1007.2s (16:47), recorded from
`golden-four-ep5-script-v1.1.md`.

Beat timecodes below are **estimates** based on each beat's word count. They
still need checking against a transcript before the cuts are locked.

Sources: symbolic stock B-roll (Pexels) plus official stills, backdrops and
posters from TMDB (The Movie Database), which the user asked to add. TMDB images
are copyrighted by the studios. Use them as commentary: show each one only while
the narration is discussing that film or role, keep it on screen briefly
(3–6s, with a Ken Burns move), and never use one as a full-frame backdrop behind
unrelated narration. Still no film clips, trailers or convention footage.

## Beats

| Beat | Est. time | Visual direction (symbolic) |
|---|---|---|
| 0 Cold open | 0:00–1:40 | Starfield/stardust drift → four gold points of light → a fifth, green light approaching. Title card "EP 5 · THE COLLISION". "We have not seen it" line over a dark, empty cinema. |
| 1 Foundation | 1:40–4:00 | Four chapters, ~30s each: slow-burn candle/ember (Reed); a sprinting runner / time-lapse traffic (Johnny); a door opening onto light (Sue); a sculptor's hands on stone (Ben). End on a family dinner table seen from above. |
| 2 Doom proposition | 4:00–6:35 | Vintage comic-shop shelves (no readable covers); a green cloak and iron textures; forge sparks; a chessboard with one side advancing; a mask on a pedestal (generic, not Doom's design). "Tony chose his limits" over a workshop bench with tools set down. |
| 3 Collision point | 6:35–8:55 | Two chairs facing each other in an empty hall (the conversation); chalkboard equations; then fire: a lit match, bonfire, sparks against the night (Johnny). |
| 4 Mother's choice | 8:55–10:55 | A hospital corridor at dawn; a hand on a crib; soft refracted light / prism (invisibility motif); a protective hand shielding a candle from the wind. |
| 5 Thing and stone | 10:55–12:40 | Quarry and granite close-ups; a weathered statue in the rain; a boxing gym (Ben's Yancy Street grit); a kitchen line (a nod to The Bear, generic). |
| 6 Variant theory | 12:40–14:25 | A mirror maze / infinite reflections; a desert cave mouth; an empty workshop; a split-screen light graphic, gold left and green right. |
| 7 Why casting matters | 14:25–15:30 | Five light points taking positions (motion graphic), each lighting up as its actor's name is spoken. |
| 8 Close | 15:30–16:47 | Stardust drift returns; four gold points and a green point collide in a bloom of light; end card "Avengers: Doomsday · Dec 18" + subscribe. |

## TMDB pulls (by beat)

Look up the TMDB IDs through the API when it's reachable; don't hardcode them from memory.

| Beat | Title (TMDB type) | Image use |
|---|---|---|
| 1 | The Fantastic Four: First Steps (movie) | backdrop of the team; individual character stills for each actor's chapter |
| 2 | Iron Man (movie), Avengers: Endgame (movie) | one backdrop each for "Tony chose his limits" |
| 2, 8 | Avengers: Doomsday (movie) | official poster/backdrop, if TMDB has one |
| 3 | Game of Thrones, Narcos, The Last of Us (tv) | one still each for Oberyn / Peña / Joel |
| 3 | Stranger Things (tv), A Quiet Place: Day One, Gladiator II (movie) | one still each for Eddie / Day One / Geta |
| 4 | The Crown (tv), Mission: Impossible – Fallout, Pieces of a Woman (movie) | one still each |
| 5 | The Punisher, Andor, The Bear (tv) | one still each; The Bear gets the most screen time |
| 6 | Iron Man (movie) | cave/workshop backdrop for the "cave in Afghanistan" line |

## vidiq_compose segments (≤240s each)

5 segments of about 200s each, with cut points to be moved to the nearest sentence pause once
the audio is transcribed:

1. 0:00 – ~3:20 (Beats 0–1)
2. ~3:20 – ~6:40 (end of Beat 1 – Beat 2)
3. ~6:40 – ~10:05 (Beats 3–4)
4. ~10:05 – ~13:25 (end of Beat 4 – Beat 6)
5. ~13:25 – 16:47 (end of Beat 6 – Beat 8)

## Open items

- Transcribe the voiceover to lock the timecodes (a local transcription model can't be
  downloaded because this session's network is restricted).
- Source the B-roll URLs (Pexels, or vidIQ B-roll generation).
- TMDB: needs `api.themoviedb.org` and `image.tmdb.org` allowed in the environment's
  network settings, plus a TMDB API key stored as an environment secret (for example `TMDB_API_KEY`).
- Thumbnail: graphic only (four gold quadrants + a green mask silhouette); no faces.
