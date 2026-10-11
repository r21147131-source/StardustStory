"""Build the 9:16 short "HBO's Harry Potter trailer broke every record" from
official TMDB series stills (backdrops + cast headshots) with Ken Burns moves.

Usage: TMDB_API_KEY=... python3 hbo-hp-trailer-tmdb-build.py <voiceover.mp3> <workdir> <out.mp4>

Images are fetched from the TMDB API (series id 224377). They remain the
property of their owners; the user accepted responsibility for that use.
Caption/overlay timings come from the pauses in the recorded voiceover.
"""
import json, os, subprocess, sys, urllib.request

VO, WORK, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(WORK, exist_ok=True)
W, H, FPS = 1080, 1920, 30
DUR = 60.92
IMG = "https://image.tmdb.org/t/p/original"
API = "https://api.themoviedb.org/3/tv/224377"
KEY = os.environ["TMDB_API_KEY"]


def api(path):
    with urllib.request.urlopen(f"{API}/{path}?api_key={KEY}&include_image_language=en,null") as r:
        return json.load(r)


# (image, mode, start, end, pan_dir)  mode: cover = crop to 9:16, fit = blurred bg
# backdrops by index in TMDB's list: 0 logo, 1 logo/Christmas 2026, 2 Harry+owl
# cage, 3 Quidditch jersey, 4 Harry smiling, 5 Gryffindor celebration,
# 6 logo+Harry, 7 Hogwarts Express at night, 8 trio in corridor
SHOTS = [
    ("bd7", "cover", 0.0, 5.6, 1),
    ("bd1", "fit", 5.6, 12.15, 1),
    ("bd2", "cover", 12.15, 17.2, -1),
    ("bd5", "cover", 17.2, 22.1, 1),
    ("bd3", "cover", 22.1, 25.1, -1),
    ("bd8", "cover", 25.1, 28.2, 1),
    ("cast_dominic", "cover", 28.2, 30.4, 1),
    ("cast_arabella", "cover", 30.4, 32.7, -1),
    ("cast_alastair", "cover", 32.7, 34.8, 1),
    ("cast_john", "cover", 34.8, 36.6, -1),
    ("cast_paapa", "cover", 36.6, 38.5, 1),
    ("cast_nick", "cover", 38.5, 40.7, -1),
    ("bd4", "cover", 40.7, 49.2, 1),
    ("bd6", "fit", 49.2, 56.0, -1),
    ("bd2", "cover", 56.0, DUR, 1),
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


def fetch():
    needed = {s[0].split("_")[1] for s in SHOTS if s[0].startswith("cast_")}
    imgs = api("images")["backdrops"]
    for n, b in enumerate(imgs):
        p = os.path.join(WORK, f"bd{n}.jpg")
        if not os.path.exists(p):
            urllib.request.urlretrieve(IMG + b["file_path"], p)
    for person in api("credits")["cast"]:
        first = person["name"].split()[0].lower()
        p = os.path.join(WORK, f"cast_{first}.jpg")
        if first not in needed:
            continue
        if person.get("profile_path") and not os.path.exists(p):
            urllib.request.urlretrieve(IMG + person["profile_path"], p)


def main():
    fetch()
    segs = []
    for i, (img, mode, a, b, d) in enumerate(SHOTS):
        L = b - a
        seg = os.path.join(WORK, f"seg{i:02d}.mp4")
        pan = f"(iw-{W})/2+({d})*(iw-{W})*0.12*(t/{L:.3f}-0.5)"
        fade = f"fade=t=in:st=0:d=0.2,fade=t=out:st={L-0.2:.3f}:d=0.2"
        grade = ("eq=contrast=1.05:saturation=0.95,vignette=PI/6,"
                 f"fps={FPS},{fade}")
        if mode == "cover":
            fc = (f"[0:v]scale={int(W*1.25)}:{int(H*1.25)}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H}:x='{pan}':y='(ih-{H})*0.3',{grade}[v]")
        else:  # fit: blurred full-bleed background + width-fitted foreground
            fc = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},boxblur=40:5,eq=brightness=-0.15[bg];"
                  f"[b]scale={int(W*(1.0+0.08))}:-2,crop={W}:ih:x='(iw-{W})/2+({d})*(iw-{W})*(t/{L:.3f}-0.5)':y=0[fg];"
                  f"[bg][fg]overlay=(W-w)/2:(H-h)/2,{grade}[v]")
        run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-framerate", str(FPS),
             "-t", f"{L:.3f}", "-i", os.path.join(WORK, f"{img}.jpg"),
             "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264",
             "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
             "-t", f"{L:.3f}", seg])
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
