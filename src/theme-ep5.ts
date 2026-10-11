export const themeEp5 = {
  colors: {
    bg: "#15110D",
    bgAlt: "#1C1712",
    stone: "#241D15",
    stoneLight: "#2D2419",
    crimson: "#7A2634",
    crimsonDim: "#4A1620",
    crimsonLight: "#A33B4B",
    bronze: "#B08D57",
    bronzeDim: "#7A6239",
    gold: "#D9BF8C",
    goldLight: "#EDDCB8",
    parchment: "#E8E1D3",
    text: "#E8E1D3",
    textDim: "#B5AB98",
    textFaint: "#857B6A",
    line: "rgba(176,141,87,0.22)",
    westRegion: "#7A2634",
    eastRegion: "#B08D57",
    sea: "#0F0C09",
  },
  font: {
    display: '"Cinzel", "Georgia", serif',
    body: '"Crimson Text", Georgia, serif',
    mono: '"Courier New", monospace',
  },
} as const;

export const EASE_EP5 = {
  standard: [0.22, 1, 0.36, 1] as [number, number, number, number],
};
