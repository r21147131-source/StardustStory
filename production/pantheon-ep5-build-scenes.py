import json, math

shots = json.load(open("/home/user/StardustStory/production/pantheon-ep5-rome-shot-list-final.json"))
by_id = {s["id"]: s for s in shots}

GRAPHIC_ID_TO_FILE = {
    "B006": "EP5-B006-TitleCard", "B009": "EP5-B009-MapRoadsRule",
    "B013": "EP5-B013-MapEmpireSplits", "B014": "EP5-B014-MapEmpireSplitsLabels",
    "B020": "EP5-B020-MapCrossingRiver", "B021": "EP5-B021-MapArmyMasses",
    "B025": "EP5-B025-TollOfAdrianople", "B027": "EP5-B027-MapThreeMarches",
    "B030": "EP5-B030-MapFourthMarch", "B045": "EP5-B045-HandCutOff",
    "B050": "EP5-B050-Vandalism", "B052": "EP5-B052-NineEmperors",
    "B058": "EP5-B058-Map476Regalia", "B059": "EP5-B059-Date476Card",
    "B061": "EP5-B061-EndingContinues", "B063": "EP5-B063-MapSuccessorKingdoms",
    "B065": "EP5-B065-CrownShatters", "B066": "EP5-B066-CaesarShadow",
    "B067": "EP5-B067-CaesarCaption", "B069": "EP5-B069-ClosingThesis",
}

# ffprobe'd durations of every AI clip actually referenced by the shot list
AI_SRC_DUR = json.load(open(
    "/tmp/claude-0/-home-user-StardustStory/1e81929f-1efd-5891-adfc-4a1c8f67420f/scratchpad/ep5-clip-durs.json"
))

order = [s["id"] for s in shots]  # already in narration order (B000 pre-title first)
scenes = []

for sid in order:
    s = by_id[sid]
    final_dur = s["final_dur"]

    if sid in GRAPHIC_ID_TO_FILE:
        fname = f"pantheon-ep5-motion-graphics/{GRAPHIC_ID_TO_FILE[sid]}.mp4"
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

    # type == "ai" (includes B000, the silent pre-title beat)
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
print(f"Target (3.0s silent pre-roll + real VO 666.12s): 669.12s")

out_path = "/home/user/StardustStory/production/pantheon-ep5-scenes.json"
json.dump(scenes, open(out_path, "w"), indent=2, ensure_ascii=False)
print(f"Wrote {out_path}")
