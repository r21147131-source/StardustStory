"""Stardust Story (Deborah Ann Woll / Karen Page) — edit decision list.

Times come from the Descript SRT of the voiceover (running time across hook, act1-act5, end).
Each seg() starts at a time and runs until the next seg() begins. Plates are picture sources:
  tmdb:<title-or-person>:<file>   real TMDB image  (b* = backdrop still, p* = portrait, post* = poster)
  place:<NAME>|<sub>|<coords>     typographic location card
  chapter:<ROMAN>|<TITLE>         black chapter card
  quote:<TEXT>|<ATTRIBUTION>|<bg tmdb plate or ''>
  end                             closing card
Labels: ('name', line1, line2) ('title', line1, line2) ('stat', big, caption)
"""

def t(s):
    """'M:SS.s' or seconds -> float seconds"""
    if isinstance(s, (int, float)):
        return float(s)
    m, sec = s.split(":")
    return int(m) * 60 + float(sec)

NARRATION_END = 801.646   # sum of the seven mp3 durations
TAIL = 6.0
T_END = NARRATION_END + TAIL
SERIES_TAG = ("STARDUST STORY", "KAREN PAGE")
SERIES_TAG_UNTIL = 11.0
CHAPTER_LEN = 1.3

def T(k, n): return f"tmdb:{k}:{n}"
KP = [T("woll", f"p{i}") for i in range(6)]
DD = [T("daredevil", f"b{i}") for i in range(8)]
BA = [T("born_again", f"b{i}") for i in (0, 1, 5, 6, 4, 1, 5, 6)]   # b2/b3/b7 are duplicates of b0 key art
TB = [T("trueblood", f"b{i}") for i in range(8)]

SEGS = []
def seg(start, plates, label=None, nosplit=False, dissolve=False, kb=None, flash=False, dur_override=None):
    SEGS.append(dict(t0=t(start), plates=plates, label=label, nosplit=nosplit,
                     dissolve=dissolve, kb=kb, flash=flash, dur=dur_override))

def name(a, b=""): return ("name", a, b)
def title(a, b=""): return ("title", a, b)
def stat(a, b=""): return ("stat", a, b)

# ---- HOOK -------------------------------------------------------------
seg(0.0, [BA[0]])
seg("0:01.14", [BA[1], BA[2], BA[3]], title("DAREDEVIL: BORN AGAIN", "DISNEY+ · 2025"))
seg("0:09.84", [T("donofrio", "p0")], name("VINCENT D'ONOFRIO", "ACTOR · WILSON FISK"))
seg("0:11.92", [T("bethel", "p0")], name("WILSON BETHEL", "ACTOR · BENJAMIN POINDEXTER"))
seg("0:14.14", [T("bernthal", "p0")], name("JON BERNTHAL", "ACTOR · FRANK CASTLE"))
seg("0:16.47", [T("ritter", "p0"), T("ritter", "p1")], name("KRYSTEN RITTER", "ACTOR · JESSICA JONES"))
seg("0:20.53", [KP[0]], name("DEBORAH ANN WOLL", "ACTOR · KAREN PAGE"), nosplit=True, kb="in")
seg("0:22.54", [DD[0], KP[1], DD[1], DD[2], KP[2], BA[4], DD[3], KP[3]])
seg("0:51.59", [KP[4]], nosplit=True, kb="in", dissolve=False)

# ---- CHAPTER I : BROOKLYN ------------------------------------------------
seg("0:53.87", ["chapter:I|THE BROOKLYN KID"], nosplit=True, dur_override=CHAPTER_LEN)
seg("0:55.17", ["place:BROOKLYN, NEW YORK|BOROUGH OF KINGS COUNTY|40.6782° N  73.9442° W"], nosplit=True)
seg("0:57.95", ["place:BERKELEY CARROLL SCHOOL|PARK SLOPE, BROOKLYN|40.6720° N  73.9770° W"], nosplit=True)
seg("1:04.77", [KP[1], KP[2], KP[3]], dissolve=True)
seg("1:13.90", ["place:UNIVERSITY OF SOUTHERN CALIFORNIA|LOS ANGELES, CALIFORNIA|34.0224° N  118.2851° W"], nosplit=True)
seg("1:19.00", [KP[4]], nosplit=True)
seg("1:22.98", [KP[5]], nosplit=True)
seg("1:25.70", ["place:ROYAL ACADEMY OF DRAMATIC ARTS|LONDON, ENGLAND|51.5222° N  0.1318° W"], nosplit=True)
seg("1:31.25", [KP[0], KP[3]])

# ---- CHAPTER II : THE APPRENTICESHIP ---------------------------------------
seg("1:37.22", ["chapter:II|THE LONG APPRENTICESHIP"], nosplit=True, dur_override=CHAPTER_LEN)
seg("1:38.52", [KP[2], KP[4], KP[1]], dissolve=True)
seg("1:43.52", [KP[5]], stat("10", "YEARS OF WORK BEFORE TRUE BLOOD"), nosplit=True, flash=True)
seg("1:47.50", [KP[0], KP[2], KP[3], KP[4]])
seg("1:56.47", [KP[1]], nosplit=True)
seg("1:57.40", [T("life", "b0")], title("LIFE", "NBC · 2007"), nosplit=True)
seg("1:58.75", [T("er", "b0")], title("ER", "NBC · 1994"), nosplit=True)
seg("2:01.39", [T("csi", "b0")], title("CSI: CRIME SCENE INVESTIGATION", "CBS · 2000"), nosplit=True)
seg("2:03.17", [T("earl", "b0")], title("MY NAME IS EARL", "NBC · 2005"), nosplit=True)
seg("2:05.00", [T("mentalist", "b0")], title("THE MENTALIST", "CBS · 2008"), nosplit=True)
seg("2:07.16", [KP[0], KP[1]])
seg("2:09.50", ["place:BON TEMPS, LOUISIANA|THE FICTIONAL TOWN OF TRUE BLOOD|"], nosplit=True)
seg("2:13.50", [KP[2]], nosplit=True)

# ---- CHAPTER III : TRUE BLOOD ------------------------------------------------
seg("2:16.67", ["chapter:III|TRUE BLOOD"], nosplit=True, dur_override=CHAPTER_LEN)
seg("2:17.97", [TB[0], TB[1]], title("TRUE BLOOD", "HBO · 2008"))
seg("2:29.50", [T("paquin", "p0")], name("ANNA PAQUIN", "ACTOR · SOOKIE STACKHOUSE"), nosplit=True)
seg("2:35.62", [KP[0]], name("DEBORAH ANN WOLL", "ACTOR · JESSICA HAMBY"), nosplit=True)
seg("2:41.36", [TB[2], KP[1], TB[3], KP[2], TB[4]])
seg("3:09.39", [TB[5]], stat("7", "SEASONS"), nosplit=True, flash=True)
seg("3:11.88", [T("trueblood", "post0")], title("SATELLITE AWARD", "BEST CAST · TELEVISION SERIES"), nosplit=True)
seg("3:16.71", [TB[6]], title("SCREEN ACTORS GUILD AWARD", "NOMINATION"), nosplit=True)
seg("3:21.75", [TB[7], KP[3], TB[0]])
seg("3:32.51", [T("paquin", "p1")], name("ANNA PAQUIN", "ACTOR"), nosplit=True)
seg("3:35.58", [KP[2]], nosplit=True)
seg("3:37.12", [KP[4], KP[5]], dissolve=True)

# ---- CHAPTER IV : KAREN PAGE ----------------------------------------------------
seg("3:44.53", ["chapter:IV|KAREN PAGE"], nosplit=True, dur_override=CHAPTER_LEN)
seg("3:45.83", [DD[0]], stat("2014", "MARVEL & NETFLIX COME CALLING"), nosplit=True, flash=True)
seg("3:49.20", [DD[1]], title("DAREDEVIL", "NETFLIX · 2015"), nosplit=True)
seg("3:52.69", [DD[2], DD[3]])
seg("4:00.20", [DD[4]], stat("1999", "KAREN PAGE KILLED IN THE COMICS"), nosplit=True, flash=True)
seg("4:03.60", [DD[5], KP[2]])
seg("4:09.43", [KP[3], DD[6]])
seg("4:26.31", ["quote:\"IF SHE'S JUST GOING TO BE SOMEONE'S GIRLFRIEND, I DON'T WANT TO DO IT.\"|DEBORAH ANN WOLL · PANEL|" + KP[4]], nosplit=True)
seg("4:30.60", [DD[7], KP[0], DD[0], KP[1]])
seg("4:48.90", ["place:HELL'S KITCHEN|MANHATTAN, NEW YORK|40.7638° N  73.9918° W"], nosplit=True)
seg("4:53.33", [DD[2]], title("DAREDEVIL", "NETFLIX · SEASONS 1–3"), nosplit=True)
seg("4:56.85", [T("punisher", "b0")], title("THE PUNISHER", "NETFLIX · 2017"), nosplit=True)
seg("4:58.00", [T("defenders", "b0")], title("THE DEFENDERS", "NETFLIX · 2017"), nosplit=True)
seg("5:01.00", [KP[2], DD[3], KP[4], DD[5], KP[0], DD[6]])
seg("5:23.03", ["quote:\"YOU MIGHT NOT SEE THE KAREN PAGE STORY, BUT SHE'S HAVING A WHOLE TV SHOW ON HER OWN THAT NO ONE FILMED. MAKE SURE THAT WE JUST CONTINUE TO HONOR THAT THEY HAVE FULL LIVES.\"|DEBORAH ANN WOLL|" + KP[5]], nosplit=True)
seg("5:33.50", [KP[1]], nosplit=True)
seg("5:34.87", [DD[7]], stat("2019", "NETFLIX CANCELS EVERYTHING"), nosplit=True, flash=True)
seg("5:38.30", [KP[3], DD[0], KP[4]], dissolve=True)

# ---- CHAPTER V : THE QUIET YEARS ---------------------------------------------------
seg("5:43.97", ["chapter:V|THE QUIET YEARS"], nosplit=True, dur_override=CHAPTER_LEN)
seg("5:45.27", [KP[0], KP[1]], dissolve=True)
seg("5:47.42", [T("cox", "p0")], name("CHARLIE COX", "MATT MURDOCK"), nosplit=True)
seg("5:48.40", [T("donofrio", "p1")], name("VINCENT D'ONOFRIO", "WILSON FISK"), nosplit=True)
seg("5:49.40", [T("bernthal", "p1")], name("JON BERNTHAL", "FRANK CASTLE"), nosplit=True)
seg("5:50.40", [T("ritter", "p2")], name("KRYSTEN RITTER", "JESSICA JONES"), nosplit=True)
seg("5:52.06", [KP[2], KP[3]], dissolve=True)
seg("6:01.52", [KP[4]], nosplit=True)
seg("6:03.69", [KP[5]], stat("D&D", "DUNGEONS & DRAGONS"), nosplit=True)
seg("6:07.00", [KP[0], KP[1]])
seg("6:10.59", [T("critrole", "b0"), T("critrole", "b1")], title("CRITICAL ROLE", "ACTUAL PLAY WEB SERIES"))
seg("6:16.00", [T("mercer", "p0")], name("MATTHEW MERCER", "DUNGEON MASTER · CRITICAL ROLE"), nosplit=True)
seg("6:18.60", [T("critrole", "b2")], title("TWIGGY", "GUEST CHARACTER · GNOME ROGUE"), nosplit=True)
seg("6:22.92", [KP[2]], title("FORCE GREY: LOST CITY OF OMU", "DUNGEONS & DRAGONS"), nosplit=True)
seg("6:26.07", [KP[3], KP[4]])
seg("6:29.25", [T("critrole", "b3"), KP[5]])
seg("6:36.54", [KP[0], KP[1], KP[2]], dissolve=True)

# ---- escape room, God of War, Queen of the Ring -----------------------------------------
seg("6:54.69", [KP[3]], nosplit=True)
seg("6:57.80", [T("escape1", "b0")], title("ESCAPE ROOM", "2019"), nosplit=True)
seg("7:00.40", [T("escape2", "b1")], title("ESCAPE ROOM: TOURNAMENT OF CHAMPIONS", "2021"), nosplit=True)
seg("7:05.07", ["place:GOD OF WAR|VIDEO GAME · 2022 · FAYE|VOICE & MOTION CAPTURE"], nosplit=True)
seg("7:11.00", [KP[4], KP[5], KP[0]])
seg("7:23.68", [T("queen", "b0"), T("queen", "b1")], title("QUEEN OF THE RING", "2024"))
seg("7:29.00", ["place:E.J. SCOTT|HER HUSBAND · LIVING WITH CHOROIDEREMIA|"], nosplit=True)
seg("7:37.69", [KP[2]], nosplit=True)
seg("7:39.25", [KP[3], KP[4], KP[5]])
seg("7:58.32", [KP[0], KP[1], KP[2], KP[3]], dissolve=True)
seg("8:08.40", [KP[5]], nosplit=True, kb="in")

# ---- CHAPTER VI : BORN AGAIN -----------------------------------------------------------------
seg("8:12.24", ["chapter:VI|BORN AGAIN"], nosplit=True, dur_override=CHAPTER_LEN)
seg("8:13.54", [BA[3]], title("DAREDEVIL: BORN AGAIN", "DISNEY+ · 2025"), nosplit=True)
seg("8:20.77", [T("henson", "p0")], name("ELDEN HENSON", "ACTOR · FOGGY NELSON"), nosplit=True)
seg("8:23.79", [BA[4], BA[5]])
seg("8:35.00", [T("cox", "p1")], name("CHARLIE COX", "ACTOR · MATT MURDOCK"), nosplit=True)
seg("8:36.60", [T("donofrio", "p2")], name("VINCENT D'ONOFRIO", "ACTOR · WILSON FISK"), nosplit=True)
seg("8:41.68", [BA[6], DD[2]])
seg("8:46.20", [BA[7]], stat("SEPT 2023", "BORN AGAIN OVERHAULED MID-PRODUCTION"), nosplit=True, flash=True)
seg("8:51.18", [BA[0], BA[1]])
seg("8:57.40", [T("scardapane", "p0")], name("DARIO SCARDAPANE", "SHOWRUNNER · DAREDEVIL: BORN AGAIN"), nosplit=True)
seg("9:03.88", [T("scardapane", "p0")], nosplit=True)
seg("9:06.23", [KP[0]], nosplit=True)
seg("9:07.77", [KP[4]], nosplit=True, kb="in")
seg("9:14.00", [KP[1], KP[2], KP[3]], dissolve=True)
seg("9:44.10", [T("scardapane", "p0")], nosplit=True)
seg("9:50.00", [KP[5]], nosplit=True)
seg("9:55.88", [KP[0], KP[1], KP[2]], dissolve=True)
seg("10:05.50", [BA[2]])
seg("10:08.00", [BA[3]], stat("MARCH 2025", "BORN AGAIN · SEASON ONE"), nosplit=True, flash=True)
seg("10:12.50", [BA[4]], stat("3", "EPISODES FOR KAREN PAGE IN SEASON ONE"), nosplit=True)
seg("10:16.60", [BA[5], BA[6]])
seg("10:20.81", [T("henson", "p1")], name("ELDEN HENSON", "FOGGY NELSON"), nosplit=True)
seg("10:22.17", [T("cox", "p2")], name("CHARLIE COX", "MATT MURDOCK"), nosplit=True)
seg("10:24.61", [KP[1], KP[2], KP[3], KP[4]], dissolve=True)

# ---- CHAPTER VII : SEASON TWO ----------------------------------------------------------------------
seg("10:48.86", ["chapter:VII|SEASON TWO"], nosplit=True, dur_override=CHAPTER_LEN)
seg("10:50.20", [BA[5]], title("DAREDEVIL: BORN AGAIN", "DISNEY+ · SEASON TWO"), nosplit=True)
seg("10:54.50", [BA[6]], stat("2026", "SEASON TWO"), nosplit=True, flash=True)
seg("10:58.90", [KP[3], KP[4]])
seg("11:06.90", [T("scardapane", "p0")], name("DARIO SCARDAPANE", "SHOWRUNNER"), nosplit=True)
seg("11:10.50", ["place:HELL'S KITCHEN|MANHATTAN, NEW YORK|40.7638° N  73.9918° W"], nosplit=True)
seg("11:13.20", [BA[7], T("cox", "p0"), BA[0], KP[5], BA[1]])
seg("11:26.00", [BA[2]], stat("EPISODE 3", "KAREN KIDNAPS A FEDERAL AGENT"), nosplit=True, flash=True)
seg("11:30.00", [BA[3], BA[4]])
seg("11:36.99", ["quote:\"IN MY MIND AND IN DEBS'S MIND, SHE HAS NEVER BEEN A SIDEKICK. SHE HAS NEVER BEEN A GIRLFRIEND.\"|DARIO SCARDAPANE · SHOWRUNNER|" + T("scardapane", "p0")], nosplit=True)
seg("11:44.85", [KP[0], KP[1], KP[2]], dissolve=True)
seg("11:54.21", [DD[4]], nosplit=True)
seg("11:56.30", [DD[5]], stat("2014", "SHE SET HER TERMS"), nosplit=True, flash=True)
seg("11:58.11", [DD[6], KP[3]])
seg("12:04.02", [BA[4], KP[4]])
seg("12:12.82", [DD[7]], nosplit=True)
seg("12:15.50", [DD[0]], stat("1999", "DEAD IN THE COMICS"), nosplit=True, flash=True)
seg("12:20.16", [KP[5], BA[1], KP[0], BA[2]])

# ---- CHAPTER VIII : A FULL LIFE -----------------------------------------------------------------------------
seg("12:46.81", ["chapter:VIII|A FULL LIFE"], nosplit=True, dur_override=CHAPTER_LEN)
seg("12:48.11", [KP[1], KP[2], KP[3], KP[4]], dissolve=True)
seg("13:12.50", [KP[4]], stat("10 YEARS", "FIGHTING FOR A FICTIONAL WOMAN"), nosplit=True, flash=True)
seg("13:19.90", [KP[0]], nosplit=True, kb="in")
seg(NARRATION_END + 0.2, ["end"], nosplit=True)

SFX_CHAPTERS = [s["t0"] for s in SEGS if s["plates"][0].startswith("chapter:")]
SFX_STATS = [s["t0"] for s in SEGS if s["label"] and s["label"][0] == "stat"]
SFX_QUOTES = [s["t0"] for s in SEGS if s["plates"][0].startswith("quote:")]
