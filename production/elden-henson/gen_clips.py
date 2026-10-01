"""Write clips.json for build_eh.py from hand-picked trailer moments.

Usage: python gen_clips.py CLIPDIR PICKS.txt OUT.json
PICKS.txt lines: "key: t1 t2 ..." (start seconds of usable shots in CLIPDIR/key.*,
chosen from contact sheets). Each cue below names the footage it draws from; picks are
consumed in order per film and wrap around, so shots repeat only when a film is used a lot.
"""
import glob, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
clipdir, picks_f, out = sys.argv[1:4]
sents = json.load(open(os.path.join(HERE, "sent_times.json")))
picks = {}
for line in open(picks_f):
    if ":" in line:
        k, v = line.split(":", 1)
        picks[k.strip()] = [float(x) for x in v.split()]
files = {}
for k in picks:
    for ext in (".mp4", ".mkv", ".webm"):
        if os.path.exists(os.path.join(clipdir, k + ext)):
            files[k] = os.path.join(clipdir, k + ext)
            break
SHOT = 3.5
# cue prefix -> (films to draw from in rotation, seconds of the cue's own still to show first)
PLAN = {
 "The show had been gone": (["daredevil", "daredevil3", "daredevil2"], 0), "When Netflix cancelled": (["daredevil", "daredevil3", "daredevil2"], 0),
 "And the characters inside": (["daredevil", "daredevil3", "daredevil2"], 0),
 "Then Disney Plus answered": (["born_again"], 0), "Daredevil: Born Again launched": (["born_again"], 0),
 "And Elden Henson stepped back": (["born_again"], 3.5),
 "The wait was over": (["born_again"], 0), "Foggy Nelson did not survive": (["born_again"], 0),
 "Before the first hour": (["born_again"], 2.5),
 "Henson watched the character": (["daredevil", "defenders"], 0),
 "He showed up at fan conventions": (["int_henson1"], 0),
 "And the moment the industry": (["born_again"], 0), "This is how that pattern": (["mighty_ducks"], 0),
 "He had a role in Turner": (["turner_hooch"], 0), "None of these were the break": (["turner_hooch"], 0),
 "In 1992, when he was fourteen": (["mighty_ducks"], 0), "Disney was making": (["mighty_ducks"], 0),
 "The Mighty Ducks needed": (["mighty_ducks"], 0), "Fulton Reed was that": (["mighty_ducks"], 0),
 "The Mighty Ducks was a hit": (["mighty_ducks"], 0), "A sequel, D2": (["d2"], 0), "D3 came in 1996": (["d3"], 0),
 "Henson appeared in all three": (["d2", "d3", "mighty_ducks"], 0), "He had been a franchise player": (["d3", "d2"], 0),
 "After the Mighty Ducks trilogy": (["d3"], 0), "He worked consistently": (["d2"], 0),
 "In 1998 he appeared in The Mighty": (["the_mighty"], 0), "Then She's All That": (["shes_all_that"], 0),
 "Idle Hands": (["idle_hands"], 0), "The Battle of Shaker": (["shaker_heights"], 0),
 "The Butterfly Effect": (["butterfly_effect"], 0), "Lords of Dogtown": (["lords_of_dogtown"], 0),
 "Henson was aware": (["int_henson1"], 0), "He said in interviews": (["int_henson1"], 0),
 "The industry had a clear category": (["shes_all_that", "butterfly_effect", "idle_hands"], 0),
 "For fifteen years": (["lords_of_dogtown", "the_mighty"], 0),
 "In 2014, a second franchise": (["mockingjay1"], 0), "The Hunger Games had become": (["mockingjay1"], 0),
 "It was a supporting role": (["mockingjay1"], 0), "Henson appeared in Mockingjay": (["mockingjay2"], 0),
 "His face was on the screen": (["mockingjay2"], 0), "He took the job": (["mockingjay1", "mockingjay2"], 0),
 "In 2015, Netflix launched": (["daredevil", "daredevil3", "daredevil2"], 0), "Franklin Foggy Nelson": (["daredevil", "daredevil3", "daredevil2"], 0),
 "He was also funny": (["daredevil", "daredevil3", "daredevil2"], 0), "He built it": (["daredevil", "daredevil3", "daredevil2"], 0),
 "He reprised the role": (["defenders"], 0), "He became, quietly": (["defenders", "daredevil"], 0),
 "For three years": (["daredevil", "daredevil3", "daredevil2"], 0), "On November 29, 2018": (["daredevil", "daredevil3", "daredevil2"], 0),
 "The show, along with": (["defenders"], 0), "For years, nobody knew": (["daredevil", "daredevil3", "daredevil2"], 0),
 "Then in 2023, Martin Scorsese": (["killers"], 3.0), "The film was one of": (["killers"], 0),
 "Henson played Duke Burkhart": (["killers"], 0), "In a film three and a half": (["killers"], 0),
 "The gap between": (["killers"], 0), "Then came the reversal": (["born_again"], 0),
 "When the dust settled": (["born_again"], 0), "Set photos": (["born_again"], 0),
 "Daredevil: Born Again premiered": (["born_again"], 0), "Within that hour": (["born_again"], 2.5),
 "The showrunner": (["born_again"], 0), "Foggy Nelson had been cancelled twice": (["daredevil", "born_again"], 0),
 "Then Marvel TV boss": (["born_again"], 0), "The character died": (["born_again", "daredevil"], 0),
 "Season two of Born Again": (["born_again"], 0), "He was joking": (["int_henson1"], 0),
 "The man has spent": (["mighty_ducks", "d2", "mockingjay1", "daredevil", "killers", "born_again"], 0),
}
starts = {}
for s in sents:
    t = s["text"].replace("’", "'")
    for pre in PLAN:
        if t.startswith(pre) and pre not in starts:
            starts[pre] = s["t"]
# cue end = next cue start in build_eh.py's cue list
sys.path.insert(0, HERE)
src = open(os.path.join(HERE, "build_eh.py")).read()
cue_prefixes = [line.split('"')[1] for line in src.split("CUES = [")[1].split("\n]")[0].splitlines() if line.strip().startswith('("')]
cstart = {}
for pre in cue_prefixes:
    cstart[pre] = next(s["t"] for s in sents if s["text"].replace("’", "'").startswith(pre))
order = sorted(cstart, key=cstart.get)
T = 845.904
ptr = {k: 0 for k in picks}
res = {}
for pre, (films, still) in PLAN.items():
    films = [f for f in films if f in files]
    if not films:
        continue
    i = order.index(pre)
    span = (cstart[order[i + 1]] if i + 1 < len(order) else T) - cstart[pre]
    lst = [["STILL", 0, still]] if still else []
    n = max(1, math.ceil((span - still) / SHOT))
    for j in range(n):
        f = films[j % len(films)]
        st = picks[f][ptr[f] % len(picks[f])]; ptr[f] += 1
        lst.append([files[f], st, SHOT])
    res[pre] = lst
json.dump(res, open(out, "w"), indent=1)
print(f"{len(res)} cues use footage from {len({f for v in res.values() for f, *_ in v if f != 'STILL'})} files")
