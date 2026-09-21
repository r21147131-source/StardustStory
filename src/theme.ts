export const theme = {
  colors: {
    bg: "#10151c",
    bgAlt: "#161d26",
    ink: "#0a0d12",
    glacialBlue: "#6fb3d8",
    glacialBlueDim: "#3d6d8a",
    glacialBlueDark: "#24445a",
    ashGray: "#9aa0a8",
    ashGrayDim: "#565d66",
    ashGrayDark: "#2b3038",
    terracotta: "#c17a56",
    terracottaDim: "#8a4f34",
    terracottaDark: "#4a2a1c",
    ember: "#e0793f",
    text: "#f2efe9",
    textDim: "#b7b2a8",
    textFaint: "#736e66",
  },
  font: {
    display: '"Georgia", "Times New Roman", serif',
    body: '"Helvetica Neue", Arial, sans-serif',
    mono: '"Courier New", monospace',
  },
} as const;

export const EASE = {
  standard: [0.22, 1, 0.36, 1] as [number, number, number, number],
};
