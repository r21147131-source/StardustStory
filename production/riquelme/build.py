"""Riquelme documentary: cut stock B-roll to the voiceover, grade, mux. Usage: python3 build.py"""
import json, os, subprocess, sys, urllib.request, collections

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
VO = os.path.join(REPO, "public", "riquelme-voiceover.mp3")
WORK = os.environ.get("RIQ_WORK", "/tmp/riq-work")
OUT = os.path.join(REPO, "output", "riquelme")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
P = "https://videos.pexels.com/video-files/"
CLIPS = {
 "night_a": P+"32614272/13908526_640_360_30fps.mp4",
 "night_b": P+"34590578/14658140_640_360_30fps.mp4",
 "night_c": P+"34743669/14729230_640_360_60fps.mp4",
 "night_d": P+"35002181/14828534_640_360_30fps.mp4",
 "night_e": P+"34514079/14623432_640_360_32fps.mp4",
 "crowd_a": P+"34671875/14695685_640_360_30fps.mp4",
 "crowd_b": P+"34699780/14708158_640_360_60fps.mp4",
 "crowd_c": P+"39711248/16931647_640_360_25fps.mp4",
 "crowd_d": P+"11208468/11208468-hd_1920_1080_30fps.mp4",
 "ball_street": P+"16436835/16436835-hd_1280_720_24fps.mp4",
 "kick_a": P+"3192082/3192082-hd_1920_1080_25fps.mp4",
 "kick_b": P+"3192198/3192198-hd_1280_720_25fps.mp4",
 "ball_play": P+"10349005/10349005-hd_2048_1080_25fps.mp4",
 "kid_dirt": P+"19253585/19253585-hd_1280_720_24fps.mp4",
 "rural": P+"39710146/16930504_640_360_47fps.mp4",
 "ba_drive": P+"19908995/19908995-hd_1920_1080_25fps.mp4",
 "ba_obelisk": P+"31563866/13451927_640_360_50fps.mp4",
 "ba_law": P+"19596479/19596479-hd_1920_1080_30fps.mp4",
 "ba_street": P+"10229755/10229755-hd_1280_720_27fps.mp4",
 "bcn_aerial": P+"3143827/3143827-hd_1922_1080_24fps.mp4",
 "bcn_aerial2": P+"3143889/3143889-hd_1282_720_24fps.mp4",
 "bcn_beach": P+"15431566/15431566-hd_1280_720_30fps.mp4",
 "bcn_park": P+"10801860/10801860-hd_1280_720_30fps.mp4",
 "play_a": P+"6077714/6077714-hd_1280_720_25fps.mp4",
 "play_b": P+"6077713/6077713-hd_1920_1080_25fps.mp4",
 "play_c": P+"9431557/9431557-hd_1366_720_24fps.mp4",
 "match_a": P+"15448985/15448985-hd_1280_720_60fps.mp4",
 "match_b": P+"15462727/15462727-hd_1920_1080_60fps.mp4",
 "pen_a": P+"15436955/15436955-hd_1906_1080_30fps.mp4",
 "pen_b": P+"15436956/15436956-hd_1906_1080_30fps.mp4",
 "drone": P+"6079615/6079615-hd_1920_1080_25fps.mp4",
 "empty": P+"8938609/8938609-hd_1920_1080_25fps.mp4",
 "warmup": P+"5625447/5625447-hd_1280_720_30fps.mp4",
 "boys": P+"8940719/8940719-hd_1920_1080_25fps.mp4",
}
SCENES = collections.OrderedDict([
 ("S1", ["night_a","kick_a","ball_street","night_b","kick_b"]),
 ("S2", ["kid_dirt","ba_street","rural","ba_obelisk","ball_play","ba_law","boys","ba_drive"]),
 ("S3", ["bcn_aerial","bcn_beach","kick_b","bcn_park","bcn_aerial2","play_c","bcn_aerial"]),
 ("S4", ["match_a","play_c","match_b","play_b","play_a","match_a","warmup"]),
 ("S5", ["night_c","crowd_a","crowd_d","night_d","pen_a","crowd_c","night_e","pen_b","crowd_b","night_a"]),
 ("S6", ["kick_a","play_b","kick_b","play_c","warmup","ball_play","play_a"]),
 ("S7", ["crowd_d","crowd_b","crowd_c","match_b","boys","night_c","crowd_a"]),
 ("S8", ["drone","empty","ball_street","kick_a","empty"]),
])
SLOT = 9.0
GRADE = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=25,"
         "eq=saturation=0.7:contrast=1.08:brightness=-0.04,"
         "vignette=PI/4,noise=alls=9:allf=t,format=yuv420p")

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-1500:])
    return r.stdout

def dur(path):
    return float(run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",path]).strip())

def main():
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    local, length = {}, {}
    for k, u in CLIPS.items():
        p = os.path.join(WORK, k + ".mp4")
        if not os.path.exists(p):
            run(['curl','-sSfL','--retry','3','-o',p,u])
        local[k], length[k] = p, dur(p)
    total = dur(VO)
    words = collections.OrderedDict()
    cur = None
    for line in open(os.path.join(ROOT, "narration.txt"), encoding="utf-8"):
        if line.startswith("## "): cur = line[3:].strip(); words[cur] = 0
        elif cur: words[cur] += len(line.split())
    wsum = sum(words.values())
    scene_dur = {s: total * w / wsum for s, w in words.items()}
    # User-supplied footage: put files in public/riquelme-footage/S1..S8/ -- those replace stock for that scene.
    foot = os.path.join(REPO, "public", "riquelme-footage")
    for s in SCENES:
        d = os.path.join(foot, s)
        files = sorted(f for f in os.listdir(d) if f.lower().endswith((".mp4", ".mov", ".mkv", ".webm"))) if os.path.isdir(d) else []
        if files:
            keys = []
            for f in files:
                k = f"user_{s}_{f}"; local[k] = os.path.join(d, f); length[k] = dur(local[k]); keys.append(k)
            SCENES[s] = keys
    segs, used = [], collections.Counter()
    for s, clips in SCENES.items():
        n = max(1, round(scene_dur[s] / SLOT)); slot = scene_dur[s] / n
        for i in range(n):
            k = clips[i % len(clips)]
            avail = length[k]; seen = used[k]; used[k] += 1
            ss = min(seen * 0.45 * avail, max(0.0, avail - 1.0)) if seen else 0.0
            rem = avail - ss
            factor = 1.0 if rem >= slot else min(2.2, slot / max(rem, 0.5))
            seg = os.path.join(WORK, f"seg{len(segs):03d}.mp4")
            vf = f"setpts=PTS*{factor:.3f}," + GRADE if factor > 1 else GRADE
            vf += ",fade=t=in:st=0:d=0.6,fade=t=out:st=%.2f:d=0.6" % (slot - 0.6)
            run(["ffmpeg","-y","-hide_banner","-loglevel","error","-stream_loop","-1","-ss",f"{ss:.2f}",
                 "-i",local[k],"-t",f"{slot:.3f}","-vf",vf,"-an","-c:v","libx264","-preset","veryfast","-crf","21",seg])
            segs.append(seg)
    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    t1 = ("drawtext=fontfile=%s:text='THE BITTERSWEET LEGACY OF':fontsize=44:fontcolor=white@0.9:x=(w-tw)/2:y=h*0.40:enable='between(t,4,13)':alpha='min(1,(t-4)/1.5)',"
          "drawtext=fontfile=%s:text='JUAN ROM\\u00c1N RIQUELME':fontsize=84:fontcolor=white:x=(w-tw)/2:y=h*0.47:enable='between(t,4,13)':alpha='min(1,(t-4)/1.5)'") % (FONT, FONT)
    e0 = total - 24
    t2 = ("drawtext=fontfile=%s:text='JUAN ROM\\u00c1N RIQUELME':fontsize=84:fontcolor=white:x=(w-tw)/2:y=h*0.42:enable='gt(t,%.1f)':alpha='min(1,(t-%.1f)/2)',"
          "drawtext=fontfile=%s:text='Some geniuses are remembered for what they won. Others, for how they made us feel.':fontsize=30:fontcolor=white@0.85:x=(w-tw)/2:y=h*0.56:enable='gt(t,%.1f)':alpha='min(1,(t-%.1f)/2)'") % (FONT, e0, e0, FONT, e0+2, e0+2)
    final = os.path.join(OUT, "riquelme-bittersweet-legacy.mp4")
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",lst,"-i",VO,
         "-vf",t1+","+t2+f",fade=t=out:st={total-2.5:.2f}:d=2.5","-af",f"afade=t=out:st={total-2.5:.2f}:d=2.5",
         "-c:v","libx264","-preset","medium","-crf","22","-c:a","aac","-b:a","160k","-shortest",final])
    print(final, f"{total:.1f}s", {s: round(d,1) for s, d in scene_dur.items()})
main()
