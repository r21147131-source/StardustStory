"""Build cues.json: timed shot list for Vanished Ep1 from the script + voiceover.

No STT model is reachable, so timing is estimated: words are spread
proportionally over the audio, then snapped to real pauses found by ffmpeg
silencedetect (section starts +-6s, shots +-2s).
"""
import json, re, subprocess, sys, pathlib
root = pathlib.Path(__file__).parent
script = (root / "../vanished-ep1-edward-furlong-script.md").read_text()
audio = sys.argv[1]
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",audio]))
out = subprocess.run(["ffmpeg","-hide_banner","-i",audio,"-af","silencedetect=noise=-35dB:d=0.6","-f","null","-"],capture_output=True,text=True).stderr
sil = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", out)]
def snap(t, r):
    c = [s for s in sil if abs(s-t) <= r]
    return min(c, key=lambda s: abs(s-t)) if c else t

secs = []
for blk in re.split(r"\n## \[", script)[1:]:
    head, *body = blk.split("\n", 1)
    title = head.split("] ",1)[1].strip()
    paras = [p.strip() for p in (body[0] if body else "").split("\n\n") if p.strip() and not p.startswith("---")]
    secs.append((title, paras))
words = lambda s: len(re.findall(r"\w+", s))
total = sum(words(p) for _, ps in secs for p in ps)
# slot guidance per section: (kind, what to cut in)
SLOT = {
 "THE HOOK": ("film", "Terminator 2 - John Connor / T-800 scenes"),
 "PREMISE STAMP": ("title", "Stardust Story / Vanished title card"),
 "THE BOY": ("photo", "Archival childhood photos of Furlong; Pasadena Boys' Club; T2 casting-era stills"),
 "THE EXPLOSION": ("film", "T2 hits (sewer/bike chase, 'No problemo'); Guns N' Roses 'You Could Be Mine' video"),
 "THE NINETIES": ("film", "Pet Sematary II, American Heart, A Home of Our Own, Brainscan"),
 "THE MID-ROLL CALLBACK": ("interview", "Interview clip - Furlong reflecting on early fame"),
 "THE COMEBACK THAT WAS REAL": ("film", "American History X, Pecker, Detroit Rock City"),
 "THE FALL": ("interview", "Interview clip - Furlong on addiction/recovery"),
 "THE RECASTING": ("film", "Terminator 3 (Nick Stahl) vs T2 John Connor; interview on the recasting"),
 "THE LONG QUIET": ("film", "Later indie / genre work; convention footage"),
 "THE GHOST": ("film", "Terminator: Dark Fate opening scene"),
 "THE LENS": ("interview", "Interview clip / T2 stills, slow push-ins"),
 "TODAY": ("interview", "Recent interview or convention footage; sobriety statement"),
 "OPEN-LOOP CTA": ("film", "Molly Ringwald - Sixteen Candles / Breakfast Club"),
 "EPISODE TWO TRAILER": ("film", "Molly Ringwald trailer montage"),
}
# names get a lower-third ONLY at first mention in the whole video
LABELS = [("Edward Furlong","Edward Furlong","actor"),("Terminator 2","Terminator 2: Judgment Day","1991"),
 ("Schwarzenegger","Arnold Schwarzenegger","actor"),("Mali Finn","Mali Finn","casting director"),
 ("James Cameron","James Cameron","director"),("Jeff Bridges","Jeff Bridges","actor"),
 ("American History X","American History X","1998"),("Edward Norton","Edward Norton","actor"),
 ("John Waters","John Waters","director"),("Nick Stahl","Nick Stahl","actor"),
 ("Dark Fate","Terminator: Dark Fate","2019"),("Molly Ringwald","Molly Ringwald","actress")]
seen=set()
# section starts
pos=0; starts=[]
for title,ps in secs:
    starts.append(pos/total*dur); pos+=sum(words(p) for p in ps)
starts=[0.0]+[snap(s,6) for s in starts[1:]]
shots=[]
for i,(title,ps) in enumerate(secs):
    end = starts[i+1] if i+1<len(secs) else dur
    ws=[words(p) for p in ps]; acc=0; group=[]; groups=[]
    for p,w in zip(ps,ws):
        group.append(p); acc+=w
        if acc/total*dur>=12: groups.append(group); group=[]; acc=0
    if group: groups.append(group) if not groups or acc/total*dur>=5 else groups[-1].extend(group)
    gw=[sum(words(p) for p in g) for g in groups]; sw=sum(gw); t=starts[i]
    for k,(g,w) in enumerate(zip(groups,gw)):
        s=t; t=t+(end-starts[i])*w/sw
        e = end if k==len(groups)-1 else snap(t,2)
        t=e
        text=" ".join(g); labels=[]
        for key,name,sub in LABELS:
            if key in text and name not in seen: seen.add(name); labels.append([name,sub])
        shots.append({"id":f"s{len(shots)+1:02d}","start":round(s,2),"end":round(e,2),"section":title,
                      "kind":SLOT[title][0],"slot":SLOT[title][1],"labels":labels,"narration":text[:160]})
json.dump({"audio":audio,"duration":dur,"shots":shots},open(root/"cues.json","w"),indent=1)
print(len(shots),"shots",round(dur,1),"s")
