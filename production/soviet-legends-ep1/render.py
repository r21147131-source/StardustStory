#!/usr/bin/env python3
"""Local renderer: narration + scenes.csv -> episode.mp4. Needs ffmpeg. Missing files are skipped (black card).
usage: python3 render.py NARRATION.mp3 [--out episode.mp4] [--limit SECONDS] [--credits credits.txt]"""
import argparse, csv, os, subprocess, sys, tempfile
W, H, FPS = 1920, 1080, 25
FONT = next((f for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "C:/Windows/Fonts/arialbd.ttf"] if os.path.exists(f)), None)
VID = (".mp4", ".mov", ".mkv", ".webm")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit("ffmpeg failed:\n" + r.stderr[-1500:])

def esc(t): return t.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\u2019")

def make_seg(path, dur, label, out, i):
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS}"
    if path and os.path.exists(path) and path.lower().endswith(VID):
        src = ["-stream_loop", "-1", "-i", path]; vf = base
    elif path and os.path.exists(path):
        frames = int(dur * FPS) + 1
        z = "min(zoom+0.0006,1.15)" if i % 2 == 0 else "max(1.15-0.0006*on,1.0)"
        src = ["-loop", "1", "-i", path]
        vf = f"scale=2400:-1,zoompan=z='{z}':d={frames}:s={W}x{H}:fps={FPS},setsar=1"
    else:
        src = ["-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r={FPS}"]; vf = "null"
    if label and FONT:
        vf += (f",drawtext=fontfile='{FONT}':text='{esc(label)}':fontsize=54:fontcolor=white:"
               f"box=1:boxcolor=black@0.55:boxborderw=18:x=80:y=h-170:enable='between(t,0.6,{max(dur-0.6,1):.2f})'")
    run(["ffmpeg", "-y", "-v", "error", *src, "-t", f"{dur:.3f}", "-vf", vf, "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("audio"); ap.add_argument("--out", default="episode.mp4")
    ap.add_argument("--limit", type=float); ap.add_argument("--credits")
    a = ap.parse_args(); here = os.path.dirname(os.path.abspath(__file__)); os.chdir(here)
    tmp = tempfile.mkdtemp(); segs = []; n = 0
    for row in csv.reader(l for l in open("scenes.csv") if l.strip() and not l.startswith("#")):
        _, s, e, label, files = row[:5]; s, e = float(s), float(e)
        if a.limit and s >= a.limit: break
        if a.limit: e = min(e, a.limit)
        fl = [f for f in files.split("|") if f] or [None]
        have = [f for f in fl if f and os.path.exists(f)] or [None]
        d = (e - s) / len(have)
        for f in have:
            out = os.path.join(tmp, f"s{n:03d}.mp4"); make_seg(f, d, label, out, n); segs.append(out); n += 1
    lst = os.path.join(tmp, "list.txt"); open(lst, "w").write("".join(f"file '{p}'\n" for p in segs))
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", a.audio,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", a.out])
    print("wrote", a.out)
main()
