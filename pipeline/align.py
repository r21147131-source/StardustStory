"""Step 1: transcribe the narration and align it to the episode script.

Produces build/alignment.json: a flat list of every spoken word with its
start/end time in seconds, taken from faster-whisper's word-level timestamps
and then snapped onto the script's own text so downstream steps can look up
"when was word N of the script spoken" reliably even where the ASR transcript
differs slightly from the script (numbers, punctuation, mishearings).
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from rapidfuzz import fuzz

from . import config

# Markdown/production markup that never gets spoken.
_STRIP_LINE_RE = re.compile(r"^\s*\[[^\]]+\]\s*$")          # [SECTION HEADER]
_STRIP_TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}(:\d{2})?\b")
_STRIP_STAGE_NOTE_RE = re.compile(r"\(([^)]*)\)")            # (stage note)
_WORD_RE = re.compile(r"[A-Za-z0-9'’-]+")


@dataclass
class Word:
    index: int
    text: str
    start: float
    end: float
    script_word: bool  # True if matched to a script token, False if ASR-only


def clean_script_to_spoken_text(raw: str) -> str:
    """Strip headers, timestamps, and stage notes; keep only spoken lines."""
    lines, _ = _clean_with_sections(raw)
    return "\n".join(lines)


def extract_sections(raw: str) -> list[dict]:
    """Return [{title, start_word_index}] for each [SECTION] header, where
    start_word_index indexes into script_tokens(clean_script_to_spoken_text(raw))."""
    lines, sections = _clean_with_sections(raw)
    word_count = 0
    out = []
    for title, line_idx in sections:
        preceding_text = "\n".join(lines[:line_idx])
        word_count = len(script_tokens(preceding_text))
        out.append({"title": title, "start_word_index": word_count})
    return out


def _clean_with_sections(raw: str) -> tuple[list[str], list[tuple[str, int]]]:
    lines: list[str] = []
    sections: list[tuple[str, int]] = []  # (title, index into `lines`)
    for line in raw.splitlines():
        header = _STRIP_LINE_RE.match(line)
        if header:
            sections.append((line.strip().strip("[]"), len(lines)))
            continue
        line = _STRIP_STAGE_NOTE_RE.sub("", line)
        line = _STRIP_TIMESTAMP_RE.sub("", line)
        line = line.strip()
        # Drop markdown headings ("# Title") and blank/rule lines.
        if not line or line.startswith("#") or set(line) <= {"-", "="}:
            continue
        lines.append(line)
    return lines, sections


def script_tokens(spoken_text: str) -> List[str]:
    return _WORD_RE.findall(spoken_text)


def transcribe(audio_path: Path) -> List[dict]:
    """Run faster-whisper and return a flat list of {text, start, end}."""
    from faster_whisper import WhisperModel

    model_size = "small.en"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _info = model.transcribe(
        str(audio_path), word_timestamps=True, vad_filter=True,
    )
    words: List[dict] = []
    for seg in segments:
        for w in seg.words or []:
            words.append({
                "text": w.word.strip(),
                "start": float(w.start),
                "end": float(w.end),
            })
    return words


def align(script_tokens_: List[str], asr_words: List[dict]) -> List[Word]:
    """Greedy monotonic alignment of script tokens onto ASR words.

    Whisper's transcript is the timing source; the script is the text source.
    We walk both sequences with a small look-ahead window and fuzzy-match so
    minor ASR errors (misheard names, numerals vs digits) don't break sync.
    """
    aligned: List[Word] = []
    ai = 0
    window = 6
    for si, stok in enumerate(script_tokens_):
        best_j, best_score = None, 0.0
        for j in range(ai, min(ai + window, len(asr_words))):
            score = fuzz.ratio(stok.lower(), asr_words[j]["text"].lower())
            if score > best_score:
                best_score, best_j = score, j
        if best_j is not None and best_score >= 60:
            w = asr_words[best_j]
            aligned.append(Word(si, stok, w["start"], w["end"], True))
            ai = best_j + 1
        elif aligned:
            # No confident ASR match: interpolate a zero-length stamp just
            # after the previous word so downstream lookups still resolve.
            prev = aligned[-1]
            aligned.append(Word(si, stok, prev.end, prev.end, False))
        else:
            aligned.append(Word(si, stok, 0.0, 0.0, False))
    return aligned


def run(script_path: Path, audio_path: Path) -> Path:
    raw = script_path.read_text()
    spoken = clean_script_to_spoken_text(raw)
    tokens = script_tokens(spoken)
    asr_words = transcribe(audio_path)
    aligned = align(tokens, asr_words)

    sections = extract_sections(raw)
    for sec in sections:
        idx = min(sec["start_word_index"], len(aligned) - 1)
        sec["start_time"] = aligned[idx].start if aligned else 0.0

    out = {
        "script_path": str(script_path),
        "audio_path": str(audio_path),
        "spoken_text": spoken,
        "words": [asdict(w) for w in aligned],
        "sections": sections,
    }
    out_path = config.DIR_BUILD / "alignment.json"
    out_path.write_text(json.dumps(out, indent=2))
    unmatched = sum(1 for w in aligned if not w.script_word)
    print(f"[align] {len(aligned)} words aligned, {unmatched} unmatched "
          f"(interpolated) -> {out_path}")
    return out_path


if __name__ == "__main__":
    import sys
    run(Path(sys.argv[1]), Path(sys.argv[2]))
