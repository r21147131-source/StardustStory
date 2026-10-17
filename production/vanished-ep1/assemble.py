"""Assemble the video from cues.json.

For each shot, uses assets/<id>.{mp4,mov,mkv,webm,jpg,jpeg,png} if present
(trimmed/looped to the shot length, scaled to 1280x720, with a slow push-in on
stills); otherwise renders a labeled placeholder card. Name lower-thirds are
drawn once, at each person/title's first mention. Voiceover is the audio track.
Usage: python3 assemble.py [out.mp4]
"""
import json, pathlib, subprocess, sys, textwrap
root = pathlib.Path(__file__).parent
cues = json.load(open(root/"cues.json"))
audio = (root/".."/".."/"public"/"vanished-ep1-voiceover.mp3").resolve()
out = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else root/"vanished-ep1-draft.mp4")
tmp = root/"build"; tmp.mkdir(exist_ok=True)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
W,H,FPS=1280,720,24
COL={"film":"0x3a1f1f","interview":"0x1f2e3a","photo":"0x2e2a1f","title":"0x15151f"}
def esc(s): return s.replace("\\","\\\\").replace(":","\\:").replace("'","\u2019").replace("%","\\%")
def find(i):
    for ext in ("mp4","mov","mkv","webm","jpg","jpeg","png"):
        p=root/"assets"/f"{i}.{ext}"
        if p.exists(): return p
parts=[]
for s in cues["shots"]:
    d=s["end"]-s["start"]; a=find(s["id"]); seg=tmp/f'{s["id"]}.mp4'
    vf_tail=[]
    for n,(name,sub) in enumerate(s["labels"]):
        y=H-150-n*0 ; # stacked labels get staggered in time instead
        t0=0.6+n*3.2
        vf_tail.append(f"drawbox=x=60:y={H-130}:w=560:h=84:color=black@0.6:t=fill:enable='between(t,{t0},{t0+3})'")
        vf_tail.append(f"drawtext=fontfile={FONT}:text='{esc(name)}':fontsize=34:fontcolor=white:x=80:y={H-122}:enable='between(t,{t0},{t0+3})'")
        vf_tail.append(f"drawtext=fontfile={FONT}:text='{esc(sub)}':fontsize=22:fontcolor=0xdddddd:x=80:y={H-78}:enable='between(t,{t0},{t0+3})'")
    fade=f"fade=t=in:d=0.3,fade=t=out:st={max(d-0.3,0):.2f}:d=0.3"
    if a is None:
        title=f'{s["id"]}  [{s["kind"].upper()}]'
        lines=textwrap.wrap(s["slot"],48)[:3]
        vf=[f"drawtext=fontfile={FONT}:text='{esc(title)}':fontsize=44:fontcolor=white:x=(w-tw)/2:y=250"]
        vf+=[f"drawtext=fontfile={FONT}:text='{esc(l)}':fontsize=28:fontcolor=0xcccccc:x=(w-tw)/2:y={320+k*40}" for k,l in enumerate(lines)]
        cmd=["ffmpeg","-y","-v","error","-f","lavfi","-i",f"color=c={COL[s['kind']]}:s={W}x{H}:r={FPS}:d={d:.3f}",
             "-vf",",".join(vf+vf_tail+[fade]),"-an","-c:v","libx264","-pix_fmt","yuv420p",str(seg)]
    elif a.suffix in (".jpg",".jpeg",".png"):
        z=f"zoompan=z='min(zoom+0.0006,1.15)':d={int(d*FPS)}:s={W}x{H}:fps={FPS}"
        cmd=["ffmpeg","-y","-v","error","-i",str(a),"-vf",",".join([f"scale={W*2}:-2,{z}"]+vf_tail+[fade]),
             "-t",f"{d:.3f}","-an","-c:v","libx264","-pix_fmt","yuv420p",str(seg)]
    else:
        base=f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,fps={FPS},setsar=1"
        cmd=["ffmpeg","-y","-v","error","-stream_loop","-1","-i",str(a),"-vf",",".join([base]+vf_tail+[fade]),
             "-t",f"{d:.3f}","-an","-c:v","libx264","-pix_fmt","yuv420p",str(seg)]
    subprocess.run(cmd,check=True); parts.append(seg)
lst=tmp/"list.txt"; lst.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-i",str(audio),
                "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-shortest",str(out)],check=True)
print("wrote",out)
