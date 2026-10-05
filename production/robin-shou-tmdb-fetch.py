#!/usr/bin/env python3
"""Fetch Robin Shou edit assets from TMDB. Needs TMDB_TOKEN (v4 read token) in env."""
import json, os, sys, time, urllib.parse, urllib.request
TOK = os.environ.get("TMDB_TOKEN") or sys.exit("set TMDB_TOKEN")
OUT = os.path.join(os.path.dirname(__file__), "robin-shou-assets")
API, IMG = "https://api.themoviedb.org/3", "https://image.tmdb.org/t/p/"

def get(path, **q):
    r = urllib.request.Request(f"{API}{path}?{urllib.parse.urlencode(q)}",
                               headers={"Authorization": f"Bearer {TOK}"})
    return json.load(urllib.request.urlopen(r, timeout=20))

def dl(path, name, size="original"):
    dest = os.path.join(OUT, name)
    for attempt in range(4):
        if os.path.exists(dest): break
        try:
            urllib.request.urlretrieve(IMG + size + path, dest)
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return os.path.relpath(dest, os.path.dirname(os.path.abspath(__file__)))

def person(name, beat, n=2):
    p = get("/search/person", query=name)["results"][0]
    imgs = get(f"/person/{p['id']}/images")["profiles"][:n]
    slug = name.lower().replace(" ", "-")
    return {"beat": beat, "label": name.upper(), "tmdb_id": p["id"],
            "files": [dl(i["file_path"], f"{slug}-{k}.jpg") for k, i in enumerate(imgs)]}

def movie(title, year, beat, n=12):
    m = next(x for x in get("/search/movie", query=title, year=year)["results"])
    im = get(f"/movie/{m['id']}/images", include_image_language="en,null")
    slug = f"{title.lower().replace(' ', '-')}-{year}"
    files = [dl(i["file_path"], f"{slug}-bd{k}.jpg") for k, i in enumerate(im["backdrops"][:n])]
    if m.get("poster_path"): files.append(dl(m["poster_path"], f"{slug}-poster.jpg", "w780"))
    vids = [f"https://youtu.be/{v['key']}" for v in get(f"/movie/{m['id']}/videos")["results"]
            if v["site"] == "YouTube" and v["type"] in ("Trailer", "Clip")][:3]
    return {"beat": beat, "title": m["title"], "tmdb_id": m["id"], "files": files, "videos": vids}

def credits(n=14):
    cast = get("/person/57250/combined_credits")["cast"]
    cast = [c for c in cast if c.get("backdrop_path")]
    cast.sort(key=lambda c: -c.get("popularity", 0))
    files = []
    for c in cast[:n]:
        t = (c.get("title") or c.get("name")).lower().replace(" ", "-").replace("/", "-")
        files.append(dl(c["backdrop_path"], f"credit-{t}-{c['id']}.jpg"))
    return {"beat": "ANY", "title": "Robin Shou other credits", "files": files, "videos": []}

man = {"people": [
    person("Robin Shou", "B02,B21", 4), person("Donnie Yen", "B12"), person("Yuen Woo-ping", "B12"),
    person("Simon Yam", "B12"), person("Cynthia Rothrock", "B12"),
    person("Paul W. S. Anderson", "B17"), person("Talisa Soto", "B20")],
  "movies": [movie("Mortal Kombat", 1995, "B01,B14,B15,B18,B19"),
    movie("Mortal Kombat Annihilation", 1997, "B20"), movie("Tiger Cage 2", 1990, "B12"),
    movie("Shaolin Temple", 1982, "B07"), credits()]}
json.dump(man, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
print(json.dumps({k: [(x.get("label") or x["title"], len(x["files"])) for x in v] for k, v in man.items()}))
