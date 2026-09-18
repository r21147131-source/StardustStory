import json
TOTAL = 543.852
SAFETY = 0.4
MAX_SHOT = 20.0

# id, planned, avail, url
shots = [
("S01",9.5,15,"https://videos.pexels.com/video-files/3945446/3945446-hd_2048_1080_25fps.mp4"),
("S02",9.55,24,"https://videos.pexels.com/video-files/11356024/11356024-hd_1920_1080_50fps.mp4"),
("S03",13,21,"https://videos.pexels.com/video-files/11272050/11272050-hd_1920_1080_30fps.mp4"),
("S04",13,32,"https://videos.pexels.com/video-files/6472910/6472910-hd_1920_1080_24fps.mp4"),
("S05",13,37,"https://videos.pexels.com/video-files/8089118/8089118-hd_1366_720_25fps.mp4"),
("S06",13,14,"https://videos.pexels.com/video-files/6274805/6274805-hd_1280_720_30fps.mp4"),
("S07",13,13,"https://videos.pexels.com/video-files/6332847/6332847-hd_1366_720_25fps.mp4"),
("S08",16.5,21,"https://videos.pexels.com/video-files/12695733/12695733-hd_1920_1080_24fps.mp4"),
("S09",13.5,19,"https://videos.pexels.com/video-files/16146237/16146237-hd_1280_720_24fps.mp4"),
("S10",15,12,"https://videos.pexels.com/video-files/7988643/7988643-hd_2048_1080_25fps.mp4"),
("S11",14,14,"https://videos.pexels.com/video-files/6274805/6274805-hd_1280_720_30fps.mp4"),
("S12",15.05,17,"https://videos.pexels.com/video-files/10238038/10238038-hd_1920_1080_25fps.mp4"),
("S13",13.95,14,"https://videos.pexels.com/video-files/853794/853794-hd_1280_720_50fps.mp4"),
("S14",18.47,30,"https://videos.pexels.com/video-files/9160922/9160922-hd_1280_720_24fps.mp4"),
("S15",13.53,15,"https://videos.pexels.com/video-files/39239777/16698596_640_360_30fps.mp4"),
("S16",13,30,"https://videos.pexels.com/video-files/8061378/8061378-hd_1280_720_25fps.mp4"),
("S17",17.24,23,"https://videos.pexels.com/video-files/32497448/13857508_640_360_25fps.mp4"),
("S18",12.76,18,"https://videos.pexels.com/video-files/36097843/15308644_640_360_25fps.mp4"),
("S19",13,39,"https://videos.pexels.com/video-files/8089122/8089122-hd_2048_1080_25fps.mp4"),
("S20",15,12,"https://videos.pexels.com/video-files/5659681/5659681-hd_1280_720_24fps.mp4"),
("S21",14.35,21,"https://videos.pexels.com/video-files/7984186/7984186-hd_2048_1080_25fps.mp4"),
("S22",13.65,15,"https://videos.pexels.com/video-files/8089116/8089116-hd_1366_720_25fps.mp4"),
("S23",13,25,"https://videos.pexels.com/video-files/8515272/8515272-hd_1280_720_25fps.mp4"),
("S24",13,21,"https://videos.pexels.com/video-files/37158428/15741621_640_360_60fps.mp4"),
("S25",13,35,"https://videos.pexels.com/video-files/6894274/6894274-hd_2048_1080_25fps.mp4"),
("S26",10.57,14,"https://videos.pexels.com/video-files/6896247/6896247-hd_1366_720_25fps.mp4"),
("S27",14.43,36,"https://videos.pexels.com/video-files/32600355/13902262_640_360_25fps.mp4"),
("S28",14.34,75,"https://videos.pexels.com/video-files/6896244/6896244-hd_1366_720_25fps.mp4"),
("S29",13.66,18,"https://videos.pexels.com/video-files/20606535/20606535-hd_1920_1080_24fps.mp4"),
("S30",13,21,"https://videos.pexels.com/video-files/12695733/12695733-hd_1920_1080_24fps.mp4"),
("S31",13,15,"https://videos.pexels.com/video-files/39239777/16698596_640_360_30fps.mp4"),
("S32",13,15,"https://videos.pexels.com/video-files/7346142/7346142-hd_960_720_25fps.mp4"),
("S33",13.81,9,"https://videos.pexels.com/video-files/3945485/3945485-hd_2048_1080_25fps.mp4"),
("S34",13.19,42,"https://videos.pexels.com/video-files/30509780/13070902_640_360_30fps.mp4"),
("S35",13,28,"https://videos.pexels.com/video-files/29974687/12862949_640_360_24fps.mp4"),
("S36",13,11,"https://videos.pexels.com/video-files/11714486/11714486-hd_1920_1080_30fps.mp4"),
("S37",13,30,"https://videos.pexels.com/video-files/9160922/9160922-hd_1280_720_24fps.mp4"),
("S38",10.22,27,"https://videos.pexels.com/video-files/13205825/13205825-hd_1920_1080_25fps.mp4"),
("S39",13.78,75,"https://videos.pexels.com/video-files/6896244/6896244-hd_1366_720_25fps.mp4"),
("S40",19.85,15,"https://videos.pexels.com/video-files/3945446/3945446-hd_2048_1080_25fps.mp4"),
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

with open("ep2long_final_shots.json","w") as f:
    json.dump(out, f, indent=2)
