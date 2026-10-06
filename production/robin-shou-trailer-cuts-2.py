import subprocess,glob
U="/root/.claude/uploads/7718add0-037e-5b8f-a338-cc685b021f90/"
SRC={"A":glob.glob(U+"31f8f961-*.mp4")[0],"R":glob.glob(U+"951def60-*.mp4")[0],"C":glob.glob(U+"1f9e7921-*.mp4")[0],"T":glob.glob(U+"5041308d-*.mp4")[0]}
SC={"A":"../tr/scenes_a1P1j6MP920.txt","R":"../tr/scenes_dimVCTUBJEA.txt","C":"../tr/scenes_gscqagF0_SE.txt","T":"../tc/scenes.txt"}
scenes={k:[float(x) for x in open(v).read().split()] for k,v in SC.items()}
def snap(k,t):
    c=[s for s in scenes[k] if abs(s-t)<=2.0]
    return min(c,key=lambda s:abs(s-t)) if c else t
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SLOT=334/25
def build(i,cuts,cap=None,exact=()):
    d=SLOT/len(cuts); inputs=[];fc=[]
    for n,(k,t) in enumerate(cuts):
        s=t if (k,t) in exact else snap(k,t)
        inputs+=["-ss",f"{s:.3f}","-t",f"{d+0.1:.3f}","-i",SRC[k]]
        fc.append(f"[{n}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=25,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{n}]")
    chain="".join(f"[v{n}]" for n in range(len(cuts)))+f"concat=n={len(cuts)}:v=1:a=0,fade=t=in:st=0:d=0.4,fade=t=out:st={SLOT-0.4:.2f}:d=0.4"
    if cap:
        t=cap.replace(":","\\:")
        chain+=f",drawtext=fontfile={FONT}:text='{t}':fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.82:enable='between(t,0.8,6.8)'"
    fc.append(chain+"[o]")
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(fc),"-map","[o]","-frames:v","334","-r","25","-pix_fmt","yuv420p","-c:v","libx264","-preset","veryfast","-crf","20",f"clips/{i:02d}.mp4"],check=True)
    print("slot",i,flush=True)
slots={
 0:([("A",0),("A",15),("A",20)],None),
 1:([("A",35),("A",40),("A",50)],None),
 2:([("A",60),("A",65),("A",70)],None),
 13:([("T",190.891),("T",202.536),("T",214.214)],"1994 · Back in Los Angeles"),
 15:([("A",95),("A",100),("A",5)],"Mortal Kombat (1995)"),
 16:([("A",75),("A",80),("C",93)],None),
 17:([("A",50),("A",55),("A",45)],None),
 18:([("A",10),("A",25),("A",30)],None),
 19:([("A",15),("A",65),("C",20)],None),
 20:([("A",40),("C",65),("A",70)],None),
 21:([("C",15),("A",60),("C",70)],None),
 22:([("A",65),("A",70),("A",85)],None),
 23:([("A",85),("A",90),("A",35)],"August 18, 1995"),
 24:([("R",40),("R",45),("R",50)],"Mortal Kombat: Annihilation (1997)"),
 25:([("R",55),("R",60),("R",65)],None),
 26:([("R",70),("R",35),("R",10)],None),
}
for i,(c,cap) in slots.items(): build(i,c,cap,exact=tuple(x for x in c if x[0]=="T"))
open("list.txt","w").write("".join(f"file 'clips/{i:02d}.mp4'\n" for i in range(28)))
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","list.txt","-i",U+"251e3e10-Video_Project_62.m4a","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-t","373.61","robin-shou-v3.mp4"],check=True)
print("FINAL DONE")
