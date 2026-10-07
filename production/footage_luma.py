#!/usr/bin/env python3
"""Mean luma per frame at 8 fps for every downloaded trailer -> footage/luma.json (used to trim fades to black)."""
import json, os, subprocess
import numpy as np
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLIPS = f"{ROOT}/footage/clips"
out = {}
for f in sorted(os.listdir(CLIPS)):
    if not f.endswith(".mp4"): continue
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{CLIPS}/{f}", "-an", "-vf", "fps=8,scale=64:36,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8).reshape(-1, 64 * 36).mean(axis=1)
    out[f[:-4]] = [round(float(x), 1) for x in a]
    print(f[:-4], len(a), "frames; dark<16:", int((a < 16).sum()))
json.dump(out, open(f"{ROOT}/footage/luma.json", "w"))
