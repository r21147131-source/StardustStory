"""Step 2: detect every MOVIE/SHOW and PERSON mention in the script and map
each one to its exact spoken timestamp via build/alignment.json.

Two-pass detection, per the brief ("NER + a manual pass"):
  1. Automatic: spaCy NER when a model is installed, else a title-case /
     quoted-phrase heuristic. Both are best-effort — neither needs network
     access at run time once a spaCy model is pre-installed.
  2. Manual: an optional script/<slug>.entities.json file the editor curates
     (exact name, type, year, aliases). Manual entries always win over
     automatic guesses for the same span, and are the recommended way to
     get reliable results in an environment where NER models can't be
     downloaded on demand (logged to build/decisions.md when that happens).

Composite mentions ("the Duffer Brothers") are split into individual PERSON
entities via ALIAS_SPLITS, all sharing the one spoken span.
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Optional

from . import config

# Built-in composite-mention splits. Extend per-episode via
# script/<slug>.aliases.json (same shape, merged on top of this).
ALIAS_SPLITS: dict[str, list[str]] = {
    "the duffer brothers": ["Matt Duffer", "Ross Duffer"],
    "duffer brothers": ["Matt Duffer", "Ross Duffer"],
    "the russo brothers": ["Anthony Russo", "Joe Russo"],
    "russo brothers": ["Anthony Russo", "Joe Russo"],
    "the coen brothers": ["Joel Coen", "Ethan Coen"],
    "coen brothers": ["Joel Coen", "Ethan Coen"],
    "the wachowskis": ["Lana Wachowski", "Lilly Wachowski"],
}

# Words that are capitalized because they start a sentence, not because
# they're a name/title — used to suppress false positives in the regex path.
_SENTENCE_STARTERS = {
    "the", "this", "that", "he", "she", "they", "it", "then", "and", "but",
    "here", "now", "today", "not", "nobody", "no", "quinn", "within",
}

_QUOTED_RE = re.compile(r"[“\"]([^”\"]{2,80})[”\"]")
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_TITLECASE_RUN_RE = re.compile(
    r"\b([A-Z][a-zA-Z']*(?:\s+(?:[A-Z][a-zA-Z']*|of|the|and))*\s+[A-Z][a-zA-Z']*)\b"
)
_SEASON_RE = re.compile(r"\s+Season\s+\d+\b", re.IGNORECASE)
_YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


@dataclass
class Entity:
    type: str                    # "MOVIE" | "SHOW" | "PERSON"
    name: str                    # as spoken
    canonical_title: Optional[str]
    canonical_person: Optional[str]
    year: Optional[int]
    mention_start: float
    mention_end: float
    sentence_start: float
    sentence_end: float
    source: str                  # "manual" | "spacy" | "heuristic" | "alias_split"


def _load_alignment() -> dict:
    path = config.DIR_BUILD / "alignment.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — run pipeline.align first (Step 1)."
        )
    return json.loads(path.read_text())


def _sentence_bounds(spoken_text: str, words: list[dict]) -> list[tuple[int, int]]:
    """Return (first_word_idx, last_word_idx) for each sentence, by index
    into `words` (which is 1:1 with the tokenized spoken_text)."""
    from .align import _WORD_RE, script_tokens  # reuse the same tokenizer

    tokens = script_tokens(spoken_text)
    bounds = []
    start = 0
    # Recompute sentence breaks on the original text by walking tokens and
    # checking the character immediately following each token's match.
    pos = 0
    sent_start_idx = 0
    for i, tok in enumerate(tokens):
        m = _WORD_RE.search(spoken_text, pos)
        end = m.end() if m else pos
        pos = end
        tail = spoken_text[end:end + 2]
        if re.match(r"^[.!?]", tail.strip()[:1] or ""):
            bounds.append((sent_start_idx, i))
            sent_start_idx = i + 1
    if sent_start_idx <= len(tokens) - 1:
        bounds.append((sent_start_idx, len(tokens) - 1))
    return bounds


def _word_index_of_sentence(bounds: list[tuple[int, int]], idx: int) -> tuple[int, int]:
    for s, e in bounds:
        if s <= idx <= e:
            return s, e
    return idx, idx


def _spacy_candidates(spoken_text: str) -> list[tuple[str, str]]:
    """Return (text, label) pairs from spaCy NER, or [] if unavailable."""
    try:
        import spacy
        if not spacy.util.is_package("en_core_web_sm"):
            return []
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        return []
    doc = nlp(spoken_text)
    out = []
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "WORK_OF_ART", "ORG"):
            out.append((ent.text, ent.label_))
    return out


def _heuristic_candidates(spoken_text: str) -> list[tuple[str, str]]:
    """Quoted phrases -> titles. Multi-word Title Case runs -> ambiguous,
    classified PERSON/TITLE by a couple of cheap positional cues. Runs
    per-sentence so a run never spans a sentence boundary."""
    out = []
    for m in _QUOTED_RE.finditer(spoken_text):
        out.append((m.group(1).strip(), "WORK_OF_ART"))
    for sentence in _SENTENCE_SPLIT_RE.split(spoken_text):
        for m in _TITLECASE_RUN_RE.finditer(sentence):
            phrase = m.group(1).strip()
            first_word = phrase.split()[0].lower()
            if first_word in _SENTENCE_STARTERS:
                continue
            if len(phrase.split()) < 2:
                continue
            # crude heuristic: 2 capitalized words with no connector -> person name
            label = "PERSON" if len(phrase.split()) == 2 and " of " not in phrase and " the " not in phrase.lower() else "WORK_OF_ART"
            out.append((phrase, label))
    return out


def _find_span(tokens: list[str], phrase: str) -> Optional[tuple[int, int]]:
    ptoks = phrase.split()
    n = len(ptoks)
    for i in range(len(tokens) - n + 1):
        if all(tokens[i + k].lower() == ptoks[k].lower().strip("'\".,") for k in range(n)):
            return i, i + n - 1
    return None


def _apply_alias_splits(name: str) -> Optional[list[str]]:
    key = name.lower().strip()
    if key in ALIAS_SPLITS:
        return ALIAS_SPLITS[key]
    for k, v in ALIAS_SPLITS.items():
        if k in key:
            return v
    return None


def _load_manual_overrides(slug: str) -> list[dict]:
    path = config.DIR_SCRIPT / f"{slug}.entities.json"
    if not path.exists():
        return []
    return json.loads(path.read_text())


def _load_alias_overrides(slug: str) -> None:
    path = config.DIR_SCRIPT / f"{slug}.aliases.json"
    if path.exists():
        ALIAS_SPLITS.update(json.loads(path.read_text()))


def run(slug: str) -> Path:
    data = _load_alignment()
    words = data["words"]
    tokens = [w["text"] for w in words]
    spoken_text = data["spoken_text"]
    bounds = _sentence_bounds(spoken_text, words)
    _load_alias_overrides(slug)

    decisions: list[str] = []
    candidates = _spacy_candidates(spoken_text)
    if candidates:
        source = "spacy"
    else:
        decisions.append(
            "entities: spaCy model unavailable (no network to fetch "
            "en_core_web_sm in this environment) — used title-case/quoted "
            "heuristic NER instead. Add script/<slug>.entities.json to "
            "correct any misses."
        )
        candidates = _heuristic_candidates(spoken_text)
        source = "heuristic"

    manual = _load_manual_overrides(slug)
    entities: list[Entity] = []
    seen_spans: set[tuple[int, int]] = set()

    def emit(name: str, etype: str, year: Optional[int], span: tuple[int, int], src: str):
        si, ei = span
        ws, we = words[si]["start"], words[ei]["end"]
        sb, se = _word_index_of_sentence(bounds, si)
        ss, se_ = words[sb]["start"], words[se]["end"]
        splits = _apply_alias_splits(name) if etype == "PERSON" else None
        if splits:
            for person in splits:
                entities.append(Entity(
                    "PERSON", name, None, person, year, ws, we, ss, se_,
                    "alias_split",
                ))
        else:
            entities.append(Entity(
                "MOVIE" if etype in ("WORK_OF_ART", "MOVIE", "SHOW") else "PERSON",
                name,
                name if etype in ("WORK_OF_ART", "MOVIE", "SHOW") else None,
                None if etype in ("WORK_OF_ART", "MOVIE", "SHOW") else name,
                year, ws, we, ss, se_, src,
            ))

    for m in manual:
        span = _find_span(tokens, m["name"])
        if not span:
            decisions.append(f"entities: manual entry '{m['name']}' not found "
                              f"in spoken text; skipped.")
            continue
        seen_spans.add(span)
        emit(m["name"], m["type"], m.get("year"), span, "manual")

    for name, label in candidates:
        clean = _SEASON_RE.sub("", name).strip()
        span = _find_span(tokens, clean) or _find_span(tokens, name)
        if not span or span in seen_spans:
            continue
        year_m = _YEAR_RE.search(name)
        year = int(year_m.group(0)) if year_m else None
        emit(clean, label, year, span, source)
        seen_spans.add(span)

    entities.sort(key=lambda e: e.mention_start)
    out_path = config.DIR_BUILD / "entities.json"
    out_path.write_text(json.dumps([asdict(e) for e in entities], indent=2))

    if decisions:
        dpath = config.DIR_BUILD / "decisions.md"
        with dpath.open("a") as f:
            for d in decisions:
                f.write(f"- {d}\n")

    print(f"[entities] {len(entities)} entities detected "
          f"({sum(1 for e in entities if e.type=='PERSON')} people, "
          f"{sum(1 for e in entities if e.type=='MOVIE')} titles) -> {out_path}")
    return out_path


if __name__ == "__main__":
    import sys
    run(sys.argv[1])
