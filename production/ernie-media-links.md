# Ernie Reyes Jr. — footage links and slot map

Download each clip (1080p), rename it to the **slot** name, and drop it in `production/media/`
(`.mp4`, `.mov`, `.mkv`, `.webm`, `.jpg` or `.png`). Re-run `python3 production/ernie-build.py`
and each slot replaces the generated title card, graded, with all labels kept.

Download command (on your machine, with your own cookies file):

    yt-dlp --cookies cookies.txt --extractor-args "youtube:player_client=web_safari" \
      -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "<slot>.mp4" "<URL>"

Clips are looped to fill the scene, so a 20–30 s excerpt per slot is enough
(trim with `-ss 00:00:10 -t 25` via ffmpeg if you like).

| Slot | Scene (VO time) | Link | Channel / length |
|---|---|---|---|
| s02 | Early 1990s (0:20) | https://www.youtube.com/watch?v=UlLWmFpEouI | Surf Ninjas trailer — Rotten Tomatoes Classic Trailers, 2:08 |
| s03 | "Then it all stopped" (0:41) | any dark/fade clip, or leave as card | — |
| s06 | Ernie Reyes Sr. (1:48) | https://www.youtube.com/watch?v=rjUhnpjbDMQ | Sr. + West Coast Action Demo Team, 4:35 |
| s07 | Dojo training (2:11) | https://www.youtube.com/watch?v=I0YGSMq0wSQ | West Coast Demo with Sr. & Jr., 1990, 10:00 |
| s08 | Demonstration team tours (2:33) | https://www.youtube.com/watch?v=oifngY5UhPI | West Coast Next Generation, '98, 4:41 |
| s09 | Bruce Lee / Jackie Chan (3:00) | https://www.youtube.com/watch?v=5RGju9NuoOU | Enter the Dragon trailer — Warner Bros., 2:11 |
| s10 | The Last Dragon (3:29) | https://www.youtube.com/watch?v=Z7Crt4S1IZM | Official trailer — Sony Pictures, 1:28 |
| s11 | Red Sonja (3:51) | https://www.youtube.com/watch?v=LWfEL_zAA78 | 1985 original trailer — HD Retro Trailers, 2:04 |
| s12–s13 | Reputation / TV (4:14, 4:37) | https://www.youtube.com/watch?v=CcEbxUJi7uA | Ernie Reyes Jr. action highlights — Loopkicks, 6:38 |
| s14 | TMNT 1990 (5:01) | https://www.youtube.com/watch?v=FMJPwRWaZBI | Official trailer — Rotten Tomatoes Classic Trailers, 1:28 |
| s15–s16 | Inside the suit / Donatello (5:26, 5:51) | https://www.youtube.com/watch?v=3y9C_P7dG6s | TMNT 4K trailer — Arrow Video, 2:07 |
| s17 | Budget / box office (6:13) | https://www.youtube.com/watch?v=T6sjDuhZKCQ | TMNT original trailer — Unseen Trailers, 2:01 |
| s18 | TMNT II / Keno (6:34) | https://www.youtube.com/watch?v=al9jfY7zOBY | Official trailer — Rotten Tomatoes Classic Trailers, 2:06 |
| s19 | Kids copied his kicks (7:01) | https://www.youtube.com/watch?v=7ycjTzPPdIc | Intro pizza scene (HD), 1:52 |
| s20 | VHS / magazines (7:26) | https://www.youtube.com/watch?v=1ulJwDjpD30 | TMNT II 4K trailer — Arrow Video, 1:31 |
| s21 | His own movie (7:46) | https://www.youtube.com/watch?v=0vidhKXSlYs | "Pizza Boy" clip — JoBlo, 4:17 |
| s22 | Surf Ninjas (8:10) | https://www.youtube.com/watch?v=UlLWmFpEouI | Official trailer — Rotten Tomatoes Classic Trailers, 2:08 |
| s23 | Genre gamble (8:37) | https://www.youtube.com/watch?v=khoiWMnQw6o | Surf Ninjas VHS trailer, 1:39 |
| s24 | Box office / Van Damme (8:58) | https://www.youtube.com/watch?v=bCZ1CIQ64YQ | Bloodsport trailer — Amazon MGM, 1:47 |
| s25–s27 | Smaller roles, adapting (9:28–10:10) | https://www.youtube.com/watch?v=FkZFmpVKnFY | Ernie Reyes Jr. talks TMNT/Surf Ninjas/The Rock — Koffin Radio, 11:17 |
| s28–s30 | Hidden army / stunt career (10:42–11:25) | https://www.youtube.com/watch?v=bf61mm7ClbQ | Ernie Reyes Jr. on fight scenes — Mad Bros Media, 4:26 |
| s31 | The Rundown (P2 0:22) | https://www.youtube.com/watch?v=XmUOlVAuGeo | The Rundown fight scene — Ernie Reyes' World Martial Arts, 3:10 |
| s32 | Fight analysis (P2 0:46) | https://www.youtube.com/watch?v=AYSVCFfgSu0 | The Rock vs. Manito, 6:17 |
| s33–s34 | "What if?" (P2 1:12–1:32) | https://www.youtube.com/watch?v=R2CPfA5eFa4 | The Rundown trailer — HD Retro Trailers, 2:36 |
| s35–s36 | Kidney failure (P2 1:51–2:16) | https://www.youtube.com/watch?v=IipH4uShx34 | ABS-CBN: Ernie Reyes Jr. needs kidney, 0:35 |
| s37 | Fundraising / sister (P2 2:38) | https://www.youtube.com/watch?v=mgmdy4Ygzyc | Ernie Jr. on health after kidney failure — Raav, 1:57 |
| s38–s40 | Recovery, teaching (P2 3:01–3:47) | https://www.youtube.com/watch?v=BRmuJrG7uHg | Full interview — Taboo's Comics & Kicks, 1:09:35 |
| s41–s42 | Legacy (P2 4:15–4:40) | https://www.youtube.com/watch?v=iR-VrtGdkiQ | The Art of Action: Ernie Reyes Jr. — Scott Adkins, 38:32 |

Photos (people): drop `.jpg` into the matching slot instead of a clip — e.g. `s09.jpg` for Bruce Lee,
`s31.jpg` for Dwayne Johnson. Photos get the same slow push-in as the generated cards.

Links come from YouTube search results; I could not open them from this sandbox, so check each one is the
right cut before using it. Fan-uploaded clips may be claimed or removed at any time. Trailers and film clips are
copyrighted — fair-use commentary/documentary use is your call and responsibility.
