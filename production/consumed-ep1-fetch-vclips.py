"""Download vidiq_generate_clips results and list them for consumed-ep1-edit.py.

Usage: python3 production/consumed-ep1-fetch-vclips.py JOBS.json
JOBS.json maps a clip name (as used in C() cues, e.g. "blood") to the list of
clipUrl values a generate_clips job returned. Writes render/vclips/<name>_<k>.mp4
and production/consumed-ep1-vclips.json with each file's length and letterbox crop.
"""
import json, os, re, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "render/vclips")
os.makedirs(OUT, exist_ok=True)


def probe(path):
    err = subprocess.run([FF, "-hide_banner", "-i", path, "-vf", "cropdetect=24:2:0", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    crops = re.findall(r"crop=(\d+:\d+:\d+:\d+)", err)
    crop = max(set(crops), key=crops.count) if crops else "iw:ih:0:0"
    return int(h) * 3600 + int(m) * 60 + float(s), crop


pools = {}
for name, urls in json.load(open(sys.argv[1])).items():
    for k, url in enumerate(urls):
        rel = f"render/vclips/{name}_{k}.mp4"
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            subprocess.run(["curl", "-sSfL", "--retry", "4", "--retry-all-errors", "-o", path, url], check=True)
        dur, crop = probe(path)
        pools.setdefault(name, []).append({"file": rel, "dur": round(dur - 0.3, 2), "crop": crop})
        print(f"{rel}  {dur:5.1f}s  crop={crop}")
json.dump(pools, open(os.path.join(ROOT, "production/consumed-ep1-vclips.json"), "w"), indent=1)
