#!/usr/bin/env python3
"""Build the Ernie Reyes Jr. documentary from the two voiceover MP3s.

Usage:  python3 production/ernie-build.py [--only s04,s05] [--res 1920x1080]

Every scene has a media slot.  Drop a clip or photo named <scene-id>.mp4/.mov/.mkv/
.jpg/.png into  production/media/  (e.g. s10.mp4 for The Last Dragon) and re-run:
the clip replaces the generated card, gets graded, and keeps all the labels.
Scenes without media use an animated generated title card.
"""
import argparse, math, os, random, subprocess, sys, glob, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(ROOT, "media")
WORK = os.environ.get("ERNIE_WORK", "/tmp/ernie-work")
OUT = os.path.join(os.path.dirname(ROOT), "output", "ernie-reyes-jr.mp4")
VO1 = "/root/.claude/uploads/d9ee64d3-1860-5d99-bef8-6d5081458d32/f8de7028-11CapCut_TTS_Bill_D20260713_T081806.mp3"
VO2 = "/root/.claude/uploads/d9ee64d3-1860-5d99-bef8-6d5081458d32/9138e33a-22CapCut_TTS_Bill_D20260713_T082752.mp3"
P1, TOTAL = 694.595918, 694.595918 + 342.674285
FPS = 24
F = "/usr/share/fonts/opentype/inter/"
def font(name, size):
    return ImageFont.truetype(F + name + ".otf", size)

RED, AMBER, CREAM = (229, 9, 20), (255, 190, 90), (245, 238, 225)
THEMES = {  # chapter palettes: (center glow, edge)
    "open": ((60, 14, 14), (6, 4, 6)), "prodigy": ((70, 48, 14), (8, 6, 4)),
    "break": ((16, 56, 70), (4, 8, 10)), "fall": ((64, 16, 22), (8, 4, 5)),
    "second": ((40, 44, 60), (5, 6, 9)), "battle": ((22, 50, 52), (4, 8, 9)),
    "legacy": ((78, 54, 20), (8, 6, 4)),
}
def p2(m, s): return P1 + m * 60 + s
def p1(m, s): return m * 60 + s

# id, start, theme, chapter(kicker), headline lines, labels, watermark
# labels: ("name", text, sub) | ("movie", title, year) | ("city", text) | ("money", big, caption)
SC = [
 ("s01", p1(0, 0), "open", "STARDUST STORY", ["Whatever happened", "to that kid?"], [], ""),
 ("s02", p1(0, 20), "open", "THE EARLY 1990s", ["Impossible", "to ignore."], [("name", "ERNIE REYES JR.", "Martial artist · Actor")], "1990"),
 ("s03", p1(0, 41), "open", "", ["Then it", "all stopped."], [], ""),
 ("s04", p1(1, 3), "open", "", ["ERNIE REYES JR.", "The kid Hollywood forgot"], [], ""),
 ("s05", p1(1, 25), "prodigy", "CHAPTER I · THE PRODIGY", ["Born to", "the dojo."], [("city", "CALIFORNIA, USA · 1972")], "1972"),
 ("s06", p1(1, 48), "prodigy", "THE FATHER", ["Speed. Flexibility.", "Showmanship."], [("name", "ERNIE REYES SR.", "Master instructor · Father")], ""),
 ("s07", p1(2, 11), "prodigy", "", ["Every kick sharper.", "Every landing cleaner."], [], ""),
 ("s08", p1(2, 33), "prodigy", "THE DEMONSTRATION TEAM", ["Across", "America."], [("city", "UNITED STATES · TOURING")], ""),
 ("s09", p1(3, 0), "prodigy", "THE MID-1980s", ["Hollywood", "came calling."], [("name", "BRUCE LEE", "The inspiration")], "1985"),
 ("s10", p1(3, 29), "prodigy", "FIRST CREDITS", ["Learning", "the craft."], [("movie", "THE LAST DRAGON", "1985")], ""),
 ("s11", p1(3, 51), "prodigy", "SHARING THE SCREEN", ["Work hard.", "Stay humble."], [("movie", "RED SONJA", "1985")], ""),
 ("s12", p1(4, 14), "prodigy", "", ["Never missed", "a mark."], [], ""),
 ("s13", p1(4, 37), "prodigy", "", ["TV. Guest roles.", "Commercials."], [], ""),
 ("s14", p1(5, 1), "break", "CHAPTER II · THE BREAKTHROUGH", ["Millions watched him", "without knowing."], [("movie", "TEENAGE MUTANT NINJA TURTLES", "1990")], "1990"),
 ("s15", p1(5, 26), "break", "INSIDE THE SUIT", ["Every punch.", "Every flip."], [], ""),
 ("s16", p1(5, 51), "break", "THE PERFECT FIT", ["Donatello."], [("name", "DONATELLO", "Suit performance")], ""),
 ("s17", p1(6, 13), "break", "AN UNEXPECTED SENSATION", ["Modest budget.", "Massive hit."], [("money", "~$13.5M → ~$202M", "BUDGET → WORLDWIDE GROSS · TMNT (1990)")], ""),
 ("s18", p1(6, 34), "break", "THE SEQUEL", ["A chance", "to be seen."], [("movie", "TMNT II: THE SECRET OF THE OOZE", "1991"), ("name", "KENO", "Played by Ernie Reyes Jr.")], "1991"),
 ("s19", p1(7, 1), "break", "", ["Kids copied", "his kicks."], [], ""),
 ("s20", p1(7, 26), "break", "", ["Magazines.", "VHS covers."], [], ""),
 ("s21", p1(7, 46), "break", "THE NEXT STEP", ["His own", "movie."], [], ""),
 ("s22", p1(8, 10), "fall", "CHAPTER III · THE FALL", ["Surf Ninjas."], [("movie", "SURF NINJAS", "1993")], "1993"),
 ("s23", p1(8, 37), "fall", "A GENRE GAMBLE", ["Too many", "ideas at once."], [], ""),
 ("s24", p1(8, 58), "fall", "THE VERDICT", ["Quietly gone", "from theaters."], [("money", "BOX OFFICE DISAPPOINTMENT", "SURF NINJAS (1993)"), ("name", "JEAN-CLAUDE VAN DAMME", "The league he missed")], ""),
 ("s25", p1(9, 28), "fall", "", ["Numbers matter", "more than potential."], [], ""),
 ("s26", p1(9, 48), "fall", "", ["Not less talented.", "Just smaller roles."], [], ""),
 ("s27", p1(10, 10), "fall", "", ["He", "adapted."], [], ""),
 ("s28", p1(10, 42), "fall", "", ["The spotlight faded.", "Hollywood still called."], [], ""),
 ("s29", p1(11, 4), "second", "CHAPTER IV · THE SECOND ACT", ["The hidden army", "of Hollywood."], [("city", "HOLLYWOOD, CALIFORNIA")], "2000s"),
 ("s30", p1(11, 25), "second", "", ["Ernie found", "his place."], [], ""),
 ("s31", p2(0, 22), "second", "2003", ["The fight", "everyone remembers."], [("movie", "THE RUNDOWN", "2003"), ("name", "DWAYNE JOHNSON", "Star of The Rundown"), ("name", "MANITO", "Played by Ernie Reyes Jr.")], "2003"),
 ("s32", p2(0, 46), "second", "", ["Fast. Physical.", "Creative."], [], ""),
 ("s33", p2(1, 12), "second", "", ["What if?"], [], ""),
 ("s34", p2(1, 32), "second", "", ["Some get many chances.", "Others get one."], [], ""),
 ("s35", p2(1, 51), "battle", "CHAPTER V · THE BATTLE", ["A challenge", "no script could write."], [("city", "2014 · KIDNEY FAILURE")], "2014"),
 ("s36", p2(2, 16), "battle", "", ["The world", "reached out."], [], ""),
 ("s37", p2(2, 38), "battle", "A SECOND CHANCE", ["His sister's", "gift."], [("money", "FUNDRAISING CAMPAIGN", "MEDICAL EXPENSES · KIDNEY TRANSPLANT")], ""),
 ("s38", p2(3, 1), "battle", "", ["Simple movements", "became victories."], [], ""),
 ("s39", p2(3, 22), "battle", "", ["Passing it", "on."], [], ""),
 ("s40", p2(3, 47), "battle", "", ["A different", "definition of success."], [], ""),
 ("s41", p2(4, 15), "legacy", "CHAPTER VI · THE LEGACY", ["Not every talent", "becomes A-list."], [], ""),
 ("s42", p2(4, 40), "legacy", "", ["Something", "much rarer."], [("name", "JACKIE CHAN", "The star he never had to be")], ""),
 ("s43", p2(5, 10), "legacy", "STARDUST STORY", ["Your favorite", "Ernie performance?"], [], ""),
]

def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit("FAILED: " + " ".join(cmd[:6]) + "\n" + r.stderr[-1800:])
    return r

def frames():
    b = [round(s[1] * FPS) for s in SC] + [round(TOTAL * FPS)]
    return [(SC[i][0], b[i], b[i + 1] - b[i]) for i in range(len(SC))]

# ---------- generated background (original art: glow, streaks, perforation strip, watermark) ----------
def make_bg(W, H, theme, mark, seed, path):
    c, e = THEMES[theme]
    rnd = random.Random(seed)
    img = Image.new("RGB", (W, H), e)
    px = Image.new("RGB", (W, H), e)
    glow = Image.new("RGB", (W, H), c)
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    cx, cy = int(W * rnd.uniform(0.35, 0.65)), int(H * rnd.uniform(0.4, 0.6))
    d.ellipse([cx - W * 0.55, cy - H * 0.75, cx + W * 0.55, cy + H * 0.75], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(W // 6))
    img = Image.composite(glow, img, mask)
    # diagonal light streaks
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for _ in range(5):
        x = rnd.randint(-W // 4, W); w = rnd.randint(30, 160)
        od.polygon([(x, 0), (x + w, 0), (x + w - H // 2, H), (x - H // 2, H)], fill=(*CREAM, rnd.randint(4, 12)))
    ov = ov.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img.convert("RGBA"), ov)
    # film perforation strips
    od = ImageDraw.Draw(img)
    for x0 in (int(W * 0.035), int(W * 0.945)):
        for y in range(-20, H, 70):
            od.rounded_rectangle([x0, y, x0 + 34, y + 44], 8, fill=(0, 0, 0, 120))
    if mark:
        f = font("InterDisplay-Black", int(H * 0.5))
        tw = ImageDraw.Draw(img).textlength(mark, font=f)
        while tw > W * 0.95:
            f = font("InterDisplay-Black", int(f.size * 0.9)); tw = ImageDraw.Draw(img).textlength(mark, font=f)
        wm = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(wm).text((W / 2 - tw / 2, H * 0.17), mark, font=f, fill=(*CREAM, 16))
        img = Image.alpha_composite(img, wm)
    img.convert("RGB").save(path, quality=95)

# ---------- text overlays ----------
def shadow_text(img, xy, text, f, fill, spacing=0, anchor="la"):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((xy[0] + 3, xy[1] + 4), text, font=f, fill=(0, 0, 0, 200), anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(5))
    img.alpha_composite(layer)
    d = ImageDraw.Draw(img)
    if spacing:
        x = xy[0]
        for ch in text:
            d.text((x, xy[1]), ch, font=f, fill=fill, anchor=anchor); x += d.textlength(ch, font=f) + spacing
    else:
        d.text(xy, text, font=f, fill=fill, anchor=anchor)

def spaced_w(text, f, sp):
    d = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    return sum(d.textlength(c, font=f) + sp for c in text) - sp

def png_kicker(W, H, text, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x, y = int(W * 0.075), int(H * 0.455)
    d.rectangle([x, y, x + int(6 * s), y + int(34 * s)], fill=RED)
    shadow_text(img, (x + int(22 * s), y + int(2 * s)), text, font("Inter-SemiBold", int(28 * s)), (*AMBER, 255), spacing=int(5 * s))
    img.save(path)

def png_headline(W, H, text, idx, nlines, path, big=True, maxw=0.85):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    size = int((112 if big else 84) * s)
    f = font("InterDisplay-Black", size)
    while ImageDraw.Draw(img).textlength(text, font=f) > W * maxw and size > 40:
        size -= 4; f = font("InterDisplay-Black", size)
    x = int(W * 0.075)
    y = int(H * 0.515 + idx * size * 1.08)
    shadow_text(img, (x, y), text, f, (*CREAM, 255))
    img.save(path)

def png_center(W, H, title, sub, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    size = int(130 * s); f = font("InterDisplay-Black", size)
    while ImageDraw.Draw(img).textlength(title, font=f) > W * 0.86: size -= 4; f = font("InterDisplay-Black", size)
    shadow_text(img, (W / 2, H * 0.44), title, f, (*CREAM, 255), anchor="mm")
    if sub:
        fs = font("Inter-SemiBold", int(34 * s)); sp = int(8 * s); sw = spaced_w(sub.upper(), fs, sp)
        shadow_text(img, (W / 2 - sw / 2, H * 0.44 + size * 0.85), sub.upper(), fs, (*AMBER, 255), spacing=sp)
    img.save(path)

def png_name(W, H, name, sub, slot, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x, y = int(W * 0.075), int(H * 0.765) - slot * int(120 * s)
    f1, f2 = font("InterDisplay-ExtraBold", int(50 * s)), font("Inter-Medium", int(26 * s))
    w = max(d.textlength(name, font=f1), d.textlength(sub, font=f2)) + int(60 * s)
    d.rectangle([x - 20 * s, y - 14 * s, x + w, y + 96 * s], fill=(0, 0, 0, 150))
    d.rectangle([x - 20 * s, y - 14 * s, x - 14 * s, y + 96 * s], fill=RED)
    shadow_text(img, (x + 8 * s, y), name, f1, (*CREAM, 255))
    shadow_text(img, (x + 8 * s, y + 62 * s), sub.upper(), f2, (*AMBER, 255), spacing=int(2 * s))
    img.save(path)

def png_movie(W, H, title, year, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x, y = int(W * 0.075), int(H * 0.215)
    f1 = font("InterDisplay-Black", int(54 * s))
    while d.textlength(title, font=f1) > W * 0.8: f1 = font("InterDisplay-Black", int(f1.size * 0.92))
    d.rectangle([x, y - 4 * s, x + 5 * s, y + 118 * s], fill=AMBER)
    shadow_text(img, (x + 24 * s, y), "FILM", font("Inter-SemiBold", int(22 * s)), (*AMBER, 255), spacing=int(6 * s))
    shadow_text(img, (x + 24 * s, y + 30 * s), title, f1, (*CREAM, 255))
    shadow_text(img, (x + 24 * s, y + 30 * s + f1.size * 1.15), year, font("Inter-Medium", int(30 * s)), (*CREAM, 210), spacing=int(4 * s))
    img.save(path)

def png_city(W, H, text, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("Inter-Bold", int(34 * s)); sp = int(5 * s)
    tw = spaced_w(text, f, sp)
    x = W - int(W * 0.075) - tw; y = int(H * 0.215)
    r = 14 * s; cx, cy = x - 44 * s, y + 20 * s
    d.polygon([(cx - r, cy), (cx + r, cy), (cx, cy + 2.2 * r)], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    d.ellipse([cx - r / 2.4, cy - r / 2.4, cx + r / 2.4, cy + r / 2.4], fill=(0, 0, 0, 255))
    shadow_text(img, (x, y), text, f, (*CREAM, 255), spacing=sp)
    img.save(path)

def png_money(W, H, big, cap, path):
    s = H / 1080
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    f = font("InterDisplay-Black", int(96 * s))
    while d.textlength(big, font=f) > W * 0.8: f = font("InterDisplay-Black", int(f.size * 0.92))
    bw = d.textlength(big, font=f) + 120 * s
    x0, y0 = W / 2 - bw / 2, H * 0.185
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + 250 * s], 16, fill=(0, 0, 0, 175), outline=(*AMBER, 230), width=int(3 * s))
    shadow_text(img, (W / 2, y0 + 105 * s), big, f, (*AMBER, 255), anchor="mm")
    shadow_text(img, (W / 2, y0 + 190 * s), cap, font("Inter-SemiBold", int(26 * s)), (*CREAM, 235), spacing=int(4 * s), anchor="mm") if False else None
    cw = spaced_w(cap, font("Inter-SemiBold", int(26 * s)), int(4 * s))
    shadow_text(img, (W / 2 - cw / 2, y0 + 178 * s), cap, font("Inter-SemiBold", int(26 * s)), (*CREAM, 235), spacing=int(4 * s))
    img.save(path)

def photo_card(src, W, H, path):
    """Blurred, darkened cover of the photo as backdrop + the photo itself, framed, on the right."""
    im = Image.open(src).convert("RGB")
    bg = im.copy(); r = max(W / bg.width, H / bg.height)
    bg = bg.resize((int(bg.width * r) + 1, int(bg.height * r) + 1))
    bg = bg.crop(((bg.width - W) // 2, (bg.height - H) // 2, (bg.width - W) // 2 + W, (bg.height - H) // 2 + H))
    bg = bg.filter(ImageFilter.GaussianBlur(H // 28))
    bg = Image.blend(bg, Image.new("RGB", (W, H), (6, 5, 5)), 0.62)
    ph = H * 0.62
    r = min(ph / im.height, (W * 0.5) / im.width)
    im = im.resize((int(im.width * r), int(im.height * r)))
    x, y = int(W * 0.80 - im.width / 2), int(H * 0.5 - im.height / 2)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([x - 6, y - 4, x + im.width + 14, y + im.height + 20], fill=(0, 0, 0, 190))
    bg = Image.alpha_composite(bg.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(14))).convert("RGB")
    ImageDraw.Draw(bg).rectangle([x - 3, y - 3, x + im.width + 2, y + im.height + 2], outline=(*CREAM,), width=2)
    bg.paste(im, (x, y)); bg.save(path, quality=95)

# ---------- ffmpeg ----------
# per-slot clip options: start offset (s) into the clip, fraction of frame height to crop off the bottom (watermarks)
SLOT_OPTS = {"s02": {"start": 2}, "s06": {"start": 60, "crop_bottom": 0.12}}

ALIAS = {"s02": "ernie_jr", "s09": "bruce", "s42": "chan", "s24": "jcvd", "s31": "rock"}

def find_media(sid):
    for name in (sid, ALIAS.get(sid)):
        if not name: continue
        for ext in ("mp4", "m4v", "mov", "mkv", "webm", "jpg", "jpeg", "png"):
            p = os.path.join(MEDIA, f"{name}.{ext}")
            if os.path.exists(p) and os.path.getsize(p) > 20000: return p
    return None

def _unused_find_media(sid):
    for ext in ("mp4", "m4v", "mov", "mkv", "webm", "jpg", "jpeg", "png"):
        p = os.path.join(MEDIA, f"{sid}.{ext}")
        if os.path.exists(p): return p
    return None

EASE = lambda s0, d: f"(1-pow(1-min(1,max(0,(t-{s0:.3f})/{d})),3))"

def render_scene(W, H, sc, f0, nf):
    sid, _, theme, kicker, lines, labels, mark = sc
    D = nf / FPS
    wd = os.path.join(WORK, sid); os.makedirs(wd, exist_ok=True)
    out = os.path.join(WORK, f"{sid}.mp4")
    media = find_media(sid)
    photo = bool(media) and media.lower().endswith((".jpg", ".jpeg", ".png"))
    inputs, fc = [], []
    # --- background ---
    if media and media.lower().endswith((".mp4", ".m4v", ".mov", ".mkv", ".webm")):
        o = SLOT_OPTS.get(sid, {})
        inputs += ["-stream_loop", "-1", "-ss", str(o.get("start", 0)), "-i", media]
        cb = o.get("crop_bottom", 0)
        pre = f"crop=iw:ih*{1-cb:.3f}:0:0," if cb else ""
        fc.append(f"[0:v]fps={FPS},{pre}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                  f"eq=contrast=1.1:saturation=0.88:brightness=-0.03,colorbalance=rs=-0.05:bs=0.06:rh=0.06:bh=-0.05,"
                  f"trim=duration={D:.3f},setpts=PTS-STARTPTS[bg0]")
    else:
        if media:
            src = os.path.join(wd, "bg.png"); photo_card(media, W * 2, H * 2, src)
        else:
            src = os.path.join(wd, "bg.png")
            make_bg(W * 2, H * 2, theme, mark, hash(sid) % 1000, src)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-i", src]
        fc.append(f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
                  f"zoompan=z='1+0.10*on/{nf}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},"
                  f"trim=duration={D:.3f},setpts=PTS-STARTPTS[bg0]")
    # dim lower third for legibility
    fc.append("[bg0]null[bg1]")
    # --- overlays ---
    ov = []   # (png, start, dur, kind)
    t = 0.35
    if kicker:
        p = os.path.join(wd, "k.png"); png_kicker(W, H, kicker, p); ov.append((p, 0.25, D - 0.9, "up"))
    big = len(lines) <= 2 and not (sid in ("s04",))
    if sid == "s04":
        p = os.path.join(wd, "c.png"); png_center(W, H, lines[0], lines[1], p); ov.append((p, 0.2, D - 0.7, "fade"))
    else:
        for i, ln in enumerate(lines):
            p = os.path.join(wd, f"h{i}.png"); png_headline(W, H, ln, i, len(lines), p, maxw=(0.58 if photo else 0.85)); ov.append((p, 0.35 + i * 0.28, D - 0.95 - i * 0.28, "up"))
    nslot, mslot = 0, 0
    for k, lab in enumerate(labels):
        at = min(2.0 + k * 6.2, max(1.0, D - 4.5))
        du = min(5.5, D - at - 0.6)
        if du < 1.5: at, du = 0.6, min(4.5, D - 1.2)
        p = os.path.join(wd, f"l{k}.png")
        if lab[0] == "name": png_name(W, H, lab[1], lab[2], 0, p); kind = "left"
        elif lab[0] == "movie": png_movie(W, H, lab[1], lab[2], p); kind = "left"
        elif lab[0] == "city": png_city(W, H, lab[1], p); kind = "right"
        else: png_money(W, H, lab[1], lab[2], p); kind = "pop"
        ov.append((p, at, du, kind))
    last = "bg1"
    for i, (p, st, du, kind) in enumerate(ov):
        du = max(0.8, du)
        inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{st+du+0.6:.3f}", "-i", p]
        n = i + 1
        fc.append(f"[{n}:v]format=rgba,fade=t=in:st={st:.3f}:d=0.55:alpha=1,fade=t=out:st={st+du:.3f}:d=0.45:alpha=1[o{i}]")
        e = EASE(st, 0.8)
        pos = {"up": ("0", f"40*(1-{e})"), "left": (f"-120*(1-{e})", "0"), "right": (f"120*(1-{e})", "0"), "fade": ("0", "0"),
               "pop": ("0", f"-24*(1-{e})")}[kind]
        fc.append(f"[{last}][o{i}]overlay=x='{pos[0]}':y='{pos[1]}':eof_action=pass:format=auto[v{i}]")
        last = f"v{i}"
    # --- cinematic finish: grade, vignette, grain, letterbox, fades ---
    bar = int(H * 0.1278)
    fc.append(f"[{last}]vignette=angle=0.55,noise=alls=5:allf=t,"
              f"drawbox=0:0:iw:{bar}:color=black:t=fill,drawbox=0:ih-{bar}:iw:{bar}:color=black:t=fill,"
              f"fade=t=in:st=0:d=0.35,fade=t=out:st={D-0.35:.3f}:d=0.35,format=yuv420p[vout]")
    script = os.path.join(wd, "graph.txt")
    open(script, "w").write(";\n".join(fc))
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *inputs, "-filter_complex_script", script,
        "-map", "[vout]", "-frames:v", str(nf), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "29",
        "-pix_fmt", "yuv420p", "-an", out])
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only"); ap.add_argument("--res", default="1920x1080"); ap.add_argument("--no-audio", action="store_true"); ap.add_argument("--assemble", action="store_true")
    a = ap.parse_args()
    W, H = map(int, a.res.split("x"))
    os.makedirs(WORK, exist_ok=True); os.makedirs(os.path.dirname(OUT), exist_ok=True); os.makedirs(MEDIA, exist_ok=True)
    only = set(a.only.split(",")) if a.only else None
    fr = frames(); scenes = {s[0]: s for s in SC}
    for sid, f0, nf in fr:
        if only and sid not in only: continue
        if a.assemble: continue
        print("scene", sid, f"{nf/FPS:.1f}s", "media" if find_media(sid) else "card", flush=True)
        render_scene(W, H, scenes[sid], f0, nf)
    if only and not a.assemble: return
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{WORK}/{sid}.mp4'\n" for sid, _, _ in fr))
    vid = os.path.join(WORK, "video.mp4")
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    # audio: voiceover + soft synthesized pad, gentle fade out
    vo = os.path.join(WORK, "vo.wav")
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", VO1, "-i", VO2, "-filter_complex",
        "[0:a][1:a]concat=n=2:v=0:a=1,aresample=48000,loudnorm=I=-16:TP=-1.5[a]", "-map", "[a]", vo])
    pad = f"sine=f=55:d={TOTAL},sine=f=82.4:d={TOTAL}"
    sh(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", vid, "-i", vo,
        "-f", "lavfi", "-i", f"sine=f=55:r=48000:d={TOTAL:.2f}", "-f", "lavfi", "-i", f"sine=f=82.41:r=48000:d={TOTAL:.2f}",
        "-filter_complex",
        f"[2:a][3:a]amix=inputs=2,lowpass=f=200,volume=0.045,tremolo=f=0.12:d=0.6[pad];"
        f"[1:a][pad]amix=inputs=2:duration=first:normalize=0,afade=t=out:st={TOTAL-2.5:.2f}:d=2.5[aout]",
        "-map", "0:v", "-map", "[aout]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT])
    print("wrote", OUT)

if __name__ == "__main__":
    main()
