"""Keanu Reeves episode — edit decision list (times from the Descript transcript of the merged 9:03 narration).

Run with:  PROJECT=keanu python3 production/build_stardust.py all
Plates: tmdb:<key>:<file> (keanu portraits p*, film stills b*/post*), foot:<src,...> (trailer footage),
        place:/chapter:/quote:/end/trailer: typographic cards.
"""
def t(s):
    if isinstance(s, (int, float)): return float(s)
    m, sec = s.split(":"); return int(m) * 60 + float(sec)

PROJECT_NAME = "keanu"
TMDB_ROOT = "footage/tmdb_keanu"
CLIPS_DIR = "footage/clips_keanu"
NARR_FILES = ["footage/keanu/keanu_narration.wav"]
NARRATION_END = 543.262
TAIL = 30.0                       # next-episode trailer after the narration (placeholder title)
T_END = NARRATION_END + TAIL
SERIES_TAG = ("STARDUST STORY", "KEANU REEVES")
SERIES_TAG_UNTIL = 12.0
CHAPTER_LEN = 1.3
OUT_DIR = "output/keanu"
OUT_BASENAME = "keanu-reeves-stardust-story"
NEXT_TITLE = "NEW STARDUST STORY"          # swap when the next episode title is chosen

def T(k, n): return f"tmdb:{k}:{n}"
KP = [T("keanu", f"p{i}") for i in range(10)]
MATRIX = [T("matrix", f"b{i}") for i in (3, 5, 7, 4, 6, 2)]
RELOADED = [T("reloaded", f"b{i}") for i in (2, 4, 6, 7, 5)]
WICK = [T("wick", f"b{i}") for i in (1, 3, 6, 5, 2)]
SPEED = [T("speed", f"b{i}") for i in (0, 4, 6, 5, 7)]
PB = [T("pointbreak", f"b{i}") for i in (2, 3, 6, 5, 1)]
BT = [T("billted", f"b{i}") for i in (1, 0, 2)]
F_MATRIX, F_WICK, F_SPEED, F_PB, F_BT = ("foot:matrix", "foot:wick", "foot:speed", "foot:pointbreak", "foot:billted")
F_ANY = "foot:matrix,wick,speed,pointbreak"
F_INT = "foot:interview"
FALLBACK = {"matrix": MATRIX, "wick": WICK, "speed": SPEED, "pointbreak": PB, "billted": BT, "reloaded": RELOADED}

SEGS = []
def seg(start, plates, label=None, nosplit=False, dissolve=False, kb=None, flash=False, dur_override=None):
    SEGS.append(dict(t0=t(start), plates=plates, label=label, nosplit=nosplit,
                     dissolve=dissolve, kb=kb, flash=flash, dur=dur_override))
def name(a, b=""): return ("name", a, b)
def title(a, b=""): return ("title", a, b)
def stat(a, b=""): return ("stat", a, b)

# ---- HOOK 0:00-0:22 -----------------------------------------------------------------------
seg(0.0, [F_MATRIX, F_WICK, KP[1]], name("KEANU REEVES", "ACTOR"))          # "stood on the biggest stages"
seg("0:03.68", [F_WICK, F_MATRIX, F_SPEED])                                            # "face of billion-dollar franchises"
seg("0:07.67", [KP[2], KP[3]], dissolve=True)                                          # "refused to put his name on"
seg("0:13.80", [T("matrix", "b2"), KP[4], KP[5]], dissolve=True)                       # hospital wards for sick children
seg("0:17.60", [KP[6]], nosplit=True, kb="in")                                         # "never see his name on the wall"
# ---- THE BOY 0:22-1:16 ----------------------------------------------------------------------
seg("0:22.50", [F_WICK, F_MATRIX])                                                      # "before the money, before the leather coat"
seg("0:26.20", [F_WICK], title("JOHN WICK", "2014"), nosplit=True)                       # "...John Wick"
seg("0:30.90", ["place:TORONTO, CANADA|WHERE HE LEARNED INSTABILITY|43.6532° N  79.3832° W"], nosplit=True)
seg("0:33.90", [KP[7], KP[8], KP[7]], dissolve=True)                                   # moving between countries
seg("0:40.20", [KP[9], KP[8]], dissolve=True)                                          # father absent, mother
seg("0:47.00", [KP[3], KP[1]], dissolve=True)                                          # learned to read people
seg("0:53.50", [KP[7]], nosplit=True, kb="in")                                         # close to his sisters
# ---- THE WOUND 1:02-2:34 ---------------------------------------------------------------------
seg("1:02.99", [F_PB, F_BT, F_SPEED])                                                   # late 80s / early 90s: rising name
seg("1:07.14", [F_BT], title("BILL & TED'S EXCELLENT ADVENTURE", "1989"), nosplit=True)
seg("1:08.30", [F_PB], title("POINT BREAK", "1991"), nosplit=True)
seg("1:09.60", [F_SPEED], title("SPEED", "1994"), nosplit=True)
seg("1:11.52", [F_ANY, F_INT, KP[2]])
seg("1:16.49", [KP[6]], nosplit=True, kb="in")                                          # "something happened that had nothing to do with a camera"
seg("1:20.29", [KP[5], KP[4]], stat("1991", "HIS SISTER KIM IS DIAGNOSED WITH LEUKEMIA"))
seg("1:25.09", [KP[4]], nosplit=True, kb="in")
seg("1:26.52", [KP[2], KP[3], KP[9]], dissolve=True)
seg("1:35.86", [KP[1]], nosplit=True, kb="in")                                          # "Reeves did something... He stayed."
seg("1:40.77", [KP[7], KP[8], KP[4]], dissolve=True)
seg("1:52.55", [KP[3], KP[5]], dissolve=True)
seg("2:03.69", [KP[9], KP[2]], dissolve=True)
seg("2:14.10", [KP[6]], nosplit=True, kb="in")                                          # "Kim survived."
seg("2:18.18", [KP[7], KP[1], KP[0]], dissolve=True)
# ---- THE MATRIX MONEY 2:34-4:42 ---------------------------------------------------------------
seg("2:34.27", [F_MATRIX], title("THE MATRIX", "1999"), nosplit=True)
seg("2:37.80", [F_MATRIX, MATRIX[0], F_MATRIX])
seg("2:44.80", [F_MATRIX, MATRIX[1]])
seg("2:50.56", [MATRIX[2], F_MATRIX], stat("70%", "OF HIS MATRIX EARNINGS — A WIDELY REPEATED CLAIM"), flash=True)
seg("3:04.00", [MATRIX[3]], stat("$31 MILLION", "THE FIGURE OFTEN QUOTED — UNVERIFIED"), nosplit=True)
seg("3:10.45", [F_MATRIX, MATRIX[4], F_MATRIX])
seg("3:14.90", [KP[2], KP[0]], title("ONE MEDIA REPORT", "NO FILING, NO FOUNDATION RECORD"), dissolve=True)
seg("3:21.50", ["quote:WE TELL YOU IT EXISTS.\nWE TELL YOU WHY TO BE SKEPTICAL.||"], nosplit=True)
seg("3:30.50", [MATRIX[5], F_MATRIX, MATRIX[0]])
seg("3:43.45", [KP[3]], nosplit=True, kb="in")                                          # "Because it fits."
seg("3:50.70", [T("reloaded", "b0"), F_MATRIX], title("THE MATRIX RELOADED", "2003"), nosplit=False)
seg("3:56.00", [RELOADED[0], RELOADED[1], F_MATRIX])
seg("4:10.74", [RELOADED[2], RELOADED[3]], stat("MOTORCYCLES", "REPORTEDLY GIFTED TO HIS STUNT TEAM"))
seg("4:16.80", [RELOADED[4], F_MATRIX, RELOADED[0]])
seg("4:23.65", [KP[2], KP[6]], dissolve=True)
seg("4:32.74", [KP[1]], nosplit=True, kb="in")
# ---- MID-ROLL CALLBACK CARD + THE CONFESSION 4:42-6:12 ------------------------------------------
seg("4:42.38", ["quote:IF YOU SAW OUR LAST EPISODE,\nYOU KNOW FAME USUALLY CHANGES\nA PERSON'S APPETITE FOR CREDIT.\nKEANU WENT THE OPPOSITE DIRECTION.|STARDUST STORY|"], nosplit=True, dur_override=5.0)
seg("4:47.50", [KP[4], KP[2]], dissolve=True)
seg("4:49.40", [KP[6]], stat("2009", "LADIES' HOME JOURNAL"), nosplit=True, flash=True)
seg("4:53.60", [KP[5], KP[1]], dissolve=True)
seg("4:58.80", [KP[7]], nosplit=True, kb="in")
seg("5:09.37", [KP[0]], name("KEANU REEVES", "\"I DON'T LIKE TO ATTACH MY NAME TO IT\""), nosplit=True)
seg("5:14.62", [F_MATRIX], flash=True, nosplit=True)                                      # PATTERN INTERRUPT: "Sit with how unusual that is."
seg("5:18.00", [KP[3], KP[9]], dissolve=True)
seg("5:34.49", ["quote:NO BANNER.\nNO BRANDING.\nNO RED CARPET LAUNCH.||"], nosplit=True)
seg("5:41.01", [KP[4], KP[2]], dissolve=True)
seg("5:45.65", ["place:WHAT WE DO NOT KNOW|THE FOUNDATION'S NAME  ·  ITS TOTAL SIZE  ·  WHICH HOSPITALS|"], nosplit=True)
seg("5:56.00", [KP[5]], nosplit=True, kb="in")
seg("6:01.20", [KP[6], KP[8]], dissolve=True)
seg("6:06.23", [KP[1]], nosplit=True, kb="in")
# ---- 70% CTA 6:20.5 (on screen only; VO to be recorded) + THE HONEST COMPLICATION 6:13-7:24 ------
seg("6:13.60", [F_WICK, KP[9]], dissolve=False)
seg("6:20.50", [KP[0]], title("NEXT FRIDAY", NEXT_TITLE), nosplit=True)
seg("6:26.80", [KP[7]], stat("$19,000+", "ZOOM CALL AUCTION  →  CAMP RAINBOW GOLD"), nosplit=True, flash=True)
seg("6:35.98", [KP[2], KP[3]], dissolve=True)
seg("6:44.18", [KP[4]], stat("2008", "STAND UP TO CANCER TELETHON"), nosplit=True)
seg("6:52.32", [KP[5], F_INT, KP[1]])
seg("7:02.01", [KP[6], KP[8]], dissolve=True)
seg("7:15.40", [KP[0]], nosplit=True, kb="in")
# ---- WHY IT LANDS 7:24-8:14 ---------------------------------------------------------------------------
seg("7:24.60", [F_INT, KP[2], F_ANY])
seg("7:44.90", [KP[7], KP[3]], dissolve=True)
seg("7:56.90", ["place:A HOSPITAL CORRIDOR|1991|"], nosplit=True)
seg("8:00.50", [KP[9], KP[4]], dissolve=True)
seg("8:08.95", [KP[6]], nosplit=True, kb="in")
# ---- THE BLUEPRINT 8:14-8:40 ------------------------------------------------------------------------------
seg("8:14.62", ["chapter:BLUEPRINT|WHAT HE BUILT"], nosplit=True, dur_override=CHAPTER_LEN)
seg("8:17.08", [KP[0]], stat("ONE", "A PERSONAL WOUND  →  A PERMANENT MISSION"), nosplit=True)
seg("8:23.56", [KP[3]], stat("TWO", "THE CAUSE SEPARATED FROM THE CREDIT"), nosplit=True)
seg("8:31.03", [KP[5]], stat("THREE", "HIS NAME USED TACTICALLY, NOT CONSTANTLY"), nosplit=True)
seg("8:40.69", [F_ANY, KP[1]], dissolve=False)
seg("8:45.00", ["end"], nosplit=True, dur_override=4.2)
seg("8:49.20", [KP[0], KP[3], KP[6]], dissolve=True)
# ---- NEXT-EPISODE TRAILER (final 30 s, after the narration: 3 text lines + 2 shots; title is a placeholder) ----
_N = NARRATION_END + 0.2
seg(_N, [F_WICK, F_MATRIX], stat("NEXT FRIDAY", NEXT_TITLE), nosplit=True, flash=True, dur_override=9.0)
seg(_N + 9.0, [KP[2]], title("WHAT HAPPENS WHEN A STAR", "DOES THE EXACT OPPOSITE"), nosplit=True, dur_override=9.0)
seg(_N + 18.0, [F_ANY], nosplit=True, dur_override=5.5)
seg(_N + 23.5, ["trailer:NEXT FRIDAY|" + NEXT_TITLE], nosplit=True)

SFX_CHAPTERS = [s["t0"] for s in SEGS if s["plates"][0].startswith("chapter:")]
SFX_STATS = [s["t0"] for s in SEGS if s["label"] and s["label"][0] == "stat"]
SFX_QUOTES = [s["t0"] for s in SEGS if s["plates"][0].startswith("quote:")]
