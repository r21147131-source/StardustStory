import subprocess,os
F="/root/.claude/uploads/7718add0-037e-5b8f-a338-cc685b021f90/5041308d-Trailer_____Tiger_Cage_II_-_HD_Version_8Q_R8lQfWjs.mp4"
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SLOT=334/25
slots={
 8:[48.3817,54.8882,74.441],
 9:[25.025,30.8642,97.5975],
 10:[119.953,126.159,140.307],
 11:[148.015,152.819,159.159],
 12:[41.0,111.0,166.266,176.843],
 13:[190.891,202.536,214.214],
}
caps={8:"Hong Kong · late 1980s",9:"Stunt work",12:"Tiger Cage II (1990)"}
for i,starts in slots.items():
    d=SLOT/len(starts)
    inputs=[];fc=[]
    for k,s in enumerate(starts):
        inputs+=["-ss",f"{s}","-t",f"{d+0.05:.3f}","-i",F]
        fc.append(f"[{k}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=25,setsar=1,trim=duration={d:.3f},setpts=PTS-STARTPTS[v{k}]")
    fc.append("".join(f"[v{k}]" for k in range(len(starts)))+f"concat=n={len(starts)}:v=1:a=0,fade=t=in:st=0:d=0.4,fade=t=out:st={SLOT-0.4:.2f}:d=0.4[o]")
    out=f"clips/{i:02d}.mp4"; lab="[o]"
    if i in caps:
        t=caps[i].replace(":","\\:")
        fc[-1]=fc[-1].replace("[o]","[p]")+f";[p]drawtext=fontfile={FONT}:text='{t}':fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=18:x=(w-text_w)/2:y=h*0.82:enable='between(t,0.8,6.8)'[o]"
    subprocess.run(["ffmpeg","-y","-loglevel","error",*inputs,"-filter_complex",";".join(fc),"-map","[o]","-frames:v","334","-r","25","-pix_fmt","yuv420p","-c:v","libx264","-preset","veryfast","-crf","20",out],check=True)
    print("slot",i,"ok",flush=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i","list.txt","-i","/root/.claude/uploads/7718add0-037e-5b8f-a338-cc685b021f90/251e3e10-Video_Project_62.m4a","-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-t","373.61","robin-shou-v2.mp4"],check=True)
print("FINAL DONE")
