"""Build vidiq_compose payloads for Golden Four Ep5 from aligned sentence times.

Inputs: sent_times.json (script sentences + start times aligned to the voiceover),
tmdb-images.json, interview clip URLs (signed; pass via clips.json).
Output: compose-seg{1..5}.json
"""
import json, itertools, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sents = json.load(open(sys.argv[1]))
clips = json.load(open(sys.argv[2])) if sys.argv[2] != "-" else {}
tm = json.load(open(os.path.join(HERE, "tmdb-images.json")))
# re-recorded voiceover (v1.1 script); cuts sit on section-break pauses
T = 873.639
CUTS = [0, 202.03, 342.01, 568.14, 804.03, T]
VO = ("https://raw.githubusercontent.com/r21147131-source/StardustStory/"
      "claude/eager-lamport-84svgu/public/golden-four-ep5-voiceover.mp3")

def img(key, i=0, poster=False):
    e = tm[key]
    if poster:
        return ("img", f"https://image.tmdb.org/t/p/w780/{e['poster']}.jpg", "fit")
    p = e["imgs"][i % len(e["imgs"])]
    portrait = key.startswith("p_")
    size = "w780" if portrait else "w1280"
    return ("img", f"https://image.tmdb.org/t/p/{size}/{p}.jpg", "fit" if portrait else "fill")

PX = "https://videos.pexels.com/video-files/"
def vid(path, dur):
    return ("vid", PX + path, dur)
V = dict(
    star=vid("12286525/12286525-hd_1920_1028_60fps.mp4", 26),
    nebula=vid("34075476/14452744_640_360_24fps.mp4", 59),
    gold=vid("35286672/14948778_640_360_24fps.mp4", 120),
    glitter=vid("5561380/5561380-hd_1280_720_50fps.mp4", 36),
    runner=vid("8456204/8456204-hd_1280_720_25fps.mp4", 14),
    door=vid("10639202/10639202-hd_2048_1080_25fps.mp4", 17),
    sculpt=vid("6719220/6719220-hd_1920_1080_25fps.mp4", 16),
    sculpt2=vid("6719632/6719632-hd_1920_1080_25fps.mp4", 13),
    dinner=vid("34344023/14549708_640_360_30fps.mp4", 24),
    books=vid("17833065/17833065-hd_1920_1080_25fps.mp4", 27),
    forge=vid("5846589/5846589-hd_1280_720_25fps.mp4", 18),
    forge2=vid("5846301/5846301-hd_1280_720_25fps.mp4", 17),
    chess=vid("6599643/6599643-hd_1920_1080_25fps.mp4", 21),
    chess2=vid("10586237/10586237-hd_1920_1080_24fps.mp4", 18),
    smoke=vid("7122113/7122113-hd_1920_1080_30fps.mp4", 23),
    gsmoke=vid("10004372/10004372-hd_2048_1080_30fps.mp4", 59),
    tools=vid("7541835/7541835-hd_1366_720_25fps.mp4", 16),
    chairs=vid("2996079/2996079-hd_1920_1080_24fps.mp4", 65),
    chalk=vid("3196425/3196425-hd_1280_720_25fps.mp4", 20),
    bonfire=vid("4777136/4777136-hd_1906_1080_24fps.mp4", 30),
    bonfire2=vid("6900893/6900893-hd_1280_720_30fps.mp4", 20),
    match=vid("35888101/15221261_640_360_25fps.mp4", 19),
    candle=vid("14090582/14090582-hd_1920_1080_60fps.mp4", 50),
    hospital=vid("3192916/3192916-hd_1920_1080_24fps.mp4", 21),
    mother=vid("7509030/7509030-hd_2048_1080_25fps.mp4", 22),
    crib=vid("7508465/7508465-hd_1366_720_25fps.mp4", 16),
    prism=vid("30879511/13203416_640_360_30fps.mp4", 13),
    prism2=vid("6244085/6244085-hd_1280_720_25fps.mp4", 11),
    quarry=vid("31100162/13288573_640_360_60fps.mp4", 18),
    statue=vid("9888215/9888215-hd_1920_1080_30fps.mp4", 40),
    bag=vid("6296509/6296509-hd_1920_1080_25fps.mp4", 18),
    kitchen=vid("4253723/4253723-hd_1366_720_50fps.mp4", 60),
    mirror=vid("17552070/17552070-hd_1920_1080_24fps.mp4", 119),
    reflect=vid("853955/853955-hd_1280_720_60fps.mp4", 13),
    cave=vid("7043842/7043842-hd_1920_1080_30fps.mp4", 32),
    burst=vid("36042949/15285406_640_360_30fps.mp4", 10),
    burst2=vid("35782164/15170196_640_360_24fps.mp4", 120),
)
FS = lambda i: img("first_steps", i)
P = lambda who, i=0: img("p_" + who, i)
B = lambda key, i=0: img(key, i)
DD = img("doomsday"); DDP = img("doomsday", poster=True)

# (sentence prefix, assets, optional lower-third label) — prefixes from golden-four-ep5-recording-script.txt
CUES = [
 ("Welcome back", [V["star"], V["nebula"]], None),
 ("You watched Pedro", [P("pascal", 0), B("last_of_us")], None),
 ("You traced Joseph", [B("stranger_things"), P("quinn", 0)], None),
 ("You followed Vanessa", [P("kirby", 0), B("the_crown")], None),
 ("And last week", [B("iron_man", 0), P("rdj", 0), DD], None),
 ("And standing beside them", [P("ebon", 0), B("the_bear")], None),
 ("This is Episode Five", [V["gold"], DDP, V["glitter"]], None),
 ("One note before", [V["books"], DDP, V["candle"]], None),
 ("Before Doom arrives", [FS(0), FS(1), FS(2), FS(3)], None),
 ("Pedro Pascal spent", [P("pascal", 1), B("narcos", 0), B("got", 0), B("last_of_us"), FS(4), P("pascal", 2)], None),
 ("Joseph Quinn came", [V["runner"], B("stranger_things"), B("quiet_place_day_one"), B("gladiator_ii"), P("quinn", 1), FS(5)], None),
 ("Vanessa Kirby was never", [V["door"], B("the_crown"), B("mi_fallout"), P("kirby", 1), FS(6), P("kirby", 2)], None),
 ("And Ebon Moss-Bachrach", [V["sculpt"], B("the_bear"), P("ebon", 1), FS(7)], None),
 ("Together, they built", [FS(8), V["dinner"], FS(9)], None),
 ("But every family", [V["gsmoke"]], None),
 ("Doctor Doom has haunted", [V["books"], V["forge"], V["smoke"], V["chess"]], None),
 ("Victor von Doom believes", [DD, V["gsmoke"], V["forge2"]], None),
 ("When Marvel revealed", [P("rdj", 1), DDP], None),
 ("Villainy is not", [V["smoke"], V["chess2"]], None),
 ("That is why the casting lands", [B("iron_man", 1), B("iron_man", 2), B("endgame", 0), P("rdj", 2)], None),
 ("In the comics, Doom", [FS(10), FS(11), FS(12), FS(13), V["chess"]], None),
 ("To Doom, the Fantastic Four", [FS(14), V["forge"]], None),
 ("Tony Stark's story", [P("rdj", 3), B("iron_man", 3), B("endgame", 1)], None),
 ("Tony Stark chose his", [B("endgame", 2), V["tools"]], None),
 ("Doctor Doom rejected", [V["gsmoke"]], None),
 ("We do not know how", [V["chairs"], DD, V["chalk"], FS(15)], None),
 ("And it is exactly the kind", [P("pascal", 3), B("last_of_us"), B("narcos", 1), B("got", 1), FS(16), P("pascal", 4)], None),
 ("Johnny Storm's collision", [V["match"], V["bonfire"]], None),
 ("Joseph Quinn has spent", [P("quinn", 2)], None),
 ("Eddie Munson was not", [B("stranger_things")], "STRANGER THINGS (2022)"),
 ("In A Quiet Place", [B("quiet_place_day_one")], "A QUIET PLACE: DAY ONE (2024)"),
 ("In Gladiator II", [B("gladiator_ii")], "GLADIATOR II (2024)"),
 ("On paper, Johnny", [V["bonfire2"], FS(17), V["candle"]], None),
 ("That is what Joseph Quinn brings", [P("quinn", 3), FS(18)], None),
 ("At the heart of The Fantastic Four", [V["mother"], V["crib"], FS(19)], None),
 ("Vanessa Kirby's career", [P("kirby", 3)], None),
 ("The Crown made her", [B("the_crown")], "THE CROWN (2016)"),
 ("Instead, she played", [B("mi_fallout"), P("kirby", 1)], "MISSION: IMPOSSIBLE – FALLOUT (2018)"),
 ("In the comics, Sue Storm", [FS(20), V["prism"], FS(21), V["hospital"], V["prism2"], FS(22), P("kirby", 0)], None),
 ("Ben Grimm may be", [V["quarry"], V["statue"], V["sculpt2"], FS(23), FS(24)], None),
 ("Ebon Moss-Bachrach knows", [P("ebon", 2), B("punisher"), B("andor"), B("the_bear"), V["kitchen"], P("ebon", 3)], None),
 ("Imagine Doom meeting", [V["bag"], FS(25), V["statue"], FS(26), V["quarry"]], None),
 ("And then there is the theory", [P("rdj", 0), DD, V["mirror"], V["cave"], B("iron_man", 4), B("endgame", 3), V["reflect"], DDP], None),
 ("Reed, the genius", [P("pascal", 0)], None),
 ("Johnny, the fire", [P("quinn", 0)], None),
 ("Sue, the mother", [P("kirby", 1)], None),
 ("Ben, the man", [P("ebon", 3)], None),
 ("To that Doom", [V["mirror"], DD], None),
 ("Whatever Doomsday turns out", [FS(27), FS(28)], None),
 ("Robert Downey Jr. gets", [P("rdj", 1), DD], None),
 ("Pedro Pascal gets", [P("pascal", 1)], None),
 ("Joseph Quinn gets", [P("quinn", 2)], None),
 ("Vanessa Kirby gets", [P("kirby", 2)], None),
 ("And Ebon Moss-Bachrach gets", [P("ebon", 0)], None),
 ("The Fantastic Four are not heroes", [FS(29), FS(30), FS(31)], None),
 ("The Golden Four is complete", [V["nebula"], FS(32)], None),
 ("Pedro Pascal taught", [P("pascal", 2)], None),
 ("Joseph Quinn showed", [P("quinn", 1)], None),
 ("Vanessa Kirby showed", [P("kirby", 3)], None),
 ("Ebon Moss-Bachrach reminded", [P("ebon", 1)], None),
 ("And Robert Downey Jr. reminded", [P("rdj", 2)], None),
 ("On December eighteenth, we find", [DDP, V["burst"]], None),
 ("Subscribe, share", [V["burst2"], V["star"]], None),
]

norm = lambda s: s.replace("’", "'")
cue_t = []
for pre, assets, label in CUES:
    m = [s for s in sents if norm(s["text"]).startswith(pre)]
    if not m:
        sys.exit(f"cue not found: {pre}")
    cue_t.append((m[0]["t"], assets, label))
cue_t.sort(key=lambda c: c[0])
cue_t[0] = (0.0,) + cue_t[0][1:]

# expand cues into shots
shots = []  # (start, dur, asset, label)
for k, (t0, assets, label) in enumerate(cue_t):
    t1 = cue_t[k + 1][0] if k + 1 < len(cue_t) else T
    span = t1 - t0
    if span <= 0:
        continue
    n = max(1, round(span / 6.0))
    n = min(n, max(1, int(span // 2.5)))
    d = span / n
    for j in range(n):
        shots.append((t0 + j * d, d, assets[j % len(assets)], label if j == 0 else None))

# cut into segments
KB = [({"scale": 1, "x": .5, "y": .5}, {"scale": 1.12, "x": .5, "y": .45}),
      ({"scale": 1.12, "x": .5, "y": .5}, {"scale": 1, "x": .5, "y": .5}),
      ({"scale": 1.05, "x": .4, "y": .5}, {"scale": 1.15, "x": .6, "y": .5})]
kb = itertools.cycle(KB)
vstart = {}
segs = []
for si in range(5):
    a, b = CUTS[si], CUTS[si + 1]
    scenes, overlays = [], []
    for (s, d, asset, label) in shots:
        e = s + d
        lo, hi = max(s, a), min(e, b)
        if hi - lo < 0.05:
            continue
        dur = round(hi - lo, 3)
        if asset[0] == "img":
            f, t = next(kb)
            sc = {"type": "image", "source": asset[1], "duration": dur, "layout": asset[2],
                  "kenBurns": {"from": f, "to": t}}
        else:
            src, avail = asset[1], asset[2]
            st = vstart.get(src, 0.5)
            if st + dur > avail - 0.3:
                st = 0.3
            st = max(0, min(st, avail - dur - 0.3))
            vstart[src] = st + dur
            sc = {"type": "video", "source": src, "duration": dur, "startFromSeconds": round(st, 2)}
        if lo == s:
            sc["transitionIn"] = {"kind": "fade", "duration": 0.35}
        scenes.append(sc)
        if label and lo == s:
            overlays.append({"kind": "text", "text": label, "start": round(lo - a + 0.3, 2),
                             "duration": min(4.0, round(dur - 0.4, 2)),
                             "position": {"x": 0.05, "y": 0.84, "width": 0.6, "height": 0.08},
                             "style": {"color": "#F2D27A", "fontSize": 40, "fontWeight": 700,
                                       "textAlign": "left", "background": "rgba(0,0,0,0.45)"}})
    # fix rounding so scene total == segment length
    diff = round((b - a) - sum(x["duration"] for x in scenes), 3)
    scenes[-1]["duration"] = round(scenes[-1]["duration"] + diff, 3)
    segs.append({"format": "landscape", "scenes": scenes, "overlays": overlays,
                 "voiceover": {"audioUrl": VO, "trimStartSeconds": a, "durationSeconds": round(b - a, 3)}})

def at(pre):
    return next(s["t"] for s in sents if norm(s["text"]).startswith(pre))
def add_overlay(t, ov):
    for si in range(5):
        if CUTS[si] <= t < CUTS[si + 1]:
            ov["start"] = round(max(0, t - CUTS[si]), 2)
            end = CUTS[si + 1] - CUTS[si]
            ov["duration"] = round(min(ov["duration"], end - ov["start"] - 0.1), 2)
            segs[si]["overlays"].append(ov)
            return
INSET = {"x": 0.60, "y": 0.06, "width": 0.36, "height": 0.2025}
CAP = {"x": 0.60, "y": 0.265, "width": 0.36, "height": 0.05}
capstyle = {"color": "#FFFFFF", "fontSize": 26, "background": "rgba(0,0,0,0.55)", "textAlign": "center"}
title = {"color": "#F2D27A", "fontSize": 84, "fontWeight": 800, "textAlign": "center"}
add_overlay(at("This is Episode Five"), {"kind": "text", "text": "EPISODE 5 · THE COLLISION", "duration": 5.5,
            "position": {"x": 0.1, "y": 0.40, "width": 0.8, "height": 0.16}, "style": title})
add_overlay(at("This is Episode Five") + 0.2, {"kind": "text", "text": "THE GOLDEN FOUR", "duration": 5.3,
            "position": {"x": 0.25, "y": 0.57, "width": 0.5, "height": 0.07},
            "style": {"color": "#FFFFFF", "fontSize": 40, "textAlign": "center"}})
for pre, clip, st, d, cap in [
        ("Together, they built", "imax", 104, 12, "THE CAST · IMAX INTERVIEW (2025)"),
        ("When Marvel revealed", "rdj", 26, 14, "SAN DIEGO COMIC-CON · HALL H (2024)"),
        ("And it is exactly the kind", "pascal", 10, 12, "FIRST STEPS WORLD PREMIERE (2025)")]:
    if clip not in clips:
        continue
    t = at(pre) + 0.5
    add_overlay(t, {"kind": "video", "src": clips[clip], "startFromSeconds": st, "duration": d, "position": INSET})
    add_overlay(t, {"kind": "text", "text": cap, "duration": d, "position": CAP, "style": capstyle})
t = at("On December eighteenth, we find")
add_overlay(t, {"kind": "text", "text": "AVENGERS: DOOMSDAY · DEC 18, 2026", "duration": 12,
                "position": {"x": 0.1, "y": 0.36, "width": 0.8, "height": 0.1}, "style": title})
add_overlay(t + 0.5, {"kind": "text", "text": "SUBSCRIBE · STARDUST STORY", "duration": 12,
                      "position": {"x": 0.25, "y": 0.50, "width": 0.5, "height": 0.07},
                      "style": {"color": "#FFFFFF", "fontSize": 44, "textAlign": "center"}})
add_overlay(1.0, {"kind": "text", "text": "Stills: TMDB · Stock: Pexels", "duration": 5,
                  "position": {"x": 0.70, "y": 0.93, "width": 0.28, "height": 0.05},
                  "style": {"color": "#DDDDDD", "fontSize": 22, "textAlign": "right"}})

out = sys.argv[3]
for i, sg in enumerate(segs, 1):
    tot = sum(x["duration"] for x in sg["scenes"])
    print(f"seg{i}: {len(sg['scenes'])} scenes, {len(sg['overlays'])} overlays, {tot:.2f}s")
    assert len(sg["scenes"]) <= 50 and len(sg["overlays"]) <= 50 and tot <= 240
    json.dump(sg, open(os.path.join(out, f"compose-seg{i}.json"), "w"), indent=1)
