#!/usr/bin/env python3
"""Sharper variant of hbo-hp-trailer-clips-build.py: each 9:16 crop of the 360p
source is upscaled 4x with Real-ESRGAN (realesr-general-x4v3, CPU) before the
final scale/grade, captions and mux. Title-card ("fit") shots skip the model.

Usage: python3 hbo-hp-trailer-esrgan-build.py <voiceover.mp3> <clean_cut.m4v> <et_cut.m4v> <weights.pth> <workdir> <out.mp4>
Needs: torch (CPU is fine), numpy, ffmpeg.
"""
import os, subprocess, sys
import numpy as np, torch, torch.nn as nn

VO, CLEAN, ET, WEIGHTS, WORK, OUT = sys.argv[1:7]
# reuse SHOTS / CAPS / CARDS / build_ass / run from the plain clips build
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "hbo-hp-trailer-clips-build.py")).read()
sys.argv = ["x", VO, CLEAN, ET, WORK, OUT]
exec(src[src.index("import os"):src.index("def main():")])


class SRVGGNetCompact(nn.Module):  # Real-ESRGAN "general-x4v3" architecture
    def __init__(self, nf=64, nc=32, up=4):
        super().__init__()
        self.up = up
        self.body = nn.ModuleList([nn.Conv2d(3, nf, 3, 1, 1), nn.PReLU(nf)])
        for _ in range(nc):
            self.body += [nn.Conv2d(nf, nf, 3, 1, 1), nn.PReLU(nf)]
        self.body.append(nn.Conv2d(nf, 3 * up * up, 3, 1, 1))
        self.shuf = nn.PixelShuffle(up)

    def forward(self, x):
        o = x
        for l in self.body:
            o = l(o)
        return self.shuf(o) + nn.functional.interpolate(x, scale_factor=self.up, mode="nearest")


def load_model():
    m = SRVGGNetCompact()
    sd = torch.load(WEIGHTS, map_location="cpu", weights_only=True)
    m.load_state_dict(sd.get("params", sd))
    torch.set_num_threads(os.cpu_count() or 4)
    return m.eval()


def esrgan_segment(model, lo, hi, w=202, h=360):
    """Pipe raw frames of `lo` through the model into `hi` (4x size)."""
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", lo, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                          stdout=subprocess.PIPE)
    wr = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{w*4}x{h*4}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                           "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", hi],
                          stdin=subprocess.PIPE)
    n = w * h * 3
    while True:
        buf = rd.stdout.read(n)
        if len(buf) < n:
            break
        x = torch.from_numpy(np.frombuffer(buf, np.uint8).copy()).view(h, w, 3).permute(2, 0, 1).float().div(255)[None]
        with torch.no_grad():
            y = model(x).clamp(0, 1)[0].permute(1, 2, 0).mul(255).round().byte().numpy()
        wr.stdin.write(y.tobytes())
    wr.stdin.close(); wr.wait(); rd.wait()


def main():
    model = load_model()
    segs = []
    for i, shot in enumerate(SHOTS):
        s, ss, L = shot[:3]
        mode = shot[3] if len(shot) > 3 else 0.5
        out = shot[4] if len(shot) > 4 else L
        slow = f"setpts=PTS*{out/L:.4f}," if out != L else ""
        seg = os.path.join(WORK, f"seg{i:02d}.mp4")
        fade = f"fade=t=in:st=0:d=0.12,fade=t=out:st={max(out-0.12,0):.3f}:d=0.12"
        d = 1 if i % 2 == 0 else -1
        if os.path.exists(seg):
            segs.append(seg); continue
        if mode == "fit":
            fc = (f"[0:v]split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,"
                  f"crop={W}:{H},boxblur=40:5,eq=brightness=-0.2[bg];"
                  f"[b]scale={W}:-2:flags=lanczos,unsharp=5:5:0.7[fg];"
                  f"[bg][fg]overlay=0:(H-h)/2-110,fps={FPS},{fade}[v]")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss}", "-t", f"{L:.3f}", "-i", SRC[s],
                 "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-preset", "veryfast",
                 "-crf", "18", "-pix_fmt", "yuv420p", "-t", f"{out:.3f}", seg])
        else:
            lo = os.path.join(WORK, f"lo{i:02d}.mp4"); hi = os.path.join(WORK, f"hi{i:02d}.mp4")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ss}", "-t", f"{L:.3f}", "-i", SRC[s],
                 "-vf", f"{slow}crop=202:360:x='(iw-202)*{mode}+({d})*50*(t/{out:.3f}-0.5)':y=0,fps={FPS}",
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "8", "-pix_fmt", "yuv420p",
                 "-t", f"{out:.3f}", lo])
            esrgan_segment(model, lo, hi)
            run(["ffmpeg", "-v", "error", "-y", "-i", hi, "-vf",
                 f"scale={W}:{H}:flags=lanczos,cas=0.4,eq=contrast=1.05,vignette=PI/6,{fade}",
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", seg])
            os.remove(lo); os.remove(hi)
        segs.append(seg); print("shot", i + 1, "/", len(SHOTS), flush=True)

    lst = os.path.join(WORK, "list.txt")
    open(lst, "w").write("".join(f"file '{s}'\n" for s in segs))
    base = os.path.join(WORK, "base.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-c", "copy", base])

    ass = os.path.join(WORK, "overlay.ass")
    build_ass(ass)
    run([
        "ffmpeg", "-v", "error", "-y", "-i", base, "-i", VO,
        "-vf", f"subtitles={ass}",
        "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow",
        "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
        "-af", "apad", "-t", f"{DUR:.2f}", "-movflags", "+faststart", OUT,
    ])


if __name__ == "__main__":
    main()
