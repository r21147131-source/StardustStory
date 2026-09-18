import json
TOTAL = 257.883
SAFETY = 0.4
MAX_SHOT = 24.0

shots = [
("S01", 9.0,  15, "https://videos.pexels.com/video-files/3945446/3945446-hd_2048_1080_25fps.mp4"),
("S02", 11.0, 24, "https://videos.pexels.com/video-files/11356024/11356024-hd_1920_1080_50fps.mp4"),
("S03", 13.0, 21, "https://videos.pexels.com/video-files/27170840/12089451_840_360_30fps.mp4"),
("S04", 13.0, 14, "https://videos.pexels.com/video-files/6896247/6896247-hd_1366_720_25fps.mp4"),
("S05", 13.0, 37, "https://videos.pexels.com/video-files/8089118/8089118-hd_1366_720_25fps.mp4"),
("S06", 11.0, 25, "https://videos.pexels.com/video-files/8515272/8515272-hd_1280_720_25fps.mp4"),
("S07", 12.0, 35, "https://videos.pexels.com/video-files/6894274/6894274-hd_2048_1080_25fps.mp4"),
("S08", 14.0, 14, "https://videos.pexels.com/video-files/6274805/6274805-hd_1280_720_30fps.mp4"),
("S09", 14.0, 19, "https://videos.pexels.com/video-files/16146237/16146237-hd_1280_720_24fps.mp4"),
("S10", 12.0, 17, "https://videos.pexels.com/video-files/10238038/10238038-hd_1920_1080_25fps.mp4"),
("S11", 13.0, 26, "https://videos.pexels.com/video-files/6742732/6742732-hd_1280_720_24fps.mp4"),
("S12", 13.0, 23, "https://videos.pexels.com/video-files/32497448/13857508_640_360_25fps.mp4"),
("S13", 13.0, 18, "https://videos.pexels.com/video-files/36097843/15308644_640_360_25fps.mp4"),
("S14", 14.0, 21, "https://videos.pexels.com/video-files/12695733/12695733-hd_1920_1080_24fps.mp4"),
("S15", 13.0, 15, "https://videos.pexels.com/video-files/39239777/16698596_640_360_30fps.mp4"),
("S16", 18.0, 42, "https://videos.pexels.com/video-files/30509780/13070902_640_360_30fps.mp4"),
("S17", 14.0, 11, "https://videos.pexels.com/video-files/11714486/11714486-hd_1920_1080_30fps.mp4"),
("S18a", 15.0, 15, "https://videos.pexels.com/video-files/7346142/7346142-hd_960_720_25fps.mp4"),
("S18b", 22.88, 75, "https://videos.pexels.com/video-files/6896244/6896244-hd_1366_720_25fps.mp4"),
]

out = []
for id_, planned, avail, url in shots:
    cap = max(2.0, min(planned, avail - SAFETY))
    flex = max(0.0, min(avail - SAFETY, MAX_SHOT) - planned)
    out.append({"id": id_, "dur": round(cap,2), "flex": round(flex,2), "src": url})

total = sum(o["dur"] for o in out)
deficit = TOTAL - total
print(f"base total {total:.2f} deficit {deficit:.2f}")

flex_pool = [o for o in out if o["flex"] > 0]
headroom = sum(o["flex"] for o in flex_pool)
if deficit > 0 and headroom > 0:
    for o in flex_pool:
        add = min(deficit * (o["flex"]/headroom), o["flex"])
        o["dur"] = round(o["dur"] + add, 2)

total2 = sum(o["dur"] for o in out)
print(f"final total {total2:.2f} target {TOTAL:.2f} diff {TOTAL-total2:.2f}")
for o in out:
    print(f'{o["id"]:5s} dur={o["dur"]:6.2f}  {o["src"]}')

with open("ep2_final_shots.json","w") as f:
    json.dump(out, f, indent=2)
