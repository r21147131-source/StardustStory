"""Shot allocation for "The $20 Storage Unit" — cuts land on transcript timestamps.

Each shot starts at the narration beat it illustrates (from a local Vosk
word-timestamp transcript of public/storage-unit-voiceover.m4a) and runs
until the next beat. Segments are cut at shot boundaries so each stays under
vidIQ compose's 240s cap. Visuals are symbolic stock B-roll only: no
depictions of the victim or the accused.
"""
import json

TOTAL = 645.58
SAFETY = 0.4
P = "https://videos.pexels.com/video-files/"

# (start, source path, clip length, trim-in)
shots = [
    (0.0,   "12260947/12260947-hd_1920_1080_25fps.mp4", 41, 0),   # storage units aerial
    (10.7,  "4889026/4889026-hd_1280_720_24fps.mp4", 13, 0),      # rusty padlock
    (21.5,  "5531385/5531385-hd_1920_1080_24fps.mp4", 47, 0),     # highway drive
    (32.1,  "38630005/16406650_640_360_24fps.mp4", 15, 0),        # Columbia Gorge
    (42.1,  "4941466/4941466-hd_1920_1080_25fps.mp4", 18, 0),     # stacked storage bins
    (52.3,  "32078346/13674096_640_360_60fps.mp4", 24, 0),        # roll-up door at night
    (62.6,  "32538553/13876654_640_360_24fps.mp4", 26, 0),        # police lights
    (73.3,  "5555355/5555355-hd_1280_720_24fps.mp4", 20, 0),      # candle — Kiki
    (83.7,  "30490553/13065400_640_360_30fps.mp4", 13, 0),        # Montana
    (93.9,  "8246470/8246470-hd_1920_1080_25fps.mp4", 12, 0),     # wedding invitations
    (104.0, "5368229/5368229-hd_1920_1080_25fps.mp4", 11, 0),     # calendar
    (114.0, "8549580/8549580-hd_1920_1080_25fps.mp4", 38, 0),     # rain on window
    (124.3, "5237057/5237057-hd_1920_1080_30fps.mp4", 16, 0),     # fishing rods, riverbank
    (134.6, "11115114/11115114-hd_1280_720_30fps.mp4", 14, 0),    # rural road
    (144.8, "9306134/9306134-hd_1366_720_30fps.mp4", 19, 0),      # notices on corkboard
    (154.9, "5366344/5366344-hd_1920_1080_30fps.mp4", 12, 0),     # raindrops
    (164.9, "9028591/9028591-hd_1280_720_30fps.mp4", 15, 0),      # Columbia River aerial
    (174.9, "3999371/3999371-hd_1920_1080_24fps.mp4", 14, 0),     # chained gate
    (185.8, "12260947/12260947-hd_1920_1080_25fps.mp4", 41, 15),  # storage units aerial
    (196.5, "7685212/7685212-hd_1280_720_24fps.mp4", 25, 0),      # signing paperwork
    (206.7, "3908915/3908915-hd_1280_720_30fps.mp4", 36, 0),      # night road
    # --- segment 2
    (217.2, "8846989/8846989-hd_1280_720_30fps.mp4", 13, 0),      # locked door
    (227.3, "8480228/8480228-hd_1280_720_25fps.mp4", 11, 0),      # auction listing on laptop
    (237.5, "5466769/5466769-hd_1280_720_25fps.mp4", 14, 0),      # counting cash
    (247.8, "8523640/8523640-hd_1920_1080_25fps.mp4", 15, 0),     # laptop
    (258.2, "6893879/6893879-hd_1280_720_50fps.mp4", 13, 0),      # plastic container
    (268.4, "10476430/10476430-hd_2048_1080_25fps.mp4", 23, 0),   # police officers
    (278.4, "10466486/10466486-hd_2048_1080_25fps.mp4", 20, 0),   # police tape
    (289.1, "11195129/11195129-hd_2048_1080_50fps.mp4", 19, 0),   # crime-scene technician
    (299.1, "10482308/10482308-hd_1366_720_25fps.mp4", 12, 0),    # evidence markers
    (310.1, "5500355/5500355-hd_1280_720_25fps.mp4", 20, 0),      # charcoal
    (320.2, "8731441/8731441-hd_1280_720_25fps.mp4", 14, 0),      # report being written
    (330.3, "5636967/5636967-hd_1280_720_24fps.mp4", 10, 0),      # scales of justice
    (339.9, "8382677/8382677-hd_2048_1080_25fps.mp4", 63, 0),     # fingerprints
    (350.5, "5555358/5555358-hd_1920_1080_24fps.mp4", 20, 0),     # candles
    (360.9, "35647503/15106474_640_360_50fps.mp4", 25, 0),        # excavator
    (370.9, "31890003/13583399_640_360_60fps.mp4", 29, 0),        # bridge over river
    (382.1, "8731580/8731580-hd_1280_720_25fps.mp4", 12, 0),      # pen, documents
    (392.1, "5211616/5211616-hd_1280_720_24fps.mp4", 23, 0),      # jail cells
    (399.0, "35305253/14958110_640_360_30fps.mp4", 13, 0),        # mobile home park
    (405.0, "3999394/3999394-hd_1280_720_24fps.mp4", 13, 0),      # wet road driving
    (412.6, "5636977/5636977-hd_1280_720_24fps.mp4", 10, 0),      # scales and gavel
    (422.2, "12374854/12374854-hd_1920_1080_60fps.mp4", 27, 0),   # parking lot at night
    # --- segment 3
    (433.1, "13619802/13619802-hd_1280_720_60fps.mp4", 17, 0),    # rain on window
    (443.2, "2055336/2055336-hd_1366_720_24fps.mp4", 12, 0),      # Colorado town
    (453.2, "7773340/7773340-hd_1280_720_30fps.mp4", 10, 0),      # handcuffs
    (462.8, "8061659/8061659-hd_1920_1080_25fps.mp4", 22, 0),     # Lady Justice
    (474.9, "8316467/8316467-hd_1920_1080_30fps.mp4", 13, 0),     # burning charcoal
    (485.4, "6101367/6101367-hd_1366_720_30fps.mp4", 11, 0),      # gavel
    (495.4, "2618443/2618443-hd_1280_720_24fps.mp4", 11, 0),      # weathered door & lock
    (505.5, "6581271/6581271-hd_1920_1080_24fps.mp4", 15, 0),     # police line
    (515.9, "12260947/12260947-hd_1920_1080_25fps.mp4", 41, 28),  # storage units aerial
    (527.0, "6326929/6326929-hd_1366_720_25fps.mp4", 21, 0),      # cash
    (537.0, "8060389/8060389-hd_1366_720_25fps.mp4", 18, 0),      # phone ringing
    (547.2, "7685212/7685212-hd_1280_720_24fps.mp4", 25, 12),     # paperwork
    (557.2, "5555354/5555354-hd_1920_1080_24fps.mp4", 20, 0),     # candles
    (567.4, "4889026/4889026-hd_1280_720_24fps.mp4", 13, 0),      # padlock
    (577.5, "5930874/5930874-hd_1280_720_24fps.mp4", 25, 0),      # rain & lightning
    (587.5, "36447967/15455385_640_360_60fps.mp4", 11, 0),        # river
    (597.9, "8846989/8846989-hd_1280_720_30fps.mp4", 13, 0),      # locked door
    (608.5, "4941466/4941466-hd_1920_1080_25fps.mp4", 18, 0),     # storage bins
    (618.8, "12374854/12374854-hd_1920_1080_60fps.mp4", 27, 10),  # parking lot at night
    (628.9, "5555356/5555356-hd_1280_720_24fps.mp4", 20, 0),      # lighting a candle
]
SEG_STARTS = [0.0, 217.2, 433.1]

out = []
for i, (start, path, avail, trim) in enumerate(shots):
    end = shots[i + 1][0] if i + 1 < len(shots) else TOTAL
    dur = round(end - start, 2)
    room = avail - trim - SAFETY
    if dur > room:
        print(f"WARN shot@{start}: needs {dur}s, clip has {room:.1f}s")
    out.append({"start": start, "dur": dur, "src": P + path, "trim": trim})

segments = []
for s, seg_start in enumerate(SEG_STARTS):
    seg_end = SEG_STARTS[s + 1] if s + 1 < len(SEG_STARTS) else TOTAL
    scenes = [o for o in out if seg_start <= o["start"] < seg_end]
    total = round(sum(o["dur"] for o in scenes), 2)
    print(f"segment {s+1}: {len(scenes)} scenes, {total}s (vo {seg_start}-{seg_end})")
    segments.append({"voiceover_trim": seg_start, "duration": total, "scenes": scenes})

with open("production/storage-unit-segments.json", "w") as f:
    json.dump(segments, f, indent=1)
