#!/usr/bin/env python3
"""Clean segments = detected scenes minus dilated emoji frames. Writes footage/clean.json and review sheets."""
import json, os, subprocess, sys, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLIPS = f"{ROOT}/footage/clips"; SHEETS = f"{ROOT}/footage/csheets"; THUMBS = f"{ROOT}/footage/cthumbs"
os.makedirs(SHEETS, exist_ok=True); os.makedirs(THUMBS, exist_ok=True)
scenes = json.load(open(f"{ROOT}/footage/scenes.json")); emoji = json.load(open(f"{ROOT}/footage/emoji.json"))
PAD, MIN_SEG, TRIM = 0.4, 1.1, 0.12     # dilation around flagged frames, min clean length, trim at hard cuts

def clean_segments(src):
    bad = sorted(emoji[src]); out = []
    for a, b in scenes[src]["scenes"]:
        a, b = a + TRIM, b - TRIM
        cur = a
        for t in [t for t in bad if a - PAD <= t <= b + PAD]:
            lo, hi = t - PAD, t + PAD + 1 / 8
            if lo > cur: out.append([cur, min(lo, b)])
            cur = max(cur, hi)
        if b > cur: out.append([cur, b])
    return [[round(x, 3), round(y, 3)] for x, y in out if y - x >= MIN_SEG]

def thumb(args):
    src, i, a, b = args
    o = f"{THUMBS}/{src}_{i:03d}.jpg"
    if not os.path.exists(o):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{(a + b) / 2:.3f}", "-i", f"{CLIPS}/{src}.mp4", "-frames:v", "1", "-vf", "scale=320:-1", o], check=True)
    return o

if __name__ == "__main__":
    res = {s: clean_segments(s) for s in scenes}
    json.dump(res, open(f"{ROOT}/footage/clean.json", "w"))
    tot = 0
    for s, v in res.items():
        d = sum(b - a for a, b in v); tot += d
        print(f"{s:16s} {len(v):3d} segs {d:6.1f}s of {scenes[s]['duration']:.0f}s")
    print(f"TOTAL clean {tot:.0f}s")
    if len(sys.argv) > 1 and sys.argv[1] == "sheets":
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        for src, segs in res.items():
            with cf.ThreadPoolExecutor(4) as ex:
                paths = list(ex.map(thumb, [(src, i, a, b) for i, (a, b) in enumerate(segs)]))
            per, cols = 40, 5
            for n in range(0, len(segs), per):
                chunk = paths[n:n + per]; rows = (len(chunk) + cols - 1) // cols
                sheet = Image.new("RGB", (cols * 320, rows * 180), (20, 20, 20)); d = ImageDraw.Draw(sheet)
                for k, p in enumerate(chunk):
                    x, y = (k % cols) * 320, (k // cols) * 180
                    sheet.paste(Image.open(p).resize((320, 180)), (x, y))
                    d.rectangle((x, y, x + 56, y + 24), fill=(0, 0, 0)); d.text((x + 4, y + 2), str(n + k), fill=(255, 255, 0), font=font)
                sheet.save(f"{SHEETS}/{src}_{n // per}.png")
