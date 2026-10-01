"""Build render payloads for the Elden Henson episode (one segment per script section).

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
T = 845.904
CUTS = [0, 111.977, 196.601, 280.296, 393.573, 456.37, 535.932, 624.411, 731.976, T]

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
    glitter=vid("5561380/5561380-hd_1280_720_50fps.mp4", 36),
    door=vid("10639202/10639202-hd_2048_1080_25fps.mp4", 17),
    books=vid("17833065/17833065-hd_1920_1080_25fps.mp4", 27),
    smoke=vid("7122113/7122113-hd_1920_1080_30fps.mp4", 23),
    gsmoke=vid("10004372/10004372-hd_2048_1080_30fps.mp4", 59),
    chairs=vid("2996079/2996079-hd_1920_1080_24fps.mp4", 65),
    chalk=vid("3196425/3196425-hd_1280_720_25fps.mp4", 20),
    candle=vid("14090582/14090582-hd_1920_1080_60fps.mp4", 50),
)
B = lambda k, i=0: img(k, i)
P = lambda k, i=0: img("p_" + k, i)
PO = lambda k: img(k, poster=True)

CUES = [
 # Hook
 ("The show had been gone", [B("daredevil", 0), V["gsmoke"]], None),
 ("When Netflix cancelled", [B("daredevil", 1), B("daredevil", 2)], None),
 ("And the characters inside", [B("daredevil", 3), P("cox"), P("woll"), B("daredevil", 4)], None),
 ("Fans spent years", [V["chairs"]], None),
 ("Then Disney Plus answered", [PO("born_again")], None),
 ("Daredevil: Born Again launched", [B("born_again", 0)], "DAREDEVIL: BORN AGAIN (2025)"),
 ("Charlie Cox was back", [P("cox")], "CHARLIE COX · MATT MURDOCK"),
 ("Deborah Ann Woll returned", [P("woll")], "DEBORAH ANN WOLL · KAREN PAGE"),
 ("And Elden Henson stepped back", [P("elden", 0), B("daredevil", 6), B("born_again", 1)], "ELDEN HENSON · FOGGY NELSON"),
 ("The wait was over", [B("born_again", 2)], None),
 ("Foggy Nelson did not survive", [B("born_again", 3)], None),
 ("Before the first hour", [P("bethel"), B("born_again", 4)], "WILSON BETHEL · BULLSEYE"),
 ("Henson watched the character", [B("daredevil", 7), B("defenders", 0), B("daredevil", 8)], None),
 ("He showed up at fan conventions", [P("elden", 1)], None),
 ("But the math", [V["candle"]], None),
 ("Elden Henson had been a working actor", [P("elden", 2)], None),
 ("He had been waiting", [V["door"]], None),
 ("And the moment the industry", [B("born_again", 5)], None),
 ("This is how that pattern", [B("mighty_ducks", 0), V["star"]], None),
 ("Because some careers", [V["nebula"]], None),
 # 2 — The kid from Maryland
 ("Elden Ryan Ratliff was born", [P("elden", 3), V["books"]], None),
 ("The family moved to Burbank", [V["glitter"]], None),
 ("By age six", [V["chalk"]], None),
 ("Most people spend", [V["candle"]], None),
 ("He appeared in a 1981", [P("lumet")], "SIDNEY LUMET"),
 ("He appeared on the CBS", [V["chairs"]], None),
 ("He guest-starred on Amazing", [V["smoke"]], None),
 ("He played a child role", [V["books"]], None),
 ("He had a role in Turner", [B("turner_hooch", 0), B("turner_hooch", 1)], "TURNER & HOOCH (1989)"),
 ("None of these were the break", [B("turner_hooch", 2)], None),
 ("He had been in the industry for a decade", [P("elden", 4)], None),
 # 3 — Fulton Reed
 ("In 1992, when he was fourteen", [B("mighty_ducks", 1), PO("mighty_ducks")], "THE MIGHTY DUCKS (1992)"),
 ("Disney was making", [B("mighty_ducks", 2), P("estevez"), B("mighty_ducks", 3)], None),
 ("The Mighty Ducks needed", [B("mighty_ducks", 4)], None),
 ("Fulton Reed was that", [B("mighty_ducks", 5), B("mighty_ducks", 6)], "FULTON REED"),
 ("The Mighty Ducks was a hit", [B("mighty_ducks", 7)], None),
 ("A sequel, D2", [B("d2", 0), B("d2", 1)], "D2: THE MIGHTY DUCKS (1994)"),
 ("D3 came in 1996", [B("d3", 0), B("d3", 1)], "D3: THE MIGHTY DUCKS (1996)"),
 ("Henson appeared in all three", [B("d2", 3), B("d3", 2), B("d2", 4)], None),
 ("He briefly attended", [V["books"], V["chalk"]], None),
 ("He had been a franchise player", [B("d3", 3), B("d2", 5)], None),
 # 4 — The long middle
 ("What came after", [V["chairs"]], None),
 ("After the Mighty Ducks trilogy", [B("d3", 4), V["door"]], None),
 ("He worked consistently", [B("d2", 6)], None),
 ("In 1998 he appeared in The Mighty", [B("the_mighty", 0), B("the_mighty", 1), PO("the_mighty")], "THE MIGHTY (1998)"),
 ("Then She's All That", [B("shes_all_that", 0), B("shes_all_that", 1), B("shes_all_that", 2)], "SHE'S ALL THAT (1999)"),
 ("Idle Hands", [B("idle_hands", 0), B("idle_hands", 1)], "IDLE HANDS (1999)"),
 ("The Battle of Shaker", [B("shaker_heights", 0), P("labeouf"), B("shaker_heights", 1)], "THE BATTLE OF SHAKER HEIGHTS (2003)"),
 ("The Butterfly Effect", [B("butterfly_effect", 0), B("butterfly_effect", 1)], "THE BUTTERFLY EFFECT (2004)"),
 ("Lords of Dogtown", [B("lords_of_dogtown", 0), B("lords_of_dogtown", 1)], "LORDS OF DOGTOWN (2005)"),
 ("Television guest spots", [V["smoke"], V["chairs"]], None),
 ("Henson was aware", [P("elden", 5)], None),
 ("He said in interviews", [P("elden", 6)], None),
 ("The industry had a clear category", [B("shes_all_that", 3), B("butterfly_effect", 3), B("idle_hands", 2)], None),
 ("For fifteen years", [B("lords_of_dogtown", 2), B("the_mighty", 3)], None),
 # 5 — Pollux
 ("In 2014, a second franchise", [B("mockingjay1", 0), PO("mockingjay1")], "THE HUNGER GAMES: MOCKINGJAY – PART 1 (2014)"),
 ("The Hunger Games had become", [B("mockingjay1", 1), B("mockingjay1", 2), B("mockingjay1", 3)], None),
 ("It was a supporting role", [B("mockingjay1", 4), B("mockingjay1", 5)], None),
 ("Henson appeared in Mockingjay", [B("mockingjay2", 0), PO("mockingjay2"), B("mockingjay2", 1)], "MOCKINGJAY – PART 2 (2015)"),
 ("His face was on the screen", [B("mockingjay2", 2), B("mockingjay2", 3)], None),
 ("He took the job", [B("mockingjay1", 6), B("mockingjay2", 4)], None),
 ("The difference between", [V["candle"]], None),
 # 6 — Foggy Nelson
 ("In 2015, Netflix launched", [PO("daredevil"), B("daredevil", 9)], "DAREDEVIL (2015–2018)"),
 ("Franklin Foggy Nelson", [B("daredevil", 10), B("daredevil", 11), B("daredevil", 12)], None),
 ("He was also funny", [B("daredevil", 13), P("elden", 0)], None),
 ("He built it", [B("daredevil", 14), B("daredevil", 15), B("daredevil", 16)], None),
 ("He reprised the role", [PO("defenders"), B("defenders", 1), B("defenders", 2)], "THE DEFENDERS (2017)"),
 ("He became, quietly", [B("defenders", 3), B("daredevil", 17)], None),
 ("For three years", [B("daredevil", 18), B("daredevil", 19)], None),
 # 7 — The cancellation
 ("On November 29, 2018", [V["gsmoke"], B("daredevil", 0)], None),
 ("The show, along with", [B("defenders", 4), V["chairs"]], None),
 ("For years, nobody knew", [B("daredevil", 2)], None),
 ("Henson had spent three years", [P("elden", 1)], None),
 ("He kept working", [V["door"]], None),
 ("Then in 2023, Martin Scorsese", [P("scorsese"), PO("killers")], "KILLERS OF THE FLOWER MOON (2023)"),
 ("The film was one of", [P("dicaprio"), P("deniro"), B("killers", 0), B("killers", 1)], None),
 ("Henson played Duke Burkhart", [B("killers", 2), B("killers", 3), B("killers", 4)], None),
 ("In a film three and a half", [B("killers", 5), B("killers", 6)], None),
 ("The gap between", [B("killers", 7)], None),
 # 8 — Born Again
 ("Then came the reversal", [PO("born_again"), B("born_again", 6)], None),
 ("Initially, the reports", [P("woll"), P("elden", 2)], None),
 ("Fan outrage", [V["smoke"]], None),
 ("When the dust settled", [B("born_again", 7), B("born_again", 8)], None),
 ("Set photos", [B("born_again", 9)], None),
 ("Daredevil: Born Again premiered", [B("born_again", 10), B("born_again", 11)], "DAREDEVIL: BORN AGAIN · \"HEAVEN'S HALF HOUR\""),
 ("Within that hour", [P("bethel"), B("born_again", 0)], None),
 ("Fans watched his funeral", [V["candle"]], None),
 ("The showrunner", [B("born_again", 1), B("born_again", 2)], None),
 ("Foggy Nelson had been cancelled twice", [B("daredevil", 3), B("born_again", 3)], None),
 # 9 — Still coming back
 ("Here is where the story", [V["star"]], None),
 ("Following Foggy's death", [P("elden", 3)], None),
 ("Then Marvel TV boss", [B("born_again", 4)], None),
 ("The character died", [B("born_again", 5), B("daredevil", 4)], None),
 ("Season two of Born Again", [PO("born_again"), P("elden", 4)], None),
 ("He was joking", [P("elden", 5)], None),
 ("The man has spent", [B("mighty_ducks", 0), B("d2", 0), B("mockingjay1", 0), B("daredevil", 5), B("killers", 0), B("born_again", 6)], None),
 ("He is still here", [P("elden", 0)], None),
 ("Some careers do not burn", [V["nebula"], V["star"]], None),
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
t = at("Because some careers")
add_overlay(t, {"kind": "text", "text": "ELDEN HENSON", "duration": 5.5,
                "position": {"x": 0.1, "y": 0.38, "width": 0.8, "height": 0.16}, "style": title})
add_overlay(t + 0.3, {"kind": "text", "text": "THE DEFENDERS · WHERE ARE THEY NOW", "duration": 5.2,
                      "position": {"x": 0.15, "y": 0.56, "width": 0.7, "height": 0.07}, "style": sub})
for pre, txt in [("Elden Ryan Ratliff was born", "THE KID FROM MARYLAND"), ("In 1992, when he was fourteen", "FULTON REED"),
                 ("What came after", "THE LONG MIDDLE"), ("In 2014, a second franchise", "POLLUX"),
                 ("In 2015, Netflix launched", "FOGGY NELSON"), ("On November 29, 2018", "THE CANCELLATION"),
                 ("Then came the reversal", "BORN AGAIN"), ("Here is where the story", "STILL COMING BACK")]:
    add_overlay(at(pre) + 0.2, {"kind": "text", "text": txt, "duration": 3.2,
                                "position": {"x": 0.05, "y": 0.06, "width": 0.5, "height": 0.07},
                                "style": {"color": "#FFFFFF", "fontSize": 34, "fontWeight": 700, "textAlign": "left",
                                          "background": "rgba(0,0,0,0.45)"}})
t = at("Some careers just keep burning")
add_overlay(t, {"kind": "text", "text": "ELDEN HENSON", "duration": 8, "position": {"x": 0.1, "y": 0.38, "width": 0.8, "height": 0.14}, "style": title})
add_overlay(t + 0.5, {"kind": "text", "text": "SUBSCRIBE · STARDUST STORY", "duration": 8,
                      "position": {"x": 0.25, "y": 0.54, "width": 0.5, "height": 0.07}, "style": sub})
add_overlay(1.0, {"kind": "text", "text": "Stills: TMDB · Stock: Pexels", "duration": 5,
                  "position": {"x": 0.70, "y": 0.93, "width": 0.28, "height": 0.05},
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
