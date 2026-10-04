// Shared schematic Nile-valley coordinates for Pantheon Ep.4 motion graphics.
// Canvas is 1920x1080. North (Delta/Mediterranean) is up, south (Kush) is down.

export type CityKey =
  | "sais"
  | "memphis"
  | "herakleopolis"
  | "hermopolis"
  | "thebes"
  | "napata"
  | "jebelBarkal"
  | "meroe";

export const CITY_POS: Record<CityKey, { x: number; y: number; label: string }> = {
  sais: { x: 740, y: 150, label: "Sais" },
  memphis: { x: 810, y: 270, label: "Memphis" },
  herakleopolis: { x: 845, y: 375, label: "Herakleopolis" },
  hermopolis: { x: 870, y: 460, label: "Hermopolis" },
  thebes: { x: 925, y: 630, label: "Thebes" },
  napata: { x: 985, y: 820, label: "Napata" },
  jebelBarkal: { x: 955, y: 845, label: "Jebel Barkal" },
  meroe: { x: 1045, y: 985, label: "Meroe" },
};

// A gently curving river path through the cities, top to bottom.
export const RIVER_PATH =
  "M 700,60 C 720,110 735,130 740,150 " +
  "C 760,200 800,230 810,270 " +
  "C 825,310 835,345 845,375 " +
  "C 855,405 865,430 870,460 " +
  "C 885,520 905,570 925,630 " +
  "C 945,690 965,760 985,820 " +
  "C 1000,860 1020,920 1045,985 " +
  "C 1060,1020 1070,1040 1075,1050";

export const EGYPT_BAND_Y = [40, 700] as const; // Delta through Upper Egypt
export const KUSH_BAND_Y = [700, 1060] as const; // Napata through Meroe
export const BORDER_Y = 700; // roughly the First Cataract / traditional Egypt-Kush line
