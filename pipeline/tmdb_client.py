"""Thin TMDB client with on-disk caching and graceful degradation.

Every call is wrapped so a network failure (no key, no egress, rate limit,
no match) never crashes the pipeline: it logs the miss and returns None /
[] so callers fall back per the brief (local footage -> TMDB stills ->
logged in build/missing_footage.md).
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Optional

import requests

from . import config

_session = requests.Session()
_warned_no_key = False
_warned_unreachable = False


def _cache_path(key: str) -> Path:
    h = hashlib.sha1(key.encode()).hexdigest()
    return config.DIR_TMDB_CACHE / f"{h}.json"


def _get(endpoint: str, params: Optional[dict] = None) -> Optional[dict]:
    global _warned_no_key, _warned_unreachable
    params = dict(params or {})

    if not config.TMDB_API_KEY:
        if not _warned_no_key:
            _log_decision("tmdb: TMDB_API_KEY not set (.env) — all TMDB "
                           "lookups skipped, local-only fallback used.")
            _warned_no_key = True
        return None

    cache_key = f"{endpoint}?{json.dumps(params, sort_keys=True)}"
    cpath = _cache_path(cache_key)
    if cpath.exists():
        return json.loads(cpath.read_text())

    params["api_key"] = config.TMDB_API_KEY
    url = f"{config.TMDB_BASE}{endpoint}"
    try:
        resp = _session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        if not _warned_unreachable:
            _log_decision(
                f"tmdb: could not reach {config.TMDB_BASE} ({e.__class__.__name__}) "
                "— this sandbox's egress policy blocks api.themoviedb.org "
                "directly. Falls back to local footage / logs missing_footage.md "
                "for everything that needed a TMDB lookup. Run this pipeline "
                "somewhere with TMDB access to fill those in."
            )
            _warned_unreachable = True
        return None

    cpath.write_text(json.dumps(data))
    return data


def _log_decision(msg: str) -> None:
    path = config.DIR_BUILD / "decisions.md"
    with path.open("a") as f:
        f.write(f"- {msg}\n")


def search_movie(title: str, year: Optional[int] = None) -> Optional[dict]:
    params = {"query": title}
    if year:
        params["year"] = year
    data = _get("/search/movie", params)
    if not data or not data.get("results"):
        return None
    return data["results"][0]


def search_tv(title: str) -> Optional[dict]:
    data = _get("/search/tv", {"query": title})
    if not data or not data.get("results"):
        return None
    return data["results"][0]


def search_person(name: str) -> Optional[dict]:
    data = _get("/search/person", {"query": name})
    if not data or not data.get("results"):
        return None
    return data["results"][0]


def person_images(person_id: int) -> list[dict]:
    data = _get(f"/person/{person_id}/images")
    if not data:
        return []
    profiles = sorted(
        data.get("profiles", []),
        key=lambda p: (p.get("vote_average", 0), p.get("width", 0)),
        reverse=True,
    )
    return profiles


def person_combined_credits(person_id: int) -> list[dict]:
    data = _get(f"/person/{person_id}/combined_credits")
    if not data:
        return []
    cast = data.get("cast", [])
    return sorted(cast, key=lambda c: c.get("popularity", 0), reverse=True)


def movie_images(movie_id: int) -> list[dict]:
    data = _get(f"/movie/{movie_id}/images")
    if not data:
        return []
    return sorted(data.get("backdrops", []), key=lambda b: b.get("vote_average", 0), reverse=True)


def tv_images(tv_id: int) -> list[dict]:
    data = _get(f"/tv/{tv_id}/images")
    if not data:
        return []
    return sorted(data.get("backdrops", []), key=lambda b: b.get("vote_average", 0), reverse=True)


def image_url(file_path: str, size: str = "original") -> str:
    return f"{config.TMDB_IMG_BASE}/{size}{file_path}"


def download_image(file_path: str, dest: Path, size: str = "original") -> Optional[Path]:
    url = image_url(file_path, size)
    try:
        resp = _session.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(resp.content)
    return dest
