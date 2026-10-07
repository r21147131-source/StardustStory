#!/usr/bin/env python3
"""Flag frames carrying OpusClip's auto-emoji overlays (flat saturated yellow/green blobs).

  python3 production/emoji_detect.py            # all sources -> footage/emoji.json
  python3 production/emoji_detect.py born_again # one source, prints flagged times
Sampled at 8 fps on 480x270 frames. Output: {src: [flagged times in seconds]}.
"""
import json, os, subprocess, sys
import numpy as np, cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLIPS = f"{ROOT}/footage/clips"
FPS, W, H = 8, 480, 270

# Emoji overlays are always horizontally centred (x~0.5) and sit in the middle band of the frame.
ROI = (int(W * 0.38), int(H * 0.24), int(W * 0.62), int(H * 0.72))

def masks(bgr):
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    warm = (h >= 5) & (h <= 34) & (s >= 100) & (v >= 130)       # yellow / orange faces, money bag
    green = (h >= 40) & (h <= 90) & (s >= 100) & (v >= 110)     # check marks
    red = ((h <= 4) | (h >= 172)) & (s >= 130) & (v >= 140)     # hearts, fire
    blue = (h >= 95) & (h <= 125) & (s >= 150) & (v >= 170)     # tears, phones
    return warm, green, red, blue

def has_emoji(bgr):
    x0, y0, x1, y1 = ROI
    sub = bgr[y0:y1, x0:x1]
    for m in masks(sub):
        m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        for i in range(1, n):
            x, y, w, hh, area = stats[i]
            if area < 300 or w < 14 or hh < 14 or w > 90 or hh > 90: continue
            if not (0.55 < w / hh < 1.8): continue
            if area / (w * hh) < 0.5: continue
            return True
    return False

def scan(src):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", f"{CLIPS}/{src}.mp4", "-an", "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE)
    flagged, i = [], 0
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        if has_emoji(frame): flagged.append(round(i / FPS, 3))
        i += 1
    p.wait()
    return flagged

if __name__ == "__main__":
    srcs = sys.argv[1:] or sorted(f[:-4] for f in os.listdir(CLIPS) if f.endswith(".mp4"))
    out = {}
    for s in srcs:
        out[s] = scan(s)
        print(s, len(out[s]), "flagged frames", flush=True)
        if len(srcs) == 1: print(out[s])
    if len(srcs) > 1:
        json.dump(out, open(f"{ROOT}/footage/emoji.json", "w"))
