#!/usr/bin/env python3
"""Build the 9:16 short "HBO's Harry Potter trailer broke every record" from
the user-supplied trailer files (real series footage, used at the user's own
fair-use risk), with the user's voiceover and burned-in captions.

Usage: python3 hbo-hp-trailer-clips-build.py <voiceover.mp3> <clean_cut.m4v> <et_cut.m4v> <workdir> <out.mp4>

Sources are 16:9 360p; each shot is cut to a true 9:16 window (202x360, then
upscaled), so it is soft but full-bleed, and the corner logos fall outside it.
"""
import os, subprocess, sys

VO, CLEAN, ET, WORK, OUT = sys.argv[1:6]
os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 30
DUR = 60.92
SRC = {"B": CLEAN, "A": ET}

# (source, in_seconds, source_duration[, x-focus 0..1 | "fit"[, on-screen duration: slow-mo]]) in timeline order; windows follow the VO beats.
# "fit" shows the whole 16:9 frame over a blurred copy (used for the title cards).
SHOTS = [
    ("B", 66.3, 2.0), ("B", 56.6, 3.6),                          # hook: Express, King's Cross
    ("B", 48.0, 2.2), ("B", 61.0, 2.2), ("B", 83.0, 2.15),      # most-watched record
    ("B", 78.0, 2.95), ("B", 72.0, 1.2), ("B", 74.0, 0.9),      # arrival, Great Hall, McGonagall
    ("B", 75.0, 1.2), ("A", 40.0, 1.8), ("A", 45.0, 1.9),       # Sorting, Gryffindor
    ("B", 90.0, 1.5), ("B", 91.0, 1.5),                          # Quidditch
    ("A", 125.0, 1.5), ("B", 103.0, 1.6),                        # mountain troll, corridor
    ("B", 100.0, 2.2), ("B", 109.0, 2.3), ("B", 108.0, 2.1),    # Harry, Hermione, Ron
    ("B", 104.0, 1.8, 0.62), ("A", 127.45, 1.0, 0.5, 1.9), ("B", 46.7, 1.3), ("B", 45.0, 0.9),     # Dumbledore, Snape, Hagrid
    ("B", 112.0, 2.0), ("B", 110.0, 2.1),                        # Ron's question
    ("B", 107.0, 2.2), ("B", 93.0, 2.2),                         # eight episodes
    ("B", 92.0, 2.2), ("B", 97.0, 2.2), ("B", 99.0, 2.4),       # series info
    ("B", 115.2, 2.5, "fit"), ("B", 119.7, 2.42, "fit"),                       # title + Christmas 2026 cards
]
assert abs(sum(x[4] if len(x) > 4 else x[2] for x in SHOTS) - DUR) < 0.01, sum(x[4] if len(x) > 4 else x[2] for x in SHOTS)

# Captions: (start, end, text) -- aligned to pauses in the recording
CAPS = [
    (0.05, 3.55, "277 million views in 48 hours."),
    (4.12, 8.00, "HBO's Harry Potter trailer is now the most-watched in HBO history,"),
    (8.43, 11.36, "beating the old record by more than double."),
    (12.16, 14.84, "The trailer opens with first-years arriving at Hogwarts,"),
    (15.18, 17.21, "McGonagall leading them into the Great Hall,"),
    (17.66, 19.61, "then the Sorting Ceremony,"),
    (19.96, 21.55, "with Harry placed in Gryffindor."),
    (22.15, 23.52, "There's the first Quidditch match."),
    (24.05, 25.81, "There's the mountain troll in the bathroom,"),
    (26.14, 27.77, "with the trio facing it together."),
    (28.63, 30.22, "Dominic McLaughlin is Harry,"),
    (30.60, 34.50, "with Arabella Stanton as Hermione and Alastair Stout as Ron."),
    (35.11, 36.42, "John Lithgow is Dumbledore,"),
    (36.82, 38.37, "Paapa Essiedu is Snape,"),
    (38.70, 40.32, "and Nick Frost is Hagrid."),
    (41.07, 42.46, "It ends on Ron's question:"),
    (42.73, 44.33, "“Are you really Harry Potter?”"),
    (45.20, 46.55, "Eight episodes this season,"),
    (46.92, 48.73, "one book per season after that."),
    (49.58, 51.39, "Season 2 is already in the works."),
    (51.73, 55.65, "It premieres Christmas 2026, only on HBO Max."),
    (56.34, 58.98, "Does a story this familiar still have room to surprise you?"),
    (59.47, 60.60, "Tell me in the comments."),
]

# Big on-screen cards: (start, end, style, text, pos_y)
CARDS = [
    (0.05, 5.4, "Stat", "277M", 760),
    (0.05, 5.4, "StatSub", "VIEWS IN 48 HOURS", 900),
    (5.7, 11.9, "Tag", "MOST-WATCHED TRAILER\\NIN HBO HISTORY", 330),
    (6.4, 11.9, "StatSub", "2×+ THE OLD RECORD", 560),
    (12.3, 21.5, "Tag", "THE ARRIVAL · THE SORTING", 330),
    (22.2, 28.0, "Tag", "QUIDDITCH · THE TROLL", 330),
    (28.7, 30.4, "Cast", "HARRY\\NDominic McLaughlin", 300),
    (30.6, 32.7, "Cast", "HERMIONE\\NArabella Stanton", 300),
    (32.7, 34.6, "Cast", "RON\\NAlastair Stout", 300),
    (35.1, 36.5, "Cast", "DUMBLEDORE\\NJohn Lithgow", 300),
    (36.8, 38.4, "Cast", "SNAPE\\NPaapa Essiedu", 300),
    (38.7, 40.4, "Cast", "HAGRID\\NNick Frost", 300),
    (42.7, 44.5, "Quote", "“Are you really\\NHarry Potter?”", 760),
    (45.2, 56.0, "Tag", "HBO MAX · CHRISTMAS 2026", 330),
    (45.2, 46.6, "Info", "8 EPISODES", 760),
    (46.9, 48.8, "Info", "1 BOOK PER SEASON", 760),
    (49.5, 51.5, "Info", "SEASON 2\\NIN THE WORKS", 760),
    (51.7, 56.0, "Info", "PREMIERES\\NCHRISTMAS 2026", 760),
]


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def build_ass(path):
    hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Cap,Inter,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6,3,2,80,80,330,1
Style: Stat,Inter,230,&H0055C8F2,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,8,4,5,40,40,0,1
"""
    hdr += (
        "Style: StatSub,Inter,64,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,6,0,1,5,3,5,40,40,0,1\n"
        "Style: Tag,Inter,44,&H0055C8F2,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,5,0,1,4,2,8,60,60,0,1\n"
        "Style: Cast,Inter,76,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,6,3,5,60,60,0,1\n"
        "Style: Quote,Inter,92,&H0055C8F2,&H000000FF,&H00000000,&H80000000,1,1,0,0,100,100,0,0,1,7,3,5,60,60,0,1\n"
        "Style: Info,Inter,88,&H0055C8F2,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,3,0,1,7,3,5,60,60,0,1\n"
        "\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
    )
    ev = []
    for s, e, style, text, y in CARDS:
        ev.append(
            f"Dialogue: 1,{ts(s)},{ts(e)},{style},,0,0,0,,"
            f"{{\\pos({W//2},{y})\\fad(180,180)}}{text}"
        )
    for s, e, text in CAPS:
        ev.append(f"Dialogue: 2,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\fad(90,90)}}{text}")
    open(path, "w").write(hdr + "\n".join(ev) + "\n")


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    segs = []
    for i, shot in enumerate(SHOTS):
        src, ss, L = shot[:3]
        mode = shot[3] if len(shot) > 3 else 0.5
        out = shot[4] if len(shot) > 4 else L
        slow = f"setpts=PTS*{out/L:.4f}," if out != L else ""
        seg = os.path.join(WORK, f"seg{i:02d}.mp4")
        fade = f"fade=t=in:st=0:d=0.12,fade=t=out:st={max(out-0.12,0):.3f}:d=0.12"
        d = 1 if i % 2 == 0 else -1
        if mode == "fit":
            fc = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},boxblur=40:5,eq=brightness=-0.2[bg];"
                  f"[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.7[fg];"
                  f"[bg][fg]overlay=0:(H-h)/2-110,fps={FPS},{fade}[v]")
        else:
            # true 9:16 cut: a 202x360 window of the 16:9 frame, drifting slowly.
            # Near-centre windows exclude both the ET (bottom-left) and HBO Max
            # (top-right) corner logos.
            fc = (f"[0:v]{slow}crop=202:360:x='(iw-202)*{mode}+({d})*50*(t/{out:.3f}-0.5)':y=0,"
                  f"hqdn3d=2:2:6:6,scale={W//2}:{H//2}:flags=bicubic,scale={W}:{H}:flags=lanczos,"
                  f"cas=0.7,unsharp=5:5:0.5:3:3:0.3,"
                  f"eq=contrast=1.05,vignette=PI/6,fps={FPS},{fade}[v]")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss}", "-t", f"{L:.3f}",
             "-i", SRC[src], "-filter_complex", fc, "-map", "[v]", "-an",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
             "-pix_fmt", "yuv420p", "-t", f"{out:.3f}", seg])
        segs.append(seg)

    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    base = os.path.join(WORK, "base.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", base])

    ass = os.path.join(WORK, "overlay.ass")
    build_ass(ass)
    run([
        "ffmpeg", "-v", "error", "-y", "-i", base, "-i", VO,
        "-vf", f"subtitles={ass}",
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-af", "apad", "-t", f"{DUR:.2f}", "-movflags", "+faststart", OUT,
    ])


if __name__ == "__main__":
    main()
