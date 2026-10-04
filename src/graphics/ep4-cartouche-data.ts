// Shared cartouche-wall grid for MG6 (title card / erasure / refill), Pantheon Ep.4.

export type Cartouche = { x: number; y: number; w: number; h: number };

export const CARTOUCHE_GRID: Cartouche[] = (() => {
  const cells: Cartouche[] = [];
  const cols = 6;
  const rows = 3;
  const w = 150;
  const h = 210;
  const gapX = 40;
  const gapY = 50;
  const totalW = cols * w + (cols - 1) * gapX;
  const totalH = rows * h + (rows - 1) * gapY;
  const startX = (1920 - totalW) / 2;
  const startY = (1080 - totalH) / 2;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      cells.push({
        x: startX + c * (w + gapX),
        y: startY + r * (h + gapY),
        w,
        h,
      });
    }
  }
  return cells;
})();

export const KING_NAMES = ["PIYE", "TAHARQA", "TANTAMANI", "AMANIRENAS"];
