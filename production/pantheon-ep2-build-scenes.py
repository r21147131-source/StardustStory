import json, math

BASE = "https://raw.githubusercontent.com/r21147131-source/StardustStory/claude/younger-dryas-impact-doc-yoy0v3/public/"

shots = json.load(open("/home/user/StardustStory/production/pantheon-ep2-shot-list-final.json"))
by_id = {s["id"]: s for s in shots}

GRAPHIC_FILE = {
    "S02": "EP2-S02-BridgeTimeline.mp4",
    "S06": "EP2-S06-TasTepelerMap.mp4",
    "S10": "EP2-S10-ComparativeTimeline.mp4",
    "S11": "EP2-S11-InvertedSequenceBars.mp4",
    "S15": "EP2-S15-LaborConvergence.mp4",
    "S19": "EP2-S19-VultureStoneOverlay.mp4",
    "S23": "EP2-S23-AgricultureSpreadMap.mp4",
    "S24": "EP2-S24-EinkornComparison.mp4",
    "S28": "EP2-S28-ClosingStatCard.mp4",
    "S29": "EP2-S29-LogoCard.mp4",
    "S30": "EP2-S30-CitationCrawl.mp4",
}

# source clip durations measured via ffprobe
AI_SRC_DUR = {
    "pantheon-ep2-clips/S03a-aerial-enclosure-construction.mp4": 4.54,
    "pantheon-ep2-clips/S05a-hunter-band-dusk-gazelle-herd.mp4": 5.5,
    "pantheon-ep2-clips/S08a-archaeologist-recognition-hillside.mp4": 10.04,
    "pantheon-ep2-clips/S17a-night-feast-firelight-pillars.mp4": 10.04,
    "pantheon-ep2-clips/S20a-vulture-stone-pushin.mp4": 10.04,
    "pantheon-ep2-clips/S22a-burial-pouring-rubble-twopillars.mp4": 10.04,
    "pantheon-ep2-clips/S22b-burial-dense-fill-carved-pillar.mp4": 10.04,
    "pantheon-ep2-clips/S25a-camp-to-settlement-timelapse.mp4": 10.04,
    "pantheon-ep2-clips/S27a-modern-site-sunset-aerial.mp4": 10.04,
    "pantheon-ep2-clips/S13a-stone-pillar-hauling-canyon-angle1.mp4": 10.04,
    "pantheon-ep2-clips/S13b-stone-pillar-hauling-canyon-angle2.mp4": 10.04,
    "pantheon-ep2-clips/S13c-stone-pillar-hauling-quarry-wide.mp4": 10.04,
}

def img_or_vid(path):
    return "image" if path.lower().endswith((".jpg", ".jpeg", ".png", ".webp")) else "video"

order = [s["id"] for s in shots]  # already in narration order
scenes = []

for sid in order:
    s = by_id[sid]
    final_dur = s["final_dur"]

    if sid in GRAPHIC_FILE:
        fname = GRAPHIC_FILE[sid]
        scenes.append({
            "shot": sid, "type": "video",
            "source": BASE + "pantheon-ep2-motion-graphics/" + fname,
            "duration": round(final_dur, 2),
        })
        continue

    if sid == "S13":
        paths = s["src"]
        each = final_dur / len(paths)
        for p in paths:
            scenes.append({"shot": sid, "type": "video", "source": BASE + p, "duration": round(each, 2)})
        continue

    if sid == "S12":
        p = s["src"][0]  # primary local photo
        scenes.append({"shot": sid, "type": "image", "source": BASE + p, "duration": round(final_dur, 2)})
        continue

    src = s["src"]
    if isinstance(src, list):
        src = src[0]

    if src.startswith("http"):
        # archival image hotlinked from the web
        scenes.append({"shot": sid, "type": img_or_vid(src), "source": src, "duration": round(final_dur, 2)})
        continue

    kind = img_or_vid(src)
    full_url = BASE + src
    if kind == "image":
        scenes.append({"shot": sid, "type": "image", "source": full_url, "duration": round(final_dur, 2)})
    else:
        src_dur = AI_SRC_DUR[src]
        if final_dur <= src_dur + 0.05:
            scenes.append({"shot": sid, "type": "video", "source": full_url, "duration": round(final_dur, 2)})
        else:
            n = math.ceil(final_dur / src_dur)
            per = final_dur / n
            for _ in range(n):
                scenes.append({"shot": sid, "type": "video", "source": full_url, "duration": round(per, 2)})

total = sum(sc["duration"] for sc in scenes)
print(f"Total scenes: {len(scenes)}  Total duration: {total:.2f}s")

# split into <=240s segments
segments = []
cur = []
cur_dur = 0.0
for sc in scenes:
    if cur and cur_dur + sc["duration"] > 240.0:
        segments.append(cur)
        cur = []
        cur_dur = 0.0
    cur.append(sc)
    cur_dur += sc["duration"]
if cur:
    segments.append(cur)

offset = 0.0
for i, seg in enumerate(segments, 1):
    seg_dur = sum(sc["duration"] for sc in seg)
    print(f"Segment {i}: {len(seg)} scenes, {seg_dur:.2f}s, VO offset {offset:.2f}s")
    payload = {
        "scenes": [{k: v for k, v in sc.items() if k != "shot"} for sc in seg],
        "format": "landscape",
        "voiceover": {
            "audioUrl": BASE + "pantheon-ep2-voiceover.mp3",
            "trimStartSeconds": round(offset, 2),
            "durationSeconds": round(seg_dur, 2),
        },
    }
    json.dump(payload, open(f"/home/user/StardustStory/production/pantheon-ep2-compose-segment-{i}.json", "w"), indent=2)
    offset += seg_dur

print(f"\nGrand total: {offset:.2f}s")
