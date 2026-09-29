"""Shot list for "How a Poor Boy Built Honda" — cuts land on transcript beats.

Voiceover: public/honda-voiceover.mp3 (the user's honda1 take, 8:02).
Beats come from a local Vosk word-timestamp transcript. Visuals are stock
Pexels B-roll only, with no AI depiction of Soichiro Honda.
Writes production/honda-shots.json for production/render-local.py.
"""
import json

TOTAL = 482.38
P = "https://videos.pexels.com/video-files/"

# (start, source path, clip length, trim-in)
shots = [
    (0.0,   "8219164/8219164-hd_1920_1080_30fps.mp4", 17, 0),       # abandoned building
    (5.2,   "20706788/20706788-hd_1280_720_25fps.mp4", 75, 0),      # fire
    (10.7,  "4876874/4876874-hd_1280_720_30fps.mp4", 12, 0),        # demolished building
    (15.5,  "7185277/7185277-hd_1920_1080_30fps.mp4", 12, 0),       # antique bicycle
    (20.8,  "30283095/12981259_640_360_25fps.mp4", 71, 0),          # motorcycle assembly line
    (31.2,  "10755266/10755266-hd_2560_1440_30fps.mp4", 30, 0),     # earth from space
    (36.5,  "856237/856237-hd_1920_1080_30fps.mp4", 30, 0),         # bicycle spokes
    (41.4,  "7251360/7251360-hd_1280_720_30fps.mp4", 26, 0),        # rural Japan aerial
    (46.5,  "5846389/5846389-hd_1920_1080_25fps.mp4", 22, 0),       # forging metal
    (51.6,  "12455626/12455626-hd_1280_720_60fps.mp4", 31, 0),      # fixing a bicycle
    (61.6,  "9963499/9963499-hd_1280_720_30fps.mp4", 15, 0),        # bike gears
    (72.4,  "13444565/13444565-hd_1920_1080_30fps.mp4", 15, 0),     # vehicles on dirt road
    (82.5,  "8987271/8987271-hd_1280_720_30fps.mp4", 15, 0),        # pouring engine oil
    (92.8,  "17371342/17371342-hd_1280_720_30fps.mp4", 22, 0),      # train arriving, Japan
    (102.9, "8469674/8469674-hd_1920_1080_25fps.mp4", 20, 0),       # car repair
    (107.6, "5592640/5592640-hd_1280_720_24fps.mp4", 17, 0),        # sweeping floor
    (112.9, "7565185/7565185-hd_1366_720_25fps.mp4", 36, 0),        # mechanic close-up
    (123.2, "27925020/12264906_840_360_30fps.mp4", 17, 0),          # night workshop
    (133.8, "3066422/3066422-hd_1366_720_24fps.mp4", 20, 0),        # vintage race car
    (144.1, "10231514/10231514-hd_2560_1440_30fps.mp4", 12, 0),     # old racer on circuit
    (149.2, "3066425/3066425-hd_2048_1080_24fps.mp4", 16, 0),       # exposed engine
    (154.3, "3066429/3066429-hd_1366_720_24fps.mp4", 17, 0),        # vintage sports car
    (164.6, "4872871/4872871-hd_1280_720_25fps.mp4", 10, 0),        # crumpled papers
    (170.0, "5846591/5846591-hd_1920_1080_25fps.mp4", 18, 0),       # plasma cutter sparks
    (174.7, "8321907/8321907-hd_1366_720_25fps.mp4", 31, 0),        # lathe
    (185.3, "3066417/3066417-hd_2048_1080_24fps.mp4", 17, 0),       # engine detail
    (190.6, "7668957/7668957-hd_1920_1080_25fps.mp4", 17, 0),       # paper into bin
    (195.4, "7668507/7668507-hd_1920_1080_25fps.mp4", 14, 0),       # paper into bin
    (205.7, "9570402/9570402-hd_1366_720_25fps.mp4", 24, 0),        # studying books
    (216.0, "5121751/5121751-hd_1920_1080_25fps.mp4", 14, 0),       # molten steel
    (221.2, "20706788/20706788-hd_1280_720_25fps.mp4", 75, 20),     # fire
    (226.4, "15202764/15202764-hd_1920_1080_30fps.mp4", 29, 0),     # ruined interior
    (237.1, "6498490/6498490-hd_1920_1080_24fps.mp4", 45, 0),       # cracked ground
    (242.2, "8219164/8219164-hd_1920_1080_30fps.mp4", 17, 5),       # abandoned building
    (247.2, "4882461/4882461-hd_1366_720_25fps.mp4", 35, 0),        # walking through ruins
    (257.6, "37681296/15976023_640_360_30fps.mp4", 29, 0),          # cycling through streets
    (267.6, "30288950/12984020_640_360_25fps.mp4", 29, 0),          # engine assembly
    (277.7, "5052415/5052415-hd_1280_720_30fps.mp4", 11, 0),        # motorbike countryside
    (283.0, "32189924/13727419_640_360_30fps.mp4", 15, 0),          # vintage scooter ride
    (287.9, "8449431/8449431-hd_1920_1080_25fps.mp4", 16, 0),       # blueprint
    (298.2, "30283093/12981243_640_360_25fps.mp4", 18, 0),          # motorcycle factory
    (308.5, "8449347/8449347-hd_1280_720_25fps.mp4", 10, 0),        # engineers at plans
    (313.6, "6615508/6615508-hd_1280_720_25fps.mp4", 14, 0),        # compass on drawing
    (318.7, "30288948/12984025_640_360_25fps.mp4", 33, 0),          # assembly line work
    (329.1, "30283098/12981273_640_360_25fps.mp4", 13, 0),          # engine part line
    (340.0, "30523150/13076575_640_360_60fps.mp4", 36, 0),          # container ship
    (350.0, "32554208/13883008_640_360_120fps.mp4", 12, 0),         # motorcycle race
    (355.4, "30398173/13027563_640_360_60fps.mp4", 10, 0),          # motorcycle race
    (360.3, "14055755/14055755-hd_1920_1080_30fps.mp4", 16, 0),     # riding on road
    (366.0, "5052603/5052603-hd_1280_720_30fps.mp4", 13, 0),        # motorcycle
    (371.3, "1192116/1192116-hd_1920_1080_30fps.mp4", 66, 0),       # busy street
    (376.6, "29576549/12731045_640_360_24fps.mp4", 21, 0),          # filling up with fuel
    (381.4, "15510227/15510227-hd_1280_720_30fps.mp4", 26, 0),      # night highway aerial
    (391.8, "10641848/10641848-hd_1920_1080_25fps.mp4", 24, 0),     # welding in factory
    (402.0, "30288947/12984004_640_360_25fps.mp4", 34, 0),          # engine line workers
    (412.1, "28221363/12331857_640_360_30fps.mp4", 10, 0),          # CNC machine
    (417.0, "6187626/6187626-hd_1280_720_25fps.mp4", 19, 0),        # airplane
    (422.2, "35462656/15024365_640_360_30fps.mp4", 43, 0),          # Tokyo aerial
    (432.4, "1251527/1251527-hd_1280_720_25fps.mp4", 9, 0),         # speedboat
    (437.2, "34905668/14787305_640_360_25fps.mp4", 42, 0),          # plane with contrail
    (442.6, "856237/856237-hd_1920_1080_30fps.mp4", 30, 10),        # bicycle spokes
    (447.6, "5592525/5592525-hd_1280_720_24fps.mp4", 14, 0),        # sweeping
    (452.8, "29504948/12700561_640_360_30fps.mp4", 12, 0),          # cracked earth aerial
    (457.8, "7185277/7185277-hd_1920_1080_30fps.mp4", 12, 0),       # antique bicycle
    (462.9, "33354461/14202809_640_360_30fps.mp4", 38, 0),          # mountain sunrise
    (473.4, "17956563/17956563-hd_1920_1080_60fps.mp4", 76, 0),     # city skyline
]

out = []
for i, (start, path, avail, trim) in enumerate(shots):
    end = shots[i + 1][0] if i + 1 < len(shots) else TOTAL
    if end - start > avail - trim - 0.4:
        print(f"WARN shot@{start}: needs {end-start:.1f}s, clip has {avail-trim:.1f}s")
    out.append({"start": start, "src": P + path, "trim": trim})
json.dump({"total": TOTAL, "shots": out}, open("production/honda-shots.json", "w"), indent=1)
print(len(out), "shots")
