import json, math

shots = json.load(open("/home/user/StardustStory/production/pantheon-ep4-shot-list-final.json"))
by_id = {s["id"]: s for s in shots}

GRAPHIC_ID_TO_FILE = {
    "B008": "EP4-B008-MapEgyptKush", "B011": "EP4-B011-TitleCard",
    "B017": "EP4-B017-MapEgyptCracks", "B019": "EP4-B019-MapKushGrows",
    "B022": "EP4-B022-MapAlaraKashta", "B026": "EP4-B026-MapCoalitionMarches",
    "B027": "EP4-B027-MapMemphisHerakleopolis", "B030": "EP4-B030-MapArmyFollowsPiye",
    "B039": "EP4-B039-MemphisHarborSchematic", "B056": "EP4-B056-MapEmpireGlows",
    "B062": "EP4-B062-MapAssyriaSpreads", "B069": "EP4-B069-AssyrianTimeline",
    "B083": "EP4-B083-ErasureSequence", "B084": "EP4-B084-MapNapataDims",
    "B091": "EP4-B091-KandakeTypography", "B093": "EP4-B093-RomeKushTerms",
    "B102": "EP4-B102-KingListScroll", "B103": "EP4-B103-ErasureRepeat",
    "B106": "EP4-B106-MeroiticScript", "B110": "EP4-B110-NamesRefill",
}

# ffprobe'd durations of every AI clip actually referenced by the shot list
AI_SRC_DUR = json.load(open(
    "/tmp/claude-0/-home-user-StardustStory/1e81929f-1efd-5891-adfc-4a1c8f67420f/scratchpad/ep4-clip-durs.json"
))

def img_or_vid(path):
    return "image" if path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) else "video"

order = [s["id"] for s in shots]  # already in narration order
scenes = []

for sid in order:
    s = by_id[sid]
    final_dur = s["final_dur"]

    if sid == "B049":
        # Cutaway insert nested inside B048's narration window (no runtime of
        # its own per the shot list notes) — borrow a slice from the previous
        # scene instead of adding a zero-duration entry.
        borrow = min(4.0, scenes[-1]["duration"] - 2.0) if scenes else 0
        if borrow > 0:
            scenes[-1]["duration"] = round(scenes[-1]["duration"] - borrow, 2)
        src = s["src"]
        scenes.append({"shot": sid, "type": "video", "source": src, "duration": round(borrow, 2) if borrow > 0 else 1.5})
        continue

    if sid in GRAPHIC_ID_TO_FILE:
        fname = f"pantheon-ep4-motion-graphics/{GRAPHIC_ID_TO_FILE[sid]}.mp4"
        scenes.append({"shot": sid, "type": "video", "source": fname, "duration": round(final_dur, 2)})
        continue

    src = s["src"]
    if s["type"] == "archival":
        if isinstance(src, list):
            each = final_dur / len(src)
            for p in src:
                scenes.append({"shot": sid, "type": "image", "source": p, "duration": round(each, 2)})
        else:
            scenes.append({"shot": sid, "type": "image", "source": src, "duration": round(final_dur, 2)})
        continue

    # type == "ai"
    if isinstance(src, list):
        each = final_dur / len(src)
        for p in src:
            src_dur = AI_SRC_DUR.get(p)
            scenes.append({"shot": sid, "type": "video", "source": p, "duration": round(each, 2), "_native": src_dur})
        continue

    src_dur = AI_SRC_DUR.get(src)
    if src_dur is None:
        print(f"WARNING: no probed duration for {sid} -> {src}")
        scenes.append({"shot": sid, "type": "video", "source": src, "duration": round(final_dur, 2)})
        continue

    if final_dur <= src_dur + 0.05:
        scenes.append({"shot": sid, "type": "video", "source": src, "duration": round(final_dur, 2), "_native": src_dur})
    else:
        n = math.ceil(final_dur / src_dur)
        per = final_dur / n
        for _ in range(n):
            scenes.append({"shot": sid, "type": "video", "source": src, "duration": round(per, 2), "_native": src_dur})

total = sum(sc["duration"] for sc in scenes)
print(f"Total scenes: {len(scenes)}  Total duration: {total:.2f}s")
print(f"Target (real VO): 759.43s")

out_path = "/home/user/StardustStory/production/pantheon-ep4-scenes.json"
json.dump(scenes, open(out_path, "w"), indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
