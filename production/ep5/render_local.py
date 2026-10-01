"""Render Golden Four Ep5 locally with ffmpeg from the vidiq_compose payloads.

Usage:
  python render_local.py WORKDIR OUT.mp4 [--placeholders] [--only SEG] [--preview]

Needs only an ffmpeg binary (with libx264, libfreetype): set FFMPEG=/path/to/ffmpeg,
otherwise `ffmpeg` on PATH is used. No Python packages required.

WORKDIR must contain compose-seg{1..5}.json (from build_compose.py).
Assets are downloaded into WORKDIR/cache. With --placeholders, assets that
can't be fetched are replaced by a labelled grey card (for pipeline tests).
The voiceover is read from $VO (default public/golden-four-ep5-voiceover.mp3).
"""
import hashlib, json, os, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
import shutil

FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg")
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VO = os.environ.get("VO") or os.path.join(REPO, "public", "golden-four-ep5-voiceover.mp3")
W, H, FPS = 1920, 1080, 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

args = sys.argv[1:]
WORK, OUT = args[0], args[1]
PLACEHOLDERS = "--placeholders" in args
PREVIEW = "--preview" in args
ONLY = int(args[args.index("--only") + 1]) if "--only" in args else None
if PREVIEW:
    W, H, FPS = 960, 540, 24
CACHE = os.path.join(WORK, "cache"); os.makedirs(CACHE, exist_ok=True)
TMP = os.path.join(WORK, "tmp"); os.makedirs(TMP, exist_ok=True)


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit("ffmpeg failed:\n" + " ".join(cmd) + "\n" + r.stderr[-2000:])


def fetch(url):
    if url.startswith("/"):  # local file (e.g. a user-supplied clip)
        return (url, True) if os.path.exists(url) else ("missing local file", False)
    ext = ".mp4" if ".mp4" in url.split("?")[0] else ".jpg"
    path = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest()[:16] + ext)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path, True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r, open(path + ".part", "wb") as f:
            f.write(r.read())
        os.replace(path + ".part", path)
        return path, True
    except Exception as e:
        return f"{type(e).__name__}", False


def placeholder(label):
    p = os.path.join(CACHE, "ph_" + hashlib.sha1(label.encode()).hexdigest()[:10] + ".jpg")
    if not os.path.exists(p):
        run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x282830:s=1920x1080",
             "-frames:v", "1", p])
    return p


def plate_filter(layout):
    """Filter making a 1.2x-oversized 16:9 plate so zoompan has room to move."""
    PW, PH = int(W * 1.2) // 2 * 2, int(H * 1.2) // 2 * 2
    fill = f"scale={PW}:{PH}:force_original_aspect_ratio=increase,crop={PW}:{PH}"
    if layout != "fit":
        return fill
    return (f"split[a][b];[a]{fill},boxblur=40:2,colorchannelmixer=rr=.45:gg=.45:bb=.45[bg];"
            f"[b]scale={int(PW*0.9)}:{int(PH*0.92)}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2")


def scene_clip(i, sc, out):
    n = max(1, round(sc["duration"] * FPS))
    if sc["type"] == "image":
        kb = sc.get("kenBurns") or {"from": {"scale": 1, "x": .5, "y": .5}, "to": {"scale": 1, "x": .5, "y": .5}}
        f, t = kb["from"], kb["to"]
        # plate is 1.2x the frame; zoom z maps to (1.2*z) relative to output
        z0, z1 = f["scale"], t["scale"]
        z = f"({z0}+({z1}-{z0})*on/{n})"
        fx = f"({f['x']}+({t['x']}-{f['x']})*on/{n})"
        fy = f"({f['y']}+({t['y']}-{f['y']})*on/{n})"
        vf = (plate_filter(sc.get("layout", "fill")) + f",scale={int(W*1.2*2)}:{int(H*1.2*2)},"
              f"zoompan=z='1.2*{z}':x='max(0,min(iw-iw/zoom,iw*{fx}-iw/zoom/2))':"
              f"y='max(0,min(ih-ih/zoom,ih*{fy}-ih/zoom/2))':d={n}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p")
        run([FF, "-y", "-loglevel", "error", "-i", sc["_local"], "-filter_complex", vf, "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-an", out])
    else:
        ss = sc.get("startFromSeconds", 0)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={FPS},format=yuv420p")
        run([FF, "-y", "-loglevel", "error", "-ss", str(ss), "-i", sc["_local"], "-vf", vf,
             "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-an", out])
    return out


def text_filters(ov, a, b, k):
    """drawbox/drawtext filters for one text overlay, active between a and b."""
    p, st = ov["position"], ov.get("style", {})
    size = int(st.get("fontSize", 40) * W / 1920)
    font = FONT_B if st.get("fontWeight", 400) >= 600 else FONT
    bx, by, bw, bh = int(p["x"] * W), int(p["y"] * H), int(p["width"] * W), int(p["height"] * H)
    en = f"enable='between(t,{a:.2f},{b:.2f})'"
    out = []
    if st.get("background"):
        rgba = [float(c) for c in st["background"].replace("rgba(", "").replace(")", "").split(",")]
        col = "0x%02X%02X%02X@%.2f" % (int(rgba[0]), int(rgba[1]), int(rgba[2]), rgba[3])
        out.append(f"drawbox=x={bx}:y={by}:w={bw}:h={bh}:color={col}:t=fill:{en}")
    tf = os.path.join(TMP, f"txt{k}.txt")
    open(tf, "w").write(ov["text"])
    align = st.get("textAlign", "center")
    x = f"{bx+12}" if align == "left" else (f"{bx+bw-12}-text_w" if align == "right" else f"{bx}+({bw}-text_w)/2")
    col = st.get("color", "#FFFFFF").replace("#", "0x")
    out.append(f"drawtext=fontfile={font}:textfile={tf}:fontsize={size}:fontcolor={col}:"
               f"borderw={max(2, size // 18)}:bordercolor=black@0.85:x={x}:y={by}+({bh}-text_h)/2:{en}")
    return out


def main():
    nseg = len([f for f in os.listdir(WORK) if f.startswith("compose-seg") and f.endswith(".json")])
    segs = [json.load(open(os.path.join(WORK, f"compose-seg{i}.json"))) for i in range(1, nseg + 1)]
    offsets, t = [], 0.0
    for sg in segs:
        offsets.append(t); t += sum(s["duration"] for s in sg["scenes"])
    total = t
    idx = [ONLY - 1] if ONLY else range(nseg)

    # download
    urls = set()
    for si in idx:
        for sc in segs[si]["scenes"]:
            urls.add(sc["source"])
        for ov in segs[si]["overlays"]:
            if ov["kind"] == "video":
                urls.add(ov["src"])
    with ThreadPoolExecutor(8) as ex:
        res = dict(zip(urls, ex.map(fetch, urls)))
    missing = [u for u, (p, ok) in res.items() if not ok]
    if missing:
        print(f"{len(missing)}/{len(urls)} assets could not be fetched, e.g. {missing[0][:90]} ({res[missing[0]][0]})")
        if not PLACEHOLDERS:
            sys.exit("re-run with --placeholders to test the pipeline anyway")

    # scene clips
    jobs = []
    for si in idx:
        for k, sc in enumerate(segs[si]["scenes"]):
            p, ok = res[sc["source"]]
            if not ok:
                sc = dict(sc, type="image", layout="fill")
                p = placeholder(sc["source"])
            sc["_local"] = p
            jobs.append((si, k, sc, os.path.join(TMP, f"s{si+1}_{k:03d}.mp4")))
    with ThreadPoolExecutor(os.cpu_count() or 2) as ex:
        list(ex.map(lambda j: scene_clip(j[1], j[2], j[3]), jobs))
        print(f"rendered {len(jobs)} scene clips")

    lst = os.path.join(TMP, "list.txt")
    with open(lst, "w") as f:
        for j in jobs:
            f.write(f"file '{j[3]}'\n")
    base = os.path.join(TMP, "base.mp4")
    run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", base])

    # overlays + audio
    t0 = offsets[idx[0]]
    seg_len = sum(sum(s["duration"] for s in segs[si]["scenes"]) for si in idx)
    inputs = ["-i", base, "-ss", str(t0), "-t", str(seg_len), "-i", VO]
    chain, cur, n_in, texts = [], "[0:v]", 2, []
    for si in idx:
        for k, ov in enumerate(segs[si]["overlays"]):
            a = offsets[si] - t0 + ov["start"]; b = a + ov["duration"]
            if ov["kind"] == "text":
                texts += text_filters(ov, a, b, f"{si}_{k}")
                continue
            else:
                p, ok = res[ov["src"]]
                if not ok:
                    continue
                pos = ov["position"]
                w, h = int(pos["width"] * W) // 2 * 2, int(pos["height"] * H) // 2 * 2
                inputs += ["-ss", str(ov.get("startFromSeconds", 0)), "-t", str(ov["duration"]), "-i", p]
                chain.append(f"[{n_in}:v]scale={w}:{h},setpts=PTS-STARTPTS+{a:.2f}/TB,"
                             f"pad={w+8}:{h+8}:4:4:color=0xF2D27A[i{n_in}];"
                             f"{cur}[i{n_in}]overlay={int(pos['x']*W)-4}:{int(pos['y']*H)-4}:"
                             f"eof_action=pass:enable='between(t,{a:.2f},{b:.2f})'[v{n_in}]")
            cur = f"[v{n_in}]"; n_in += 1
    if texts:
        chain.append(f"{cur}{','.join(texts)}[vt]"); cur = "[vt]"
    fade = f"{cur}fade=t=in:st=0:d=1,fade=t=out:st={seg_len-1.5:.2f}:d=1.5[vout]" if not ONLY else f"{cur}null[vout]"
    chain.append(fade)
    run([FF, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chain),
         "-map", "[vout]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT])
    print("wrote", OUT, f"{seg_len:.1f}s", "(with placeholders)" if missing else "")


main()
