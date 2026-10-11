// Shared stylized "flat ink-and-gold" Mediterranean-world map for Pantheon
// Ep.5 motion graphics (MG1, MG2, MG3, MG5, MG9, MG10). Canvas is 1920x1080.
//
// This is a deliberately simplified schoolbook-style schematic — suggestive
// coastlines and proportionate west-to-east placement (Britannia down to the
// Euphrates frontier, North Africa along the south), not a traced geographic
// map. That matches the brief's own description of MG1 as "a flat
// ink-and-gold map," the same simplified-campaign-map idiom used in print
// histories of the period.

export const SEA_COLOR = "#0F0C09";

// Northern landmasses (Britannia, Gaul, Hispania, Italia, the Balkans/Greece,
// Asia Minor, Syria) as simplified coastline polygons.
export const REGION_BRITANNIA =
  "M 230,150 L 300,140 L 340,175 L 330,230 L 360,270 L 320,320 L 270,300 L 240,250 L 210,200 Z";

export const REGION_GAUL_HISPANIA =
  "M 130,560 L 160,480 L 230,430 L 280,350 L 360,300 L 440,290 L 500,330 " +
  "L 560,310 L 630,350 L 650,420 L 600,470 L 560,500 L 540,560 L 480,610 " +
  "L 420,660 L 350,700 L 260,720 L 180,680 L 140,620 Z";

export const REGION_ITALIA =
  "M 640,420 L 700,410 L 730,460 L 715,540 L 740,600 L 720,660 L 745,710 " +
  "L 760,760 L 740,800 L 710,790 L 700,730 L 680,670 L 660,610 L 650,540 " +
  "L 630,480 Z";

export const REGION_SICILIA =
  "M 700,815 L 740,808 L 760,830 L 735,850 L 700,845 Z";

export const REGION_BALKANS_GREECE =
  "M 780,440 L 870,420 L 950,440 L 1000,490 L 980,540 L 1010,580 L 990,630 " +
  "L 950,670 L 920,730 L 890,780 L 860,760 L 870,700 L 840,650 L 800,600 " +
  "L 790,540 L 760,490 Z";

export const REGION_ASIA_MINOR =
  "M 1020,480 L 1120,460 L 1230,470 L 1340,490 L 1400,530 L 1380,580 " +
  "L 1300,600 L 1200,590 L 1100,570 L 1030,540 Z";

export const REGION_SYRIA_LEVANT =
  "M 1400,540 L 1480,530 L 1550,560 L 1580,620 L 1550,680 L 1490,690 " +
  "L 1440,650 L 1410,590 Z";

// North Africa coastal strip (Mauretania -> Numidia -> Africa Proconsularis
// (Carthage) -> Cyrenaica -> Aegyptus), a long simplified east-west band.
export const REGION_NORTH_AFRICA =
  "M 160,760 L 300,730 L 420,740 L 540,760 L 650,750 L 760,770 L 880,790 " +
  "L 1000,800 L 1120,810 L 1260,820 L 1400,830 L 1520,850 L 1540,900 " +
  "L 1400,890 L 1260,880 L 1120,870 L 1000,860 L 880,850 L 760,840 " +
  "L 650,830 L 540,820 L 420,810 L 300,800 L 160,810 Z";

export type CityKey =
  | "londinium"
  | "treveri"
  | "mediolanum"
  | "roma"
  | "ravenna"
  | "carnuntum"
  | "adrianopolis"
  | "constantinopolis"
  | "thessalonica"
  | "antiochia"
  | "carthago"
  | "hispalis";

export const CITY_POS: Record<CityKey, { x: number; y: number; label: string }> = {
  londinium: { x: 290, y: 230, label: "Londinium" },
  treveri: { x: 470, y: 340, label: "Treveri" },
  hispalis: { x: 210, y: 630, label: "Hispalis" },
  mediolanum: { x: 670, y: 460, label: "Mediolanum" },
  roma: { x: 700, y: 650, label: "Roma" },
  ravenna: { x: 715, y: 560, label: "Ravenna" },
  carnuntum: { x: 820, y: 460, label: "Carnuntum" },
  adrianopolis: { x: 960, y: 560, label: "Adrianopolis" },
  constantinopolis: { x: 1040, y: 540, label: "Constantinopolis" },
  thessalonica: { x: 900, y: 580, label: "Thessalonica" },
  antiochia: { x: 1500, y: 610, label: "Antiochia" },
  carthago: { x: 650, y: 790, label: "Carthago" },
};

// Simplified road network for MG1 (Roads and Rule): Londinium through Gaul,
// down to Roma, across to Constantinopolis, out to Antiochia on the
// Euphrates frontier.
export const ROAD_PATH =
  "M 290,230 C 350,270 420,300 470,340 " +
  "C 540,390 610,430 670,460 " +
  "C 690,520 700,580 700,650 " +
  "M 700,650 C 760,600 830,570 900,560 " +
  "C 960,555 1000,545 1040,540 " +
  "C 1150,560 1280,570 1400,570 " +
  "C 1450,580 1480,595 1500,610";

// The Danube frontier (MG3): a west-east river line separating Roman Italy/
// the Balkans from the free Gothic lands beyond.
export const DANUBE_PATH =
  "M 660,420 C 740,400 800,410 850,430 C 910,450 960,460 1020,480";

// March routes toward Rome (MG5): three failed loops through the Balkans/
// Greece, then one final unbroken line into Italy.
export const MARCH_LOOP_1 =
  "M 820,460 C 870,500 900,560 880,620 C 860,670 900,700 940,720";
export const MARCH_LOOP_2 =
  "M 940,720 C 900,740 860,710 850,660 C 840,610 870,560 820,520";
export const MARCH_LOOP_3 =
  "M 820,520 C 790,560 800,620 840,650 C 870,675 900,700 890,740";
export const MARCH_FINAL =
  "M 890,740 C 840,760 780,730 750,690 C 720,650 715,600 710,560 C 705,610 700,630 700,650";
