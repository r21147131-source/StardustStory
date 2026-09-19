"""Step 3: resolve each entity to a concrete visual source.

MOVIE/SHOW -> ranked, deduped shots from footage/movies/<Title (Year)>/,
              scene-detected, face-ranked, OCR-filtered; TMDB backdrop
              Ken-Burns fallback when no local footage exists.
PERSON     -> TMDB portrait, background-removed, composited into a 2.5D
              parallax shot over a blurred backdrop from their best-known
              title.
no entity  -> caller (edl.py) continues the current source or falls back
              to Joseph-Quinn-style subject B-roll; this module only
              resolves entities, it doesn't fill gaps.
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

from . import config, tmdb_client as tmdb

try:
    import cv2
    import numpy as np
except ImportError:
    cv2 = None
    np = None


@dataclass
class Shot:
    source_file: str
    start: float
    end: float
    has_face: bool = False
    motion_score: float = 0.0
    rejected_reason: Optional[str] = None


def _log_missing(title: str, kind: str, reason: str) -> None:
    path = config.DIR_BUILD / "missing_footage.md"
    header = "# Missing / fallback footage\n\n" if not path.exists() else ""
    with path.open("a") as f:
        if header:
            f.write(header)
        f.write(f"- **{title}** ({kind}): {reason}\n")


def _find_footage_dir(title: str, year: Optional[int]) -> Optional[Path]:
    candidates = list(config.DIR_FOOTAGE.glob("*"))
    wanted = f"{title} ({year})".lower() if year else title.lower()
    for c in candidates:
        if not c.is_dir():
            continue
        name = c.name.lower()
        if name == wanted or name.startswith(title.lower()):
            return c
    return None


def detect_shots(video_path: Path, cache_key: str) -> list[Shot]:
    cache_path = config.DIR_SHOTS / f"{cache_key}.json"
    if cache_path.exists():
        return [Shot(**s) for s in json.loads(cache_path.read_text())]

    from scenedetect import open_video, SceneManager
    from scenedetect.detectors import ContentDetector

    video = open_video(str(video_path))
    duration = video.duration.get_seconds()
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(video)
    scene_list = scene_manager.get_scene_list()

    head_tail = config.SKIP_FOOTAGE_HEAD_TAIL_S
    shots: list[Shot] = []
    for start_tc, end_tc in scene_list:
        s, e = start_tc.get_seconds(), end_tc.get_seconds()
        if s < head_tail or e > duration - head_tail:
            continue
        if e - s < config.MIN_SHOT_S:
            continue
        shots.append(Shot(str(video_path), s, e))

    cache_path.write_text(json.dumps([asdict(s) for s in shots], indent=2))
    return shots


def _sample_frame(video_path: str, t: float):
    if cv2 is None:
        return None
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, frame = cap.read()
    cap.release()
    return frame if ok else None


def _has_burned_in_text(frame) -> bool:
    """OCR check for subtitles / on-screen text (lower third of frame)."""
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        return False
    if frame is None:
        return False
    h, w = frame.shape[:2]
    lower = frame[int(h * 0.75):, :]
    rgb = cv2.cvtColor(lower, cv2.COLOR_BGR2RGB) if cv2 else lower
    text = pytesseract.image_to_string(Image.fromarray(rgb)).strip()
    return len(text) >= 3


def _motion_score(video_path: str, s: float, e: float) -> float:
    if cv2 is None:
        return 0.0
    f1 = _sample_frame(video_path, s + (e - s) * 0.25)
    f2 = _sample_frame(video_path, s + (e - s) * 0.75)
    if f1 is None or f2 is None:
        return 0.0
    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(g1, g2)
    return float(diff.mean())


def _has_reference_face(frame, reference_encodings) -> bool:
    try:
        import face_recognition
    except ImportError:
        return False
    if frame is None or not reference_encodings:
        return False
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    locations = face_recognition.face_locations(rgb)
    if not locations:
        return False
    encodings = face_recognition.face_encodings(rgb, locations)
    for enc in encodings:
        matches = face_recognition.compare_faces(reference_encodings, enc, tolerance=0.5)
        if any(matches):
            return True
    return False


def load_reference_encodings(person_name: str) -> list:
    try:
        import face_recognition
    except ImportError:
        return []
    ref_dir = config.DIR_PEOPLE / person_name.lower().replace(" ", "_")
    encodings = []
    if ref_dir.exists():
        for img_path in ref_dir.glob("*.jpg"):
            img = face_recognition.load_image_file(str(img_path))
            found = face_recognition.face_encodings(img)
            if found:
                encodings.append(found[0])
    return encodings


def rank_shots_for_movie(title: str, year: Optional[int], lead_person: str,
                          used_shots: set[str]) -> list[Shot]:
    footage_dir = _find_footage_dir(title, year)
    if footage_dir is None:
        _log_missing(title, "MOVIE/SHOW", "no local footage folder found — "
                     "falling back to TMDB backdrop Ken Burns.")
        return []

    files = list(footage_dir.glob("*.mp4")) + list(footage_dir.glob("*.mkv"))
    if not files:
        _log_missing(title, "MOVIE/SHOW", f"footage folder {footage_dir} is "
                     "empty — falling back to TMDB backdrop Ken Burns.")
        return []

    ref_encodings = load_reference_encodings(lead_person)
    all_shots: list[Shot] = []
    for f in files:
        cache_key = f"{title}_{f.stem}".replace(" ", "_").replace("/", "_")
        for shot in detect_shots(f, cache_key):
            key = f"{shot.source_file}:{shot.start:.2f}"
            if key in used_shots:
                continue
            mid = (shot.start + shot.end) / 2
            frame = _sample_frame(shot.source_file, mid)
            if _has_burned_in_text(frame):
                shot.rejected_reason = "burned-in text/subtitles"
                continue
            shot.has_face = _has_reference_face(frame, ref_encodings)
            shot.motion_score = _motion_score(shot.source_file, shot.start, shot.end)
            all_shots.append(shot)

    all_shots.sort(key=lambda s: (not s.has_face, -s.motion_score))
    return all_shots


def _local_person_dir(person_name: str) -> Path:
    return config.DIR_PEOPLE / person_name.lower().replace(" ", "_")


def _find_local_portrait(person_name: str) -> Optional[Path]:
    """A locally supplied photo always wins over TMDB — drop it at
    assets/people/<name>/portrait.(jpg|png) (or any single image in that
    folder), or assets/people/<name>_portrait.jpg directly."""
    person_dir = _local_person_dir(person_name)
    if person_dir.is_dir():
        named = person_dir / "portrait.jpg"
        if named.exists():
            return named
        named = person_dir / "portrait.png"
        if named.exists():
            return named
        for img in sorted(person_dir.glob("*.jpg")) + sorted(person_dir.glob("*.png")):
            return img
    flat = config.DIR_PEOPLE / f"{person_name.lower().replace(' ', '_')}_portrait.jpg"
    return flat if flat.exists() else None


def _find_local_backdrop(person_name: str) -> Optional[Path]:
    person_dir = _local_person_dir(person_name)
    if person_dir.is_dir():
        for name in ("backdrop.jpg", "backdrop.png"):
            candidate = person_dir / name
            if candidate.exists():
                return candidate
    flat = config.DIR_PEOPLE / f"{person_name.lower().replace(' ', '_')}_backdrop.jpg"
    return flat if flat.exists() else None


def resolve_person_portrait(person_name: str) -> Optional[dict]:
    local_portrait = _find_local_portrait(person_name)
    if local_portrait:
        local_backdrop = _find_local_backdrop(person_name)
        return {
            "portrait": str(local_portrait),
            "backdrop": str(local_backdrop) if local_backdrop else str(local_portrait),
            "tmdb_id": None,
        }

    person = tmdb.search_person(person_name)
    if not person:
        _log_missing(person_name, "PERSON", "no local photo in "
                     f"{_local_person_dir(person_name)}/, and TMDB search "
                     "returned no match (or TMDB unreachable) — no portrait "
                     "available.")
        return None

    images = tmdb.person_images(person["id"])
    if not images:
        _log_missing(person_name, "PERSON", "TMDB has no profile images for "
                     "this person.")
        return None

    best = images[0]
    dest = config.DIR_PEOPLE / f"{person_name.lower().replace(' ', '_')}_portrait.jpg"
    if not dest.exists():
        tmdb.download_image(best["file_path"], dest)

    credits = tmdb.person_combined_credits(person["id"])
    backdrop_path = None
    for credit in credits:
        cid = credit.get("id")
        is_tv = credit.get("media_type") == "tv"
        backdrops = tmdb.tv_images(cid) if is_tv else tmdb.movie_images(cid)
        if backdrops:
            backdrop_path = backdrops[0]["file_path"]
            break

    backdrop_dest = None
    if backdrop_path:
        backdrop_dest = config.DIR_PEOPLE / f"{person_name.lower().replace(' ', '_')}_backdrop.jpg"
        if not backdrop_dest.exists():
            tmdb.download_image(backdrop_path, backdrop_dest)

    return {
        "portrait": str(dest) if dest.exists() else None,
        "backdrop": str(backdrop_dest) if backdrop_dest and backdrop_dest.exists() else None,
        "tmdb_id": person["id"],
    }


def resolve_title_fallback_backdrop(title: str, year: Optional[int], is_tv: bool) -> Optional[Path]:
    result = tmdb.search_tv(title) if is_tv else tmdb.search_movie(title, year)
    if not result:
        return None
    images = tmdb.tv_images(result["id"]) if is_tv else tmdb.movie_images(result["id"])
    if not images:
        return None
    dest = config.DIR_TMDB_CACHE / f"{title.lower().replace(' ', '_')}_backdrop.jpg"
    if not dest.exists():
        tmdb.download_image(images[0]["file_path"], dest)
    return dest if dest.exists() else None


def build_parallax_person_shot(person_name: str, assets: dict, out_path: Path,
                                duration: float) -> Optional[Path]:
    """rembg-cut subject layer + blurred/darkened backdrop, slow push-in."""
    portrait = assets.get("portrait")
    backdrop = assets.get("backdrop") or portrait
    if not portrait:
        return None

    try:
        from rembg import remove
    except ImportError:
        _log_missing(person_name, "PERSON", "rembg not installed — used flat "
                     "portrait instead of 2.5D parallax cutout.")
        subject_path = Path(portrait)
    else:
        subject_path = config.DIR_PEOPLE / f"{Path(portrait).stem}_cutout.png"
        if not subject_path.exists():
            data = Path(portrait).read_bytes()
            subject_path.write_bytes(remove(data))

    w, h = config.WIDTH, config.HEIGHT
    fps = config.FPS
    frames = int(duration * fps)
    zoom_expr = f"'min(zoom+0.0007,1.15)'"
    filter_complex = (
        f"[1:v]scale={w*1.2}:-1,boxblur=20:1,eq=brightness=-0.12,"
        f"zoompan=z={zoom_expr}:d={frames}:s={w}x{h}:fps={fps}[bg];"
        f"[0:v]scale=-1:{int(h*0.9)}[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)*0.55:shortest=1[out]"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", str(subject_path),
        "-loop", "1", "-i", str(backdrop),
        "-filter_complex", filter_complex, "-map", "[out]",
        "-t", str(duration), "-r", str(fps),
        "-c:v", "libx264", "-crf", str(config.CRF), "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
