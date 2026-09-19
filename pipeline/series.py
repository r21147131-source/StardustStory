"""Step 6: series/channel elements layered on top of the base EDL —
mid-roll callback PiP, the clean final-20s frame for the YouTube end
screen, and the closing tagline card.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import config, assets_resolve as assets, look
from .edl import Segment


@dataclass
class CallbackEvent:
    time: float
    person_name: str
    series: str
    episode: int


def find_callbacks(entities: list[dict], series: str, episode: int) -> list[CallbackEvent]:
    """A PERSON entity mentioned in this script who was the subject of an
    earlier episode of the same series is an in-story callback."""
    index = config.SERIES_INDEX.get(series.upper(), {})
    prior_subjects = {name.lower(): ep for ep, name in index.items() if ep != episode}
    out = []
    seen = set()
    for e in entities:
        if e["type"] != "PERSON":
            continue
        name = e.get("canonical_person") or e["name"]
        key = name.lower()
        if key in prior_subjects and key not in seen:
            out.append(CallbackEvent(e["mention_start"], name, series, prior_subjects[key]))
            seen.add(key)
    return out


def apply_callback(segments: list[Segment], event: CallbackEvent) -> None:
    """Layer a PiP callback card on top of whatever is already showing
    during [event.time, event.time+5], rather than replacing it outright —
    the base visual keeps playing underneath the slide-in card."""
    portrait_assets = assets.resolve_person_portrait(event.person_name)
    if not portrait_assets or not portrait_assets.get("portrait"):
        return
    window_end = event.time + 5.0
    for s in segments:
        if s.end <= event.time or s.start >= window_end:
            continue
        s.extra_overlays.append({
            "kind": "callback_pip",
            "portrait": portrait_assets["portrait"],
            "name": event.person_name,
            "badge": f"{event.series.upper()} · EP {event.episode}",
            "window_start": event.time,
            "window_end": window_end,
        })


def apply_end_screen_darken(segments: list[Segment], total_duration: float) -> None:
    """Darken (don't replace) the last 20s so the video frame stays clean
    under YouTube's end-screen elements."""
    cutoff = total_duration - 20.0
    for s in segments:
        if s.end > cutoff:
            s.end_screen_darken = True


def tagline_segment(total_duration: float) -> Segment:
    return Segment(
        start=total_duration, end=total_duration + 4.0,
        source_type="tagline_card", source=None,
        effect="static", transition_in="dip_to_black",
        overlay={"kind": "tagline"},
    )


def apply(segments: list[Segment], entities: list[dict], series: str,
          episode: int, total_duration: float) -> list[Segment]:
    for ev in find_callbacks(entities, series, episode):
        apply_callback(segments, ev)
    apply_end_screen_darken(segments, total_duration)
    segments.append(tagline_segment(total_duration))
    segments.sort(key=lambda s: s.start)
    return segments
