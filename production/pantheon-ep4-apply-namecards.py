import json, subprocess, sys, os
from collections import defaultdict

# Composites each person's name card (output/ep4-namecards/<key>.mp4, rendered
# by pantheon-ep4-render-namecards.py) onto its target scene in
# output/ep4-segments/, in place. Cards are rendered against solid chroma-key
# green and keyed out with ffmpeg's colorkey filter (see
# src/graphics/Ep4NameCard.tsx for why -- true alpha export wasn't reliable
# in this pipeline).
data = json.load(open("production/pantheon-ep4-names.json"))
scenes = json.load(open("production/pantheon-ep4-scenes.json"))

by_scene = defaultdict(list)
for d in data:
    by_scene[d["scene_idx"]].append(d)

CARD_DIR = "output/ep4-namecards"
SEG_DIR = "output/ep4-segments"

n = 0
total = len(by_scene)
for scene_idx, cards in sorted(by_scene.items()):
    n += 1
    sc = scenes[scene_idx]
    seg_path = f"{SEG_DIR}/{scene_idx:04d}_{sc['shot']}.mp4"
    if not os.path.exists(seg_path):
        print(f"MISSING SEGMENT: {seg_path}")
        sys.exit(1)

    tmp_out = seg_path + ".namecard.mp4"

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
            # Prepend chroma-key-green padding so this card's visible
            # content starts at start_s on the shared scene timeline,
            # instead of relying on overlay's enable gating + setpts
            # (less robust -- frame availability before an input's first
            # shifted PTS is not well-defined across ffmpeg versions).
            filter_parts.append(
                f"[{i}:v]tpad=start_duration={start_s}:start_mode=add:color=0x00FF00[pad{i}]"
            )
            src = f"pad{i}"
        else:
            src = f"{i}:v"
        # similarity=0.38/blend=0.15: a hard edge between the card's near-
        # black box (#0A0908) and the pure green backdrop leaves 1-2
        # compression-blurred transition pixels that aren't close enough to
        # pure green to key at the stricter 0.35/0.08 (visible as a thin
        # solid-green line down the box's edge in every card). This setting
        # softens that fringe to near-invisible without touching the box's
        # own opaque content -- verified pixel-by-pixel against the
        # MANETHO card's right edge.
        filter_parts.append(f"[{src}]colorkey=0x00FF00:0.38:0.15[{keyed}]")
        # eof_action=pass (not the default "repeat"): once a card's clip
        # ends, repeat would freeze its last frame -- which, mid-slide-out,
        # is still a partial sliver of the card clipped at x=0 -- as a
        # permanent overlay for the rest of the scene. pass instead makes
        # overlay fall through to the untouched main input once the card
        # input is exhausted. Verified against scene 25 (Alara -> Kashta).
        filter_parts.append(f"[{last_label}][{keyed}]overlay=0:0:eof_action=pass[{out_label}]")
        last_label = out_label

    filter_complex = ";".join(filter_parts)
    cmd = (
        ["ffmpeg", "-y"] + inputs +
        ["-filter_complex", filter_complex, "-map", f"[{last_label}]", "-map", "0:a",
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "veryfast",
         "-c:a", "aac", tmp_out]
    )
    names = ", ".join(c["name"] for c in cards)
    print(f"[{n}/{total}] scene {scene_idx} ({sc['shot']}): {names}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", r.stderr[-2500:])
        sys.exit(1)
    os.replace(tmp_out, seg_path)

print("ALL_NAMECARD_OVERLAYS_DONE")
