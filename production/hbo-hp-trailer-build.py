#!/usr/bin/env python3
"""Build the 9:16 short "HBO's Harry Potter trailer broke every record".

Usage: python3 hbo-hp-trailer-build.py <voiceover.mp3> <workdir> <out.mp4>

Visuals are generic Pexels stock B-roll (castle, library, owl, steam train,
misty forest) -- no film/trailer footage, press photos or actor likenesses.
Caption/overlay timings come from the pauses in the recorded voiceover.
"""
import os, subprocess, sys, urllib.request

VO, WORK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 30
DUR = 60.92

BASE = "https://videos.pexels.com/video-files/"
CLIPS = {
    "castle": "30034677/12885435_1440_2560_60fps.mp4",   # lit castle at night
    "library": "29592157/12737470_1080_1920_60fps.mp4",  # arched historic library
    "train": "34458714/14601039_1080_1920_30fps.mp4",    # steam train at station
    "owl": "37518869/15895676_1440_2560_30fps.mp4",      # eagle-owl on perch
    "forest": "27127710/12080463_1440_2560_30fps.mp4",   # misty forest
}

# (clip, source_in, start, end, pan_dir)  -- timeline in seconds
SHOTS = [
    ("castle", 0.0, 0.0, 5.6, 1),
    ("train", 3.0, 5.6, 12.15, -1),
    ("library", 0.0, 12.15, 22.1, 1),
    ("owl", 4.0, 22.1, 28.2, -1),
    ("forest", 0.0, 28.2, 34.8, 1),
    ("castle", 1.0, 34.8, 40.7, -1),
    ("train", 18.0, 40.7, 49.2, 1),
    ("owl", 16.0, 49.2, 56.0, -1),
    ("library", 0.0, 56.0, DUR, -1),
]

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
    (28.7, 30.4, "Cast", "HARRY\\NDominic McLaughlin", 760),
    (30.6, 32.7, "Cast", "HERMIONE\\NArabella Stanton", 760),
    (32.7, 34.6, "Cast", "RON\\NAlastair Stout", 760),
    (35.1, 36.5, "Cast", "DUMBLEDORE\\NJohn Lithgow", 760),
    (36.8, 38.4, "Cast", "SNAPE\\NPaapa Essiedu", 760),
    (38.7, 40.4, "Cast", "HAGRID\\NNick Frost", 760),
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
    # fetch clips
    for name, rel in CLIPS.items():
        p = os.path.join(WORK, f"{name}.mp4")
        if not os.path.exists(p):
            print("download", name)
            urllib.request.urlretrieve(BASE + rel, p)

    # render each shot to an identical 1080x1920 30fps segment, graded
    segs = []
    for i, (clip, src_in, a, b, d) in enumerate(SHOTS):
        L = b - a
        seg = os.path.join(WORK, f"seg{i:02d}.mp4")
        # cover-crop to 9:16 with a slow horizontal drift
        vf = (
            f"scale={int(W*1.25)}:{int(H*1.25)}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H}:x='(iw-{W})/2+({d})*(iw-{W})*0.12*(t/{L:.3f}-0.5)':y='(ih-{H})/2',"
            f"scale={W}:{H},fps={FPS},"
            "eq=contrast=1.08:saturation=0.85:brightness=-0.06,"
            "colorbalance=rs=0.04:gs=0.01:bs=-0.04:rm=0.03:bm=-0.03,"
            "vignette=PI/5,"
            f"fade=t=in:st=0:d=0.2,fade=t=out:st={L-0.2:.3f}:d=0.2"
        )
        run([
            "ffmpeg", "-v", "error", "-y", "-ss", f"{src_in}", "-t", f"{L:.3f}",
            "-stream_loop", "-1",  # in case the source is shorter than needed
            "-i", os.path.join(WORK, f"{clip}.mp4"),
            "-vf", vf, "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-t", f"{L:.3f}", seg,
        ])
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
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium",
        "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-af", "apad", "-t", f"{DUR:.2f}", "-movflags", "+faststart", OUT,
    ])


if __name__ == "__main__":
    main()
