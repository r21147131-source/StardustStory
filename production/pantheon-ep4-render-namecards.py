import json, subprocess, sys

# Renders one 110-frame EP4-NameCard clip per unique person in
# pantheon-ep4-names.json, against solid chroma-key green (see
# src/graphics/Ep4NameCard.tsx). Output feeds pantheon-ep4-apply-namecards.py.
data = json.load(open("production/pantheon-ep4-names.json"))
seen = {}
for d in data:
    seen[d["key"]] = d

out_dir = "output/ep4-namecards"

for i, (key, d) in enumerate(seen.items(), 1):
    props = json.dumps({"name": d["name"], "role": d["role"]})
    out_path = f"{out_dir}/{key}.mp4"
    cmd = [
        "npx", "remotion", "render", "EP4-NameCard", out_path,
        "--props=" + props, "--log=error",
    ]
    print(f"[{i}/{len(seen)}] {key} -> {out_path}")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FAILED:", r.stderr[-2000:])
        sys.exit(1)

print("ALL_NAMECARDS_DONE")
