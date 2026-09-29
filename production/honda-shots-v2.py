"""Shot list v2 for "How a Poor Boy Built Honda": real archive + AI + stock.

Three kinds of source, cut on transcript beats of public/honda-voiceover.mp3:
  arch-NN  real photos from Wikimedia Commons (public domain / CC), animated
           with Ken Burns moves via vidIQ compose; see production/honda-credits.md
  ai-NN    AI-generated historical reconstructions (vidIQ, minimax-h3). They
           show period scenes only; Soichiro Honda himself appears solely in
           real photographs.
  pexels   stock B-roll
Writes production/honda-shots-v2.json for production/render-local.py.
"""
import json

TOTAL = 482.38
P = "https://videos.pexels.com/video-files/"

ARCH = ["1964 portrait", "1955 Asahigraph portrait", "Art-Curtiss 1924",
        "Curtiss Special (Honda Collection Hall)", "Art-Curtiss 1934 race",
        "Sakakibara brothers and Honda 1934", "Art Shokai Hamamatsu 1935",
        "Art-Curtiss 1936", "Dream D (1949)", "Super Cub (1958)", "RC142 (1959 TT)",
        "CB750", "Civic CVCC", "ASIMO", "Soichiro Honda Craftsmanship Center"]
AI = ["village road, early automobile", "1920s Tokyo garage", "piston rings on bench",
      "factory burning after air raid", "post-war street, bicycles",
      "engine bolted to bicycle", "motorized bicycle on country road",
      "1950s motorcycle assembly line", "1959 TT road race", "1973 fuel queue"]

def arch(i): return ("local/arch-%02d.mp4" % i, 7, 0)
def ai(i): return ("local/ai-%02d.mp4" % i, 6, 0)
def px(path, avail, trim=0): return (P + path, avail, trim)

shots = [
    (0.0,   px("8219164/8219164-hd_1920_1080_30fps.mp4", 17)),        # abandoned building
    (5.2,   px("20706788/20706788-hd_1280_720_25fps.mp4", 75)),       # fire
    (10.7,  px("4876874/4876874-hd_1280_720_30fps.mp4", 12)),         # demolished building
    (15.5,  px("7185277/7185277-hd_1920_1080_30fps.mp4", 12)),        # antique bicycle
    (20.8,  px("30283095/12981259_640_360_25fps.mp4", 71)),           # motorcycle assembly
    (26.0,  arch(11)),                                                # CB750
    (31.2,  px("10755266/10755266-hd_2560_1440_30fps.mp4", 30)),      # earth
    (36.5,  arch(0)),                                                 # Honda, 1964
    (41.4,  px("7251360/7251360-hd_1280_720_30fps.mp4", 26)),         # rural Japan
    (46.5,  px("5846389/5846389-hd_1920_1080_25fps.mp4", 22)),        # forging
    (51.6,  px("12455626/12455626-hd_1280_720_60fps.mp4", 31)),       # bicycle repair
    (61.6,  px("9963499/9963499-hd_1280_720_30fps.mp4", 15)),         # gears
    (66.5,  px("856237/856237-hd_1920_1080_30fps.mp4", 30)),          # spokes
    (72.4,  ai(0)),                                                   # AI: car through village
    (78.4,  px("13444565/13444565-hd_1920_1080_30fps.mp4", 15)),      # dirt road
    (82.5,  px("8987271/8987271-hd_1280_720_30fps.mp4", 15)),         # engine oil
    (92.8,  px("17371342/17371342-hd_1280_720_30fps.mp4", 22)),       # train, Japan
    (102.9, ai(1)),                                                   # AI: Tokyo garage
    (108.9, px("5592640/5592640-hd_1280_720_24fps.mp4", 17)),         # sweeping
    (112.9, px("7565185/7565185-hd_1366_720_25fps.mp4", 36)),         # mechanic
    (118.0, arch(6)),                                                 # Art Shokai 1935
    (123.2, px("27925020/12264906_840_360_30fps.mp4", 17)),           # night workshop
    (128.5, arch(2)),                                                 # Art-Curtiss 1924
    (133.8, arch(3)),                                                 # Curtiss Special today
    (140.0, arch(4)),                                                 # 1934 race
    (144.1, arch(7)),                                                 # 1936
    (149.2, px("3066425/3066425-hd_2048_1080_24fps.mp4", 16)),        # exposed engine
    (154.3, arch(5)),                                                 # Honda & Sakakibaras 1934
    (160.5, px("10231514/10231514-hd_2560_1440_30fps.mp4", 12)),      # old racer
    (164.6, px("4872871/4872871-hd_1280_720_25fps.mp4", 10)),         # crumpled papers
    (170.0, px("5846591/5846591-hd_1920_1080_25fps.mp4", 18)),        # sparks
    (174.7, px("8321907/8321907-hd_1366_720_25fps.mp4", 31)),         # lathe
    (180.0, ai(2)),                                                   # AI: piston rings
    (185.3, px("3066417/3066417-hd_2048_1080_24fps.mp4", 17)),        # engine detail
    (190.6, px("7668957/7668957-hd_1920_1080_25fps.mp4", 17)),        # rejected
    (195.4, px("7668507/7668507-hd_1920_1080_25fps.mp4", 14)),        # rejected
    (205.7, px("9570402/9570402-hd_1366_720_25fps.mp4", 24)),         # studying
    (216.0, px("5121751/5121751-hd_1920_1080_25fps.mp4", 14)),        # molten steel
    (221.2, px("20706788/20706788-hd_1280_720_25fps.mp4", 75, 20)),   # fire
    (226.4, ai(3)),                                                   # AI: factory burning
    (232.4, px("15202764/15202764-hd_1920_1080_30fps.mp4", 29)),      # ruined interior
    (237.1, px("6498490/6498490-hd_1920_1080_24fps.mp4", 45)),        # cracked ground
    (242.2, px("8219164/8219164-hd_1920_1080_30fps.mp4", 17, 5)),     # abandoned building
    (247.2, px("4882461/4882461-hd_1366_720_25fps.mp4", 35)),         # ruins
    (257.6, ai(4)),                                                   # AI: post-war bicycles
    (263.6, px("37681296/15976023_640_360_30fps.mp4", 29)),           # cycling
    (267.6, ai(5)),                                                   # AI: engine on bicycle
    (273.6, px("30288950/12984020_640_360_25fps.mp4", 29)),           # engine assembly
    (277.7, ai(6)),                                                   # AI: motorized bicycle
    (283.7, px("32189924/13727419_640_360_30fps.mp4", 15)),           # scooter ride
    (287.9, px("8449431/8449431-hd_1920_1080_25fps.mp4", 16)),        # blueprint
    (293.0, arch(8)),                                                 # Dream D
    (298.2, ai(7)),                                                   # AI: 1950s factory
    (304.2, px("30283093/12981243_640_360_25fps.mp4", 18)),           # motorcycle factory
    (308.5, px("8449347/8449347-hd_1280_720_25fps.mp4", 10)),         # engineers
    (313.6, px("6615508/6615508-hd_1280_720_25fps.mp4", 14)),         # compass
    (318.7, px("30288948/12984025_640_360_25fps.mp4", 33)),           # assembly line
    (324.0, arch(9)),                                                 # Super Cub
    (329.1, px("30283098/12981273_640_360_25fps.mp4", 13)),           # engine line
    (334.5, arch(1)),                                                 # Honda, 1955
    (340.0, px("30523150/13076575_640_360_60fps.mp4", 36)),           # container ship
    (350.0, ai(8)),                                                   # AI: TT race
    (356.0, arch(10)),                                                # RC142
    (360.3, px("14055755/14055755-hd_1920_1080_30fps.mp4", 16)),      # riding
    (366.0, px("5052603/5052603-hd_1280_720_30fps.mp4", 13)),         # motorcycle
    (371.3, arch(12)),                                                # Civic CVCC
    (376.6, ai(9)),                                                   # AI: fuel queue
    (381.4, px("15510227/15510227-hd_1280_720_30fps.mp4", 26)),       # night highway
    (391.8, arch(0)),                                                 # Honda, 1964
    (398.8, px("4872871/4872871-hd_1280_720_25fps.mp4", 10)),         # crumpled papers
    (402.0, px("30288947/12984004_640_360_25fps.mp4", 34)),           # engineers
    (412.1, arch(13)),                                                # ASIMO
    (417.0, px("6187626/6187626-hd_1280_720_25fps.mp4", 19)),         # airplane
    (422.2, px("35462656/15024365_640_360_30fps.mp4", 43)),           # Tokyo
    (432.4, px("1251527/1251527-hd_1280_720_25fps.mp4", 9)),          # speedboat
    (437.2, px("34905668/14787305_640_360_25fps.mp4", 42)),           # contrail
    (442.6, ai(0)),                                                   # recap: the boy
    (447.6, px("5592525/5592525-hd_1280_720_24fps.mp4", 14)),         # sweeping
    (452.8, ai(3)),                                                   # recap: war
    (457.8, ai(6)),                                                   # recap: bicycle
    (462.9, arch(14)),                                                # Craftsmanship Center
    (469.9, px("33354461/14202809_640_360_30fps.mp4", 38)),           # sunrise
    (473.4, px("17956563/17956563-hd_1920_1080_60fps.mp4", 76)),      # skyline
]

out = []
for i, (start, (src, avail, trim)) in enumerate(shots):
    end = shots[i + 1][0] if i + 1 < len(shots) else TOTAL
    if end - start > avail - trim - 0.05:
        print(f"WARN shot@{start}: needs {end-start:.2f}s, clip has {avail-trim}s")
    out.append({"start": start, "src": src, "trim": trim})
json.dump({"total": TOTAL, "shots": out}, open("production/honda-shots-v2.json", "w"), indent=1)
kinds = [s["src"].split("/")[-1][:3] for s in out]
print(len(out), "shots:", kinds.count("arc"), "archive,", kinds.count("ai-"), "AI")
