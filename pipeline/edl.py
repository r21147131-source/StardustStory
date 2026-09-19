"""Step 4: build the Edit Decision List and its HTML review preview.

Turns build/alignment.json + build/entities.json into build/edl.json: a
flat, time-ordered list of segments (source, in/out point, effect,
transition-in, overlay) covering the full narration timeline, cut to the
rhythm of the voiceover. Also renders build/edl_preview.html and returns
control to build.py, which pauses for the operator's "render" go-ahead.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional

from . import config, assets_resolve as assets

MONTAGE_SECTION_HINTS = {"sprint", "montage", "rise"}
REFLECTIVE_SECTION_HINTS = {"early life", "reflect", "legacy", "cold open"}
LIGHT_LEAK_HINTS = {"break", "casting", "fantastic four", "announcement"}


@dataclass
class Segment:
    start: float
    end: float
    source_type: str          # "movie" | "person" | "filler" | "chapter_card" | "tagline_card"
    source: Optional[str]
    in_point: float = 0.0
    out_point: float = 0.0
    effect: str = "none"       # "ken_burns" | "parallax" | "static" | "none"
    transition_in: str = "hard_cut"
    overlay: Optional[dict] = None
    entity_name: Optional[str] = None
    # Composable overlays that ride on top of whatever is already showing
    # (e.g. a mid-roll callback PiP over an ongoing filler/movie segment)
    # rather than replacing the segment outright.
    extra_overlays: list = field(default_factory=list)
    end_screen_darken: bool = False


def _load(name: str) -> dict | list:
    path = config.DIR_BUILD / name
    if not path.exists():
        raise FileNotFoundError(f"{path} missing — run earlier pipeline steps first.")
    return json.loads(path.read_text())


def _section_for_time(sections: list[dict], t: float) -> Optional[dict]:
    current = None
    for sec in sections:
        if sec["start_time"] <= t:
            current = sec
        else:
            break
    return current


def _pace_for_section(section: Optional[dict]) -> tuple[float, float]:
    if not section:
        return config.AVG_SHOT_S
    title = section["title"].lower()
    if any(h in title for h in MONTAGE_SECTION_HINTS):
        return config.MONTAGE_SHOT_S
    if any(h in title for h in REFLECTIVE_SECTION_HINTS):
        return config.REFLECTIVE_SHOT_S
    return config.AVG_SHOT_S


def _snap_to_word(words: list[dict], t: float, prefer: str = "start") -> float:
    """Snap a cut point onto the nearest word boundary so cuts never land
    mid-word."""
    best = t
    best_dist = float("inf")
    for w in words:
        for cand in (w["start"], w["end"]):
            d = abs(cand - t)
            if d < best_dist:
                best_dist, best = d, cand
    return best


def _split_window(start: float, end: float, words: list[dict], section: Optional[dict]) -> list[tuple[float, float]]:
    lo, hi = _pace_for_section(section)
    target = (lo + hi) / 2
    cuts = [start]
    t = start
    while t < end - config.MIN_SHOT_S:
        nxt = min(t + target, end)
        nxt = _snap_to_word(words, nxt)
        if nxt <= cuts[-1] + config.MIN_SHOT_S:
            nxt = min(t + target, end)
        cuts.append(nxt)
        t = nxt
    if cuts[-1] < end:
        cuts.append(end)
    return list(zip(cuts, cuts[1:]))


def _transition_for(prev_entity: Optional[str], entity_name: Optional[str],
                     section_changed: bool, section: Optional[dict],
                     is_montage: bool, whip_count: list[int]) -> str:
    if section_changed:
        title = (section["title"].lower() if section else "")
        if any(h in title for h in LIGHT_LEAK_HINTS):
            return "light_leak"
        return "dip_to_black"
    if is_montage and whip_count[0] < config.MAX_WHIP_PANS:
        whip_count[0] += 1
        return "whip_pan"
    if prev_entity and entity_name and prev_entity == entity_name:
        return "cross_dissolve"
    return "hard_cut"


def build(slug: str, used_shots: Optional[set[str]] = None) -> list[Segment]:
    alignment = _load("alignment.json")
    entities = _load("entities.json")
    words = alignment["words"]
    sections = alignment["sections"]
    total_duration = words[-1]["end"] if words else 0.0
    used_shots = used_shots if used_shots is not None else set()

    # One coverage window per entity mention, non-overlapping, in time order.
    entities = sorted(entities, key=lambda e: e["mention_start"])
    windows = []
    for i, e in enumerate(entities):
        cov_start = max(0.0, e["mention_start"] - config.PRE_ROLL_ENTITY_S)
        cov_end = entities[i + 1]["mention_start"] - config.PRE_ROLL_ENTITY_S \
            if i + 1 < len(entities) else total_duration
        cov_end = max(cov_end, cov_start + config.MIN_SHOT_S)
        windows.append((cov_start, cov_end, e))

    segments: list[Segment] = []
    seen_titles: set[str] = set()
    seen_people: set[str] = set()
    prev_entity_name: Optional[str] = None
    whip_count = [0]
    decisions: list[str] = []

    # The episode's subject (for face-recognition shot ranking) is whoever
    # is named most often — far more robust than "whoever is named first".
    person_counts: dict[str, int] = {}
    for e in entities:
        if e["type"] == "PERSON":
            n = e.get("canonical_person") or e["name"]
            person_counts[n] = person_counts.get(n, 0) + 1
    lead_person = max(person_counts, key=person_counts.get) if person_counts else ""

    # Any stretch with no entity mentioned (before the first mention, or
    # after the last) falls back to the episode subject's own B-roll.
    subject_backdrop = None
    if lead_person:
        subject_assets = assets.resolve_person_portrait(lead_person)
        if subject_assets:
            subject_backdrop = subject_assets.get("backdrop") or subject_assets.get("portrait")

    cursor = 0.0
    if windows and windows[0][0] > 0:
        segments.append(Segment(0.0, windows[0][0], "filler", subject_backdrop,
                                 effect="ken_burns", transition_in="hard_cut"))
        cursor = windows[0][0]

    for idx, (cov_start, cov_end, e) in enumerate(windows):
        if cov_start < cursor:
            cov_start = cursor
        if cov_end <= cov_start:
            continue
        section = _section_for_time(sections, cov_start)
        section_changed = (idx == 0) or (
            _section_for_time(sections, windows[idx - 1][0]) is not section
        )
        title_lower = (section["title"].lower() if section else "")
        is_montage = any(h in title_lower for h in MONTAGE_SECTION_HINTS)

        name = e.get("canonical_person") or e.get("canonical_title") or e["name"]
        transition = _transition_for(prev_entity_name, name, section_changed,
                                      section, is_montage, whip_count)

        overlay = None
        if e["type"] == "MOVIE" and name not in seen_titles:
            overlay = {"kind": "title_card", "title": name, "year": e.get("year")}
            seen_titles.add(name)
        elif e["type"] == "PERSON" and name not in seen_people:
            overlay = {"kind": "lower_third", "name": name}
            seen_people.add(name)

        if e["type"] == "MOVIE":
            shots = assets.rank_shots_for_movie(e.get("canonical_title") or name,
                                                 e.get("year"), lead_person, used_shots)
            t = cov_start
            first = True
            if not shots:
                segments.append(Segment(
                    cov_start, cov_end, "filler", name, effect="ken_burns",
                    transition_in=transition, overlay=overlay, entity_name=name,
                ))
            else:
                for shot in shots:
                    if t >= cov_end:
                        break
                    dur = min(config.MAX_CONTINUOUS_FILM_S, shot.end - shot.start,
                              cov_end - t)
                    if dur < 1.0:
                        continue
                    key = f"{shot.source_file}:{shot.start:.2f}"
                    used_shots.add(key)
                    segments.append(Segment(
                        t, t + dur, "movie", shot.source_file,
                        in_point=shot.start, out_point=shot.start + dur,
                        effect="none", transition_in=transition if first else "hard_cut",
                        overlay=overlay if first else None, entity_name=name,
                    ))
                    first = False
                    t += dur
                if t < cov_end:
                    segments.append(Segment(t, cov_end, "filler", name,
                                             effect="ken_burns", transition_in="hard_cut",
                                             entity_name=name))
        elif e["type"] == "PERSON":
            segments.append(Segment(
                cov_start, cov_end, "person", name, effect="parallax",
                transition_in=transition, overlay=overlay, entity_name=name,
            ))
        else:
            segments.append(Segment(
                cov_start, cov_end, "filler", name, effect="ken_burns",
                transition_in=transition, overlay=overlay, entity_name=name,
            ))

        prev_entity_name = name
        cursor = cov_end

    if cursor < total_duration:
        segments.append(Segment(cursor, total_duration, "filler", subject_backdrop,
                                 effect="ken_burns", transition_in="hard_cut"))

    # Chapter cards on section boundaries that land on a real narration
    # pause (>= 2.2s gap); otherwise a quick top-of-frame title overlay so
    # we never desync from the voiceover, which is the timing source of
    # truth. See build/decisions.md.
    for sec in sections:
        gap = _pause_at(words, sec["start_time"])
        if gap and gap[1] - gap[0] >= 2.2:
            segments.append(Segment(
                gap[0], gap[0] + config.CHAPTER_CARD_S, "chapter_card", sec["title"],
                effect="static", transition_in="dip_to_black",
                overlay={"kind": "chapter_card", "title": sec["title"]},
            ))
            segments.sort(key=lambda s: s.start)
        else:
            decisions.append(
                f"edl: no >=2.2s narration pause at section '{sec['title']}' "
                "boundary — used a quick top-of-frame chapter title overlay "
                "instead of a full black-screen chapter card, to stay in "
                "sync with the voiceover (timing source of truth)."
            )

    if decisions:
        with (config.DIR_BUILD / "decisions.md").open("a") as f:
            for d in decisions:
                f.write(f"- {d}\n")

    return segments


def _pause_at(words: list[dict], t: float, window: float = 1.0) -> Optional[tuple[float, float]]:
    for i in range(len(words) - 1):
        if abs(words[i]["end"] - t) < window:
            gap_start, gap_end = words[i]["end"], words[i + 1]["start"]
            if gap_end > gap_start:
                return gap_start, gap_end
    return None


def write_edl(segments: list[Segment], slug: str) -> Path:
    out_path = config.DIR_BUILD / "edl.json"
    out_path.write_text(json.dumps([asdict(s) for s in segments], indent=2))
    print(f"[edl] {len(segments)} segments -> {out_path}")
    return out_path


def write_preview_html(segments: list[Segment], slug: str) -> Path:
    rows = []
    for i, s in enumerate(segments):
        overlay = s.overlay["kind"] if s.overlay else ""
        rows.append(
            f"<tr><td>{i}</td><td>{s.start:.2f}</td><td>{s.end:.2f}</td>"
            f"<td>{s.end - s.start:.2f}s</td><td>{s.source_type}</td>"
            f"<td>{(s.source or '')[-40:]}</td><td>{s.effect}</td>"
            f"<td>{s.transition_in}</td><td>{overlay}</td></tr>"
        )
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{slug} EDL preview</title>
<style>
body{{font-family:Inter,Arial,sans-serif;background:{config.BRAND_BLACK};color:{config.BRAND_CREAM};margin:2rem}}
h1{{color:{config.BRAND_GOLD};font-family:Georgia,serif}}
table{{border-collapse:collapse;width:100%;font-size:13px}}
td,th{{border:1px solid #333;padding:6px 8px;text-align:left}}
th{{background:#151515;color:{config.BRAND_GOLD}}}
tr:nth-child(even){{background:#111}}
</style></head><body>
<h1>{slug} &middot; Edit Decision List preview</h1>
<p>{len(segments)} segments, total {segments[-1].end:.1f}s. Review, then reply
"render" to build the final master.</p>
<table><tr><th>#</th><th>start</th><th>end</th><th>dur</th><th>type</th>
<th>source</th><th>effect</th><th>transition in</th><th>overlay</th></tr>
{''.join(rows)}
</table></body></html>"""
    out_path = config.DIR_BUILD / "edl_preview.html"
    out_path.write_text(html)
    print(f"[edl] preview -> {out_path}")
    return out_path


def run(slug: str) -> tuple[Path, Path]:
    segments = build(slug)
    edl_path = write_edl(segments, slug)
    preview_path = write_preview_html(segments, slug)
    return edl_path, preview_path


if __name__ == "__main__":
    import sys
    run(sys.argv[1])
