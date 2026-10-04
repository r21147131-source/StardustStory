// Real-geography Nile-valley map for Pantheon Ep.4 motion graphics.
//
// Background is a real map (traced from a public-domain Nile basin map,
// Wikimedia Commons "River Nile map.svg" by Hel-hama, CC BY-SA 3.0),
// cropped to Egypt + Sudan down through Khartoum and recolored to the
// Pantheon gold/obsidian palette. City positions and the river path below
// are calibrated against that same real map (pixel-sampled river course
// and city-dot positions), not an invented schematic.
//
// Canvas is 1920x1080. North (Delta/Mediterranean) is up, south (Kush) is
// down. MAP_IMAGE sits at MAP_BOX within the canvas; all coordinates below
// are already in canvas space.

export const MAP_IMAGE = "pantheon-ep4-assets/nile-real-map.png";

// The themed map image is 720x1320 natively; displayed at this box.
export const MAP_BOX = { x: 620, y: 90, width: 491, height: 900 } as const;

export type CityKey =
  | "sais"
  | "memphis"
  | "herakleopolis"
  | "hermopolis"
  | "thebes"
  | "napata"
  | "jebelBarkal"
  | "meroe";

// Positions calibrated against the real map: pixel-sampled Cairo/Luxor/
// Aswan/Khartoum dot positions plus the real river's great-bend apex
// (4th Cataract / Napata region) and the Meroe stretch downstream of it.
export const CITY_POS: Record<CityKey, { x: number; y: number; label: string }> = {
  sais: { x: 783, y: 223, label: "Sais" },
  memphis: { x: 859, y: 274, label: "Memphis" },
  herakleopolis: { x: 874, y: 307, label: "Herakleopolis" },
  hermopolis: { x: 894, y: 350, label: "Hermopolis" },
  thebes: { x: 935, y: 442, label: "Thebes" },
  napata: { x: 870, y: 638, label: "Napata" },
  jebelBarkal: { x: 870, y: 638, label: "Jebel Barkal" },
  meroe: { x: 988, y: 796, label: "Meroe" },
};

// Real river course (Delta -> Memphis -> Thebes -> Aswan -> the great bend
// at the 4th Cataract -> Meroe -> Khartoum), built from the same
// pixel-sampled waypoints as CITY_POS via Catmull-Rom smoothing.
export const RIVER_PATH =
  "M 855,200 " +
  "C 855.7,212.3 855.8,256.2 859,274 " +
  "C 862.2,291.8 868.2,294.3 874,307 " +
  "C 879.8,319.7 883.8,327.5 894,350 " +
  "C 904.2,372.5 925.5,414.3 935,442 " +
  "C 944.5,469.7 961.8,483.3 951,516 " +
  "C 940.2,548.7 863.8,591.3 870,638 " +
  "C 876.2,684.7 972.3,763.2 988,796 " +
  "C 1003.7,828.8 968.0,828.5 964,835";

// Aswan / the traditional First Cataract border, pixel-sampled from the
// real map (where the Egypt-Kush political band split now lands).
export const BORDER_Y = 516;
export const EGYPT_BAND_Y = [MAP_BOX.y, BORDER_Y] as const;
export const KUSH_BAND_Y = [BORDER_Y, MAP_BOX.y + MAP_BOX.height] as const;
