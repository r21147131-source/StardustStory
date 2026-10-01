"""Build render payloads for the Resident Evil (2026) episode.

Usage: python build_re.py OUTDIR [CLIPDIR]

Each cue is (sentence prefix, tokens, label). Its time span runs to the next cue and is
cut into ~3.2s footage shots (or ~5s stills) cycling through its tokens:
  pool name ("film", "re2", ...)  footage picks from picks.json, rotating through the pool
  "S:key" a TMDB still of key (rotating), "P:name" a person photo, "PO:key" a poster,
  "V:name" Pexels stock.
Without CLIPDIR (or for a pool with no picks) footage falls back to stills.
"""
import itertools, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sents = json.load(open(os.path.join(HERE, "sent_times.json")))
tm = json.load(open(os.path.join(HERE, "tmdb-images.json")))
clipdir = sys.argv[2] if len(sys.argv) > 2 else None
picks = json.load(open(os.path.join(HERE, "picks.json"))) if clipdir else {}
T = 886.979
SHOT, STILL = 3.2, 5.0

PX = "https://videos.pexels.com/video-files/"
V = dict(cinema1=(PX + "7986777/7986777-hd_1366_720_25fps.mp4", 17.8),
         cinema2=(PX + "7986770/7986770-hd_1366_720_25fps.mp4", 18.6))
FALLBACK = {"film": "re2026", "feat": "re2026", "cregger": "re2026", "old": "re2002", "raccoon": "re2002",
            "barb": "barbarian", "weap": "weapons"}  # game pools fall back to re2026 too

CUES = [
 # 0 — cold open
 ("For more than twenty years", ["old"], None),
 ("Hollywood has been trying", ["old"], None),
 ("How do you turn a video game", ["games"], None),
 ("And for more than twenty years", ["old"], None),
 ("\"Apparently, not like that.\"", ["old"], None),
 ("But something very strange", ["film"], None),
 ("A new Resident Evil movie came out", ["film"], "RESIDENT EVIL (2026)"),
 ("And instead of simply adapting", ["games"], None),
 ("director Zach Cregger did", ["P:cregger"], "ZACH CREGGER · DIRECTOR"),
 ("He tried to make the audience", ["film", "games"], None),
 ("And that difference might", ["film"], None),
 # 1 — the game
 ("Let's rewind.", ["re1"], None),
 ("Resident Evil has been around since 1996", ["re1"], "RESIDENT EVIL (1996)"),
 ("The original game helped", ["re1"], None),
 ("But the concept was", ["re2"], None),
 ("You are trapped", ["re2"], None),
 ("You have to explore", ["re4"], None),
 ("And sometimes...", ["re2"], None),
 ("Because you're not a superhero", ["film", "re4"], None),
 ("That distinction is everything", ["re4"], None),
 # 2 — the franchise and Hollywood
 ("Over the years, the Resident Evil games", ["req", "re4"], None),
 ("Zombies.", ["re2"], None),
 ("Umbrella.", ["req"], None),
 ("Secret laboratories", ["re2"], None),
 ("And some of the most recognizable", ["games"], None),
 ("So when Hollywood adapted", ["old"], "RESIDENT EVIL (2002)"),
 ("Take the recognizable", ["old"], None),
 ("But there's a problem", ["old"], None),
 ("That can give you a movie", ["old"], None),
 # 3 — Cregger
 ("That's where Zach Cregger comes in", ["cregger"], None),
 ("Cregger became known", ["barb", "weap"], "BARBARIAN (2022) · WEAPONS (2025)"),
 ("And instead of simply asking", ["cregger"], None),
 ("he seems to have asked", ["feat"], None),
 ("\"What does it actually feel like", ["games"], None),
 ("That changes everything", ["games"], None),
 ("Because playing a survival", ["re2"], None),
 ("It's about your relationship", ["re4"], None),
 ("You enter a room", ["re2", "film"], None),
 ("You have a limited amount", ["re4"], None),
 ("You start thinking", ["re4", "film"], None),
 ("And then...", ["film"], None),
 ("That's the experience", ["games"], None),
 # 4 — Bryan
 ("So instead of making another", ["film"], None),
 ("Cregger created Bryan", ["film"], None),
 ("Played by Austin Abrams", ["P:abrams"], "AUSTIN ABRAMS · BRYAN"),
 ("Bryan is a medical courier", ["film"], None),
 ("He's not Leon Kennedy", ["re4"], None),
 ("He's not Chris Redfield", ["games"], None),
 ("He's not a trained", ["film"], None),
 ("And that makes the situation", ["film", "games"], None),
 ("If something stronger", ["film"], None),
 # 5 — the fan question
 ("And this is where the movie's approach", ["film"], None),
 ("Because some fans", ["games"], None),
 ("Where are Leon and Claire", ["re2"], None),
 ("Why create a new character", ["film"], None),
 ("Those are legitimate", ["film"], None),
 ("What if the goal isn't", ["games"], None),
 ("That's a completely different", ["games", "film"], None),
 # 6 — games vs movies
 ("Think about video games", ["games"], None),
 ("A game can take hours", ["re4"], None),
 ("A movie usually", ["film"], None),
 ("A game can let you", ["re2"], None),
 ("A movie has to control", ["film"], None),
 ("A game can make you solve", ["re1"], None),
 ("A movie has to show you", ["film"], None),
 ("A game can give you an inventory", ["re4"], None),
 ("A movie doesn't have", ["film"], None),
 ("So filmmakers have", ["feat"], None),
 ("And Cregger's solution", ["cregger"], None),
 # 7 — mechanics into tension
 ("Limited ammunition becomes suspense", ["re4", "film"], None),
 ("Exploration becomes", ["re2"], None),
 ("Inventory management", ["re4", "film"], None),
 ("Mission objectives", ["re4"], None),
 ("Enemies become", ["games", "film"], None),
 ("The movie reportedly uses", ["film"], None),
 ("That's an incredibly smart", ["feat"], None),
 ("Because it doesn't require", ["games"], None),
 ("You don't need to know exactly", ["re2"], "RESIDENT EVIL 2"),
 ("You don't need to remember", ["re4"], "RESIDENT EVIL 4"),
 ("You just need to understand", ["film"], None),
 # 8 — accessibility
 ("That's probably why", ["film"], None),
 ("Because the biggest challenge", ["old"], None),
 ("If you make the movie too faithful", ["old", "raccoon"], None),
 ("If you make it too different", ["old"], None),
 ("Cregger appears to have found", ["cregger"], None),
 ("Keep the DNA", ["film"], None),
 # 9 — the DNA
 ("And the DNA is everywhere", ["games"], None),
 ("Raccoon City.", ["re2"], None),
 ("The T-virus", ["req", "film"], None),
 ("Scavenging.", ["re2", "film"], None),
 ("Typewriters.", ["re1"], None),
 ("Environmental storytelling", ["re4"], None),
 ("The feeling that opening", ["film"], None),
 ("These aren't random", ["games"], None),
 # 10 — reception
 ("And that's why the movie's reception", ["film"], None),
 ("Critics and audiences", ["film"], None),
 ("Rotten Tomatoes currently", ["film"], None),
 ("the movie opened to around", ["film"], None),
 ("That's particularly notable", ["old"], None),
 ("It's another reboot", ["raccoon", "old"], "WELCOME TO RACCOON CITY (2021)"),
 ("And yet audiences showed up", ["V:cinema1"], None),
 # 11 — cursed projects
 ("But here's the really interesting", ["raccoon"], None),
 ("The movie's success could", ["V:cinema2"], None),
 ("For years, video game adaptations", ["old"], None),
 ("Studios would buy", ["old"], None),
 ("And then wonder why fans", ["old"], None),
 ("But the industry has slowly", ["games"], None),
 ("A video game isn't just", ["re4"], None),
 ("A game has player agency", ["re2"], None),
 ("And those things can", ["games"], None),
 # 12 — what players remember
 ("Think about it.", ["re4"], None),
 ("But they also remember walking", ["re2"], None),
 ("They remember hearing", ["re4"], None),
 ("They remember the feeling", ["re2"], None),
 ("That's what Cregger is trying", ["film"], None),
 # 13 — no Leon
 ("And that's why the absence", ["re4"], None),
 ("Bryan doesn't.", ["film"], None),
 # 14 — ordinary hero
 ("There's also something refreshing", ["film", "games"], None),
 ("If Superman walks", ["games"], None),
 ("If an ordinary medical courier", ["film"], None),
 ("Those are player questions", ["games"], None),
 # 15 — horror and humor
 ("The movie also embraces", ["film"], None),
 ("Resident Evil has never been purely", ["re4"], None),
 ("And Cregger's background", ["barb", "weap"], None),
 ("The movie isn't trying", ["film", "barb", "weap"], None),
 # 16 — runtime
 ("That's another reason the runtime", ["film", "games"], None),
 ("It gives the film the momentum", ["games"], None),
 ("You're moving.", ["games", "film"], None),
 ("That pace is very different", ["V:cinema2"], None),
 # 17 — game logic
 ("And there's a bigger lesson", ["games"], None),
 ("Resident Evil doesn't have to give", ["games"], None),
 ("When Bryan enters a room", ["film"], None),
 ("That's game logic", ["games"], None),
 ("But it works beautifully", ["film"], None),
 # 18 — the moment
 ("And this might explain why", ["film"], None),
 ("Gamers aren't automatically", ["games"], None),
 ("That's what Cregger appears to have prioritized", ["cregger"], None),
 ("The film takes a new story", ["film"], None),
 # 19 — the formula
 ("And now we're left", ["games"], None),
 ("Could this be the new formula", ["games"], None),
 ("Hollywood suddenly has", ["raccoon", "film"], None),
 ("You can take the world", ["games"], None),
 ("and tell a new story", ["film"], None),
 # 20 — the experiment
 ("That's what makes Resident Evil 2026", ["film"], None),
 ("It's an experiment", ["film", "cregger"], None),
 ("It makes the audience feel vulnerable", ["film"], None),
 # 21 — the core
 ("Because at the end of the day", ["games"], None),
 ("Those things are the decoration", ["req", "games"], None),
 ("That's survival horror", ["re2"], None),
 # 22 — close
 ("For twenty years, Hollywood kept", ["old"], None),
 ("Maybe they were asking", ["old", "film"], None),
 ("And in 2026", ["cregger"], None),
 ("Not by making another movie", ["film"], None),
 ("The next era of video game movies", ["film"], None),
 ("Resident Evil may have just opened", ["film"], None),
]

norm = lambda s: s.replace("’", "'").replace("“", '"').replace("”", '"')
def at(pre, after=-1.0):
    """Time of the first sentence starting with pre, after time `after`."""
    m = [s["t"] for s in sents if norm(s["text"]).startswith(pre) and s["t"] > after]
    if not m:
        sys.exit(f"cue not found: {pre}")
    return m[0]

GAME_POOLS = ("re1", "re2", "re3", "re4", "re7", "village", "req")
# pools: footage picks, combined "games" pool interleaves the game trailers
pool = {k: [(os.path.join(clipdir, f), t) for f, t in v] for k, v in picks.items()} if clipdir else {}
games = [p for k in GAME_POOLS for p in pool.get(k, [])]
games.sort(key=lambda x: (x[1] % 23, x[0]))
if games:
    pool["games"] = games
pos = {}
def take(k):
    p = pool[k]
    i = pos.get(k, 0)
    if k in GAME_POOLS and i >= len(p) and "games" in pool:
        return take("games")  # a used-up game pool borrows from the other games
    pos[k] = i + 1
    f, t = p[i % len(p)]
    return ("clip", f, t)

stillpos = {}
def still(key, poster=False, person=False):
    e = tm[key]
    if poster:
        return ("img", f"https://image.tmdb.org/t/p/w780/{e['poster']}.jpg", "fit")
    i = stillpos.get(key, 0)
    stillpos[key] = i + 1
    p = e["imgs"][i % len(e["imgs"])]
    return ("img", f"https://image.tmdb.org/t/p/{'w780' if person else 'w1280'}/{p}.jpg",
            "fit" if person else "fill")

def resolve(tok):
    if tok.startswith("S:"):
        return still(tok[2:]), STILL
    if tok.startswith("P:"):
        return still("p_" + tok[2:], person=True), STILL
    if tok.startswith("PO:"):
        return still(tok[3:], poster=True), STILL
    if tok.startswith("V:"):
        return ("vid",) + V[tok[2:]], SHOT
    if tok in pool:
        return take(tok), SHOT
    return still(FALLBACK.get(tok, "re2026")), STILL

cue_t, last = [], -1.0
for p, toks, l in CUES:  # CUES are in script order, so repeated phrases resolve in turn
    last = at(p, last)
    cue_t.append((last, p, toks, l))
cue_t[0] = (0.0,) + cue_t[0][1:]
shots = []
for k, (t0, pre, toks, label) in enumerate(cue_t):
    t1 = cue_t[k + 1][0] if k + 1 < len(cue_t) else T
    t, j, cyc = t0, 0, itertools.cycle(toks)
    while t1 - t > 0.05:
        a, d = resolve(next(cyc))
        left = t1 - t
        if left < d + 1.2:  # last shot(s): split what is left so no clip runs past SHOT
            n = 1 if a[0] == "img" or left <= SHOT else 2
            d = left / n
        shots.append((t, d, a, label if j == 0 else None))
        t += d; j += 1

# one render segment per script section
CUTS = [0.0]
body = open(os.path.join(HERE, "script.txt")).read().split("\n\n\n", 1)[1]
n = 0
for sec in body.split("—— ——")[:-1]:
    for block in re.split(r"\n\s*\n", sec):
        if block.strip():
            n += len([x for x in re.split(r"(?<=[.?!])\s+(?=[A-Z\"“])", block.strip()) if x.strip()])
    CUTS.append(sents[n]["t"])
CUTS.append(T)
# snap shot boundaries near a section start onto it
for i, (s, d, a, l) in enumerate(shots):
    for b in CUTS[1:-1]:
        if 0 < abs(s - b) < 1.0:
            prev = shots[i - 1]
            shots[i - 1] = (prev[0], b - prev[0], prev[2], prev[3])
            shots[i] = (b, s + d - b, a, l)

KB = [({"scale": 1, "x": .5, "y": .5}, {"scale": 1.12, "x": .5, "y": .45}),
      ({"scale": 1.12, "x": .5, "y": .5}, {"scale": 1, "x": .5, "y": .5}),
      ({"scale": 1.05, "x": .4, "y": .5}, {"scale": 1.15, "x": .6, "y": .5})]
kb = itertools.cycle(KB)
vstart, segs = {}, []
LABEL = {"color": "#E8D9B5", "fontSize": 40, "fontWeight": 700, "textAlign": "left", "background": "rgba(0,0,0,0.5)"}
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
title = {"color": "#C8102E", "fontSize": 104, "fontWeight": 800, "textAlign": "center"}
sub = {"color": "#FFFFFF", "fontSize": 40, "textAlign": "center"}
stat = {"color": "#E8D9B5", "fontSize": 60, "fontWeight": 800, "textAlign": "center", "background": "rgba(0,0,0,0.55)"}
t = at("Let's rewind.")
add_overlay(t - 3.0, {"kind": "text", "text": "RESIDENT EVIL", "duration": 3.0,
                      "position": {"x": 0.1, "y": 0.36, "width": 0.8, "height": 0.16}, "style": title})
add_overlay(t - 2.7, {"kind": "text", "text": "THE VIDEO GAME MOVIE THAT FINALLY UNDERSTANDS VIDEO GAMES", "duration": 2.7,
                      "position": {"x": 0.08, "y": 0.55, "width": 0.84, "height": 0.07}, "style": sub})
add_overlay(at("Rotten Tomatoes currently") + 0.5, {"kind": "text", "text": "96% CRITICS · 91% VERIFIED AUDIENCE", "duration": 6,
            "position": {"x": 0.1, "y": 0.40, "width": 0.8, "height": 0.12}, "style": stat})
add_overlay(at("the movie opened to around") + 0.5, {"kind": "text", "text": "$60M DOMESTIC · $108.3M WORLDWIDE OPENING", "duration": 7,
            "position": {"x": 0.08, "y": 0.40, "width": 0.84, "height": 0.12}, "style": stat})
add_overlay(at("That's another reason the runtime") + 2.0, {"kind": "text", "text": "RUNTIME: 1H 34M", "duration": 4,
            "position": {"x": 0.25, "y": 0.40, "width": 0.5, "height": 0.12}, "style": stat})
for pre, txt in [("Let's rewind.", "1996: SURVIVAL HORROR"), ("That's where Zach Cregger comes in", "ENTER CREGGER"),
                 ("So instead of making another", "MEET BRYAN"), ("Think about video games", "GAMES VS. MOVIES"),
                 ("And the DNA is everywhere", "THE DNA"), ("And that's why the movie's reception", "THE RECEPTION"),
                 ("The movie also embraces", "HORROR + HUMOR"), ("And now we're left", "THE NEW FORMULA")]:
    add_overlay(at(pre) + 0.2, {"kind": "text", "text": txt, "duration": 3.2,
                                "position": {"x": 0.05, "y": 0.06, "width": 0.5, "height": 0.07},
                                "style": {"color": "#FFFFFF", "fontSize": 34, "fontWeight": 700, "textAlign": "left",
                                          "background": "rgba(200,16,46,0.75)"}})
t = at("Resident Evil may have just opened")
add_overlay(t - 1.0, {"kind": "text", "text": "FAITHFUL TO THE EXPERIENCE", "duration": 6, "position": {"x": 0.1, "y": 0.36, "width": 0.8, "height": 0.12}, "style": {**title, "fontSize": 72}})
add_overlay(t + 0.5, {"kind": "text", "text": "WHICH GAME SHOULD GET THIS TREATMENT NEXT? · SUBSCRIBE", "duration": 6,
                      "position": {"x": 0.12, "y": 0.52, "width": 0.76, "height": 0.07}, "style": sub})
credit = ("Footage: Sony Pictures, Capcom, 20th Century, Warner Bros. · Stills: TMDB" if clipdir
          else "Stills: TMDB · Stock: Pexels")
add_overlay(1.0, {"kind": "text", "text": credit, "duration": 5,
                  "position": {"x": 0.40, "y": 0.93, "width": 0.58, "height": 0.05},
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
print(f"{len(segs)} segments, {nimg} still shots, {nvid} video shots, total "
      f"{sum(sum(x['duration'] for x in s['scenes']) for s in segs):.2f}s; picks used: {pos}")
