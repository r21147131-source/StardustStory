#!/usr/bin/env python3
"""Build the Robin Shou video from TMDB stills + EDL + voiceover (ffmpeg, Ken Burns)."""
import json, os, subprocess, glob, concurrent.futures as cf


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = f"{ROOT}/production/robin-shou-assets"
OUT = f"{ROOT}/output/robin-shou"; TMP = f"{OUT}/shots"
os.makedirs(TMP, exist_ok=True)
FPS, SHOT = 25, 5.0
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
edl = json.load(open(f"{ROOT}/production/robin-shou-edl.json"))
g = lambda pat: sorted(glob.glob(f"{A}/{pat}"))
MK, MKA, TC, SH, CR = (g("mortal-kombat-1995-bd*"), g("mortal-kombat-annihilation-1997-bd*"),
                       g("tiger-cage-2-1990-bd*"), g("shaolin-temple-1982-bd*"), g("credit-*"))
P = lambda n: g(f"{n}-0.jpg")[0]
# beat -> (image pool, [(portrait, label)] inserts, grade)
POOL = {
 "B01": (MK[:8], [], "hot"), "B02": ([], [(P("robin-shou"), "ROBIN SHOU")], "hot"),
 "B03": (CR, [], "cold"), "B04": (SH + CR, [], "cold"), "B05": (CR, [], "cold"),
 "B06": (CR, [], "cold"), "B07": (SH, [], "hot"), "B08": (SH + CR, [], "cold"),
 "B09": (CR, [], "cold"), "B10": (TC + CR, [], "cold"), "B11": (TC + CR, [], "hot"),
 "B12": (TC, [(P("donnie-yen"), "DONNIE YEN"), (P("yuen-woo-ping"), "YUEN WOO-PING"),
              (P("simon-yam"), ""), (P("cynthia-rothrock"), "")], "hot"),
 "B13": (CR, [], "cold"), "B14": (MK[8:] + MK, [], "hot"), "B15": (MK, [], "hot"),
 "B16": (CR, [], "cold"), "B17": (MK, [(P("paul-w.-s.-anderson"), "PAUL W. S. ANDERSON")], "hot"),
 "B18": (MK, [], "hot"), "B19": (MK + MKA, [], "hot"), "B20": (MKA, [(P("talisa-soto"), "")], "hot"),
 "B21": ([], [(P("robin-shou"), "")], "hot"),
}
used = {}
def pick(pool):
    c = min(pool, key=lambda f: (used.get(f, 0), pool.index(f)))
    used[c] = used.get(c, 0) + 1
    return c

def shots_for(b):
    pool, ins, grade = POOL[b["id"]]
    n = max(1, round(b["dur"] / SHOT))
    seq = [(i, ins and "") for i in range(n)]
    items = [(f, l) for f, l in ins] + [(pick(pool), "") for _ in range(n - len(ins))] if pool else list(ins)
    items = (items * n)[:n] if not pool else items[:n]
    # even frame split that sums exactly to the beat
    total = round(b["dur"] * FPS); base = total // len(items)
    return [(f, l, base + (1 if k < total - base * len(items) else 0), grade) for k, (f, l) in enumerate(items)]

def render(args):
    idx, f, label, frames, grade, bid, k = args
    out = f"{TMP}/{idx:03d}.mp4"
    w, h = map(int, subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=width,height","-of","csv=p=0:s=x",f]).decode().strip().split("x"))
    zi = k % 2 == 0
    z = "min(zoom+0.0007,1.18)" if zi else "if(eq(on,0),1.18,max(zoom-0.0007,1.0))"
    fg = (f"scale=2880:1620:force_original_aspect_ratio=increase,crop=2880:1620" if w / h > 1.5 else
          "split[a][b];[a]scale=2880:1620:force_original_aspect_ratio=increase,crop=2880:1620,boxblur=40:5[bg];"
          "[b]scale=-2:1500[fgp];[bg][fgp]overlay=(W-w)/2:(H-h)/2")
    vf = f"{fg},zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={FPS}"
    vf += (",eq=saturation=1.05:contrast=1.08" if grade == "hot" else ",eq=saturation=0.55:brightness=-0.07:contrast=1.1")
    vf += ",vignette=PI/4,fade=t=in:st=0:d=0.25"
    if label:
        t = label.replace("'", "\\'")
        vf += (f",drawbox=x=90:y=880:w=8:h=70:color=0xE8B04A@1:t=fill,drawtext=fontfile={FONT}:text='{t}':fontsize=54:"
               f"fontcolor=white:x=120:y=888:shadowcolor=black:shadowx=2:shadowy=2")
    if bid == "B19":
        d = frames / FPS / 3
        for i, (txt, c) in enumerate([("$23M OPENING WEEKEND", "white"), ("3 WEEKENDS AT #1", "white"), ("$122M WORLDWIDE", "0xE8B04A")]):
            vf += (f",drawtext=fontfile={FONT}:text='{txt}':fontsize=96:fontcolor={c}:x=(w-text_w)/2:y=(h-text_h)/2:"
                   f"box=1:boxcolor=black@0.55:boxborderw=28:enable='between(t,{i*d:.2f},{(i+1)*d:.2f})'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", f, "-vf", vf, "-frames:v", str(frames),
                    "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out], check=True)
    return out

jobs, idx = [], 0
for b in edl["beats"]:
    for k, (f, l, fr, gr) in enumerate(shots_for(b)):
        jobs.append((idx, f, l, fr, gr, b["id"], idx)); idx += 1
print(len(jobs), "shots", sum(j[3] for j in jobs) / FPS, "s")
with cf.ThreadPoolExecutor(os.cpu_count()) as ex: files = list(ex.map(render, jobs))
open(f"{TMP}/list.txt", "w").write("".join(f"file '{f}'\n" for f in files))
final = f"{OUT}/robin-shou.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{TMP}/list.txt", "-i", f"{ROOT}/{edl['voiceover']}",
                "-vf", f"fade=t=out:st={edl['duration']-2.5}:d=2.5", "-af", f"afade=t=out:st={edl['duration']-1.5}:d=1.5",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-shortest", final], check=True)
print(final)
