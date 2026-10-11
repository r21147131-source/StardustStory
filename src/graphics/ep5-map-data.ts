// Real-geography Mediterranean-world map for Pantheon Ep.5 motion graphics.
//
// Background is a real map (Wikimedia Commons "Roman-empire-395AD.svg" by
// AKIKA3D, CC BY-SA 4.0 — the actual political boundary map of the Western
// and Eastern Roman Empires after the death of Theodosius I), rasterized and
// recolored to the Pantheon Ep.5 crimson/bronze-gold palette (west =
// crimson, east = bronze-gold, sea/non-Roman land = transparent over the
// dark background, borders = faded gold). City positions below are
// pixel-calibrated against that same real map image, not an invented
// schematic.
//
// Canvas is 1920x1080. The map image sits at MAP_BOX within the canvas; all
// coordinates below are already in canvas space.

export const MAP_IMAGE = "pantheon-ep5-assets/roman-empire-map.png";

// The map image is 1584x1000 natively; displayed at this box.
export const MAP_BOX = { x: 168, y: 40, width: 1584, height: 1000 } as const;

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

// Positions pixel-calibrated against the real map image (see grid overlay
// used during sourcing): London, Trier, Milan, Rome, Ravenna, the Danube
// frontier near Carnuntum, Adrianople, Constantinople, Thessalonica,
// Antioch, Carthage, and Seville.
export const CITY_POS: Record<CityKey, { x: number; y: number; label: string }> = {
  londinium: { x: 620, y: 268, label: "Londinium" },
  treveri: { x: 722, y: 382, label: "Treveri" },
  hispalis: { x: 388, y: 749, label: "Hispalis" },
  mediolanum: { x: 861, y: 554, label: "Mediolanum" },
  roma: { x: 902, y: 708, label: "Roma" },
  ravenna: { x: 926, y: 611, label: "Ravenna" },
  carnuntum: { x: 999, y: 513, label: "Carnuntum" },
  adrianopolis: { x: 1179, y: 659, label: "Adrianopolis" },
  constantinopolis: { x: 1268, y: 635, label: "Constantinopolis" },
  thessalonica: { x: 1105, y: 749, label: "Thessalonica" },
  antiochia: { x: 1619, y: 774, label: "Antiochia" },
  carthago: { x: 804, y: 871, label: "Carthago" },
};

// Simplified road network for MG1 (Roads and Rule): Londinium through Gaul,
// down to Roma, across to Constantinopolis, out to Antiochia on the
// Euphrates frontier. Waypoints follow the real city positions above.
export const ROAD_PATH =
  "M 620,268 C 670,310 700,350 722,382 " +
  "C 790,440 840,490 861,554 " +
  "C 880,600 895,655 902,708 " +
  "M 902,708 C 970,660 1040,620 1105,600 " +
  "C 1150,590 1210,610 1268,635 " +
  "C 1380,670 1500,700 1619,774";

// The Danube frontier (MG3): a west-east river line separating Roman Italy/
// the Balkans from the free Gothic lands beyond, running north of
// Mediolanum/Carnuntum.
export const DANUBE_PATH =
  "M 830,490 C 890,480 950,490 999,513 C 1050,535 1100,545 1179,570";

// March routes toward Rome (MG5): three failed loops through the Balkans/
// Greece, then one final unbroken line into Italy. Anchored near
// Thessalonica/Adrianopolis, converging on Roma.
export const MARCH_LOOP_1 =
  "M 1000,560 C 1060,600 1090,660 1060,720 C 1030,770 1070,800 1105,820";
export const MARCH_LOOP_2 =
  "M 1105,820 C 1060,840 1010,800 1000,750 C 990,700 1030,650 970,610";
export const MARCH_LOOP_3 =
  "M 970,610 C 930,650 940,710 980,740 C 1020,765 1060,790 1040,830";
export const MARCH_FINAL =
  "M 1040,830 C 980,850 920,810 890,760 C 870,720 880,670 890,620 C 895,660 900,680 902,708";
