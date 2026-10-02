import json

SHOT_LIST = "/home/user/StardustStory/production/pantheon-ep2-shot-list.json"
REAL_VO_DUR = 614.870204
TAIL_IDS = {"S29", "S30"}  # fixed, not scaled (logo card, citation crawl)

shots = json.load(open(SHOT_LIST))

spoken = [s for s in shots if s["id"] not in TAIL_IDS]
tail = [s for s in shots if s["id"] in TAIL_IDS]

est_spoken_total = sum(s["est_dur"] for s in spoken)
tail_total = sum(s["est_dur"] for s in tail)
scale = REAL_VO_DUR / est_spoken_total

print(f"Estimated spoken total: {est_spoken_total:.2f}s")
print(f"Real voiceover: {REAL_VO_DUR:.2f}s")
print(f"Scale factor: {scale:.5f}")
print(f"Tail (logo+citations, fixed): {tail_total:.2f}s")
print()

MAX_SHOT = 45.0
flagged = []

for s in spoken:
    final = round(s["est_dur"] * scale, 2)
    if final > MAX_SHOT:
        flagged.append((s["id"], final))
    s["final_dur"] = final

for s in tail:
    s["final_dur"] = s["est_dur"]

total = sum(s["final_dur"] for s in shots)
print(f"New total runtime: {total:.2f}s ({total/60:.2f} min)")
print(f"vs real VO + tail target: {REAL_VO_DUR + tail_total:.2f}s")
print()

if flagged:
    print("Shots over MAX_SHOT (may need sub-clip splitting or a repeat loop):")
    for sid, dur in flagged:
        print(f"  {sid}: {dur:.2f}s")

json.dump(shots, open(SHOT_LIST.replace(".json", "-final.json"), "w"), indent=2)
print(f"\nWrote {SHOT_LIST.replace('.json', '-final.json')}")
