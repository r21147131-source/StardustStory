import json,re,os,glob,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
exec(open('labels.py').read())
UP='/root/.claude/uploads/bb9227b2-89ef-5c72-9c06-294656c4452f/'
IM='/tmp/claude-0/-home-user-StardustStory/bb9227b2-89ef-5c72-9c06-294656c4452f/images/'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
beats=json.load(open('beats.json')); st=json.load(open('align1.json'))['starts']; T=978.94
def clip(p): return glob.glob(UP+p+'*.mp4')[0]
C={ 'B002':['848f60e9'],'B003':['20818596'],'B007':['1d80fd69'],'B008':['033e1e08','ee4187ff'],'B009':['02f5f487','dea0266a'],'B010':['1fd0e419','22226bb5'],
'B011':['f107830c'],'B013':['394f7a3e'],'B014':['2626ec40'],'B015':['703503c4'],'B016':['b57c40fb'],'B018':['2314ec25'],'B020':['2f1f5572'],'B022':['ee12f2f2'],
'B024':['64daeaf9','629ce699'],'B027':['92d7c75e'],'B030':['b27f9596','8ba600c7'],'B031':['513bce4a'],'B032':['f7a326d7'],'B033':['21a49588'],'B035':['8509659c'],
'B039':['1ac9679b','89a9291b'],'B044':['29623832'],'B045':['53dacc56'],'B046':['1734f763'],'B047':['7a62cb10'],'B049':['80e1bb7c'],'B053':['ce5ec9e6'],
'B054':['6af72099','6b05aa9c'],'B056':['41055c4a','f8213684'],'B058':['c4241d73'],'B060':['502bfbee','dce7a1d5'],'B061':['f5dcd148','88d70f64'],'B063':['0c8f64f2','f3a18beb'],
'B065':['ef527525'],'B068':['14ab7de0'],'B069':['15e8f342'],'B073':['0e0cad7c'],'B074':['81683553','49b038c1'],'B078':['b4d344e6'],'B083':['f9cf3a67'],'B086':['68c255e4'],
'B088':['0ab8a6bb'],'B090':['f141272d'],'B091':['03a437e9'],'B095':['b635c99b'],'B098':['b2e70489','fa9aba4f'],'B100':['58cc8455'],'B105':['3e686545'],'B106':['d864a069'],
'B112':['a8b71931'],'B115':['2fc5cc24'],'B125':['8a3c573a'],'B126':['dbc96488'],'B128':['daff6dad'],'B134':['737196f3'],'B142':['5cffc54c'],'B143':['19d30d8f','298b474c'],
'B146':['0e857a09'],'B148':['6e6b7cbb'],'B149':['93fc0b7f'],'B150':['7ac4d64d'],'B151':['32299334']}
C.update({'B019':['f7a326d7'],'B057':['c4241d73'],'B097':['fa9aba4f'],'B099':['03a437e9'],'B103':['f7a326d7'],'B124':['737196f3'],'B123':['2fc5cc24']})
TXT={'B071','B108','B109','B110','B111','B132','B133','B144','B121'}
I={'B048':['12.jpg'],'B092':['32.jpg'],'B102':['45.jpg'],'B117':['44.jpg'],'B122':['31.jpg'],'B135':['35.jpg'],'B137':['35.jpg'],'B037':['5.jpg'],'B038':['5.jpg'],'B114':['46.jpg'],'B023':['2.jpg'],'B026':['1.webp'],'B028':['3.jpg'],'B029':['4.jpg'],'B036':['5.jpg'],'B041':['6.webp'],'B042':['8.jpg'],'B043':['9.jpg'],'B051':['17.jpg'],
'B052':['11.jpg','12.jpg'],'B059':['16.webp'],'B062':['36.jpg'],'B064':['33.jpg'],'B066':['19.jpg'],'B067':['38.jpg'],'B070':['18.jpg'],'B072':['21.jpg'],'B075':['23.jpg'],
'B076':['24.jpg'],'B077':['25.jpg'],'B079':['41.webp'],'B080':['27.webp'],'B081':['29.jpg'],'B084':['30.webp'],'B087':['39.jpg'],'B089':['40.jpg'],'B093':['32.jpg'],
'B096':['43.jpg'],'B101':['44.jpg'],'B104':['46.jpg'],'B113':['47.jpg'],'B116':['48.webp'],'B119':['31.jpg'],'B127':['34.jpg'],'B136':['35.jpg']}
CROP={'46.jpg':'crop=iw/2:ih:0:0','B114:46.jpg':'crop=iw/2:ih:iw/2:0','B037:5.jpg':'crop=iw:ih*0.28:0:ih*0.38','B038:5.jpg':'crop=iw:ih*0.28:0:ih*0.62','B137:35.jpg':'crop=iw*0.55:ih*0.55:iw*0.25:ih*0.4'}
MG=set(json.load(open('mgjobs.json'))[i][0] for i in range(len(json.load(open('mgjobs.json')))))
def esc(t): return t
def tfile(name,text):
    p=f'txt/{name}.txt'; open(p,'w').write(text); return p
def run(cmd):
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode: print('FAIL',' '.join(cmd[:12]),r.stderr[-400:],flush=True)
    return r.returncode
def overlay(bid,kind):
    f=[]
    if bid in L:
        lt,dt=L[bid]
        if lt:
            f.append(f"drawtext=fontfile={FONT}:textfile={tfile(bid+'lt',lt)}:fontcolor=0xC9A84C:fontsize=30:x=60:y=h-110:box=1:boxcolor=black@0.6:boxborderw=14:enable='between(t,0.6,4.2)'")
        if dt:
            f.append(f"drawtext=fontfile={FONT}:textfile={tfile(bid+'dt',dt)}:fontcolor=0xF0E8D0:fontsize=30:x=w-text_w-60:y=50:enable='between(t,0.6,3.6)'")
    return f
VEO_G="colorbalance=rs=.04:bs=-.05:rm=.05:gm=.01:bm=-.06,eq=saturation=0.92:contrast=1.05,noise=alls=7:allf=t,vignette=PI/5"
ARCH_G="eq=saturation=0.6,colorchannelmixer=.393:.769:.189:0:.349:.686:.168:0:.272:.534:.131:0,curves=all='0/0.04 0.85/0.80 1/0.88',colorbalance=rm=.04:bm=-.05,eq=contrast=1.06:saturation=1.1,noise=alls=9:allf=t,vignette=PI/4.5"
jobs=[];plan=[]
for i,b in enumerate(beats):
    bid=b['id']; s=st[i]; e=st[i+1] if i+1<len(st) else T; d=e-s
    base=bid; key=re.sub(r'(?<=\d)[ab]$','',bid)
    srcs=None
    if key in C: srcs=[('clip',x) for x in C[key]]
    elif key in I: srcs=[('img',x) for x in I[key]]
    # beats a/b: the brief lists B008..as one beat with two prompts, same beat id
    if bid in TXT:
        out=f'segf/{bid}_0.mp4'; jobs.append(['cp',f'txtseg/{bid}.mp4',out]); plan.append(out); continue
    if bid in MG:
        out=f'segf/{bid}_0.mp4'; jobs.append(['cp',f'mgseg/{bid}.mp4',out]); plan.append(out); continue
    n=len(srcs) if srcs else 1
    for k in range(n):
        dd=d/n
        if bid=='B074' and srcs and k==0: dd=3.0
        if bid=='B074' and srcs and k==1: dd=d-3.0
        out=f'segf/{bid}_{k}.mp4'
        ov=overlay(bid,None)
        vf=['scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x0A0908','setsar=1','fps=25']
        if srcs and srcs[k][0]=='clip':
            cmd=['ffmpeg','-v','error','-y','-i',clip(srcs[k][1]),'-an','-vf',','.join(vf+[f'tpad=stop_mode=clone:stop_duration={max(dd,0):.2f}',VEO_G]+ov),'-t',f'{dd:.3f}']
        elif srcs:
            frames=int(dd*25)+1
            vfi=(CROP.get(bid+':'+srcs[k][1],CROP.get(srcs[k][1],'null'))+',')+f"scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=0x0A0908,setsar=1,scale=2560:1440,zoompan=z='1+0.0004*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1280x720:fps=25"
            cmd=['ffmpeg','-v','error','-y','-loop','1','-i',IM+srcs[k][1],'-an','-vf',','.join([vfi,ARCH_G,f'fade=t=in:st=0:d=0.5,fade=t=out:st={max(dd-0.5,0):.2f}:d=0.5']+ov),'-t',f'{dd:.3f}']
        else:
            kind=b['kind']; lab=L.get(bid,('',''))[0] or b['narr'][:60]
            txt=f"{bid}  {kind}\n\n{lab}\n\n(no footage yet)"
            tf=tfile(bid+'ph',txt)
            cmd=['ffmpeg','-v','error','-y','-f','lavfi','-i',f'color=c=0x0A0908:s=1280x720:r=25:d={dd:.3f}','-an','-vf',f"drawtext=fontfile={FONT}:textfile={tf}:fontcolor=0x8A8070:fontsize=34:x=(w-text_w)/2:y=(h-text_h)/2:line_spacing=10"]
        cmd+=['-c:v','libx264','-preset','veryfast','-crf','28','-pix_fmt','yuv420p',out]
        jobs.append(cmd); plan.append(out)
print(len(jobs),'segments')
with ThreadPoolExecutor(4) as ex: rc=list(ex.map(lambda c:(subprocess.run(c).returncode if c[0]=='cp' else run(c)),jobs))
print('failed',sum(1 for r in rc if r))
open('concat_f.txt','w').write(''.join(f"file '{os.path.abspath(p)}'\n" for p in plan))
