#!/usr/bin/env python3
"""Fetch real portraits / posters / backdrops from TMDB into footage/tmdb/<key>/ and write footage/tmdb/manifest.json."""
import os, json, sys, urllib.request, urllib.parse, concurrent.futures as cf
KEY = os.environ["TMDB_API_KEY"]
OUT = "footage/tmdb"
API = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/"

def get(path, **p):
    p["api_key"] = KEY
    with urllib.request.urlopen(f"{API}{path}?{urllib.parse.urlencode(p)}", timeout=30) as r:
        return json.load(r)

def search(kind, q, year=None, pick=None):
    p = {"query": q}
    if year: p["first_air_date_year" if kind == "tv" else "year"] = year
    res = get(f"/search/{kind}", **p)["results"]
    if not res: return None
    if pick:
        for r in res:
            if r.get("id") == pick: return r
    return res[0]

PEOPLE = {
 "woll": "Deborah Ann Woll", "donofrio": "Vincent D'Onofrio", "bethel": "Wilson Bethel", "bernthal": "Jon Bernthal",
 "ritter": "Krysten Ritter", "cox": "Charlie Cox", "paquin": "Anna Paquin", "henson": "Elden Henson",
 "scardapane": "Dario Scardapane", "mercer": "Matthew Mercer", "ej_scott": "E.J. Scott",
}
TITLES = {  # key: (kind, query, year)
 "born_again": ("tv", "Daredevil: Born Again", 2025), "daredevil": ("tv", "Daredevil", 2015), "punisher": ("tv", "The Punisher", 2017),
 "defenders": ("tv", "Marvel's The Defenders", 2017), "trueblood": ("tv", "True Blood", 2008), "escape1": ("movie", "Escape Room", 2019),
 "escape2": ("movie", "Escape Room: Tournament of Champions", 2021), "queen": ("movie", "Queen of the Ring", 2024),
 "life": ("tv", "Life", 2007), "er": ("tv", "ER", 1994), "csi": ("tv", "CSI: Crime Scene Investigation", 2000),
 "earl": ("tv", "My Name Is Earl", 2005), "mentalist": ("tv", "The Mentalist", 2008), "voxmachina": ("tv", "The Legend of Vox Machina", 2022),
 "critrole": ("tv", "Critical Role", None),
}
os.makedirs(OUT, exist_ok=True)
manifest = {}
jobs = []
def dl(url, dest):
    if os.path.exists(dest): return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    try:
        urllib.request.urlretrieve(url, dest)
    except Exception as e:
        print("FAIL", url, e, file=sys.stderr)

for k, name in PEOPLE.items():
    r = search("person", name)
    if not r: print("no person", name); continue
    imgs = get(f"/person/{r['id']}/images")["profiles"][:6]
    files = []
    for i, im in enumerate(imgs):
        d = f"{OUT}/{k}/p{i}.jpg"; jobs.append((IMG + "original" + im["file_path"], d)); files.append(d)
    manifest[k] = {"type": "person", "name": r["name"], "id": r["id"], "files": files}
for k, (kind, q, y) in TITLES.items():
    r = search(kind, q, y)
    if not r: print("no title", q); continue
    imgs = get(f"/{kind}/{r['id']}/images", include_image_language="en,null")
    bd = [b for b in imgs["backdrops"] if b.get("iso_639_1") in (None, "xx")][:8] or imgs["backdrops"][:8]
    ps = imgs["posters"][:2]
    files_b, files_p = [], []
    for i, im in enumerate(bd):
        d = f"{OUT}/{k}/b{i}.jpg"; jobs.append((IMG + "original" + im["file_path"], d)); files_b.append(d)
    for i, im in enumerate(ps):
        d = f"{OUT}/{k}/post{i}.jpg"; jobs.append((IMG + "w780" + im["file_path"], d)); files_p.append(d)
    manifest[k] = {"type": kind, "title": r.get("name") or r.get("title"), "id": r["id"], "backdrops": files_b, "posters": files_p}
with cf.ThreadPoolExecutor(8) as ex: list(ex.map(lambda j: dl(*j), jobs))
json.dump(manifest, open(f"{OUT}/manifest.json", "w"), indent=1)
for k, v in manifest.items():
    print(k, v.get("name") or v.get("title"), len(v["files"]) if "files" in v else (len(v["backdrops"]), len(v["posters"])))
