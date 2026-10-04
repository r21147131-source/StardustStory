#!/usr/bin/env bash
# Renders every scene in pantheon-ep4-scenes.json to a normalized
# 1920x1080/30fps/yuv420p clip with a silent AAC audio track (the real
# voiceover is muxed on separately at the end), then writes a concat list.
#
# Mirrors the local-ffmpeg approach used for Ep.2 (see pantheon-ep2-status.md
# section 10) since vidiq_compose credits are insufficient for this episode.
set -euo pipefail

cd /home/user/StardustStory
OUT="$(pwd)/output/ep4-segments"
mkdir -p "$OUT"

python3 - "$OUT" << 'PYEOF'
import json, subprocess, sys, os

out_dir = sys.argv[1]
scenes = json.load(open("production/pantheon-ep4-scenes.json"))

concat_lines = []
VF = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,fps=30"
SILENT_AUDIO = ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]

for i, sc in enumerate(scenes):
    src = sc["source"]
    src_path = src if src.startswith(("public/", "/")) else f"public/{src}"
    if not os.path.exists(src_path):
        print(f"MISSING SOURCE for scene {i} ({sc['shot']}): {src_path}")
        sys.exit(1)
    dur = sc["duration"]
    out_path = f"{out_dir}/{i:04d}_{sc['shot']}.mp4"

    if sc["type"] == "image":
        # Full image content visible (blurred fill instead of a hard crop
        # that chopped off most of any non-16:9 photo) plus a slow Ken Burns
        # zoom for motion. zoompan needs d = total output frames, not d=1 —
        # with d=1 the filter silently produces zero motion (static output).
        nframes = max(1, round(dur * 30))
        img_filter = (
            "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            "gblur=sigma=40,eq=brightness=-0.08:saturation=0.75[bg];"
            "[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,format=yuva420p[fg];"
            "[bg][fg]overlay=(W-w)/2:(H-h)/2:format=auto,scale=2400:1350,setsar=1[comp];"
            f"[comp]zoompan=z='min(zoom+0.0012,1.15)':d={nframes}:"
            "x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30[vout]"
        )
        cmd = (
            ["ffmpeg", "-y", "-loop", "1", "-i", src_path] + SILENT_AUDIO +
            ["-filter_complex", img_filter, "-map", "[vout]", "-map", "1:a",
             "-frames:v", str(nframes),
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
             "-c:a", "aac", "-shortest", out_path]
        )
    else:
        native = sc.get("_native")
        in_args = []
        if native and native < dur:
            # loop the source clip to fill the allotted duration
            in_args = ["-stream_loop", str(int(dur // native) + 1)]
        elif native and native > dur:
            # trim from partway in (not always the literal start) so a
            # repeated establishing beat doesn't always show the same frame
            start_from = round(max(0.0, (native - dur) / 2), 2)
            in_args = ["-ss", str(start_from)]
        cmd = (
            ["ffmpeg", "-y"] + in_args + ["-i", src_path] + SILENT_AUDIO +
            ["-t", str(dur), "-vf", VF,
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
             "-c:a", "aac", "-shortest", out_path]
        )

    print(f"[{i+1}/{len(scenes)}] {sc['shot']} ({sc['type']}, {dur}s) -> {out_path}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        sys.exit(1)
    concat_lines.append(f"file '{os.path.abspath(out_path)}'")

with open(f"{out_dir}/concat_list.txt", "w") as f:
    f.write("\n".join(concat_lines) + "\n")

print(f"\nWrote {len(concat_lines)} segments + concat list.")
PYEOF
