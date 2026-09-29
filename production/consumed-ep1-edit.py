"""Consumed Ep. 1 (Daniel Day-Lewis): mention-driven edit + local ffmpeg render.

Visual rules (per the brief):
  - a film is named       -> its TMDB poster, then footage from its trailer
  - a person is named     -> their TMDB photo with a name caption
  - gaps                  -> interview clips, TMDB film stills, Pexels B-roll

Cue times come from production/consumed-ep1-sentences.json (sentence starts,
aligned to the voiceover by consumed-ep1-align.py). Each cue runs until the
next one starts.

Trailer and interview clips are YouTube trims made with vidiq_edit_media (TMDB
lists trailers as YouTube links). Those trims come back at about 256x144, so
they play in a frame over a blurred copy of themselves, never full screen.

Inputs (gitignored, under render/): clips/*.mp4 (trims), tmdb/{posters,people,
<film>}/*.jpg, consumed-ep1/src/*.mp4 (Pexels, from consumed-ep1-build.py).
Usage: python3 production/consumed-ep1-edit.py [--only N]
"""
import json, os, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(ROOT, "render")
VO = os.path.join(ROOT, "public/consumed-ep1-daniel-day-lewis-voiceover.mp3")
WORK = os.path.join(R, "consumed-ep1-edit")
OUT = os.path.join(ROOT, "output/consumed-ep1/daniel-day-lewis-consumed.mp4")
TOTAL = 624.93
SENT = [s["t"] for s in json.load(open(os.path.join(ROOT, "production/consumed-ep1-sentences.json")))]

# --- asset helpers --------------------------------------------------------
def B(name, start=0):            # Pexels B-roll (file name in consumed-ep1/src)
    return {"k": "broll", "src": f"{R}/consumed-ep1/src/{name}", "start": start}

def S(film, img):                # TMDB still, full frame with Ken Burns
    return {"k": "still", "src": f"{R}/tmdb/{film}/{img}.jpg"}

def D(img, label=None):          # TMDB portrait of Day-Lewis
    return {"k": "portrait", "src": f"{R}/tmdb/profile/{img}.jpg", "label": label}

def H(person, label):            # TMDB photo of a named person
    return {"k": "portrait", "src": f"{R}/tmdb/people/{person}.jpg", "label": label}

def P(film, label):              # TMDB poster
    return {"k": "poster", "src": f"{R}/tmdb/posters/{film}.jpg", "label": label}

def C(clip, start, label=None):  # trailer / interview trim, framed
    return {"k": "clip", "src": f"{R}/clips/{clip}.mp4", "start": start, "label": label}

CURTAIN = "4722613-hd_1366_720_25fps.mp4"
SPOT = "8515272-hd_1280_720_25fps.mp4"
DANCER = "11963026_640_360_30fps.mp4"
FOGMAN = "8679945-hd_1366_720_25fps.mp4"
DUST_A = "9665236-hd_1920_1080_25fps.mp4"
DUST_B = "9665237-hd_1920_1080_25fps.mp4"
PHOTOS = "11272050-hd_1920_1080_30fps.mp4"
BOW = "6899907-hd_1366_720_25fps.mp4"
SHOE = "15962716_640_360_25fps.mp4"
SHOE2 = "9936744-hd_1920_1080_25fps.mp4"
SHOE3 = "17661984-hd_1280_720_24fps.mp4"

# (sentence index, seconds after that sentence starts, visual)
CUES = [
    # COLD OPEN
    (0, 0, B(CURTAIN)), (1, 0, B(SPOT)), (2, 0, B(DANCER)), (3, 0, B(FOGMAN)),
    (5, 0, B(CURTAIN, 20)), (8, 0, D("jdEbEzHCaEGo0RkamvkjokzNtDS")),
    # PREMISE
    (9, 0, B("856593-hd_1920_1080_24fps.mp4")), (10, 0, B(DUST_A)),
    (11, 0, D("1ZQIlcZVurEXQv9SCslMtyitCrM", "Daniel Day-Lewis")),
    (12, 0, S("lincoln", "90PDnoWXUIJQCwujSJ8bfcCva0J")),
    (13, 0, S("blood", "zPQYSaRUzCAksd25fLEVbh3zQcv")), (13, 3.8, S("thread", "3SFdxy3lFAjHRxkYEP4g4j8ckXF")),
    # ACT I
    (14, 0, B("16887642_640_360_25fps.mp4")),
    (15, 0, D("3CghmDL7V3w5NYjJUkiqWLIQv8Q")),
    (16, 0, B("4061896-hd_1280_720_24fps.mp4")),
    (17, 0, B("2308576-hd_1280_720_30fps.mp4")),  # Cecil Day-Lewis: no photo on TMDB
    (18, 0, H("jill", "Jill Balcon")),
    (19, 0, H("michael", "Sir Michael Balcon  ·  Ealing Studios")),
    (20, 0, B(PHOTOS)), (22, 0, B("7546430-hd_1920_1080_25fps.mp4")),
    (24, 0, D("9qUVqOfRoMJKueEabs0ciQe9PDK")),
    (26, 0, B("5972653-hd_1280_720_25fps.mp4")), (27, 0, B("7314256-hd_2048_1080_25fps.mp4")),
    (29, 0, B("5972648-hd_1920_1080_25fps.mp4")),
    (31, 0, B("6899905-hd_1366_720_25fps.mp4")), (33, 0, B(BOW)),
    # ACT II
    (34, 0, D("true2FJMdoH5o8ORu67tToqH74a")),
    (36, 0, P("leftfoot", "My Left Foot  (1989)")), (36, 4.3, C("leftfoot", 15)),
    (37, 0, C("leftfoot", 20)), (38, 0, S("leftfoot", "zjKg04EquTcnVZUfjHboXnXzjcF")),
    (39, 0, C("leftfoot", 25)), (40, 0, S("leftfoot", "lU5hQNFC0sEHdYPZPzu4lY7QfiP")),
    (41, 0, B("8524028-hd_2048_1080_25fps.mp4")), (42, 0, S("leftfoot", "qEfLnvC2IqaQLwLT7Finvq9ocS6")),
    (43, 0, C("leftfoot", 40)), (44, 0, B("7005887-hd_1920_1080_30fps.mp4")),
    (45, 0, P("mohicans", "The Last of the Mohicans  (1992)")), (45, 3.5, C("mohicans", 5)),
    (45, 6.5, C("mohicans", 30)),
    (46, 0, P("father", "In the Name of the Father  (1993)")), (46, 3.6, C("father", 30)),
    (47, 0, C("father", 35)), (47, 4.0, S("father", "kQGWzpvCVnsULcIAsT9TsmcqfgD")),
    (48, 0, S("father", "jgD5rT4pijE7Hm596A6rp5jalXE")),
    (49, 0, B("12187197-hd_1280_720_25fps.mp4")), (50, 0, B("5481284-hd_1920_1080_24fps.mp4")),
    (51, 0, D("5J43EFBCSzbgXc46YjJBYswihTT")),
    (52, 0, B(DUST_B)), (53, 0, B("11792115-hd_1280_720_25fps.mp4")),
    # ACT III
    (54, 0, B(SPOT, 10)), (55, 0, H("eyre", "Richard Eyre  ·  director, Hamlet (1989)")),
    (56, 0, B(BOW, 10)), (57, 0, B(DANCER, 8)), (58, 0, B(FOGMAN, 5)), (59, 0, B(SPOT, 15)),
    (60, 0, B(DUST_A, 20)), (61, 0, H("charleson", "Ian Charleson")),
    (62, 0, B(PHOTOS, 8)), (63, 0, B("11839732-hd_1920_1080_25fps.mp4")),
    (64, 0, B("4230107-hd_1920_1080_30fps.mp4")), (65, 0, D("5J43EFBCSzbgXc46YjJBYswihTT")),
    (66, 0, C("int_cbs", 30, "CBS Sunday Morning, 2025")),
    (67, 0, B("11792115-hd_1280_720_25fps.mp4", 8)), (68, 0, B(CURTAIN, 40)),
    (69, 0, B(DUST_B, 20)), (72, 0, B(FOGMAN)), (73, 0, B(BOW, 25)),
    (74, 0, P("elsinore", "Elsinore  (2026)")), (74, 4.6, H("scott", "Andrew Scott as Ian Charleson")),
    # ACT IV
    (75, 0, C("boxer", 20)), (76, 0, P("boxer", "The Boxer  (1997)")),
    (76, 3.0, H("mcguigan", "Barry McGuigan  ·  former world champion")),
    (77, 0, C("boxer", 45)), (78, 0, B("11839732-hd_1920_1080_25fps.mp4", 10)),
    (81, 0, B("17138696-hd_1280_720_30fps.mp4")), (83, 0, B("5979152-hd_1920_1080_30fps.mp4")),
    (84, 0, B("7724737-hd_1920_1080_25fps.mp4")), (85, 0, B(SHOE)),
    (86, 0, B(SHOE2)), (86, 5.2, B(SHOE3)), (87, 0, B(SHOE, 12)),
    (90, 0, B(SHOE2, 8)), (91, 0, B(SHOE3, 10)), (93, 0, B(SHOE, 18)), (95, 0, B(SHOE2, 11)),
    # MID-ROLL CALLBACK
    (96, 0, B("6254907-hd_1920_1080_25fps.mp4")), (97, 0, H("ledger", "Heath Ledger")),
    (97, 4.6, P("darkknight", "The Dark Knight  (2008)")),
    (98, 0, B("17138696-hd_1280_720_30fps.mp4", 15)), (99, 0, S("posters", "darkknight_bd")),
    # ACT V
    (100, 0, C("gangs", 10)), (101, 0, H("scorsese", "Martin Scorsese")),
    (101, 2.9, P("gangs", "Gangs of New York  (2002)")), (102, 0, C("gangs", 70)),
    (103, 0, C("int_dicaprio", 5, "Leonardo DiCaprio")), (104, 0, C("gangs", 60)),
    (106, 0, B("5658155-hd_2048_1080_30fps.mp4")), (107, 0, C("gangs", 75)),
    (108, 0, B("6527469-hd_1920_1080_25fps.mp4")), (108, 4.5, S("gangs", "kr9c6sw1bUanrlP7a3OEA6OfifK")),
    (109, 0, C("gangs", 30)), (110, 0, S("gangs", "ltdMK8bimxDXKwWxn8lKnFGP20L")),
    (111, 0, P("blood", "There Will Be Blood  (2007)")), (111, 2.3, C("blood", 0)),
    (112, 0, P("lincoln", "Lincoln  (2012)")), (112, 2.5, H("spielberg", "Steven Spielberg")),
    (113, 0, C("lincoln", 45)), (113, 2.6, C("int_oscar", 75, "85th Academy Awards, 2013")),
    (114, 0, D("zvsIA89Y7HPC6ZXLbJoC3MXS71w", "Knighted, 2014")),
    (115, 0, B("12426698-hd_1920_1080_30fps.mp4")), (117, 0, C("blood", 60)),
    # OPEN-LOOP CTA
    (118, 0, B("6389055-hd_1920_1080_25fps.mp4")), (119, 0, C("lincoln", 50)),
    (120, 0, H("bale", "Christian Bale  ·  next Friday on Consumed")),
    (121, 0, B("6053511-hd_1920_1080_25fps.mp4")), (122, 0, B(DUST_A, 40)),
    # ACT VI
    (123, 0, P("thread", "Phantom Thread  (2017)")), (123, 2.7, H("pta", "Paul Thomas Anderson")),
    (124, 0, C("thread", 25)), (125, 0, B("6459999-hd_1920_1080_25fps.mp4")),
    (126, 0, C("thread", 65)), (126, 3.4, B("12837345_640_360_24fps.mp4")),
    (127, 0, S("thread", "2GjyR3g0cuv6z0R73dekLfeiDt4")), (128, 0, C("thread", 70)),
    (130, 0, B("12837345_640_360_24fps.mp4", 15)), (131, 0, C("thread", 40)),
    (132, 0, C("thread", 5)), (133, 0, C("thread", 85)), (134, 0, C("thread", 50)),
    (135, 0, S("thread", "iiZY7k4oDn5u2kS06165DZ6Th6j")), (136, 0, B("5815527-hd_1920_1080_25fps.mp4")),
    (137, 0, C("thread", 30)), (138, 0, C("thread", 60)),
    (139, 0, S("thread", "mIoKHm3LPE9zWHFOGJVpSqzkFm8")), (140, 0, B("4927854-hd_1280_720_30fps.mp4")),
    (141, 0, P("thread", "Phantom Thread  (2017)")), (142, 0, S("thread", "vpRMzPqHC03I7hPPET4Av2OT8dI")),
    (143, 0, B(CURTAIN, 60)),
    # ACT VII
    (144, 0, C("anemone", 0)), (145, 0, H("scorsese", "Martin Scorsese")),
    (146, 0, H("spielberg", "Steven Spielberg")), (147, 0, B("5104195-hd_1920_1080_30fps.mp4")),
    (148, 0, H("ronan", "Ronan Day-Lewis")), (148, 3.5, C("int_cbs", 5)),
    (149, 0, P("anemone", "Anemone  (2025)")), (149, 2.3, H("bean", "Sean Bean")),
    (150, 0, C("int_cbs", 35, "CBS Sunday Morning, 2025")), (152, 0, C("anemone", 10)),
    (153, 0, C("int_nyff", 0, "New York Film Festival, 2025")), (154, 0, C("int_nyff", 10)),
    (155, 0, C("int_nyff", 40)), (156, 0, C("anemone", 15)), (157, 0, C("int_cbs", 60)),
    (158, 0, C("anemone", 20)), (159, 0, C("int_cbs", 70)),
    (160, 0, B(PHOTOS, 12)), (161, 0, B("7546430-hd_1920_1080_25fps.mp4")),
    (162, 0, B(CURTAIN, 30)), (162, 3.2, D("jdEbEzHCaEGo0RkamvkjokzNtDS")),
    (163, 0, S("anemone", "5NiaMhJPXB4tTpmVvufH9oIdIGR")), (163, 3.8, H("ronan", "Ronan Day-Lewis")),
    (164, 0, C("anemone", 5)), (165, 0, S("anemone", "jJ96OtfgitSPw07Z9JVOSN5Qo8C")),
    (166, 0, S("anemone", "rMCTzLujqBbdc50D6fxrJgACDDV")), (166, 3.6, D("3kNA9VcmymoEwT0btQ4bvMYxzcP")),
    (167, 0, B("5004222-hd_1920_1080_24fps.mp4")), (168, 0, B(DUST_B, 40)),
    (169, 0, B("6867012-hd_1280_720_24fps.mp4")),
]

TITLES = [(9, "CONSUMED\\N{\\fs44}Episode One  ·  Daniel Day-Lewis"), (14, "ACT I\\N{\\fs44}The Poet's Son"),
          (34, "ACT II\\N{\\fs44}The Disappearing Man"), (54, "ACT III\\N{\\fs44}The Ghost"),
          (75, "ACT IV\\N{\\fs44}The Bench"), (100, "ACT V\\N{\\fs44}The Butcher and the President"),
          (123, "ACT VI\\N{\\fs44}The Last Thread"), (144, "ACT VII\\N{\\fs44}The Return")]


# Sharper 9:16 clips from vidiq_generate_clips (1080x1920), listed by fetch_vclips.py.
# When a clip name has a pool here, its C() cues use the pool instead of the 256x144 trim,
# taking the next unused stretch of footage in order.
VCLIPS_JSON = os.path.join(ROOT, "production/consumed-ep1-vclips.json")
VCLIPS = json.load(open(VCLIPS_JSON)) if os.path.exists(VCLIPS_JSON) else {}


def build_shots():
    cues = sorted(((SENT[i] + off, v) for i, off, v in CUES), key=lambda c: c[0])
    shots, cursor = [], {}
    for n, (t, v) in enumerate(cues):
        end = cues[n + 1][0] if n + 1 < len(cues) else TOTAL
        shot = dict(v, t=round(t, 3), dur=round(end - t, 3))
        name = os.path.basename(shot["src"])[:-4] if shot["k"] == "clip" else None
        pool = VCLIPS.get(name)
        if pool:
            k, off = cursor.get(name, (0, 0.0))
            for _ in range(len(pool) + 1):  # next clip with enough footage left
                if pool[k]["dur"] - off >= shot["dur"] + 0.2:
                    break
                k, off = (k + 1) % len(pool), 0.0
            c = pool[k]
            shot.update(k="vclip", src=os.path.join(ROOT, c["file"]), start=round(off, 2), crop=c["crop"])
            cursor[name] = (k, off + shot["dur"] + 0.3)
        shots.append(shot)
    return shots


def ass_time(s):
    h, s = divmod(s, 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_ass(path, shots):
    ev, busy = [], []
    band = "m 0 0 l 1520 0 l 1520 250 l 0 250"
    for i, title in TITLES:  # act titles on a soft dark band so they read over posters too
        s = SENT[i] + 0.6
        busy.append((s, s + 4.5))
        ev.append(f"Dialogue: 0,{ass_time(s)},{ass_time(s + 4.5)},T,"
                  f"{{\\an7\\pos(200,780)\\p1\\bord0\\shad0\\blur16\\1c&H000000&\\1a&H28&\\fad(700,900)}}{band}")
        ev.append(f"Dialogue: 1,{ass_time(s)},{ass_time(s + 4.5)},T,{{\\fad(700,900)}}{title}")
    for s in shots:
        if not s.get("label"):
            continue
        a, b = s["t"] + 0.3, s["t"] + min(3.9, s["dur"] - 0.1)
        for t0, t1 in busy:  # never stack a caption on an act title
            if a < t1 and b > t0:
                a = t1
        if b - a >= 1.2:
            ev.append(f"Dialogue: 2,{ass_time(a)},{ass_time(b)},L,{{\\fad(300,400)}}{s['label']}")
    open(path, "w").write("\n".join([
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Spacing",
        "Style: T,DejaVu Serif,96,&H00F0F0F0,&H00000000,&H80000000,1,0,1,3,3,2,80,80,120,6",
        "Style: L,DejaVu Sans,46,&H00F5F5F5,&H00000000,&H64000000,1,0,1,3.5,2.5,1,96,96,80,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Text"] + ev) + "\n")


LOOK = "eq=saturation=0.78:contrast=1.05,vignette=PI/5,format=yuv420p"
COVER4K = "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160"
BLUR_BG = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=24:3,eq=brightness=-0.22:saturation=0.6"
MOVES = [("1.02+0.08*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
         ("1.10-0.08*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
         ("1.08", "(iw-iw/zoom)*on/{n}", "ih/2-(ih/zoom/2)"),
         ("1.08", "(iw-iw/zoom)*(1-on/{n})", "ih/2-(ih/zoom/2)")]


def shot_cmd(i, s, out):
    d, n = s["dur"], max(1, round(s["dur"] * 30))
    fade = f"fade=t=in:st=0:d=0.3,fade=t=out:st={max(0, d - 0.3):.3f}:d=0.3"
    z, x, y = (m.format(n=n) for m in MOVES[i % len(MOVES)])
    kb = f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1920x1080:fps=30"
    enc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", out]
    if s["k"] == "broll":
        vf = f"scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,{LOOK},{fade}"
        return [FF, "-y", "-ss", str(s["start"]), "-stream_loop", "-1", "-i", s["src"], "-t", f"{d:.3f}", "-vf", vf] + enc
    if s["k"] == "still":
        fc = f"[0]{COVER4K},{kb},{LOOK},{fade}"
        return [FF, "-y", "-i", s["src"], "-filter_complex", fc, "-frames:v", str(n)] + enc
    if s["k"] in ("portrait", "poster"):  # sharp image over a blurred copy of itself
        h = 2000 if s["k"] == "poster" else 2160
        fc = (f"[0]{COVER4K},boxblur=48:5,eq=brightness=-0.18:saturation=0.7[bg];[0]scale=-2:{h}[fg];"
              f"[bg][fg]overlay=(W-w)/2:(H-h)/2,{kb},{LOOK},{fade}")
        return [FF, "-y", "-i", s["src"], "-filter_complex", fc, "-frames:v", str(n)] + enc
    if s["k"] == "clip":  # low-res trim: framed window over its own blurred copy
        fc = (f"[0]fps=30,split[a][b];[a]{BLUR_BG}[bg];"
              f"[b]scale=1216:684:force_original_aspect_ratio=decrease:flags=lanczos,unsharp=5:5:0.7,"
              f"pad=iw+8:ih+8:4:4:color=0xD8D8D8[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,{LOOK},{fade}")
        return [FF, "-y", "-ss", str(s["start"]), "-stream_loop", "-1", "-i", s["src"], "-t", f"{d:.3f}",
                "-filter_complex", fc] + enc
    if s["k"] == "vclip":  # sharp 9:16 clip over its own blurred copy
        crop = band_crop(s["src"], s["start"] + d / 2) or s["crop"]
        fc = (f"[0]fps=30,crop={crop},split[a][b];[a]{BLUR_BG}[bg];"
              f"[b]scale=1904:1040:force_original_aspect_ratio=decrease:flags=lanczos,"
              f"pad=iw+8:ih+8:4:4:color=0xD8D8D8[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,{LOOK},{fade}")
        return [FF, "-y", "-ss", str(s["start"]), "-i", s["src"], "-t", f"{d:.3f}",
                "-filter_complex", fc] + enc
    raise ValueError(s["k"])


def band_crop(path, t):
    """vidIQ's 9:16 reframes often show the whole 16:9 frame as a sharp 1080x608 band with a
    blurred copy above and below. Find that band from per-row sharpness and return a crop
    for it, so the footage can play large and wide. None means use the full 9:16 frame."""
    try:
        import numpy as np
    except ImportError:
        return None
    raw = subprocess.run([FF, "-loglevel", "error", "-ss", f"{t:.2f}", "-i", path, "-frames:v", "1",
                          "-vf", "scale=270:480,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(raw) != 270 * 480:
        return None
    a = np.frombuffer(raw, np.uint8).reshape(480, 270).astype(float)
    sharp = np.abs(np.diff(a, axis=1)).mean(1) > np.percentile(np.abs(np.diff(a, axis=1)).mean(1), 90) * 0.5
    best, cur, start, gap = (0, 0), 0, 0, 0
    for y, v in enumerate(sharp):  # longest sharp run, tolerating 6-row gaps
        if v:
            if cur == 0:
                start = y
            cur, gap = y - start + 1, 0
        elif cur:
            gap += 1
            if gap > 6:
                best, cur = max(best, (cur, start)), 0
    best = max(best, (cur, start))
    run, y0 = best
    outside = sharp.sum() - sharp[y0:y0 + run].sum()
    if not (110 <= run <= 190 and outside < 40):  # a ~152-row band (608 of 1920), little else sharp
        return None
    mid = (y0 + run / 2) * 4  # back to 1920-row units
    top = int(min(max(mid - 304, 0), 1920 - 608))
    return f"1080:608:0:{top}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(" ".join(cmd[:6]) + "\n" + r.stderr[-2500:])


def main():
    shots = build_shots()
    os.makedirs(os.path.join(WORK, "shots"), exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(shots, open(os.path.join(ROOT, "production/consumed-ep1-edl.json"), "w"), indent=1)
    missing = sorted({s["src"] for s in shots if not os.path.exists(s["src"])})
    if missing:
        sys.exit("missing inputs:\n  " + "\n  ".join(missing))
    only = int(sys.argv[sys.argv.index("--only") + 1]) if "--only" in sys.argv else None
    print(f"{len(shots)} shots, {sum(s['dur'] for s in shots):.2f}s, min {min(s['dur'] for s in shots):.2f}s")
    listing = []
    for i, s in enumerate(shots):
        out = os.path.join(WORK, "shots", f"{i:03d}.mp4")
        listing.append(f"file '{out}'")
        if only is not None and i != only:
            continue
        if not os.path.exists(out) or only is not None:
            run(shot_cmd(i, s, out))
        print(f"  {i:03d} {s['k']:8s} {s['t']:7.2f} {s['dur']:5.2f}  {os.path.basename(s['src'])}")
    if only is not None:
        return
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("\n".join(listing) + "\n")
    ass = os.path.join(WORK, "titles.ass")
    write_ass(ass, shots)
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", VO, "-vf", f"subtitles={ass}",
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "21",
         "-c:a", "aac", "-b:a", "192k", "-t", str(TOTAL), "-movflags", "+faststart", OUT])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
