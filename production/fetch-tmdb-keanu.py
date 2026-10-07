#!/usr/bin/env python3
"""Keanu Reeves episode: portraits + film stills from TMDB, plus official trailer YouTube ids -> footage/tmdb_keanu/manifest.json"""
import os, json, sys, urllib.request, urllib.parse, concurrent.futures as cf
KEY = os.environ["TMDB_API_KEY"]; OUT = "footage/tmdb_keanu"; API = "https://api.themoviedb.org/3"; IMG = "https://image.tmdb.org/t/p/"
def get(path, **p):
    p["api_key"] = KEY
    with urllib.request.urlopen(f"{API}{path}?{urllib.parse.urlencode(p)}", timeout=30) as r: return json.load(r)
def dl(url, dest):
    if os.path.exists(dest): return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try: urllib.request.urlretrieve(url, dest)
    except Exception as e: print("FAIL", url, e, file=sys.stderr)
FILMS = {"matrix": ("The Matrix", 1999), "reloaded": ("The Matrix Reloaded", 2003), "wick": ("John Wick", 2014), "speed": ("Speed", 1994),
         "pointbreak": ("Point Break", 1991), "billted": ("Bill & Ted's Excellent Adventure", 1989), "wick4": ("John Wick: Chapter 4", 2023)}
man, jobs = {}, []
r = get("/search/person", query="Keanu Reeves")["results"][0]
prof = get(f"/person/{r['id']}/images")["profiles"][:10]
man["keanu"] = {"type": "person", "name": r["name"], "id": r["id"], "files": []}
for i, im in enumerate(prof):
    d = f"{OUT}/keanu/p{i}.jpg"; jobs.append((IMG + "original" + im["file_path"], d)); man["keanu"]["files"].append(d)
for k, (q, y) in FILMS.items():
    res = get("/search/movie", query=q, year=y)["results"]
    if not res: print("no film", q); continue
    m = res[0]; imgs = get(f"/movie/{m['id']}/images", include_image_language="en,null")
    bd = [b for b in imgs["backdrops"] if b.get("iso_639_1") in (None, "xx")][:8] or imgs["backdrops"][:8]
    vids = [v for v in get(f"/movie/{m['id']}/videos")["results"] if v["site"] == "YouTube" and v["type"] in ("Trailer", "Teaser")]
    vids.sort(key=lambda v: (v["type"] != "Trailer", not v.get("official", False)))
    e = {"type": "movie", "title": m["title"], "year": y, "id": m["id"], "backdrops": [], "posters": [], "trailers": [(v["key"], v["name"]) for v in vids[:4]]}
    for i, im in enumerate(bd): d = f"{OUT}/{k}/b{i}.jpg"; jobs.append((IMG + "original" + im["file_path"], d)); e["backdrops"].append(d)
    for i, im in enumerate(imgs["posters"][:2]): d = f"{OUT}/{k}/post{i}.jpg"; jobs.append((IMG + "w780" + im["file_path"], d)); e["posters"].append(d)
    man[k] = e
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(lambda j: dl(*j), jobs))
json.dump(man, open(f"{OUT}/manifest.json", "w"), indent=1)
for k, v in man.items(): print(k, v.get("name") or v.get("title"), len(v.get("files", [])) or (len(v["backdrops"]), len(v["posters"])), v.get("trailers", ""))
