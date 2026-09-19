"""Shared configuration and brand constants for the Stardust Story edit pipeline."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Directory layout (all paths relative to the repo root)
# ---------------------------------------------------------------------------
DIR_SCRIPT = ROOT / "script"
DIR_AUDIO = ROOT / "audio"
DIR_ASSETS = ROOT / "assets"
DIR_INTRO = DIR_ASSETS / "intro"
DIR_PEOPLE = DIR_ASSETS / "people"
DIR_FONTS = DIR_ASSETS / "fonts"
DIR_FOOTAGE = ROOT / "footage" / "movies"
DIR_MUSIC = ROOT / "music"
DIR_BUILD = ROOT / "build"
DIR_SHOTS = DIR_BUILD / "shots"
DIR_TMDB_CACHE = DIR_BUILD / "tmdb_cache"
DIR_OUTPUT = ROOT / "output"

for d in (DIR_SCRIPT, DIR_AUDIO, DIR_INTRO, DIR_PEOPLE, DIR_FONTS, DIR_FOOTAGE,
          DIR_MUSIC, DIR_BUILD, DIR_SHOTS, DIR_TMDB_CACHE, DIR_OUTPUT):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Brand
# ---------------------------------------------------------------------------
BRAND_BLACK = "#0A0A0A"
BRAND_GOLD = "#C9A84C"
BRAND_CREAM = "#F2E8D5"

FONT_PRIMARY = "Cinzel"          # titles / chapter cards / names
FONT_SECONDARY = "Inter"         # roles / captions / years

TAGLINE = "Fame creates stars. Time turns them into dust."

# Which real person each previous episode of a series was about, so
# pipeline/series.py can recognize an in-script callback ("...Pedro Pascal,
# the actor from episode one of this very series...") and build the
# mid-roll PiP card automatically. Extend this as new episodes ship.
SERIES_INDEX: dict[str, dict[int, str]] = {
    "GOLDEN FOUR": {
        1: "Pedro Pascal",
        2: "Joseph Quinn",
    },
}

# ---------------------------------------------------------------------------
# Render spec
# ---------------------------------------------------------------------------
WIDTH = 1920
HEIGHT = 1080
FPS = 24
CRF = 18
AUDIO_BITRATE = "320k"
LETTERBOX_ASPECT = 2.39 / 1  # applied to movie footage only

TARGET_LUFS = -14.0
MUSIC_DUCK_DB = -18.0

# ---------------------------------------------------------------------------
# Editorial rhythm
# ---------------------------------------------------------------------------
MIN_SHOT_S = 1.5
DEFAULT_SHOT_MIN_S = 2.0
DEFAULT_SHOT_MAX_S = 6.0
AVG_SHOT_S = (3.0, 4.0)
REFLECTIVE_SHOT_S = (5.0, 7.0)
MONTAGE_SHOT_S = (1.5, 2.5)
MAX_CONTINUOUS_FILM_S = 6.0
PRE_ROLL_ENTITY_S = 0.3  # visual starts this far before the word is spoken

TRANSITIONS = [
    "hard_cut",
    "cross_dissolve",       # 0.5s, between related shots
    "dip_to_black",         # 0.8s, between script sections
    "light_leak",           # 0.4s, major career turns
    "whip_pan",             # montage only, max 5 per episode
]
MAX_WHIP_PANS = 5

TITLE_CARD_HOLD_S = 2.5
TITLE_CARD_FADE_S = 0.4
LOWER_THIRD_S = 3.0
CHAPTER_CARD_S = 2.0
SERIES_BADGE_S = 8.0  # after intro

SKIP_FOOTAGE_HEAD_TAIL_S = 6 * 60  # skip first/last 6 minutes of source films

# ---------------------------------------------------------------------------
# TMDB
# ---------------------------------------------------------------------------
TMDB_API_KEY = os.environ.get("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG_BASE = "https://image.tmdb.org/t/p"
TMDB_ATTRIBUTION = (
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)


def load_dotenv(path: Path = ROOT / ".env") -> None:
    """Minimal .env loader so TMDB_API_KEY (and friends) reach os.environ."""
    global TMDB_API_KEY
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)
    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")


@dataclass
class EpisodeContext:
    """Everything a build run needs to know about the episode being cut."""
    series: str
    episode: int
    script_path: Path
    audio_path: Path
    slug: str = field(init=False)

    def __post_init__(self) -> None:
        self.slug = self.script_path.stem.lower().replace(" ", "_")

    @property
    def badge_text(self) -> str:
        return f"{self.series.upper()} · EP {self.episode}"

    @property
    def output_dir(self) -> Path:
        return DIR_OUTPUT

    def output_path(self, name: str, suffix: str) -> Path:
        return DIR_OUTPUT / f"{self.slug}_{name}{suffix}"
