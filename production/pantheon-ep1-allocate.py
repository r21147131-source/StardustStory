"""
Reconciles production/pantheon-ep1-shot-list.json against the actual
recorded voiceover duration, same pattern as golden-four-ep2-allocate.py.

Usage, once public/pantheon-voiceover.<ext> exists:
    ffprobe -v error -show_entries format=duration -of csv=p=0 public/pantheon-voiceover.m4a
    # then set TOTAL below to that number and run:
    python3 production/pantheon-ep1-allocate.py

What it does:
  - Loads the word-count-estimated durations from pantheon-ep1-shot-list.json
    (these are a rough proxy, not exact — real narration has pauses, breath,
    emphasis that a flat words-per-second rate can't capture).
  - Scales every non-fixed shot proportionally so the total matches the
    real voiceover length exactly.
  - Leaves fixed-duration cues (transitions, brand, credits) alone unless
    they'd overflow the fallback max.
  - Writes production/pantheon-ep1-shot-list-final.json for the compose step.

This does NOT know where each shot actually falls against the real audio
waveform — for a precise cut, re-time cues by ear/transcript against the
actual recording (e.g. via Whisper word timestamps) rather than trusting
pure proportional scaling once the real file exists.
"""
import json
import sys

SHOT_LIST = "production/pantheon-ep1-shot-list.json"
OUT = "production/pantheon-ep1-shot-list-final.json"

# Fill in once the real voiceover is recorded/uploaded and measured with ffprobe.
TOTAL = None  # e.g. 645.2

FIXED_TYPES = {"transition", "brand"}
MIN_SHOT = 2.0
MAX_SHOT = 35.0


def main():
    if TOTAL is None:
        print("Set TOTAL to the real voiceover duration (seconds) before running.")
        print("  ffprobe -v error -show_entries format=duration -of csv=p=0 <voiceover file>")
        sys.exit(1)

    with open(SHOT_LIST) as f:
        shots = json.load(f)

    fixed = [s for s in shots if s["type"] in FIXED_TYPES]
    flexible = [s for s in shots if s["type"] not in FIXED_TYPES]

    fixed_total = sum(s["est_dur"] for s in fixed)
    flexible_est_total = sum(s["est_dur"] for s in flexible)
    target_flexible_total = TOTAL - fixed_total

    if target_flexible_total <= 0:
        print("Fixed-duration cues alone exceed the target total — check TOTAL.")
        sys.exit(1)

    scale = target_flexible_total / flexible_est_total
    print(f"Voiceover total: {TOTAL:.2f}s | Fixed cues: {fixed_total:.2f}s | "
          f"Scaling {len(flexible)} flexible cues by {scale:.3f}x")

    for s in flexible:
        s["final_dur"] = round(min(MAX_SHOT, max(MIN_SHOT, s["est_dur"] * scale)), 2)
    for s in fixed:
        s["final_dur"] = s["est_dur"]

    out = fixed + flexible
    out.sort(key=lambda s: int(s["id"][1:]))

    final_total = sum(s["final_dur"] for s in out)
    print(f"Final total: {final_total:.2f}s (target {TOTAL:.2f}s, "
          f"diff {TOTAL - final_total:+.2f}s)")

    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
