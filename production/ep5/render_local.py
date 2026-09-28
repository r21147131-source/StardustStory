"""Render Golden Four Ep5 locally with ffmpeg from the vidiq_compose payloads.

Usage:
  python render_local.py WORKDIR OUT.mp4 [--placeholders] [--only SEG] [--preview]

WORKDIR must contain compose-seg{1..5}.json (from build_compose.py).
Assets are downloaded into WORKDIR/cache. With --placeholders, assets that
can't be fetched are replaced by a labelled grey card (for pipeline tests).
The voiceover is read from public/golden-four-ep5-voiceover.mp3.
"""
import hashlib, json, os, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VO = os.path.join(REPO, "public", "golden-four-ep5-voiceover.mp3")
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
        im = Image.new("RGB", (1920, 1080), (40, 40, 48))
        d = ImageDraw.Draw(im)
        d.text((80, 500), "PLACEHOLDER: " + label[-70:], fill=(200, 200, 200),
               font=ImageFont.truetype(FONT, 36))
        im.save(p, quality=85)
    return p


def prep_image(src, layout, out):
    """Make a 1.2x-oversized 16:9 plate so zoompan has room to move."""
    im = Image.open(src).convert("RGB")
    PW, PH = int(W * 1.2), int(H * 1.2)
    if layout == "fit":
        bg = im.copy()
        s = max(PW / bg.width, PH / bg.height)
        bg = bg.resize((int(bg.width * s) + 1, int(bg.height * s) + 1))
        bg = bg.crop(((bg.width - PW) // 2, (bg.height - PH) // 2,
                      (bg.width - PW) // 2 + PW, (bg.height - PH) // 2 + PH))
        bg = bg.filter(ImageFilter.GaussianBlur(40)).point(lambda v: int(v * 0.45))
        s = min(PW * 0.9 / im.width, PH * 0.92 / im.height)
        fg = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        bg.paste(fg, ((PW - fg.width) // 2, (PH - fg.height) // 2))
        plate = bg
    else:
        s = max(PW / im.width, PH / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        plate = im.crop(((im.width - PW) // 2, (im.height - PH) // 2,
                         (im.width - PW) // 2 + PW, (im.height - PH) // 2 + PH))
    plate.save(out, quality=92)


def scene_clip(i, sc, out):
    n = max(1, round(sc["duration"] * FPS))
    if sc["type"] == "image":
        plate = out + ".plate.jpg"
        prep_image(sc["_local"], sc.get("layout", "fill"), plate)
        kb = sc.get("kenBurns") or {"from": {"scale": 1, "x": .5, "y": .5}, "to": {"scale": 1, "x": .5, "y": .5}}
        f, t = kb["from"], kb["to"]
        # plate is 1.2x the frame; zoom z maps to (1.2*z) relative to output
        z0, z1 = f["scale"], t["scale"]
        z = f"({z0}+({z1}-{z0})*on/{n})"
        fx = f"({f['x']}+({t['x']}-{f['x']})*on/{n})"
        fy = f"({f['y']}+({t['y']}-{f['y']})*on/{n})"
        vf = (f"scale={int(W*1.2*2)}:{int(H*1.2*2)},"
              f"zoompan=z='1.2*{z}':x='max(0,min(iw-iw/zoom,iw*{fx}-iw/zoom/2))':"
              f"y='max(0,min(ih-ih/zoom,ih*{fy}-ih/zoom/2))':d={n}:s={W}x{H}:fps={FPS},"
              f"format=yuv420p")
        run([FF, "-y", "-loglevel", "error", "-i", plate, "-vf", vf, "-frames:v", str(n),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-an", out])
    else:
        ss = sc.get("startFromSeconds", 0)
        vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
              f"fps={FPS},format=yuv420p")
        run([FF, "-y", "-loglevel", "error", "-ss", str(ss), "-i", sc["_local"], "-vf", vf,
             "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-an", out])
    return out


def text_png(ov, path):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    p, st = ov["position"], ov.get("style", {})
    size = int(st.get("fontSize", 40) * W / 1920)
    font = ImageFont.truetype(FONT_B if st.get("fontWeight", 400) >= 600 else FONT, size)
    bx, by, bw, bh = p["x"] * W, p["y"] * H, p["width"] * W, p["height"] * H
    if st.get("background"):
        rgba = st["background"].replace("rgba(", "").replace(")", "").split(",")
        col = tuple(int(float(c)) for c in rgba[:3]) + (int(float(rgba[3]) * 255),)
        d.rectangle([bx, by, bx + bw, by + bh], fill=col)
    tw = d.textlength(ov["text"], font=font)
    align = st.get("textAlign", "center")
    x = bx + 12 if align == "left" else (bx + bw - tw - 12 if align == "right" else bx + (bw - tw) / 2)
    y = by + (bh - size) / 2 - size * 0.1
    d.text((x, y), ov["text"], font=font, fill=st.get("color", "#FFFFFF"),
           stroke_width=max(2, size // 18), stroke_fill=(0, 0, 0, 220))
    im.save(path)


def main():
    segs = [json.load(open(os.path.join(WORK, f"compose-seg{i}.json"))) for i in range(1, 6)]
    offsets, t = [], 0.0
    for sg in segs:
        offsets.append(t); t += sum(s["duration"] for s in sg["scenes"])
    total = t
    idx = [ONLY - 1] if ONLY else range(5)

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
    chain, cur, n_in = [], "[0:v]", 2
    for si in idx:
        for k, ov in enumerate(segs[si]["overlays"]):
            a = offsets[si] - t0 + ov["start"]; b = a + ov["duration"]
            if ov["kind"] == "text":
                png = os.path.join(TMP, f"ov{si}_{k}.png"); text_png(ov, png)
                inputs += ["-i", png]
                chain.append(f"{cur}[{n_in}:v]overlay=0:0:enable='between(t,{a:.2f},{b:.2f})'[v{n_in}]")
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
    fade = f"{cur}fade=t=in:st=0:d=1,fade=t=out:st={seg_len-1.5:.2f}:d=1.5[vout]" if not ONLY else f"{cur}null[vout]"
    chain.append(fade)
    run([FF, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chain),
         "-map", "[vout]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", OUT])
    print("wrote", OUT, f"{seg_len:.1f}s", "(with placeholders)" if missing else "")


main()
