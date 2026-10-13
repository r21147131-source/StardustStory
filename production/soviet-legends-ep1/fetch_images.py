import json, re, sys, time, urllib.parse, urllib.request
UA = "StardustStoryBot/1.0 (r21147131@gmail.com)"
API = "https://commons.wikimedia.org/w/api.php"
ACTORS = {
 "tikhonov": ["Vyacheslav Tikhonov", "Tikhonov actor Stirlitz"],
 "nikulin": ["Yuri Nikulin"],
 "leonov": ["Evgeny Leonov"],
 "smoktunovsky": ["Innokenty Smoktunovsky"],
 "samoylova": ["Tatyana Samoylova actress"],
 "mironov": ["Andrei Mironov actor"],
 "vysotsky": ["Vladimir Vysotsky"],
 "cranes": ["The Cranes Are Flying Kalatozov"],
}
def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for i in range(5):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30))
        except Exception as e:
            time.sleep(6*(i+1))
    raise SystemExit("fail "+url)
out = {}
for key, queries in ACTORS.items():
    cands = []
    for q in queries:
        r = get({"action":"query","generator":"search","gsrsearch":q,"gsrnamespace":6,"gsrlimit":15,
                 "prop":"imageinfo","iiprop":"url|size|mime|extmetadata","iiurlwidth":1280,"format":"json"})
        for p in r.get("query",{}).get("pages",{}).values():
            ii = p["imageinfo"][0]
            if ii["mime"] != "image/jpeg": continue
            m = ii.get("extmetadata",{})
            lic = m.get("LicenseShortName",{}).get("value","")
            if not re.match(r"(CC|Public domain|PD)", lic, re.I): continue
            cands.append({"title":p["title"],"thumb":ii["thumburl"],"w":ii["width"],"h":ii["height"],
                          "license":lic,"artist":re.sub("<[^>]+>","",m.get("Artist",{}).get("value","")),
                          "page":ii["descriptionurl"],"desc":re.sub("<[^>]+>","",m.get("ImageDescription",{}).get("value",""))[:160]})
    time.sleep(3); out[key] = cands
    print(key, len(cands))
json.dump(out, open("candidates.json","w"), ensure_ascii=False, indent=1)
