"""Build render payloads for The Odyssey episode (one segment per script section).

Usage: python build_eh.py OUTDIR [clips.json]

TMDB stills carry the episode: a film's stills when it is named, a person's photo
when they are named, Pexels B-roll only as filler. clips.json (optional) maps a
cue prefix to footage ranges, e.g. {"In 1992, when he was fourteen": [["/x/ducks.mp4", 31.0, 4.0]]},
played in order in place of that cue's stills (file, start s, length s); ["STILL", i, len] keeps the cue's i-th still (e.g. a person photo).
"""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sents = json.load(open(os.path.join(HERE, "sent_times.json")))
tm = json.load(open(os.path.join(HERE, "tmdb-images.json")))
clips = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else {}
T = 711.927
CUTS = [0, 39.96, 118.23, 163.49, 226.11, 265.37, 309.65, 365.36, 409.67, 452.94, 503.65, 535.03, 564.24, 596.27, 656.25, T]

def img(key, i=0, poster=False):
    e = tm[key]
    if poster:
        return ("img", f"https://image.tmdb.org/t/p/w780/{e['poster']}.jpg", "fit")
    p = e["imgs"][i % len(e["imgs"])]
    portrait = key.startswith("p_")
    return ("img", f"https://image.tmdb.org/t/p/{'w780' if portrait else 'w1280'}/{p}.jpg",
            "fit" if portrait else "fill")

PX = "https://videos.pexels.com/video-files/"
def vid(path, dur):
    return ("vid", PX + path, dur)
V = dict(
    star=vid("12286525/12286525-hd_1920_1028_60fps.mp4", 26),
    nebula=vid("34075476/14452744_640_360_24fps.mp4", 59),
    books=vid("17833065/17833065-hd_1920_1080_25fps.mp4", 27),
    candle=vid("14090582/14090582-hd_1920_1080_60fps.mp4", 50),
    statue=vid("9888215/9888215-hd_1920_1080_30fps.mp4", 40),
    storm=vid("1879456/1879456-hd_1280_720_30fps.mp4", 26),
    boat=vid("19722743/19722743-hd_1920_1080_60fps.mp4", 43),
    cinema1=vid("7986777/7986777-hd_1366_720_25fps.mp4", 17.8),
    cinema2=vid("7986770/7986770-hd_1366_720_25fps.mp4", 18.6),
    phone=vid("8942967/8942967-hd_1920_1080_25fps.mp4", 10),
    couch=vid("6337007/6337007-hd_1920_1080_25fps.mp4", 16.5),
)
B = lambda k, i=0: img(k, i)
P = lambda k, i=0: img("p_" + k, i)
PO = lambda k: img(k, poster=True)
O = lambda i: img("odyssey", i)

CUES = [
 # 0 — open
 ("What if the biggest movie", [O(0), O(1)], None),
 ("Or a video game", [V["phone"]], None),
 ("Or a bestselling novel", [V["books"]], None),
 ("What if it was a story", [V["statue"]], None),
 ("Because that's exactly what Christopher", [P("nolan")], "CHRISTOPHER NOLAN"),
 ("A story first told by Homer", [O(2)], None),
 ("A story about gods", [O(3), O(4), O(5)], None),
 ("And somehow", [O(6)], None),
 ("Christopher Nolan has taken", [PO("odyssey"), O(7)], "THE ODYSSEY (2026)"),
 # 1 — the story
 ("Let's start with", [O(8)], None),
 ("The Odyssey isn't a new story", [V["statue"]], None),
 ("In fact, it's one", [V["books"]], None),
 ("The basic premise", [O(9)], None),
 ("Odysseus has fought in the Trojan War", [O(10), O(11)], None),
 ("Now he wants to go home", [O(12)], None),
 ("But getting home", [V["storm"], O(13)], None),
 ("And along the way", [O(14), O(15), O(16)], None),
 ("There's the Cyclops", [O(17)], None),
 ("There's Circe", [O(18)], None),
 ("There's the Sirens", [O(19)], None),
 ("There's Calypso", [O(20)], None),
 ("There's Poseidon", [V["storm"], O(21)], None),
 ("And back home in Ithaca", [P("hathaway"), O(22)], None),
 ("His son, Telemachus", [P("holland"), O(23)], None),
 ("So underneath", [O(24)], None),
 ("The Odyssey is actually a story about home", [O(25)], None),
 ("And that's probably", [V["statue"]], None),
 ("Because the basic idea", [O(26)], None),
 ("You can leave home", [V["boat"]], None),
 ("You can become", [O(27)], None),
 ("You can experience", [O(28)], None),
 ("But eventually", [O(29)], None),
 # 2 — Nolan and the cast
 ("And then Christopher Nolan came along", [P("nolan")], None),
 ("Nolan is one of the few", [V["cinema2"]], None),
 ("After Oppenheimer", [B("oppenheimer", 0), PO("oppenheimer")], "OPPENHEIMER (2023)"),
 ("Homer's Odyssey", [PO("odyssey")], None),
 ("And the cast immediately", [O(30)], None),
 ("Matt Damon plays Odysseus", [P("damon")], "MATT DAMON · ODYSSEUS"),
 ("Tom Holland plays", [P("holland")], "TOM HOLLAND · TELEMACHUS"),
 ("Anne Hathaway plays", [P("hathaway")], "ANNE HATHAWAY · PENELOPE"),
 ("Zendaya appears", [P("zendaya")], "ZENDAYA · ATHENA"),
 ("Robert Pattinson", [P("pattinson")], "ROBERT PATTINSON"),
 ("Charlize Theron plays", [P("theron")], "CHARLIZE THERON · CALYPSO"),
 ("And that's only part", [O(31)], None),
 ("But the cast isn't", [O(32)], None),
 ("The craziest thing", [O(33)], None),
 # 3 — IMAX
 ("Nolan didn't approach", [O(34), O(35)], None),
 ("So the film was shot entirely", [O(36)], "SHOT ENTIRELY ON IMAX 70MM FILM"),
 ("Because IMAX isn't just", [V["cinema2"]], None),
 ("The format is designed", [O(37), O(38)], None),
 ("And Nolan has spent years", [B("oppenheimer", 1), B("oppenheimer", 2)], None),
 ("But The Odyssey pushed", [O(39)], None),
 ("IMAX developed new technology", [O(0), O(1)], None),
 ("Think about what that means", [V["books"]], None),
 ("and transforming it into", [O(2)], None),
 ("That's the central contradiction", [V["statue"]], None),
 ("but it looks incredibly modern", [O(3)], None),
 # 4 — box office
 ("And audiences clearly responded", [V["cinema1"]], None),
 ("The movie opened worldwide", [O(4)], None),
 ("But the IMAX numbers", [V["cinema2"]], None),
 ("Within its first month", [O(5)], None),
 ("That tells us", [O(6)], None),
 ("They were interested in experiencing", [V["cinema1"]], None),
 ("And that's exactly what Nolan", [P("nolan"), B("oppenheimer", 3)], None),
 # 5 — watching vs going
 ("Think about the difference", [V["couch"]], None),
 ("They're not always the same", [V["cinema1"]], None),
 ("You can watch thousands", [V["couch"]], None),
 ("You can watch huge franchises", [V["phone"]], None),
 ("So if a director wants", [V["cinema2"]], None),
 ("the movie needs to feel different", [O(7)], None),
 ("And The Odyssey was designed", [O(8)], None),
 ("It's: \"You need", [PO("odyssey")], None),
 # 6 — the story itself
 ("And then there's the story itself", [O(9)], None),
 ("It contains almost every kind", [O(10), O(11), O(12), O(13)], None),
 ("Odysseus doesn't simply fight", [O(14)], None),
 ("He constantly has to make", [O(15), O(16)], None),
 ("That's why Odysseus isn't simply", [O(17)], None),
 ("And that makes the story particularly", [P("nolan")], None),
 ("Because Nolan's protagonists", [B("oppenheimer", 4)], None),
 # 7 — consequences
 ("And Odysseus might be", [O(18)], None),
 ("Imagine surviving a war", [O(19)], None),
 ("only to discover", [V["storm"]], None),
 ("Every time Odysseus gets close", [O(20), O(21), O(22), O(23)], None),
 ("And that's where the story becomes", [O(24)], None),
 ("Because Odysseus is intelligent", [P("damon"), O(25)], None),
 ("But he's also flawed", [O(26)], None),
 ("And sometimes the person", [O(27)], None),
 # 8 — the word
 ("That makes the title", [PO("odyssey")], None),
 ("The Odyssey isn't simply the destination", [V["boat"]], None),
 ("That's where the word", [V["books"]], None),
 ("And we've all had versions", [O(28)], None),
 ("Maybe not involving Cyclopes", [O(29)], None),
 ("But everyone knows", [V["couch"]], None),
 ("And then suddenly", [V["storm"]], None),
 ("That's why a story thousands", [V["statue"]], None),
 ("The technology changes", [O(30), O(31)], None),
 # 9 — mythology in pop culture
 ("And there's another fascinating", [O(32)], None),
 ("The movie isn't just bringing", [V["books"]], None),
 ("For years, mythology", [V["statue"]], None),
 ("Superhero movies borrow", [V["cinema1"]], None),
 ("Video games reinterpret", [V["phone"]], None),
 ("Young audiences discover", [V["phone"]], None),
 ("But The Odyssey is different", [O(33)], None),
 ("Nolan isn't hiding", [P("nolan")], None),
 ("He's putting it directly", [PO("odyssey")], None),
 ("And apparently", [O(34)], None),
 # 10 — cultural moment
 ("The result is a strange", [V["cinema2"]], None),
 ("A three-thousand-year-old story is competing", [V["phone"], V["couch"]], None),
 ("And it's winning people over", [O(35)], None),
 ("Storytelling.", [O(36), O(37)], None),
 ("And the question: Will he", [O(38)], None),
 ("That's storytelling stripped", [O(39)], None),
 # 11 — opposite direction
 ("And maybe that's the biggest reason", [O(0)], None),
 ("Hollywood has spent years", [V["cinema1"], V["cinema2"]], None),
 ("But Nolan went in the opposite", [P("nolan")], None),
 ("He went back to one of the oldest", [V["statue"]], None),
 ("And instead of making it smaller", [O(1), O(2)], None),
 # 12 — performed aloud
 ("That's also why the IMAX choice", [O(3)], None),
 ("Thousands of years ago", [V["candle"], V["books"]], None),
 ("And now...", [V["cinema1"]], None),
 ("you can sit inside an IMAX", [O(4), O(5)], None),
 ("That's almost poetic", [O(6)], None),
 # 13 — the test
 ("And it explains why", [O(7)], None),
 ("It's a test", [O(8)], None),
 ("Can one of the oldest", [O(9)], None),
 ("The early answer", [V["cinema2"]], None),
 ("The film became Nolan's highest-grossing", [O(10)], None),
 ("But the more interesting", [O(11)], None),
 ("Why are audiences still", [O(12), O(13)], None),
 ("Maybe because every generation", [V["phone"]], None),
 ("But the emotions aren't new", [O(14), O(15), O(16), O(17), O(18)], None),
 ("And the desire to return home", [O(19)], None),
 # 14 — close
 ("So when you watch The Odyssey", [O(20)], None),
 ("You're watching thousands of years", [O(21), O(22)], None),
 ("Homer gave us the journey", [V["statue"]], None),
 ("Nolan gives us the spectacle", [O(23)], None),
 ("And the audience brings", [O(24)], None),
 ("And perhaps that's the real reason", [O(25)], None),
 ("Because every generation finds", [O(26)], None),
 ("And in 2026", [P("nolan")], None),
 ("Christopher Nolan decided to tell it", [O(27)], None),
 ("A 3,000-year-old story", [O(28)], None),
 ("turned into a modern", [O(29)], None),
 ("Ancient Greece didn't disappear", [V["statue"]], None),
 ("It was just waiting", [O(30)], None),
 ("to make it enormous", [PO("odyssey")], None),
 ("And now the question is", [V["nebula"], V["star"]], None),
]

norm = lambda s: s.replace("’", "'")
def at(pre):
    m = [s["t"] for s in sents if norm(s["text"]).startswith(pre)]
    if not m:
        sys.exit(f"cue not found: {pre}")
    return m[0]

cue_t = sorted(((at(pre), pre, assets, label) for pre, assets, label in CUES), key=lambda c: c[0])
if clips and not all(any(c[1] == k for c in cue_t) for k in clips):
    sys.exit("clips.json has a key that matches no cue prefix: "
             + ", ".join(k for k in clips if not any(c[1] == k for c in cue_t)))
cue_t[0] = (0.0,) + cue_t[0][1:]
# snap cues to section starts so cuts land on section boundaries
for k, c in enumerate(cue_t):
    for b in CUTS[1:-1]:
        if abs(c[0] - b) < 2.0:
            cue_t[k] = (b,) + c[1:]

shots = []
for k, (t0, pre, assets, label) in enumerate(cue_t):
    t1 = cue_t[k + 1][0] if k + 1 < len(cue_t) else T
    span = t1 - t0
    if span <= 0:
        continue
    if pre in clips:
        # real footage: [[file, start, length], ...] played in order; stills fill any remainder
        t, j = t0, 0
        for f, st, ln in clips[pre]:
            if t >= t1 - 0.05:
                break
            d = min(ln, t1 - t)
            a_ = assets[int(st)] if f == "STILL" else ("clip", f, st)  # ["STILL", i, len] = this cue's i-th still
            shots.append((t, d, a_, label if j == 0 else None))
            t += d; j += 1
        if t1 - t > 0.05:
            shots.append((t, t1 - t, assets[0], None))
        continue
    n = max(1, round(span / 5.0))
    n = min(n, max(1, int(span // 2.5)))
    d = span / n
    for j in range(n):
        shots.append((t0 + j * d, d, assets[j % len(assets)], label if j == 0 else None))

KB = [({"scale": 1, "x": .5, "y": .5}, {"scale": 1.12, "x": .5, "y": .45}),
      ({"scale": 1.12, "x": .5, "y": .5}, {"scale": 1, "x": .5, "y": .5}),
      ({"scale": 1.05, "x": .4, "y": .5}, {"scale": 1.15, "x": .6, "y": .5})]
kb = itertools.cycle(KB)
vstart, segs = {}, []
LABEL = {"color": "#F2D27A", "fontSize": 40, "fontWeight": 700, "textAlign": "left", "background": "rgba(0,0,0,0.45)"}
for si in range(len(CUTS) - 1):
    a, b = CUTS[si], CUTS[si + 1]
    scenes, overlays = [], []
    for (s, d, asset, label) in shots:
        lo, hi = max(s, a), min(s + d, b)
        if hi - lo < 0.05:
            continue
        dur = round(hi - lo, 3)
        if asset[0] == "img":
            f, t = next(kb)
            sc = {"type": "image", "source": asset[1], "duration": dur, "layout": asset[2],
                  "kenBurns": {"from": f, "to": t}}
        elif asset[0] == "clip":
            sc = {"type": "video", "source": asset[1], "duration": dur,
                  "startFromSeconds": round(asset[2] + (lo - s), 2)}
        else:
            src, avail = asset[1], asset[2]
            st = vstart.get(src, 0.5)
            if st + dur > avail - 0.3:
                st = 0.3
            st = max(0, min(st, avail - dur - 0.3))
            vstart[src] = st + dur
            sc = {"type": "video", "source": src, "duration": dur, "startFromSeconds": round(st, 2)}
        scenes.append(sc)
        if label and lo == s:
            overlays.append({"kind": "text", "text": label, "start": round(lo - a + 0.3, 2),
                             "duration": min(4.0, round(dur - 0.4, 2)),
                             "position": {"x": 0.05, "y": 0.84, "width": 0.62, "height": 0.08}, "style": LABEL})
    diff = round((b - a) - sum(x["duration"] for x in scenes), 3)
    scenes[-1]["duration"] = round(scenes[-1]["duration"] + diff, 3)
    segs.append({"scenes": scenes, "overlays": overlays})

def add_overlay(t, ov):
    for si in range(len(CUTS) - 1):
        if CUTS[si] <= t < CUTS[si + 1]:
            ov["start"] = round(max(0, t - CUTS[si]), 2)
            ov["duration"] = round(min(ov["duration"], CUTS[si + 1] - CUTS[si] - ov["start"] - 0.1), 2)
            segs[si]["overlays"].append(ov)
            return
title = {"color": "#F2D27A", "fontSize": 96, "fontWeight": 800, "textAlign": "center"}
sub = {"color": "#FFFFFF", "fontSize": 40, "textAlign": "center"}
stat = {"color": "#F2D27A", "fontSize": 64, "fontWeight": 800, "textAlign": "center", "background": "rgba(0,0,0,0.45)"}
t = at("Let's start with")
add_overlay(t - 2.5, {"kind": "text", "text": "THE ODYSSEY", "duration": 4.5,
                      "position": {"x": 0.1, "y": 0.38, "width": 0.8, "height": 0.16}, "style": title})
add_overlay(t - 2.2, {"kind": "text", "text": "WHY EVERYONE IS TALKING ABOUT AN ANCIENT STORY", "duration": 4.2,
                      "position": {"x": 0.1, "y": 0.56, "width": 0.8, "height": 0.07}, "style": sub})
add_overlay(at("The movie opened worldwide") + 0.5, {"kind": "text", "text": "NOLAN'S BIGGEST OPENING EVER", "duration": 5,
            "position": {"x": 0.15, "y": 0.40, "width": 0.7, "height": 0.12}, "style": stat})
add_overlay(at("Within its first month") + 0.5, {"kind": "text", "text": "$289M IN IMAX · AN IMAX RECORD", "duration": 6,
            "position": {"x": 0.12, "y": 0.40, "width": 0.76, "height": 0.12}, "style": stat})
add_overlay(at("The film became Nolan's highest-grossing") + 0.5, {"kind": "text", "text": "$1 BILLION+ WORLDWIDE", "duration": 5,
            "position": {"x": 0.15, "y": 0.40, "width": 0.7, "height": 0.12}, "style": stat})
add_overlay(at("He's putting it directly") + 0.8, {"kind": "text", "text": "THE ODYSSEY", "duration": 3.5,
            "position": {"x": 0.1, "y": 0.40, "width": 0.8, "height": 0.16}, "style": title})
for pre, txt in [("Let's start with", "A 3,000-YEAR-OLD STORY"), ("And then Christopher Nolan came along", "ENTER NOLAN"),
                 ("Nolan didn't approach", "SHOT ON IMAX"), ("And audiences clearly responded", "THE BOX OFFICE"),
                 ("Think about the difference", "WATCHING VS. EXPERIENCING"), ("And then there's the story itself", "WHY THE STORY WORKS"),
                 ("And there's another fascinating", "MYTHOLOGY IS BACK"), ("And it explains why", "THE TEST")]:
    add_overlay(at(pre) + 0.2, {"kind": "text", "text": txt, "duration": 3.2,
                                "position": {"x": 0.05, "y": 0.06, "width": 0.5, "height": 0.07},
                                "style": {"color": "#FFFFFF", "fontSize": 34, "fontWeight": 700, "textAlign": "left",
                                          "background": "rgba(0,0,0,0.45)"}})
t = at("And now the question is")
add_overlay(t, {"kind": "text", "text": "WHAT'S THE NEXT ANCIENT EPIC?", "duration": 6, "position": {"x": 0.1, "y": 0.38, "width": 0.8, "height": 0.12}, "style": {**title, "fontSize": 72}})
add_overlay(t + 0.5, {"kind": "text", "text": "TELL US IN THE COMMENTS · SUBSCRIBE", "duration": 6,
                      "position": {"x": 0.2, "y": 0.52, "width": 0.6, "height": 0.07}, "style": sub})
credit = "Footage: Universal Pictures, IMAX, The Daily Show · Stills: TMDB · Stock: Pexels" if clips else "Stills: TMDB · Stock: Pexels"
add_overlay(1.0, {"kind": "text", "text": credit, "duration": 5,
                  "position": {"x": 0.40 if clips else 0.70, "y": 0.93, "width": 0.58 if clips else 0.28, "height": 0.05},
                  "style": {"color": "#DDDDDD", "fontSize": 22, "textAlign": "right"}})

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    if f.startswith("compose-seg"):
        os.remove(os.path.join(out, f))
nimg = nvid = 0
for i, sg in enumerate(segs, 1):
    nimg += sum(x["type"] == "image" for x in sg["scenes"]); nvid += sum(x["type"] == "video" for x in sg["scenes"])
    json.dump(sg, open(os.path.join(out, f"compose-seg{i}.json"), "w"), indent=1)
print(f"{len(segs)} segments, {nimg} still shots, {nvid} video shots, total {sum(sum(x['duration'] for x in s['scenes']) for s in segs):.2f}s")
