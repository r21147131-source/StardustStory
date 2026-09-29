"""Consumed Ep. 1 (Daniel Day-Lewis): shot list + local ffmpeg render.

Video footage only, matching the Golden Four Ep. 2 (Joseph Quinn) build: Pexels
stock B-roll found via vidiq_generate_broll. No stills. TMDB lists film trailers
only as YouTube links, and vidIQ's YouTube trims come back at about 256x144,
too low-res for full-frame use. The item helpers still accept TMDB stills (I()).
Section start times are estimated from pauses in the voiceover plus the
script's word counts (no word-level transcript was available).

Usage: python3 production/consumed-ep1-build.py  ->  render/consumed-ep1/
"""
import json, math, os, subprocess, sys
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VO = os.path.join(ROOT, "public/consumed-ep1-daniel-day-lewis-voiceover.mp3")
WORK = os.path.join(ROOT, "render/consumed-ep1")
OUT = os.path.join(ROOT, "output/consumed-ep1/daniel-day-lewis-consumed.mp4")
TOTAL = 624.93
P = "https://videos.pexels.com/video-files/"
T = "https://image.tmdb.org/t/p/original/"

# TMDB (themoviedb.org) stills/portraits are the main visual source; TMDB's
# own "videos" are YouTube links, so moving footage is Pexels stock B-roll.
def I(tmdb_id, kind="still"):
    return ("img", tmdb_id, kind)

def V(path, secs):
    return ("vid", path, secs)

PORTRAIT = "portrait"
# (start_seconds, on-screen title or None, [clips...])
SECTIONS = [
    (0.0, None, [
        V("4722613/4722613-hd_1366_720_25fps.mp4", 77),
        V("8515272/8515272-hd_1280_720_25fps.mp4", 25),
        V("8679945/8679945-hd_1366_720_25fps.mp4", 14),
    ]),
    (21.2, "CONSUMED\\N{\\fs44}Episode One  ·  Daniel Day-Lewis", [
        V("856593/856593-hd_1920_1080_24fps.mp4", 20),
        V("9665236/9665236-hd_1920_1080_25fps.mp4", 67),
        V("855120/855120-hd_1280_720_50fps.mp4", 29),
    ]),
    (49.9, "ACT I\\N{\\fs44}The Poet's Son", [
        V("39618428/16887642_640_360_25fps.mp4", 14),
        V("4061896/4061896-hd_1280_720_24fps.mp4", 20),
        V("2308576/2308576-hd_1280_720_30fps.mp4", 18),
        V("11272050/11272050-hd_1920_1080_30fps.mp4", 21),
        V("4230107/4230107-hd_1920_1080_30fps.mp4", 12),
        V("5972653/5972653-hd_1280_720_25fps.mp4", 10),
        V("7314256/7314256-hd_2048_1080_25fps.mp4", 24),
        V("5972648/5972648-hd_1920_1080_25fps.mp4", 8),
        V("6899905/6899905-hd_1366_720_25fps.mp4", 31),
    ]),
    (115.6, "ACT II\\N{\\fs44}The Disappearing Man", [
        V("8524028/8524028-hd_2048_1080_25fps.mp4", 39),
        V("8524500/8524500-hd_1366_720_25fps.mp4", 46),
        V("8170111/8170111-hd_1920_1080_25fps.mp4", 9),
        V("8037249/8037249-hd_1920_1080_25fps.mp4", 9),
        V("10986488/10986488-hd_3840_2160_30fps.mp4", 62),
        V("8206285/8206285-hd_1920_1080_30fps.mp4", 39),
        V("10472893/10472893-hd_2048_1080_25fps.mp4", 14),
        V("10475251/10475251-hd_2048_1080_25fps.mp4", 15),
        V("10475475/10475475-hd_2048_1080_25fps.mp4", 15),
        V("12187197/12187197-hd_1280_720_25fps.mp4", 26),
        V("5481284/5481284-hd_1920_1080_24fps.mp4", 42),
    ]),
    (198.9, "ACT III\\N{\\fs44}The Ghost", [
        V("26576151/11963026_640_360_30fps.mp4", 26),
        V("8515272/8515272-hd_1280_720_25fps.mp4", 25),
        V("8679945/8679945-hd_1366_720_25fps.mp4", 14),
        V("11792115/11792115-hd_1280_720_25fps.mp4", 22),
        V("7546430/7546430-hd_1920_1080_25fps.mp4", 9),
        V("11272050/11272050-hd_1920_1080_30fps.mp4", 21),
        V("11839732/11839732-hd_1920_1080_25fps.mp4", 23),
        V("6899907/6899907-hd_1366_720_25fps.mp4", 41),
        V("4722613/4722613-hd_1366_720_25fps.mp4", 77),
    ]),
    (280.0, "ACT IV\\N{\\fs44}The Bench", [
        V("9777987/9777987-hd_1920_1080_25fps.mp4", 28),
        V("5752175/5752175-hd_1280_720_25fps.mp4", 12),
        V("17138696/17138696-hd_1280_720_30fps.mp4", 29),
        V("5979152/5979152-hd_1920_1080_30fps.mp4", 10),
        V("7724737/7724737-hd_1920_1080_25fps.mp4", 8),
        V("37655310/15962716_640_360_25fps.mp4", 25),
        V("9936744/9936744-hd_1920_1080_25fps.mp4", 17),
        V("17661984/17661984-hd_1280_720_24fps.mp4", 19),
    ]),
    (348.1, None, [
        V("6254907/6254907-hd_1920_1080_25fps.mp4", 13),
    ]),
    (359.1, "ACT V\\N{\\fs44}The Butcher and the President", [
        V("5658155/5658155-hd_2048_1080_30fps.mp4", 45),
        V("11344099/11344099-hd_1920_1080_25fps.mp4", 14),
        V("6527469/6527469-hd_1920_1080_25fps.mp4", 20),
        V("6527472/6527472-hd_1920_1080_25fps.mp4", 27),
        V("11969228/11969228-hd_1280_720_30fps.mp4", 38),
        V("7005887/7005887-hd_1920_1080_30fps.mp4", 16),
        V("12426698/12426698-hd_1920_1080_30fps.mp4", 21),
    ]),
    (426.5, None, [
        V("6389055/6389055-hd_1920_1080_25fps.mp4", 15),
        V("6053511/6053511-hd_1920_1080_25fps.mp4", 12),
    ]),
    (447.0, "ACT VI\\N{\\fs44}The Last Thread", [
        V("6424074/6424074-hd_1280_720_25fps.mp4", 17),
        V("6459999/6459999-hd_1920_1080_25fps.mp4", 41),
        V("5815527/5815527-hd_1920_1080_25fps.mp4", 21),
        V("4110287/4110287-hd_1280_720_30fps.mp4", 22),
        V("29906414/12837345_640_360_24fps.mp4", 43),
        V("4927854/4927854-hd_1280_720_30fps.mp4", 11),
        V("6899907/6899907-hd_1366_720_25fps.mp4", 41),
    ]),
    (525.0, "ACT VII\\N{\\fs44}The Return", [
        V("38492077/16347231_682_360_30fps.mp4", 10),
        V("8747604/8747604-hd_1920_1080_25fps.mp4", 8),
        V("5104195/5104195-hd_1920_1080_30fps.mp4", 15),
        V("8524028/8524028-hd_2048_1080_25fps.mp4", 39),
        V("11272050/11272050-hd_1920_1080_30fps.mp4", 21),
        V("8576481/8576481-hd_1920_1080_30fps.mp4", 9),
        V("6867012/6867012-hd_1280_720_24fps.mp4", 17),
        V("5004222/5004222-hd_1920_1080_24fps.mp4", 24),
        V("9665237/9665237-hd_1920_1080_25fps.mp4", 74),
    ]),
]
MAX_SHOT = 9.0


def build_shots():
    """Split each section across its items (stills weighted lighter than
    clips), capping clips at their length; loop the list if shots run long."""
    shots, used = [], {}
    for i, (start, _, items) in enumerate(SECTIONS):
        end = SECTIONS[i + 1][0] if i + 1 < len(SECTIONS) else TOTAL
        span = end - start
        seq = list(items)
        while span / len(seq) > MAX_SHOT:
            seq += items
        w = [1.0 if it[0] == "img" else 1.3 for it in seq]
        cap = [float("inf") if it[0] == "img" else it[2] - 0.3 for it in seq]
        dur = [0.0] * len(seq)
        free = set(range(len(seq)))
        left = span
        while free:
            tw = sum(w[k] for k in free)
            over = [k for k in free if left * w[k] / tw > cap[k]]
            if not over:
                for k in free:
                    dur[k] = left * w[k] / tw
                break
            for k in over:
                dur[k] = cap[k]; left -= cap[k]; free.discard(k)
        for it, d in zip(seq, dur):
            if it[0] == "img":
                shots.append({"type": "img", "src": T + it[1] + ".jpg", "kind": it[2], "dur": round(d, 3)})
            else:
                off = used.get(it[1], 0.0)
                if it[2] - off - d < 0.3:
                    off = 0.0
                used[it[1]] = off + d
                shots.append({"type": "vid", "src": P + it[1], "start_from": round(off, 2), "dur": round(d, 3)})
    return shots


def ass_time(s):
    h, s = divmod(s, 3600); m, s = divmod(s, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def write_titles(path):
    lines = [
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: 1920", "PlayResY: 1080", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Spacing",
        "Style: T,DejaVu Serif,96,&H00F0F0F0,&H00000000,&H80000000,1,0,1,2,3,2,80,80,120,6",
        "", "[Events]", "Format: Layer, Start, End, Style, Text",
    ]
    for start, title, _ in SECTIONS:
        if title:
            s = start + 0.6
            lines.append(f"Dialogue: 0,{ass_time(s)},{ass_time(s + 4.5)},T,{{\\fad(700,900)}}{title}")
    open(path, "w").write("\n".join(lines) + "\n")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-3000:])


def main():
    os.makedirs(os.path.join(WORK, "src"), exist_ok=True)
    os.makedirs(os.path.join(WORK, "shots"), exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shots = build_shots()
    json.dump(shots, open(os.path.join(ROOT, "production/consumed-ep1-shots.json"), "w"), indent=2)
    print(f"{len(shots)} shots, {sum(s['dur'] for s in shots):.2f}s")

    look = "eq=saturation=0.72:contrast=1.06,vignette=PI/5,format=yuv420p"
    grade = "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30," + look
    cover = "scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160"
    moves = [  # Ken Burns: slow push in, pull out, drift right, drift left
        ("1.02+0.10*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
        ("1.12-0.10*on/{n}", "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"),
        ("1.10", "(iw-iw/zoom)*on/{n}", "ih/2-(ih/zoom/2)"),
        ("1.10", "(iw-iw/zoom)*(1-on/{n})", "ih/2-(ih/zoom/2)"),
    ]
    listing = []
    for i, s in enumerate(shots):
        local = os.path.join(WORK, "src", s["src"].split("/")[-1])
        if not os.path.exists(local):
            run(["curl", "-sSfL", "--retry", "6", "--retry-all-errors", "-o", local, s["src"]])
        out = os.path.join(WORK, "shots", f"{i:03d}.mp4")
        fade = f",fade=t=in:st=0:d=0.35,fade=t=out:st={max(0, s['dur'] - 0.35):.3f}:d=0.35"
        listing.append(f"file '{out}'")
        if os.path.exists(out):  # resume an interrupted render
            continue
        if s["type"] == "img":
            n = round(s["dur"] * 30)
            z, x, y = (m.format(n=n) for m in moves[i % len(moves)])
            kb = f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1920x1080:fps=30,"
            if s["kind"] == "portrait":  # sharp portrait over a blurred copy of itself
                fc = (f"[0]{cover},boxblur=40:5,eq=brightness=-0.12[bg];[0]scale=-2:2160[fg];"
                      f"[bg][fg]overlay=(W-w)/2:0,{kb}{look}{fade}")
            else:
                fc = f"[0]{cover},{kb}{look}{fade}"
            run([FF, "-y", "-i", local, "-filter_complex", fc, "-frames:v", str(n),
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out])
        else:
            run([FF, "-y", "-ss", str(s["start_from"]), "-i", local, "-t", f"{s['dur']:.3f}", "-an",
                 "-vf", grade + fade, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out])
        print(f"  shot {i:03d} {s['type']} {s['dur']:6.2f}s")
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("\n".join(listing) + "\n")
    ass = os.path.join(WORK, "titles.ass")
    write_titles(ass)
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", VO,
         "-vf", f"subtitles={ass}", "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "192k",
         "-t", str(TOTAL), "-movflags", "+faststart", OUT])
    print("wrote", OUT)


if __name__ == "__main__":
    main()
