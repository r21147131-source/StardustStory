import json, subprocess, sys, os
from collections import defaultdict

# Composites each overlay card (output/ep5-overlays/<key>.mp4, rendered by
# pantheon-ep5-render-overlays.py) onto its target scene in
# output/ep5-segments/, in place. Cards are rendered against solid
# chroma-key green and keyed out with ffmpeg's colorkey filter (see
# src/graphics/Ep5OverlayCard.tsx). Mirrors the Ep.4 name-card pipeline.
data = json.load(open("production/pantheon-ep5-overlays.json"))
scenes = json.load(open("production/pantheon-ep5-scenes.json"))

by_scene = defaultdict(list)
for d in data:
    by_scene[d["scene_idx"]].append(d)

CARD_DIR = "output/ep5-overlays"
SEG_DIR = "output/ep5-segments"

n = 0
total = len(by_scene)
for scene_idx, cards in sorted(by_scene.items()):
    n += 1
    sc = scenes[scene_idx]
    seg_path = f"{SEG_DIR}/{scene_idx:04d}_{sc['shot']}.mp4"
    if not os.path.exists(seg_path):
        print(f"MISSING SEGMENT: {seg_path}")
        sys.exit(1)

    tmp_out = seg_path + ".overlay.mp4"

    inputs = ["-i", seg_path]
    filter_parts = []
    last_label = "0:v"
    for i, card in enumerate(cards, start=1):
        card_path = f"{CARD_DIR}/{card['key']}.mp4"
        if not os.path.exists(card_path):
            print(f"MISSING CARD: {card_path}")
            sys.exit(1)
        inputs += ["-i", card_path]
        start_s = card["start_frame"] / 30.0
        keyed = f"k{i}"
        out_label = f"v{i}"
        if start_s > 0:
            filter_parts.append(
                f"[{i}:v]tpad=start_duration={start_s}:start_mode=add:color=0x00FF00[pad{i}]"
            )
            src = f"pad{i}"
        else:
            src = f"{i}:v"
        filter_parts.append(f"[{src}]colorkey=0x00FF00:0.38:0.15[{keyed}]")
        # eof_action=pass: once a card's clip ends, fall through to the
        # untouched main input instead of freezing its last (possibly
        # mid-slide) frame as a permanent overlay for the rest of the scene.
        filter_parts.append(f"[{last_label}][{keyed}]overlay=0:0:eof_action=pass[{out_label}]")
        last_label = out_label

    filter_complex = ";".join(filter_parts)
    cmd = (
        ["ffmpeg", "-y"] + inputs +
        ["-filter_complex", filter_complex, "-map", f"[{last_label}]", "-map", "0:a",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
         "-c:a", "aac", tmp_out]
    )
    labels = ", ".join(c["line1"] for c in cards)
    print(f"[{n}/{total}] scene {scene_idx} ({sc['shot']}): {labels}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", r.stderr[-2500:])
        sys.exit(1)
    os.replace(tmp_out, seg_path)

print("ALL_OVERLAYS_APPLIED")
