import json, subprocess, sys

# Renders one 110-frame EP5-OverlayCard clip per unique key in
# pantheon-ep5-overlays.json, against solid chroma-key green (see
# src/graphics/Ep5OverlayCard.tsx). Output feeds
# pantheon-ep5-apply-overlays.py.
data = json.load(open("production/pantheon-ep5-overlays.json"))

out_dir = "output/ep5-overlays"

for i, d in enumerate(data, 1):
    props = {"kind": d["kind"], "line1": d["line1"]}
    if "line2" in d:
        props["line2"] = d["line2"]
    out_path = f"{out_dir}/{d['key']}.mp4"
    cmd = [
        "npx", "remotion", "render", "EP5-OverlayCard", out_path,
        "--props=" + json.dumps(props), "--log=error",
    ]
    print(f"[{i}/{len(data)}] {d['key']} -> {out_path}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", r.stderr[-2000:])
        sys.exit(1)

print("ALL_OVERLAYS_DONE")
