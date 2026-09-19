"""Step 8: render every segment, stitch them together with real transitions
(handle-extended so the programme length never drifts from the narration
timeline), mix the audio, mux, and write the final outputs.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from . import config, look, audiomix, assets_resolve as assets
from .edl import Segment

XFADE_DURATIONS = {
    "hard_cut": 0.0,
    "cross_dissolve": 0.5,
    "dip_to_black": 0.8,
    "light_leak": 0.4,
    "whip_pan": 0.25,
}
XFADE_TYPES = {
    "cross_dissolve": "dissolve",
    "dip_to_black": "fadeblack",
    "light_leak": "fadewhite",
    "whip_pan": "wiperight",
}


def _run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {' '.join(cmd)}\n{proc.stderr[-4000:]}")


def _clip_path(work_dir: Path, i: int) -> Path:
    return work_dir / f"seg_{i:04d}.mp4"


def _base_visual_input(seg: Segment) -> tuple[list[str], str, bool]:
    """Return (extra ffmpeg -i args, filter label for the base video, is_still)."""
    if seg.source_type == "movie" and seg.source:
        return (["-ss", f"{seg.in_point}", "-t", f"{seg.out_point - seg.in_point}",
                  "-i", seg.source], "0:v", False)
    if seg.source_type == "person" and seg.source:
        # already a complete rendered parallax clip
        return (["-i", seg.source], "0:v", False)
    if seg.source_type in ("chapter_card", "tagline_card"):
        dur = seg.end - seg.start
        return (["-f", "lavfi", "-i",
                  f"color=c={config.BRAND_BLACK}:s={config.WIDTH}x{config.HEIGHT}:"
                  f"d={dur}:r={config.FPS}"], "0:v", True)
    # filler / fallback still (TMDB backdrop or generic subject B-roll)
    still = seg.source if seg.source and Path(seg.source).exists() else None
    if not still:
        return (["-f", "lavfi", "-i",
                  f"color=c={config.BRAND_BLACK}:s={config.WIDTH}x{config.HEIGHT}:"
                  f"d={seg.end - seg.start}:r={config.FPS}"], "0:v", True)
    return (["-loop", "1", "-i", still], "0:v", True)


def render_segment_clip(seg: Segment, extend_tail: float, work_dir: Path, idx: int,
                         next_seg: Optional[Segment] = None) -> Segment:
    """Render one segment to a muted H.264 clip at the target spec. Adds
    `extend_tail` seconds to the end (only where the source allows it) so a
    following transition can overlap without shrinking total programme
    length; on failure to extend, downgrades next_seg's transition to a
    hard cut and logs it so concat_with_transitions stays consistent."""
    dur = seg.end - seg.start
    actual_extend = 0.0
    if extend_tail > 0:
        if seg.source_type == "movie" and dur + extend_tail > config.MAX_CONTINUOUS_FILM_S:
            # Borrowing extra frames would break the "never >6s continuous
            # film" rule — downgrade the upcoming transition to a hard cut.
            if next_seg is not None:
                next_seg.transition_in = "hard_cut"
            with (config.DIR_BUILD / "decisions.md").open("a") as f:
                f.write(
                    f"- render: skipped transition handle on movie segment at "
                    f"{seg.start:.2f}s (would exceed the 6s continuous-film "
                    f"cap) — used a hard cut there instead.\n"
                )
        else:
            actual_extend = extend_tail
    dur += actual_extend

    in_args, vlabel, is_still = _base_visual_input(seg)
    if seg.source_type == "movie" and actual_extend:
        in_args[in_args.index("-t") + 1] = f"{dur}"

    filters = []
    if seg.source_type == "movie":
        filters.append(f"[{vlabel}]{look.letterbox_filter()}[lb]")
        vlabel = "lb"
    elif is_still:
        filters.append(f"[{vlabel}]{look.ken_burns_filter(dur)}[kb]")
        vlabel = "kb"
    else:
        filters.append(f"[{vlabel}]scale={config.WIDTH}:{config.HEIGHT}[sc]")
        vlabel = "sc"

    filters.append(f"[{vlabel}]{look.cinematic_finish_filters()}[fin]")
    vlabel = "fin"

    overlay_chain = []
    if seg.overlay:
        kind = seg.overlay.get("kind")
        if kind == "title_card":
            overlay_chain.append(look.title_card_filter(seg.overlay["title"], seg.overlay.get("year")))
        elif kind == "lower_third":
            overlay_chain.append(look.lower_third_filter(seg.overlay["name"]))
        elif kind == "chapter_card":
            overlay_chain.append(look.chapter_card_filter(seg.overlay["title"]))
        elif kind == "tagline":
            overlay_chain.append(look.tagline_card_filter())
    if idx == 0:
        overlay_chain.append(look.series_badge_filter(seg.overlay.get("_badge", "")
                                                        if seg.overlay else ""))
    if seg.end_screen_darken:
        overlay_chain.append("eq=brightness=-0.15")

    extra_inputs: list[str] = []
    pip_filters: list[str] = []
    for i, ov in enumerate(seg.extra_overlays):
        if ov["kind"] != "callback_pip":
            continue
        extra_inputs += ["-i", ov["portrait"]]
        input_idx = 1 + i
        rel_start = max(0.0, ov["window_start"] - seg.start)
        pip_filters.append(
            f"[{input_idx}:v]scale=280:-1,drawbox=w=iw:h=ih:color="
            f"{look._hex_to_ffmpeg(config.BRAND_GOLD)}:t=3[pip{i}]"
        )
        slide = (
            f"[{vlabel}][pip{i}]overlay="
            f"x='if(lt(t-{rel_start},0.4),W-(t-{rel_start})/0.4*(w+60),W-w-60)':"
            f"y=H-h-140:enable='between(t,{rel_start},{rel_start + 5.0})'[ovl{i}]"
        )
        pip_filters.append(slide)
        vlabel = f"ovl{i}"
        overlay_chain.append(look._drawtext(
            ov["badge"], look.find_font("Cinzel"), 18,
            look._hex_to_ffmpeg(config.BRAND_GOLD), "W-320", "H-160",
        ))

    if overlay_chain:
        filters.append(f"[{vlabel}]{','.join(overlay_chain)}[ovtext]")
        vlabel = "ovtext"

    filter_complex = ";".join(filters + pip_filters)
    out_path = _clip_path(work_dir, idx)
    cmd = ["ffmpeg", "-y"] + in_args + extra_inputs + [
        "-filter_complex", filter_complex, "-map", f"[{vlabel}]",
        "-an", "-t", str(dur), "-r", str(config.FPS),
        "-c:v", "libx264", "-crf", str(config.CRF), "-pix_fmt", "yuv420p",
        str(out_path),
    ]
    _run(cmd)
    seg._rendered_path = out_path  # type: ignore[attr-defined]
    seg._rendered_extend = actual_extend  # type: ignore[attr-defined]
    return seg


def render_all_clips(segments: list[Segment], work_dir: Path, max_workers: int = 4) -> None:
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = []
        for i, seg in enumerate(segments):
            extend = 0.0
            next_seg = segments[i + 1] if i + 1 < len(segments) else None
            if next_seg is not None:
                extend = XFADE_DURATIONS.get(next_seg.transition_in, 0.0)
            futures.append(ex.submit(render_segment_clip, seg, extend, work_dir, i, next_seg))
        for f in as_completed(futures):
            f.result()


def concat_with_transitions(segments: list[Segment], work_dir: Path) -> Path:
    """Chain segments with concat (hard cuts) and xfade (everything else),
    grouping consecutive hard-cut runs to keep the filter graph small."""
    runs: list[list[Segment]] = [[segments[0]]]
    for seg in segments[1:]:
        if seg.transition_in == "hard_cut":
            runs[-1].append(seg)
        else:
            runs.append([seg])

    run_files = []
    for r_idx, run in enumerate(runs):
        if len(run) == 1:
            run_files.append(run[0]._rendered_path)  # type: ignore[attr-defined]
            continue
        list_path = work_dir / f"run_{r_idx}.txt"
        list_path.write_text("\n".join(
            f"file '{seg._rendered_path.resolve()}'" for seg in run  # type: ignore[attr-defined]
        ))
        out_path = work_dir / f"run_{r_idx}.mp4"
        _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path),
              "-c", "copy", str(out_path)])
        run_files.append(out_path)

    if len(run_files) == 1:
        return run_files[0]

    current = run_files[0]
    for i in range(1, len(run_files)):
        seg_at_boundary = runs[i][0]
        d = XFADE_DURATIONS.get(seg_at_boundary.transition_in, 0.3)
        xtype = XFADE_TYPES.get(seg_at_boundary.transition_in, "dissolve")
        offset = _duration_of(current) - d
        out_path = work_dir / f"xfade_{i}.mp4"
        _run([
            "ffmpeg", "-y", "-i", str(current), "-i", str(run_files[i]),
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={xtype}:duration={d}:offset={offset}[v]",
            "-map", "[v]", "-c:v", "libx264", "-crf", str(config.CRF),
            "-pix_fmt", "yuv420p", str(out_path),
        ])
        current = out_path
    return current


def _duration_of(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True,
    )
    return float(out.stdout.strip())


def build_master_audio(narration_path: Path, total_duration: float, work_dir: Path,
                        segments: list[Segment]) -> Path:
    music = audiomix.pick_music_bed()
    sfx = audiomix.ensure_sfx()
    measured = audiomix.measure_loudness(narration_path)

    inputs = ["-i", str(narration_path)]
    next_input_idx = 1
    filters = [f"[0:a]{audiomix.loudnorm_filter(measured)}[narr]"]
    mix_labels = ["narr"]

    if music:
        inputs += ["-stream_loop", "-1", "-i", str(music)]
        music_idx = next_input_idx
        next_input_idx += 1
        filters.append(f"[{music_idx}:a]volume=0.5[mraw]")
        filters.append(audiomix.sidechain_duck_filter("narr", "mraw", "mduck"))
        mix_labels.append("mduck")

    for seg in segments:
        if seg.transition_in in ("dip_to_black", "light_leak") and seg.start > 0:
            inputs += ["-i", str(sfx["whoosh"])]
            idx = next_input_idx
            next_input_idx += 1
            delay_ms = int(seg.start * 1000)
            label = f"sfx{idx}"
            filters.append(f"[{idx}:a]adelay={delay_ms}|{delay_ms}[{label}]")
            mix_labels.append(label)

    # amix ends at its shortest branch once that branch's stream is
    # exhausted (e.g. a delayed 0.4s SFX blip), not at the longest one as
    # its docs imply — pad every branch out to the full programme length
    # first so the mix always runs the narration's full duration.
    padded_labels = []
    for l in mix_labels:
        padded = f"{l}p"
        filters.append(f"[{l}]apad=whole_dur={total_duration}[{padded}]")
        padded_labels.append(padded)

    filters.append(
        "".join(f"[{l}]" for l in padded_labels)
        + f"amix=inputs={len(padded_labels)}:duration=longest:normalize=0[premaster]"
    )
    filters.append(f"[premaster]{audiomix.loudnorm_filter({})}[master]")

    out_path = work_dir / "master_audio.m4a"
    cmd = ["ffmpeg", "-y"] + inputs + [
        "-filter_complex", ";".join(filters), "-map", "[master]",
        "-t", str(total_duration), "-c:a", "aac", "-b:a", config.AUDIO_BITRATE,
        str(out_path),
    ]
    _run(cmd)
    return out_path


def prepend_intro(episode_video: Path, master_audio: Path, work_dir: Path,
                   context) -> tuple[Path, Path]:
    """Intro plays with its own audio, then 0.5s crossfade into the
    episode's narration+music mix. Intro video is used unchanged (just
    concatenated, no regrade)."""
    intro_candidates = list(config.DIR_INTRO.glob("*.mp4")) + list(config.DIR_INTRO.glob("*.mov"))
    if not intro_candidates:
        with (config.DIR_BUILD / "missing_footage.md").open("a") as f:
            f.write("- **Channel intro**: assets/intro/*.mp4 not found — "
                     "episode was built WITHOUT the intro bumper.\n")
        return episode_video, master_audio

    intro = intro_candidates[0]
    intro_dur = _duration_of(intro)
    xfade_d = 0.5

    video_list = work_dir / "final_video_list.txt"
    video_list.write_text(
        f"file '{intro.resolve()}'\nfile '{episode_video.resolve()}'\n"
    )
    final_video = work_dir / "with_intro.mp4"
    _run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(video_list),
          "-c:v", "libx264", "-crf", str(config.CRF), "-pix_fmt", "yuv420p",
          str(final_video)])
    video_total = _duration_of(final_video)

    # The video track is a hard cut (intro used unchanged), but the audio
    # crossfades — which shrinks the audio timeline by xfade_d relative to
    # the video. acrossfade alone would then leave the tail of the video
    # silent/truncated by -shortest, so pad the crossfaded audio back out
    # to the video's full length (trailing near-silence under the already
    # fading-to-black tagline card is the right result, not a bug).
    final_audio = work_dir / "with_intro_audio.m4a"
    _run([
        "ffmpeg", "-y", "-i", str(intro), "-i", str(master_audio),
        "-filter_complex",
        f"[0:a][1:a]acrossfade=d={xfade_d}[xf];[xf]apad=whole_dur={video_total}[a]",
        "-map", "[a]", "-c:a", "aac", "-b:a", config.AUDIO_BITRATE,
        str(final_audio),
    ])
    return final_video, final_audio


def render_episode(segments: list[Segment], narration_path: Path, context) -> dict:
    work_dir = Path(tempfile.mkdtemp(prefix="ss_render_"))
    try:
        if segments:
            segments[0].overlay = segments[0].overlay or {}
            segments[0].overlay["_badge"] = context.badge_text
        render_all_clips(segments, work_dir)
        video = concat_with_transitions(segments, work_dir)
        total_duration = _duration_of(video)
        audio = build_master_audio(narration_path, total_duration, work_dir, segments)
        video, audio = prepend_intro(video, audio, work_dir, context)

        final_path = context.output_path("final", ".mp4")
        _run([
            "ffmpeg", "-y", "-i", str(video), "-i", str(audio),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", config.AUDIO_BITRATE,
            "-shortest", str(final_path),
        ])
        return {"final": final_path, "work_dir": work_dir}
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


def write_chapters(segments: list[Segment], alignment: dict, context) -> Path:
    path = context.output_path("chapters", ".txt")
    lines = []
    intro_dur = 0.0
    intro_candidates = list(config.DIR_INTRO.glob("*.mp4"))
    if intro_candidates:
        intro_dur = _duration_of(intro_candidates[0])
        lines.append(f"00:00 Intro")
    for sec in alignment.get("sections", []):
        t = sec["start_time"] + intro_dur
        m, s = divmod(int(t), 60)
        h, m = divmod(m, 60)
        ts = f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
        lines.append(f"{ts} {sec['title'].title()}")
    path.write_text("\n".join(lines))
    return path


def write_credits(context) -> Path:
    path = context.output_path("credits", ".txt").parent / "credits.txt"
    path = config.DIR_BUILD / "credits.txt"
    path.write_text(config.TMDB_ATTRIBUTION + "\n")
    return path
