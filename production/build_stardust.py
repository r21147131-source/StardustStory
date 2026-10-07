#!/usr/bin/env python3
"""Build the Stardust Story video (Golden Four style) from stardust_timeline.py.

Stages:  plates -> render -> audio -> final      (python3 production/build_stardust.py all)
Work files live in footage/work/ (gitignored); the result goes to output/stardust-story/.
"""
import os, sys, math, json, hashlib, subprocess, concurrent.futures as cf, textwrap
sys.path.insert(0, os.path.dirname(__file__))
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import stardust_timeline as TL

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORK = f"{ROOT}/footage/work"
PLATES, LABELS, UNITS = f"{WORK}/plates", f"{WORK}/labels", f"{WORK}/units"
W, H, FPS = 1920, 1080, 24
GOLD, GOLD_DIM = (212, 175, 55), (176, 146, 52)
FD = "/usr/share/fonts/truetype/freefont/"
F_REG, F_BOLD, F_IT = FD + "FreeSerif.ttf", FD + "FreeSerifBold.ttf", FD + "FreeSerifItalic.ttf"
BAR = 138          # letterbox bar height -> 2.39:1 picture on backdrop stills
SHOT = 3.3         # target shot length (s) under narration
for d in (PLATES, LABELS, UNITS):
    os.makedirs(d, exist_ok=True)

def font(path, size): return ImageFont.truetype(path, size)

def tracked(draw, xy, text, fnt, fill, track=0, anchor="l"):
    """Draw upper-case text with letter spacing. anchor 'l' | 'm' (centered on x)."""
    widths = [fnt.getlength(c) + track for c in text]
    total = sum(widths) - track
    x, y = xy
    if anchor == "m": x -= total / 2
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += w
    return total

def tracked_width(text, fnt, track): return sum(fnt.getlength(c) + track for c in text) - track

def cover(img, w, h):
    s = max(w / img.width, h / img.height)
    img = img.resize((math.ceil(img.width * s), math.ceil(img.height * s)), Image.LANCZOS)
    l, t = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((l, t, l + w, t + h))

def blur_bg(img):
    bg = cover(img.convert("RGB"), W, H).filter(ImageFilter.GaussianBlur(38))
    return ImageEnhance.Brightness(bg).enhance(0.30)

def feathered(img, feather=26):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rectangle((feather, feather, img.width - feather, img.height - feather), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(feather * 0.55))
    out = img.convert("RGBA"); out.putalpha(m); return out

def vignette_plate(base, strength=0.55):
    v = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(v)
    d.ellipse((-W * 0.25, -H * 0.35, W * 1.25, H * 1.35), fill=255)
    v = v.filter(ImageFilter.GaussianBlur(150))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(base, Image.blend(dark, base, 1 - strength), v)

# ------------------------------------------------------------------ plates
def plate_path(key): return f"{PLATES}/{hashlib.md5(key.encode()).hexdigest()[:12]}.png"

def make_plate(key, side="right"):
    out = plate_path(key + "|" + side)
    if os.path.exists(out): return out
    kind = key.split(":", 1)[0]
    if kind == "tmdb":
        _, k, n = key.split(":")
        src = Image.open(f"{ROOT}/footage/tmdb/{k}/{n}.jpg").convert("RGB")
        if n.startswith("b"):
            im = cover(src, W, H)
        else:
            bg = blur_bg(src)
            ph = 960 if n.startswith("p") and not n.startswith("post") else 900
            scale = min(ph / src.height, 900 / src.width)
            fg = feathered(src.resize((int(src.width * scale), int(src.height * scale)), Image.LANCZOS))
            cx = int(W * 0.68) if side == "right" else int(W * 0.30)
            bg.paste(fg, (cx - fg.width // 2, (H - fg.height) // 2), fg)
            im = vignette_plate(bg, 0.5)
    elif kind == "place":
        name, sub, coords = (key.split(":", 1)[1].split("|") + ["", ""])[:3]
        glow = Image.radial_gradient("L").resize((W, H), Image.BICUBIC)      # 0 centre -> 255 edge
        glow = glow.point(lambda v: int(30 * (1 - v / 255) ** 1.6))
        im = Image.merge("RGB", (glow.point(lambda v: v + 7), glow.point(lambda v: v + 6), glow.point(lambda v: v + 5)))
        d = ImageDraw.Draw(im)
        size = 112
        lines = textwrap.wrap(name, 22) or [name]
        while tracked_width(max(lines, key=len), font(F_REG, size), 10) > W - 260: size -= 6
        fn = font(F_REG, size)
        y = H / 2 - 90 - (len(lines) - 1) * size * 0.55
        for ln in lines:
            tracked(d, (W / 2, y), ln, fn, GOLD, 10, "m"); y += size * 1.1
        d.line((W / 2 - 110, y + 18, W / 2 + 110, y + 18), fill=GOLD, width=2)
        if sub: tracked(d, (W / 2, y + 48), sub, font(F_REG, 34), (230, 224, 205), 7, "m")
        if coords: tracked(d, (W / 2, y + 108), coords, font(F_REG, 26), GOLD_DIM, 6, "m")
    elif kind == "chapter":
        num, ttl = key.split(":", 1)[1].split("|")
        im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
        tracked(d, (W / 2, 400), f"CHAPTER {num}", font(F_REG, 34), GOLD, 16, "m")
        d.line((W / 2 - 150, 466, W / 2 + 150, 466), fill=GOLD, width=2)
        size = 84
        while tracked_width(ttl, font(F_REG, size), 9) > W - 240: size -= 4
        tracked(d, (W / 2, 506), ttl, font(F_REG, size), GOLD, 9, "m")
    elif kind == "quote":
        text, attr, bgk = (key.split(":", 1)[1].split("|") + ["", ""])[:3]
        if bgk.startswith("tmdb:"):
            _, k, n = bgk.split(":")
            im = blur_bg(Image.open(f"{ROOT}/footage/tmdb/{k}/{n}.jpg"))
            im = ImageEnhance.Brightness(im).enhance(0.55)
        else:
            im = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(im)
        size = 66 if len(text) < 100 else 54
        lines = textwrap.wrap(text, 34 if size == 66 else 42)
        y = H / 2 - len(lines) * size * 0.62 - 20
        fn = font(F_IT, size)
        for ln in lines:
            w = d.textlength(ln, font=fn); d.text((W / 2 - w / 2, y), ln, font=fn, fill=(238, 232, 214)); y += size * 1.25
        d.line((W / 2 - 80, y + 24, W / 2 + 80, y + 24), fill=GOLD, width=2)
        if attr: tracked(d, (W / 2, y + 56), attr, font(F_REG, 30), GOLD, 8, "m")
    elif kind == "end":
        im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
        fn = font(F_IT, 68)
        for i, ln in enumerate(["FAME CREATES STARS.", "TIME TURNS THEM INTO DUST."]):
            w = d.textlength(ln, font=fn); d.text((W / 2 - w / 2, 400 + i * 92), ln, font=fn, fill=(238, 232, 214))
        d.line((W / 2 - 80, 625, W / 2 + 80, 625), fill=GOLD, width=2)
        tracked(d, (W / 2, 660), "STARDUST STORY", font(F_REG, 34), GOLD, 16, "m")
        tracked(d, (W / 2, 1010), "THIS PRODUCT USES THE TMDB API BUT IS NOT ENDORSED OR CERTIFIED BY TMDB.", font(F_REG, 20), (140, 135, 120), 3, "m")
    else:
        raise ValueError(key)
    im.save(out); return out

# ------------------------------------------------------------------ labels
def make_label(spec, persist=False):
    kind = spec[0]
    out = f"{LABELS}/{hashlib.md5(repr((spec, persist)).encode()).hexdigest()[:12]}.png"
    if os.path.exists(out): return out
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if kind in ("name", "title"):
        _, l1, l2 = spec
        g = Image.new("L", (1, H))                       # dark gradient for legibility
        g.putdata([int(235 * min(1, max(0, (y - H * 0.50) / (H * 0.42))) ** 1.25) for y in range(H)])
        im.paste((0, 0, 0, 255), (0, 0), g.resize((W, H)))
        size = 60
        while tracked_width(l1, font(F_REG, size), 6) > W - 420: size -= 4
        def draw_all(dr, c1, c2, c3):
            dr.rectangle((96, 846, 99, 846 + size + (60 if l2 else 0)), fill=c3)
            tracked(dr, (124, 838), l1, font(F_REG, size), c1, 6)
            if l2: tracked(dr, (124, 838 + size + 18), l2, font(F_REG, 28), c2, 6)
        sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_all(ImageDraw.Draw(sh), (0, 0, 0, 255), (0, 0, 0, 255), (0, 0, 0, 255))
        sh = sh.filter(ImageFilter.GaussianBlur(7))
        im = Image.alpha_composite(im, sh); im = Image.alpha_composite(im, sh)
        draw_all(ImageDraw.Draw(im), GOLD + (255,), (240, 230, 190, 255), GOLD + (255,))
    elif kind == "stat":
        _, big, cap = spec
        d.rectangle((0, 0, W, H), fill=(0, 0, 0, 150))
        size = 260
        while tracked_width(big, font(F_REG, size), 14) > W - 300: size -= 10
        tracked(d, (W / 2, H / 2 - size * 0.62), big, font(F_REG, size), GOLD, 14, "m")
        d.line((W / 2 - 120, H / 2 + size * 0.55, W / 2 + 120, H / 2 + size * 0.55), fill=GOLD, width=2)
        tracked(d, (W / 2, H / 2 + size * 0.55 + 28), cap, font(F_REG, 38), (236, 228, 200), 9, "m")
    elif kind == "series":
        _, a, b = spec
        w = tracked(d, (110, 66), a, font(F_REG, 26), GOLD, 11)
        d.text((110 + w + 22, 66), "·", font=font(F_REG, 26), fill=GOLD)
        tracked(d, (110 + w + 52, 66), b, font(F_REG, 26), GOLD, 11)
    im.save(out); return out

# ------------------------------------------------------------------ shots
def build_shots():
    segs, shots = TL.SEGS, []
    f_end = round(TL.T_END * FPS)
    pick = 0
    for i, s in enumerate(segs):
        f0 = round(s["t0"] * FPS)
        f1 = round(segs[i + 1]["t0"] * FPS) if i + 1 < len(segs) else f_end
        if s["dur"]: f1 = min(f1, f0 + round(s["dur"] * FPS))
        if i + 1 < len(segs) and s["dur"]:
            pass
        n = 1 if s["nosplit"] else max(1, round((f1 - f0) / FPS / SHOT))
        edges = [f0 + round((f1 - f0) * k / n) for k in range(n + 1)]
        for k in range(n):
            plates = s["plates"]
            key = plates[k % len(plates)]
            shots.append(dict(f0=edges[k], f1=edges[k + 1], plate=key, label=s["label"] if k == 0 else None,
                              flash=s["flash"] and k == 0, dissolve=s["dissolve"], seg=i, first_in_seg=k == 0,
                              kb=s["kb"]))
    # chapter cards: gap after the card (segment dur override) is filled by extending the next shot backwards
    fixed = []
    for a, b in zip(shots, shots[1:] + [None]):
        if b is not None and a["f1"] < b["f0"]: a["f1"] = b["f0"]
    # no-two-in-a-row of the same plate
    for a, b in zip(shots, shots[1:]):
        if a["plate"] == b["plate"] and not a["plate"].startswith(("chapter", "quote", "end")):
            pass
    return shots

def kb_exprs(shot, idx, N):
    kind = shot["plate"].split(":", 1)[0]
    amt = 0.035 if kind in ("chapter", "quote", "end", "place") else 0.085
    mode = shot["kb"] or ["in", "out", "in", "pan"][idx % 4]
    if mode == "in":   z, fx = f"1+{amt}*on/{N}", (0.5, 0.5)
    elif mode == "out": z, fx = f"{1 + amt}-{amt}*on/{N}", (0.5, 0.5)
    else:              z, fx = f"1+{amt * 0.7}*on/{N}", ((0.25, 0.75) if idx % 8 < 4 else (0.75, 0.25))
    fy = (0.45, 0.55) if idx % 3 == 0 else (0.55, 0.45) if idx % 3 == 1 else (0.5, 0.5)
    x = f"(iw-iw/zoom)*({fx[0]}+({fx[1]}-{fx[0]})*on/{N})"
    y = f"(ih-ih/zoom)*({fy[0]}+({fy[1]}-{fy[0]})*on/{N})"
    return z, x, y

def group_units(shots):
    units, i = [], 0
    while i < len(shots):
        a = shots[i]
        if a["dissolve"] and i + 1 < len(shots) and shots[i + 1]["seg"] == a["seg"] and (a["f1"] - a["f0"]) > 14 and (shots[i + 1]["f1"] - shots[i + 1]["f0"]) > 14:
            units.append([a, shots[i + 1]]); i += 2
        else:
            units.append([a]); i += 1
    return units

def render_unit(args):
    uid, unit, base_idx = args
    out = f"{UNITS}/{uid:04d}.mp4"
    total = sum(s["f1"] - s["f0"] for s in unit)
    if os.path.exists(out): return out
    inputs, filt = [], []
    for k, s in enumerate(unit):
        side = "left" if (base_idx + k) % 3 == 2 and not s["label"] else "right"
        inputs += ["-i", make_plate(s["plate"], side)]
    n_img = len(unit)
    frames = [s["f1"] - s["f0"] for s in unit]
    for k, s in enumerate(unit):
        N = frames[k] + (6 if len(unit) == 2 else 0)
        z, x, y = kb_exprs(s, base_idx + k, N)
        bars = ""
        if s["plate"].startswith("tmdb:") and s["plate"].split(":")[2].startswith("b"):
            bars = f",drawbox=0:0:{W}:{BAR}:black:fill,drawbox=0:{H - BAR}:{W}:{BAR}:black:fill"
        filt.append(f"[{k}:v]scale=2400:1350:flags=bicubic,zoompan=z='{z}':x='{x}':y='{y}':d={N}:s={W}x{H}:fps={FPS}{bars},setsar=1,format=yuv420p[s{k}]")
    if len(unit) == 2:
        off = (frames[0] + 6 - 12) / FPS
        filt.append(f"[s0][s1]xfade=transition=fade:duration=0.5:offset={off:.4f}[base]")
    else:
        filt.append("[s0]null[base]")
    cur = "base"
    if unit[0]["flash"]:
        filt.append(f"[{cur}]fade=t=in:st=0:d=0.22:color=white[fl]"); cur = "fl"
    if unit[0]["f0"] == 0:
        filt.append(f"[{cur}]fade=t=in:st=0:d=1.5[fi]"); cur = "fi"
    # overlays
    t_off, li = 0.0, n_img
    for k, s in enumerate(unit):
        dur = frames[k] / FPS
        ovl = []
        if s["label"]: ovl.append((make_label(s["label"]), True))
        if s["f0"] / FPS < TL.SERIES_TAG_UNTIL and s["plate"].startswith("tmdb:"):
            ovl.append((make_label(("series",) + TL.SERIES_TAG, True), False))
        for path, fades in ovl:
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{total / FPS + 1:.3f}", "-i", path]
            chain = f"[{li}:v]format=rgba"
            if fades:
                chain += f",fade=t=in:st={t_off + 0.25:.3f}:d=0.4:alpha=1,fade=t=out:st={t_off + dur - 0.55:.3f}:d=0.4:alpha=1"
            elif t_off == 0 and s["f0"] > 0:
                chain += f",fade=t=in:st=0:d=0.4:alpha=1"
            filt.append(f"{chain}[o{li}]")
            filt.append(f"[{cur}][o{li}]overlay=0:0:format=auto:shortest=1[c{li}]"); cur = f"c{li}"; li += 1
        t_off += dur
    cmd = ["ffmpeg", "-v", "error", "-y"] + inputs + ["-filter_complex", ";".join(filt), "-map", f"[{cur}]",
           "-frames:v", str(total), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16",
           "-pix_fmt", "yuv420p", "-an", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not os.path.exists(out):
        print("FAIL unit", uid, r.stderr[-600:]); sys.exit(1)
    return out

# ------------------------------------------------------------------ stages
def stage_plan():
    shots = build_shots(); units = group_units(shots)
    print(f"{len(shots)} shots in {len(units)} units; total frames {sum(s['f1']-s['f0'] for s in shots)} = {sum(s['f1']-s['f0'] for s in shots)/FPS:.2f}s")
    return shots, units

def stage_render(limit=None):
    shots, units = stage_plan()
    jobs, idx = [], 0
    for u, unit in enumerate(units):
        jobs.append((u, unit, idx)); idx += len(unit)
    if limit: jobs = jobs[:limit]
    done = 0
    with cf.ThreadPoolExecutor(4) as ex:
        for _ in ex.map(render_unit, jobs):
            done += 1
            if done % 20 == 0: print(f"  rendered {done}/{len(jobs)}", flush=True)
    if not limit:
        with open(f"{WORK}/concat.txt", "w") as f:
            for u in range(len(units)): f.write(f"file '{UNITS}/{u:04d}.mp4'\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{WORK}/concat.txt", "-c", "copy", f"{WORK}/picture.mp4"], check=True)
        print("picture.mp4 done")

def stage_audio():
    narr = [f"{ROOT}/public/stardust-story/{n}.mp3" for n in ("hook", "act1", "act2", "act3", "act4", "act5", "end")]
    T = TL.T_END
    # narration
    ins = sum([["-i", p] for p in narr], [])
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex",
        "".join(f"[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];" for i in range(7)) + "".join(f"[a{i}]" for i in range(7)) + f"concat=n=7:v=0:a=1,apad=whole_dur={T},atrim=0:{T}[n]",
        "-map", "[n]", f"{WORK}/narration.wav"], check=True)
    # music bed: low drone + pink-noise air, slow swell
    subprocess.run(["ffmpeg", "-v", "error", "-y",
        "-f", "lavfi", "-i", f"sine=f=55:d={T}:r=48000", "-f", "lavfi", "-i", f"sine=f=82.4:d={T}:r=48000",
        "-f", "lavfi", "-i", f"sine=f=110.6:d={T}:r=48000", "-f", "lavfi", "-i", f"sine=f=164.9:d={T}:r=48000",
        "-f", "lavfi", "-i", f"anoisesrc=d={T}:c=pink:r=48000:a=0.06",
        "-filter_complex",
        "[0]volume=1.0[a];[1]volume=0.6,tremolo=f=0.11:d=0.5[b];[2]volume=0.35,tremolo=f=0.13:d=0.6[c];[3]volume=0.18,tremolo=f=0.1:d=0.7[d];[4]lowpass=f=420,volume=0.7[e];"
        "[a][b][c][d][e]amix=inputs=5:normalize=0,lowpass=f=500,aecho=0.8:0.6:900|1700:0.35|0.25,"
        "volume='0.55+0.25*sin(2*PI*t/47)':eval=frame,aformat=channel_layouts=stereo,"
        f"afade=t=in:d=3,afade=t=out:st={T-4}:d=4[m]", "-map", "[m]", f"{WORK}/music.wav"], check=True)
    # sfx: sub hit + whoosh
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=f=46:d=1.6:r=48000", "-f", "lavfi",
        "-i", "anoisesrc=d=1.6:c=pink:r=48000:a=0.5", "-filter_complex",
        "[0]afade=t=in:d=0.02,afade=t=out:st=0.05:d=1.5,volume=2.2[h];"
        "[1]highpass=f=500,lowpass=f=7000,afade=t=in:d=1.0,afade=t=out:st=1.0:d=0.5,volume=0.5[w];"
        "[h][w]amix=inputs=2:normalize=0,aformat=channel_layouts=stereo[x]", "-map", "[x]", f"{WORK}/sfx_hit.wav"], check=True)
    ev = [(x - 0.6, 1.0) for x in TL.SFX_CHAPTERS] + [(x, 0.55) for x in TL.SFX_STATS] + [(x - 0.3, 0.7) for x in TL.SFX_QUOTES]
    ev = [(max(0, a), g) for a, g in ev]
    parts = "".join(f"[s{i}]adelay={int(a * 1000)}|{int(a * 1000)},volume={g}[d{i}];" for i, (a, g) in enumerate(ev))
    split = f"[0:a]asplit={len(ev)}" + "".join(f"[s{i}]" for i in range(len(ev))) + ";"
    mix = "[1:a]" + "".join(f"[d{i}]" for i in range(len(ev))) + f"amix=inputs={len(ev) + 1}:duration=first:normalize=0[sfx]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/sfx_hit.wav", "-f", "lavfi", "-t", f"{T}", "-i", "anullsrc=r=48000:cl=stereo",
                    "-filter_complex", split + parts + mix, "-map", "[sfx]", f"{WORK}/sfx.wav"], check=True)
    # final mix: duck music under narration
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/narration.wav", "-i", f"{WORK}/music.wav", "-i", f"{WORK}/sfx.wav",
        "-filter_complex",
        "[0]highpass=f=70,acompressor=threshold=0.08:ratio=3:attack=10:release=200,loudnorm=I=-16:TP=-1.5:LRA=9,asplit[nv][sc];"
        "[1]volume=1.1[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=9:attack=30:release=500[duck];"
        f"[nv][duck][2]amix=inputs=3:normalize=0:weights='1 0.9 0.8',alimiter=limit=0.95,apad=whole_dur={T},atrim=0:{T}[out]",
        "-map", "[out]", "-ar", "48000", f"{WORK}/mix.wav"], check=True)
    print("audio done")

def stage_final():
    T = TL.T_END
    outdir = f"{ROOT}/output/stardust-story"; os.makedirs(outdir, exist_ok=True)
    vf = ("eq=contrast=1.07:saturation=0.93:gamma=0.98,colorbalance=rs=-0.03:gs=0.0:bs=0.04:rh=0.04:gh=0.01:bh=-0.04,"
          "vignette=PI/5,noise=alls=6:allf=t+u,"
          f"fade=t=out:st={T-1.8}:d=1.8")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/picture.mp4", "-i", f"{WORK}/mix.wav", "-vf", vf,
        "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-af", f"afade=t=out:st={T-2}:d=2", "-movflags", "+faststart", "-shortest",
        f"{outdir}/stardust-story-karen-page.mp4"], check=True)
    print("final done")

if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "plan"
    if st == "plan": stage_plan()
    elif st == "render": stage_render(int(sys.argv[2]) if len(sys.argv) > 2 else None)
    elif st == "audio": stage_audio()
    elif st == "final": stage_final()
    elif st == "all": stage_render(); stage_audio(); stage_final()
