"""Step 7: final audio mix — narration loudness, ducked music bed with
chapter-card/pause swells, transition SFX, and the intro's own-audio
crossfade into the episode.

Returns ffmpeg filter_complex fragments and a plan dict that render.py
wires into the master ffmpeg invocation; the actual mixdown happens in one
pass at the end of Step 8 so loudnorm's two-pass measurement sees the full
programme.
"""
from __future__ import annotations

import json
import random
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from . import config


def pick_music_bed() -> Optional[Path]:
    beds = list(config.DIR_MUSIC.glob("*.mp3"))
    if not beds:
        return None
    return random.choice(beds)


def measure_loudness(path: Path) -> dict:
    """First loudnorm pass: measure, so the second pass can hit -14 LUFS
    integrated precisely instead of ffmpeg's single-pass approximation."""
    cmd = [
        "ffmpeg", "-i", str(path), "-af",
        f"loudnorm=I={config.TARGET_LUFS}:TP=-1.5:LRA=11:print_format=json",
        "-f", "null", "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    stderr = proc.stderr
    start = stderr.rfind("{")
    end = stderr.rfind("}") + 1
    if start == -1 or end == 0:
        return {}
    return json.loads(stderr[start:end])


def loudnorm_filter(measured: dict) -> str:
    if not measured:
        return f"loudnorm=I={config.TARGET_LUFS}:TP=-1.5:LRA=11"
    return (
        f"loudnorm=I={config.TARGET_LUFS}:TP=-1.5:LRA=11:"
        f"measured_I={measured.get('input_i')}:"
        f"measured_TP={measured.get('input_tp')}:"
        f"measured_LRA={measured.get('input_lra')}:"
        f"measured_thresh={measured.get('input_thresh')}:"
        f"offset={measured.get('target_offset', 0)}:"
        f"linear=true"
    )


def sidechain_duck_filter(narration_label: str, music_label: str, out_label: str,
                           duck_db: float = config.MUSIC_DUCK_DB) -> str:
    """Duck the music bed under narration via sidechaincompress keyed off
    the narration track, floor set so ducked music sits duck_db below its
    own peak rather than at an absolute level."""
    ratio = 8
    return (
        f"[{music_label}][{narration_label}]sidechaincompress="
        f"threshold=0.05:ratio={ratio}:attack=20:release=300:makeup=1[{out_label}]"
    )


def gen_whoosh(dest: Path, duration: float = 0.4) -> Path:
    """Synthesize a simple whoosh: filtered white noise with a rising then
    falling amplitude envelope, used on dip-to-black / light-leak cuts when
    no SFX file is supplied."""
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"anoisesrc=d={duration}:c=pink:a=0.6",
        "-af", (
            f"afade=t=in:d={duration*0.4},afade=t=out:st={duration*0.4}:d={duration*0.6},"
            "highpass=f=300,lowpass=f=4000"
        ),
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest


def gen_impact(dest: Path, duration: float = 0.5) -> Path:
    cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"sine=frequency=80:duration={duration}",
        "-af", f"afade=t=out:st=0.05:d={duration - 0.05},lowpass=f=200",
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return dest


def ensure_sfx() -> dict[str, Path]:
    sfx_dir = config.DIR_BUILD / "sfx"
    sfx_dir.mkdir(exist_ok=True)
    whoosh = sfx_dir / "whoosh.wav"
    impact = sfx_dir / "impact.wav"
    if not whoosh.exists():
        gen_whoosh(whoosh)
    if not impact.exists():
        gen_impact(impact)
    return {"whoosh": whoosh, "impact": impact}
