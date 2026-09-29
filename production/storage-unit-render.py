import json, subprocess, os, sys
from concurrent.futures import ThreadPoolExecutor
S=sys.argv[1]; FPS=30
segs=json.load(open('production/storage-unit-segments.json'))
shots=[o for s in segs for o in s['scenes']]
# frame-exact durations from cumulative start times so the cut grid never drifts
TOTAL=645.58
starts=[o['start'] for o in shots]+[TOTAL]
os.makedirs(f'{S}/parts',exist_ok=True)
def job(i):
    o=shots[i]
    n=round(starts[i+1]*FPS)-round(starts[i]*FPS)
    src=f"{S}/clips/{o['src'].rsplit('/',1)[1]}"
    out=f'{S}/parts/{i:03d}.mp4'
    vf=("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1,"
        f"fps={FPS},tpad=stop_mode=clone:stop=-1,"
        "eq=saturation=0.8:contrast=1.05,vignette=PI/5")
    cmd=['ffmpeg','-loglevel','error','-y','-ss',str(o['trim']),'-i',src,'-an','-vf',vf,
         '-frames:v',str(n),'-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',out]
    subprocess.run(cmd,check=True); return n
with ThreadPoolExecutor(4) as ex: frames=list(ex.map(job,range(len(shots))))
print('frames',sum(frames),'=',sum(frames)/FPS,'s')
open(f'{S}/parts/list.txt','w').write(''.join(f"file '{i:03d}.mp4'\n" for i in range(len(shots))))
