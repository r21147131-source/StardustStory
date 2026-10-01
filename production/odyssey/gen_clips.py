"""Generate clips.json for build_ody.py: swap stills for real footage.

Usage: python gen_clips.py CLIPDIR OUT.json

Each cue's assets get equal slots (as build_ody.py would cut them). Odyssey stills,
the ship/storm stock shots and the Odyssey poster become trailer shots (every third
Odyssey still stays a still); in the two IMAX passages Odyssey stills become featurette behind-the-scenes shots; Oppenheimer stills become
Oppenheimer trailer shots; Nolan's photo becomes interview close-ups (his first,
labelled appearance keeps the photo for the name card). Other people keep their
photos, other stock stays. Picks rotate through PICKS so no shot repeats until a
pool runs out. Source files: footage-sources.txt.
"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
clipdir, out = sys.argv[1], sys.argv[2]
sents = json.load(open(os.path.join(HERE, "sent_times.json")))
T = 711.927
src = open(os.path.join(HERE, "build_ody.py")).read()
cues = re.findall(r'^ \("((?:[^"\\]|\\.)*)", \[(.*?)\], (None|"[^"]*")\),$', src, re.M)

# hand-picked start times (s) from contact sheets: no titles, logos or name cards
T1 = [15.5, 22, 30, 32.5, 39.5, 41.5, 45, 48, 56, 58, 62, 66, 68.5, 74, 76, 88, 90, 92]
T2 = [6, 8, 12, 16, 18, 20, 22, 26, 38, 40, 42, 46, 48, 56, 58, 60, 62, 74, 76, 80, 82,
      90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124,
      126, 128, 130]
trail = [("ody_trailer.mp4", t) for t in T1] + [("ody_trailer2.mp4", t) for t in T2]
trail.sort(key=lambda x: (x[1] % 37, x[0]))  # interleave both trailers
PICKS = {
    "trailer": trail,
    "imax": [("ody_imax.mkv", t) for t in [12, 15, 18, 27, 39, 48, 51, 69, 72, 78, 81,
                                           90, 93, 96, 99, 111, 114, 117, 120, 129, 132, 135, 138,
                                           141, 159, 162, 165, 171, 174, 177, 180, 183, 186, 195, 198]],
    "opp": [("oppenheimer.mp4", t) for t in [6, 22, 24, 26, 30, 32, 34, 36, 38, 40, 46, 48, 50, 52, 58,
                                             64, 66, 68, 70, 72, 74, 76, 88, 90, 92, 94, 96, 98, 100,
                                             102, 104, 106, 108, 112]],
    "nolan": [("ody_nolan_int.mp4", t) for t in [135, 150, 180, 285, 345, 450, 465, 480, 525, 540, 555,
                                                 570, 630, 660, 675, 690, 720, 735, 750, 795, 870, 885,
                                                 900, 915, 1005]],
}
pos = {k: 0 for k in PICKS}
def pick(pool):
    p = PICKS[pool]
    f, t = p[pos[pool] % len(p)]
    rep = pos[pool] // len(p)  # later passes start a little later in the same shot
    pos[pool] += 1
    return os.path.join(clipdir, f), t + 0.8 * rep

norm = lambda s: s.replace("’", "'")
def at(pre):
    return next(s["t"] for s in sents if norm(s["text"]).startswith(pre))

IMAX_A, IMAX_B = at("Nolan didn't approach"), at("And audiences clearly responded")
IMAX2_A, IMAX2_B = at("That's also why the IMAX choice"), at("And it explains why")
ts = sorted((at(p.replace('\\"', '"')), p.replace('\\"', '"'), a, l) for p, a, l in cues)
ts[0] = (0.0,) + ts[0][1:]
SHOT = 3.2
res, nolan_named = {}, False
for k, (t0, pre, assets, label) in enumerate(ts):
    t1 = ts[k + 1][0] if k + 1 < len(ts) else T
    items = re.findall(r'[A-Z]+\([^()]*\)|V\["\w+"\]', assets)
    slot = (t1 - t0) / len(items)
    seq, swapped = [], False
    for i, a in enumerate(items):
        if a.startswith("O(") and int(a[2:-1]) % 3 == 2:
            seq.append(["STILL", i, slot]); continue  # keep every third TMDB still
        if a.startswith("O(") or a == 'PO("odyssey")' or a in ('V["storm"]', 'V["boat"]'):
            imax = IMAX_A <= t0 < IMAX_B or IMAX2_A <= t0 < IMAX2_B
            pool = "imax" if imax and a.startswith("O(") else "trailer"
        elif "oppenheimer" in a:
            pool = "opp"
        elif a == 'P("nolan")':
            if not nolan_named:
                nolan_named = True
                seq.append(["STILL", i, slot]); continue
            pool = "nolan"
        else:
            seq.append(["STILL", i, slot]); continue
        swapped = True
        n = max(1, math.ceil(slot / SHOT - 0.05))
        for _ in range(n):
            f, t = pick(pool)
            seq.append([f, t, round(slot / n, 2)])
    if swapped:
        res[pre] = seq
json.dump(res, open(out, "w"), indent=0)
print(f"{len(res)} cues get footage; picks used:", pos)
