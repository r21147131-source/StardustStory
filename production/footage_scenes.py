#!/usr/bin/env python3
"""Detect cuts in each downloaded trailer, write footage/scenes.json and review sheets.

  python3 production/footage_scenes.py detect     # scenes.json
  python3 production/footage_scenes.py sheets     # footage/sheets/<src>_<n>.png  (scene index labelled)
"""
import json, os, re, subprocess, sys, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLIPS = f"{ROOT}/footage/clips"
OUT = f"{ROOT}/footage/scenes.json"
SHEETS = f"{ROOT}/footage/sheets"
THUMBS = f"{ROOT}/footage/thumbs"
MIN_LEN = 0.8
os.makedirs(SHEETS, exist_ok=True); os.makedirs(THUMBS, exist_ok=True)
SOURCES = sorted(f[:-4] for f in os.listdir(CLIPS) if f.endswith(".mp4"))

def duration(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

def detect(src):
    f = f"{CLIPS}/{src}.mp4"
    dur = duration(f)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-an", "-vf", "scale=480:-1,select='gt(scene,0.2)',showinfo", "-f", "null", "-"],
                       capture_output=True, text=True)
    cuts = [0.0] + [float(m) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)] + [dur]
    scenes = []
    for a, b in zip(cuts, cuts[1:]):
        if b - a >= MIN_LEN:
            scenes.append([round(a, 3), round(b, 3)])
    return src, dur, scenes

def thumb(args):
    src, i, a, b = args
    out = f"{THUMBS}/{src}_{i:03d}.jpg"
    if not os.path.exists(out):
        t = a + min(0.6, (b - a) / 2)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", f"{CLIPS}/{src}.mp4", "-frames:v", "1", "-vf", "scale=320:-1", out], check=True)
    return out

if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "detect"
    if st == "detect":
        res = {}
        with cf.ThreadPoolExecutor(3) as ex:
            for src, dur, scenes in ex.map(detect, SOURCES):
                res[src] = {"duration": dur, "scenes": scenes}
                print(src, f"{dur:.0f}s", len(scenes), "scenes", flush=True)
        json.dump(res, open(OUT, "w"))
    else:
        data = json.load(open(OUT))
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        for src in SOURCES:
            sc = data[src]["scenes"]
            with cf.ThreadPoolExecutor(4) as ex:
                paths = list(ex.map(thumb, [(src, i, a, b) for i, (a, b) in enumerate(sc)]))
            per, cols = 40, 5
            for n in range(0, len(sc), per):
                chunk = paths[n:n + per]
                rows = (len(chunk) + cols - 1) // cols
                sheet = Image.new("RGB", (cols * 320, rows * 180), (20, 20, 20))
                d = ImageDraw.Draw(sheet)
                for k, p in enumerate(chunk):
                    im = Image.open(p).resize((320, 180))
                    x, y = (k % cols) * 320, (k // cols) * 180
                    sheet.paste(im, (x, y))
                    d.rectangle((x, y, x + 56, y + 24), fill=(0, 0, 0)); d.text((x + 4, y + 2), str(n + k), fill=(255, 255, 0), font=font)
                sheet.save(f"{SHEETS}/{src}_{n // per}.png")
            print(src, "sheets", (len(sc) + per - 1) // per)
