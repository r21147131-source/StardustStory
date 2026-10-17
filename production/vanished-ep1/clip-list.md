# Vanished Ep1 — clip list

Trim each source to the length shown, scale to 540p, drop audio, and name the file with the shot id.

```
ffmpeg -ss START -i source.mp4 -t SECONDS -vf scale=-2:540 -c:v libx264 -crf 26 -an sNN.mp4
```

`START` = any strong moment in the source (mm:ss). `SECONDS` = the length below, plus ~1s spare.
A shot can also be a still (`sNN.jpg`). Shots marked LABEL show a one-time name label, so the face or title should be clear.

| Shot | Narration time | Length | Type | What to find | Search | Label |
|---|---|---|---|---|---|---|
| s01 | 0:00–0:17 | 19s | film | Terminator 2 - John Connor / T-800 scenes | Terminator 2 Judgment Day trailer | Edward Furlong, Terminator 2: Judgment Day, Arnold Schwarzenegger |
| s02 | 0:17–0:32 | 16s | film | Terminator 2 - John Connor / T-800 scenes | Terminator 2 John Connor Sarah Connor scene | – |
| s04 | 0:48–1:00 | 13s | photo | Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills | Edward Furlong childhood photos / early interview (Pasadena, Boys' Club) | Mali Finn |
| s05 | 1:00–1:17 | 18s | photo | Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills | Terminator 2 behind the scenes Furlong Cameron | James Cameron |
| s06 | 1:17–1:30 | 13s | photo | Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills | Edward Furlong childhood photos / early interview (Pasadena, Boys' Club) | – |
| s07 | 1:30–1:43 | 15s | photo | Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills | Terminator 2 behind the scenes Furlong Cameron | – |
| s08 | 1:43–2:02 | 19s | photo | Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills | Edward Furlong childhood photos / early interview (Pasadena, Boys' Club) | – |
| s09 | 2:02–2:21 | 21s | film | T2 hits (sewer/bike chase, 'No problemo'); Guns N' Roses 'You Could Be Mine' video | Guns N' Roses You Could Be Mine official video | – |
| s10 | 2:21–2:46 | 26s | film | T2 hits (sewer/bike chase, 'No problemo'); Guns N' Roses 'You Could Be Mine' video | Terminator 2 canal chase / 'No problemo' scene | – |
| s11 | 2:46–3:01 | 16s | film | T2 hits (sewer/bike chase, 'No problemo'); Guns N' Roses 'You Could Be Mine' video | Guns N' Roses You Could Be Mine official video | – |
| s12 | 3:01–3:18 | 18s | film | T2 hits (sewer/bike chase, 'No problemo'); Guns N' Roses 'You Could Be Mine' video | Terminator 2 canal chase / 'No problemo' scene | – |
| s13 | 3:18–3:39 | 22s | film | Pet Sematary II, American Heart, A Home of Our Own, Brainscan | Brainscan 1994 trailer | Jeff Bridges |
| s14 | 3:39–3:53 | 15s | film | Pet Sematary II, American Heart, A Home of Our Own, Brainscan | Pet Sematary 2 trailer | – |
| s15 | 3:53–4:08 | 16s | film | Pet Sematary II, American Heart, A Home of Our Own, Brainscan | American Heart 1992 trailer | – |
| s16 | 4:08–4:21 | 14s | film | Pet Sematary II, American Heart, A Home of Our Own, Brainscan | A Home of Our Own 1993 trailer | – |
| s17 | 4:21–4:26 | 7s | film | Pet Sematary II, American Heart, A Home of Our Own, Brainscan | Brainscan 1994 trailer | – |
| s18 | 4:26–4:47 | 21s | interview | Interview clip - Furlong reflecting on early fame | Edward Furlong interview early fame | – |
| s19 | 4:47–5:00 | 14s | interview | Interview clip - Furlong reflecting on early fame | Edward Furlong interview early fame | – |
| s20 | 5:00–5:11 | 12s | film | American History X, Pecker, Detroit Rock City | American History X trailer | American History X, Edward Norton |
| s21 | 5:11–5:27 | 18s | film | American History X, Pecker, Detroit Rock City | Pecker 1998 trailer | – |
| s22 | 5:27–5:40 | 14s | film | American History X, Pecker, Detroit Rock City | Detroit Rock City trailer | John Waters |
| s23 | 5:40–5:58 | 19s | film | American History X, Pecker, Detroit Rock City | American History X trailer | – |
| s24 | 5:58–6:19 | 22s | interview | Interview clip - Furlong on addiction/recovery | Edward Furlong interview addiction recovery | – |
| s25 | 6:19–6:32 | 15s | interview | Interview clip - Furlong on addiction/recovery | Edward Furlong interview addiction recovery | – |
| s26 | 6:32–6:47 | 15s | interview | Interview clip - Furlong on addiction/recovery | Edward Furlong interview addiction recovery | – |
| s27 | 6:47–7:02 | 16s | interview | Interview clip - Furlong on addiction/recovery | Edward Furlong interview addiction recovery | – |
| s28 | 7:02–7:19 | 18s | interview | Interview clip - Furlong on addiction/recovery | Edward Furlong interview addiction recovery | – |
| s29 | 7:19–7:32 | 14s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Edward Furlong interview Terminator 3 recast | Nick Stahl |
| s30 | 7:32–7:47 | 16s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Terminator 3 Rise of the Machines trailer (Nick Stahl) | – |
| s31 | 7:47–8:04 | 19s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Edward Furlong interview Terminator 3 recast | – |
| s32 | 8:04–8:20 | 16s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Terminator 3 Rise of the Machines trailer (Nick Stahl) | – |
| s33 | 8:20–8:35 | 16s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Edward Furlong interview Terminator 3 recast | – |
| s34 | 8:35–8:38 | 4s | film | Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting | Terminator 3 Rise of the Machines trailer (Nick Stahl) | – |
| s35 | 8:38–8:53 | 16s | film | Later indie / genre work; convention footage | Edward Furlong later films / convention footage | – |
| s36 | 8:53–9:07 | 15s | film | Later indie / genre work; convention footage | Edward Furlong later films / convention footage | – |
| s37 | 9:07–9:25 | 19s | film | Later indie / genre work; convention footage | Edward Furlong later films / convention footage | – |
| s38 | 9:25–9:43 | 19s | film | Later indie / genre work; convention footage | Edward Furlong later films / convention footage | – |
| s39 | 9:43–9:56 | 13s | film | Terminator: Dark Fate opening scene | Terminator Dark Fate trailer | Terminator: Dark Fate |
| s40 | 9:56–10:08 | 14s | film | Terminator: Dark Fate opening scene | Terminator Dark Fate opening scene John Connor | – |
| s41 | 10:08–10:21 | 13s | film | Terminator: Dark Fate opening scene | Terminator Dark Fate trailer | – |
| s42 | 10:21–10:37 | 17s | film | Terminator: Dark Fate opening scene | Terminator Dark Fate opening scene John Connor | – |
| s43 | 10:37–10:42 | 7s | film | Terminator: Dark Fate opening scene | Terminator Dark Fate trailer | – |
| s44 | 10:42–10:57 | 16s | interview | Interview clip / T2 stills, slow push-ins | Terminator 2 John Connor and T-800 scene | – |
| s45 | 10:57–11:10 | 14s | interview | Interview clip / T2 stills, slow push-ins | Edward Furlong interview reflecting | – |
| s46 | 11:10–11:24 | 16s | interview | Interview clip / T2 stills, slow push-ins | Terminator 2 John Connor and T-800 scene | – |
| s47 | 11:24–11:37 | 13s | interview | Interview clip / T2 stills, slow push-ins | Edward Furlong interview reflecting | – |
| s48 | 11:37–11:52 | 16s | interview | Interview clip / T2 stills, slow push-ins | Terminator 2 John Connor and T-800 scene | – |
| s49 | 11:52–12:11 | 20s | interview | Interview clip / T2 stills, slow push-ins | Edward Furlong interview reflecting | – |
| s50 | 12:11–12:27 | 18s | interview | Recent interview or convention footage; sobriety statement | Edward Furlong convention panel | – |
| s51 | 12:27–12:51 | 25s | interview | Recent interview or convention footage; sobriety statement | Edward Furlong 2025 interview sobriety | – |
| s52 | 12:51–13:10 | 20s | interview | Recent interview or convention footage; sobriety statement | Edward Furlong convention panel | – |
| s53 | 13:10–13:18 | 9s | interview | Recent interview or convention footage; sobriety statement | Edward Furlong 2025 interview sobriety | – |
| s54 | 13:18–13:33 | 17s | film | Molly Ringwald - Sixteen Candles / Breakfast Club | Molly Ringwald Sixteen Candles trailer | – |
| s55 | 13:33–13:46 | 14s | film | Molly Ringwald - Sixteen Candles / Breakfast Club | Breakfast Club trailer | Molly Ringwald |
| s56 | 13:46–14:05 | 20s | film | Molly Ringwald trailer montage | Molly Ringwald Pretty in Pink trailer | – |

Priority if you only grab a few: s01, s09, s20, s24, s29, s39, s50.
Shots without a file keep the TMDB still already in `assets/` (or a placeholder card).
