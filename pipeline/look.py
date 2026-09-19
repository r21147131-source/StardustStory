"""Step 5: the cinematic look — ffmpeg filter-chain builders shared by
render.py. Nothing here shells out; these functions return filter-graph
fragments (and drawtext card renderers) that render.py assembles per
segment and wires into `-filter_complex`.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional

from . import config

_font_cache: dict[str, str] = {}

# fc-match falls back to the system default (a plain sans) for a family it
# doesn't recognize at all, which is wrong for a display serif like Cinzel —
# ask for the right *generic* family instead so the substitute at least
# reads as a serif/display face rather than UI sans.
_GENERIC_FALLBACK = {"cinzel": "serif"}


def _hex_to_ffmpeg(hexcolor: str) -> str:
    return "0x" + hexcolor.lstrip("#")


def find_font(family: str) -> str:
    """Resolve a font family to a concrete file path, preferring an
    episode-supplied file in assets/fonts/, then the system store, and
    finally a serif substitute for Cinzel (logged once)."""
    if family in _font_cache:
        return _font_cache[family]

    for ext in ("ttf", "otf"):
        for candidate in config.DIR_FONTS.glob(f"*{family}*.{ext}"):
            _font_cache[family] = str(candidate)
            return _font_cache[family]

    fc = shutil.which("fc-match")
    if fc:
        query = _GENERIC_FALLBACK.get(family.lower(), family)
        try:
            out = subprocess.run([fc, "-f", "%{file}", query],
                                  capture_output=True, text=True, check=True).stdout
            if out.strip():
                resolved = out.strip()
                if family.lower() not in resolved.lower():
                    _log_decision(
                        f"look: font '{family}' not found (Google Fonts is "
                        f"blocked in this sandbox) — substituted "
                        f"'{resolved}'. Drop the real font family into "
                        f"assets/fonts/ to fix."
                    )
                _font_cache[family] = resolved
                return resolved
        except subprocess.CalledProcessError:
            pass

    _font_cache[family] = ""
    return ""


def _log_decision(msg: str) -> None:
    path = config.DIR_BUILD / "decisions.md"
    with path.open("a") as f:
        f.write(f"- {msg}\n")


# ---------------------------------------------------------------------------
# Unified finishing chain: grade + grain + vignette + halation
# ---------------------------------------------------------------------------

def cinematic_finish_filters() -> str:
    """Warm highlights / cool shadows via curves, lifted blacks + ~85% sat
    via eq, animated film grain, soft vignette, gentle bloom on highlights."""
    curves = (
        "curves=r='0/0.03 0.5/0.52 1/0.97':"
        "b='0/0 0.5/0.48 1/0.93'"
    )
    eq = "eq=brightness=0.02:saturation=0.85:gamma=1.0"
    blacks = "curves=all='0/0.05 0.5/0.5 1/1'"
    grain = "noise=alls=6:allf=t+u"
    vignette = "vignette=PI/5"
    # cheap bloom: blur highlights and screen-blend back over the original
    bloom = (
        "split=2[base][hi];"
        "[hi]curves=all='0/0 0.7/0 1/1',gblur=sigma=8[hib];"
        "[base][hib]blend=all_mode=screen:all_opacity=0.25"
    )
    return f"{curves},{eq},{blacks},{grain},{vignette},{bloom}"


def letterbox_filter(w: int = config.WIDTH, h: int = config.HEIGHT) -> str:
    """2.39:1 letterbox bars — movie footage only, never on graphics."""
    target_h = int(w / config.LETTERBOX_ASPECT)
    pad = (h - target_h) // 2
    return f"scale={w}:-2,crop={w}:{target_h},pad={w}:{h}:0:{pad}:black"


def ken_burns_filter(duration: float, w: int = config.WIDTH, h: int = config.HEIGHT,
                      fps: int = config.FPS, zoom_from: float = 1.00,
                      zoom_to: float = 1.08, pan: str = "auto") -> str:
    frames = max(1, int(duration * fps))
    zoom_step = (zoom_to - zoom_from) / frames
    x_exprs = {
        "center": "iw/2-(iw/zoom/2)",
        "left": "0",
        "right": "iw-(iw/zoom)",
    }
    x_expr = x_exprs.get(pan, x_exprs["center"])
    y_expr = "ih/2-(ih/zoom/2)"
    return (
        f"scale={w*2}:{h*2},"
        f"zoompan=z='min(zoom+{zoom_step:.6f},{zoom_to})':"
        f"x='{x_expr}':y='{y_expr}':d={frames}:s={w}x{h}:fps={fps}"
    )


# ---------------------------------------------------------------------------
# Text overlays (drawtext) — title cards, lower thirds, chapter cards, badge
# ---------------------------------------------------------------------------

def _drawtext(text: str, font: str, size: int, color: str, x: str, y: str,
              box: bool = False, box_color: str = "black@0.0",
              alpha_expr: Optional[str] = None) -> str:
    text = text.replace("'", "’").replace(":", "\\:")
    parts = [
        f"fontfile='{font}'" if font else "font=sans",
        f"text='{text}'",
        f"fontsize={size}",
        f"fontcolor={color}",
        f"x={x}",
        f"y={y}",
    ]
    if box:
        parts.append(f"box=1:boxcolor={box_color}")
    if alpha_expr:
        parts.append(f"alpha='{alpha_expr}'")
    return "drawtext=" + ":".join(parts)


def title_card_filter(title: str, year: Optional[int]) -> str:
    """Bottom-left movie/show title card: Cinzel gold title, Inter cream
    year, fade in/out 0.4s, 2.5s hold (caller sizes the enable window)."""
    cinzel = find_font("Cinzel")
    inter = find_font("Inter")
    fade = config.TITLE_CARD_FADE_S
    hold = config.TITLE_CARD_HOLD_S
    alpha = (
        f"if(lt(t,{fade}),t/{fade},"
        f"if(lt(t,{hold - fade}),1,"
        f"if(lt(t,{hold}),(({hold}-t)/{fade}),0)))"
    )
    layers = [_drawtext(title, cinzel, 42, _hex_to_ffmpeg(config.BRAND_GOLD),
                         "80", "h-160", alpha_expr=alpha)]
    if year:
        layers.append(_drawtext(str(year), inter, 24, _hex_to_ffmpeg(config.BRAND_CREAM),
                                 "80", "h-115", alpha_expr=alpha))
    return ",".join(layers)


def lower_third_filter(name: str, role: str = "") -> str:
    cinzel = find_font("Cinzel")
    inter = find_font("Inter")
    dur = config.LOWER_THIRD_S
    fade = 0.3
    alpha = (
        f"if(lt(t,{fade}),t/{fade},"
        f"if(lt(t,{dur - fade}),1,({dur}-t)/{fade}))"
    )
    gold = _hex_to_ffmpeg(config.BRAND_GOLD)
    cream = _hex_to_ffmpeg(config.BRAND_CREAM)
    layers = [
        f"drawbox=x=80:y=h-220:w=4:h=80:color={gold}@1:t=fill:enable='lt(t,{dur})'",
        _drawtext(name, cinzel, 34, gold, "100", "h-210", alpha_expr=alpha),
    ]
    if role:
        layers.append(_drawtext(role, inter, 20, cream, "100", "h-175", alpha_expr=alpha))
    return ",".join(layers)


def person_placeholder_filter(name: str) -> str:
    """Centered name card used when no real photo is available — a gold
    rule above and below the name, clearly a designed placeholder rather
    than a broken shot."""
    cinzel = find_font("Cinzel")
    gold = _hex_to_ffmpeg(config.BRAND_GOLD)
    layers = [
        _drawtext(name, cinzel, 46, gold, "(w-text_w)/2", "(h-text_h)/2"),
        "drawbox=x=(w-240)/2:y=(h/2)-52:w=240:h=2:color=" + gold + "@0.8:t=fill",
        "drawbox=x=(w-240)/2:y=(h/2)+52:w=240:h=2:color=" + gold + "@0.8:t=fill",
    ]
    return ",".join(layers)


def chapter_card_filter(title: str) -> str:
    cinzel = find_font("Cinzel")
    gold = _hex_to_ffmpeg(config.BRAND_GOLD)
    spaced = " · ".join(list(title.upper()))  # crude letter-spacing
    return _drawtext(spaced, cinzel, 30, gold, "(w-text_w)/2", "(h-text_h)/2")


def series_badge_filter(text: str) -> str:
    cinzel = find_font("Cinzel")
    gold = _hex_to_ffmpeg(config.BRAND_GOLD)
    dur = config.SERIES_BADGE_S
    alpha = f"if(lt(t,{dur - 0.5}),1,if(lt(t,{dur}),({dur}-t)/0.5,0))"
    return _drawtext(text, cinzel, 22, gold, "60", "50", alpha_expr=alpha)


def tagline_card_filter() -> str:
    cinzel = find_font("Cinzel")
    cream = _hex_to_ffmpeg(config.BRAND_CREAM)
    return _drawtext(config.TAGLINE, cinzel, 30, cream, "(w-text_w)/2", "(h-text_h)/2")
