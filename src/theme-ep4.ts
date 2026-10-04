export const themeEp4 = {
  colors: {
    bg: "#0A0908",
    bgAlt: "#13110C",
    stone: "#1A1812",
    stoneLight: "#221F16",
    gold: "#C9A84C",
    goldLight: "#E8C97A",
    goldDim: "#8B7235",
    ember: "#C45A20",
    emberDim: "#7A3615",
    cream: "#F0E8D0",
    text: "#F0E8D0",
    textDim: "#B8AD95",
    textFaint: "#8A8070",
    line: "rgba(201,168,76,0.2)",
    kushRegion: "#C45A20",
    egyptRegion: "#C9A84C",
    assyriaRegion: "#7A2E2E",
    romeRegion: "#5A5A8B",
  },
  font: {
    display: '"Cinzel", "Georgia", serif',
    body: '"Crimson Text", Georgia, serif',
    mono: '"Courier New", monospace',
  },
} as const;

export const EASE_EP4 = {
  standard: [0.22, 1, 0.36, 1] as [number, number, number, number],
};
