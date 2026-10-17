"""Copy TMDB stills into assets/<shot id>.jpg by section theme (stills only fill
shots that have no clip; a real clip assets/<id>.mp4 always wins)."""
import json, pathlib, shutil, itertools, glob
root=pathlib.Path(__file__).parent
cues=json.load(open(root/"cues.json"))["shots"]
S=lambda *p: sorted(sum((glob.glob(str(root/"stills"/f"{x}_*.jpg")) for x in p),[]))
MAP={"THE HOOK":S("t2"),"THE BOY":S("furlong")+S("t2"),"THE EXPLOSION":S("t2"),
 "THE NINETIES":S("pet2","amheart","home","brain"),"THE MID-ROLL CALLBACK":S("furlong"),
 "THE COMEBACK THAT WAS REAL":S("ahx","pecker","drc"),"THE FALL":S("furlong","brain"),
 "THE RECASTING":S("t3","t2"),"THE LONG QUIET":S("drc","brain","furlong"),"THE GHOST":S("fate"),
 "THE LENS":S("t2","furlong"),"TODAY":S("furlong"),"OPEN-LOOP CTA":S("molly"),"EPISODE TWO TRAILER":S("molly")}
cyc={k:itertools.cycle(v) for k,v in MAP.items() if v}
(root/"assets").mkdir(exist_ok=True)
for s in cues:
    if s["section"] in cyc and not list((root/"assets").glob(s["id"]+".*")):
        shutil.copy(next(cyc[s["section"]]), root/"assets"/f'{s["id"]}.jpg')
print(len(list((root/"assets").glob("*.jpg"))),"stills assigned")
