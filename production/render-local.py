"""Render a narrated B-roll video locally with ffmpeg.

usage: render-local.py SHOTS_JSON VOICEOVER CLIP_DIR WORK_DIR OUT_MP4
SHOTS_JSON is {"total": seconds, "shots": [{"start", "src", "trim"}]};
clips must already be downloaded into CLIP_DIR under their source basename.
Each shot runs from its start to the next shot's start, frame-exact at 30fps,
so cuts stay locked to the narration.
"""
import json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

shots_json, vo, clips, work, out = sys.argv[1:6]
FPS = 30
d = json.load(open(shots_json))
shots, total = d["shots"], d["total"]
starts = [s["start"] for s in shots] + [total]
os.makedirs(work, exist_ok=True)

def part(i):
    s = shots[i]
    n = round(starts[i + 1] * FPS) - round(starts[i] * FPS)
    vf = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,"
          f"fps={FPS},tpad=stop_mode=clone:stop=-1,eq=saturation=0.85:contrast=1.05,vignette=PI/5")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(s["trim"]),
                    "-i", os.path.join(clips, s["src"].rsplit("/", 1)[1]), "-an", "-vf", vf,
                    "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", f"{work}/{i:03d}.mp4"], check=True)

with ThreadPoolExecutor(4) as ex:
    list(ex.map(part, range(len(shots))))
with open(f"{work}/list.txt", "w") as f:
    f.writelines(f"file '{i:03d}.mp4'\n" for i in range(len(shots)))
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", f"{work}/list.txt", "-i", vo, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                "-movflags", "+faststart", out], check=True)
