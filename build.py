#!/usr/bin/env python3
"""Stardust Story automated edit pipeline.

    python build.py --script script/joseph_quinn.md --audio audio/narration.mp3 \\
        --series "GOLDEN FOUR" --ep 2 [--render]

Without --render, stops after Step 4 (the EDL + build/edl_preview.html
review gate) and waits — re-run with --render once you've reviewed it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from pipeline import config, align, entities, edl, series, render


REQUIRED_INPUT_HELP = {
    "script": "the episode script (Markdown, [SECTION] headers ok)",
    "audio": "the final voiceover — the timing source of truth for every cut",
}


def check_inputs(script_path: Path, audio_path: Path) -> list[str]:
    missing = []
    if not script_path.exists():
        missing.append(f"script file not found: {script_path} "
                        f"({REQUIRED_INPUT_HELP['script']})")
    if not audio_path.exists():
        missing.append(f"audio file not found: {audio_path} "
                        f"({REQUIRED_INPUT_HELP['audio']})")
    if not list(config.DIR_INTRO.glob("*.mp4")) and not list(config.DIR_INTRO.glob("*.mov")):
        missing.append(f"no channel intro in {config.DIR_INTRO}/ — will render "
                        f"WITHOUT the intro bumper unless you add one")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--audio", required=True, type=Path)
    parser.add_argument("--series", required=True)
    parser.add_argument("--ep", required=True, type=int)
    parser.add_argument("--render", action="store_true",
                         help="skip the review gate and render the final master")
    args = parser.parse_args()

    config.load_dotenv()

    hard_missing = [m for m in check_inputs(args.script, args.audio) if "WITHOUT" not in m]
    if hard_missing:
        print("Cannot start — missing required input(s):", file=sys.stderr)
        for m in hard_missing:
            print(f"  - {m}", file=sys.stderr)
        return 2
    for m in check_inputs(args.script, args.audio):
        if "WITHOUT" in m:
            print(f"[warn] {m}")

    ctx = config.EpisodeContext(series=args.series, episode=args.ep,
                                 script_path=args.script, audio_path=args.audio)

    print(f"=== Step 1/8: alignment ===")
    align.run(ctx.script_path, ctx.audio_path)

    print(f"=== Step 2/8: entity detection ===")
    entities.run(ctx.slug)

    print(f"=== Step 3/8+4/8: asset resolution + EDL ===")
    segments = edl.build(ctx.slug)

    print(f"=== Step 6/8: series/channel elements ===")
    import json
    entities_data = json.loads((config.DIR_BUILD / "entities.json").read_text())
    alignment_data = json.loads((config.DIR_BUILD / "alignment.json").read_text())
    total_duration = alignment_data["words"][-1]["end"] if alignment_data["words"] else 0.0
    segments = series.apply(segments, entities_data, args.series, args.ep, total_duration)

    edl.write_edl(segments, ctx.slug)
    edl.write_preview_html(segments, ctx.slug)

    if not args.render:
        print()
        print(f"EDL ready for review: {config.DIR_BUILD / 'edl_preview.html'}")
        print("Re-run with --render once you've reviewed it "
              "(or run with --render up front to skip the gate).")
        return 0

    print(f"=== Step 5/8+7/8+8/8: render ===")
    result = render.render_episode(segments, ctx.audio_path, ctx)
    render.write_chapters(segments, alignment_data, ctx)
    render.write_credits(ctx)

    print()
    print(f"Done: {result['final']}")
    print(f"Chapters: {ctx.output_path('chapters', '.txt')}")
    print(f"Missing-footage log: {config.DIR_BUILD / 'missing_footage.md'}")
    print(f"Decisions log: {config.DIR_BUILD / 'decisions.md'}")
    print(f"Credits: {config.DIR_BUILD / 'credits.txt'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
