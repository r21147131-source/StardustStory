import json

SHOT_LIST = "/home/user/StardustStory/production/pantheon-ep5-rome-shot-list.json"
REAL_VO_DUR = 666.120000  # ffprobe duration of the user-supplied voiceover mp3
WPM = 150  # matches the provisional-duration convention already used for the motion graphics

# Non-narrated beats (silent pre-roll, e.g. a cold-open establishing shot before
# the voiceover starts) get a fixed duration instead of a word-count estimate,
# and sit outside the VO-scaled pool entirely.
FIXED_DURATIONS = {"B000": 3.0}

shots = json.load(open(SHOT_LIST))

for s in shots:
    if s["id"] in FIXED_DURATIONS:
        continue
    s["est_dur"] = round(s["narration_words"] / WPM * 60, 3)

est_total = sum(s["est_dur"] for s in shots if s["id"] not in FIXED_DURATIONS)
scale = REAL_VO_DUR / est_total

print(f"Beats: {len(shots)}")
print(f"Estimated total (150wpm): {est_total:.2f}s")
print(f"Real voiceover: {REAL_VO_DUR:.2f}s")
print(f"Scale factor: {scale:.5f}")
print()

MAX_SHOT = 45.0
MIN_SHOT = 1.0
flagged_long = []
flagged_short = []

for s in shots:
    if s["id"] in FIXED_DURATIONS:
        s["final_dur"] = FIXED_DURATIONS[s["id"]]
        continue
    final = round(s["est_dur"] * scale, 2)
    if final > MAX_SHOT:
        flagged_long.append((s["id"], final))
    if final < MIN_SHOT:
        flagged_short.append((s["id"], final))
    s["final_dur"] = final

total = sum(s["final_dur"] for s in shots)
pre_roll = sum(FIXED_DURATIONS.values())
print(f"New total runtime: {total:.2f}s ({total/60:.2f} min), including {pre_roll:.1f}s silent pre-roll")
print(f"vs real VO target: {REAL_VO_DUR:.2f}s (VO starts after the {pre_roll:.1f}s pre-roll)")
print()

if flagged_long:
    print("Beats over MAX_SHOT (may need sub-clip splitting or a repeat loop):")
    for sid, dur in flagged_long:
        print(f"  {sid}: {dur:.2f}s")
if flagged_short:
    print("Beats under MIN_SHOT (very tight — check these cut cleanly):")
    for sid, dur in flagged_short:
        print(f"  {sid}: {dur:.2f}s")

out_path = SHOT_LIST.replace(".json", "-final.json")
json.dump(shots, open(out_path, "w"), indent=2, ensure_ascii=False)
print(f"\nWrote {out_path}")
