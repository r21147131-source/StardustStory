import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG10: rows of Meroitic-style characters on dark stone. Known royal names light
// fully in gold; the long unreadable sentences glow faintly then go dark.
// We use simple abstract glyph marks (never an invented transliteration).
const ROW_COUNT = 5;
const GLYPHS_PER_ROW = 14;
const KNOWN_ROWS = [1, 3]; // rows that carry a "known royal name" segment

function pseudoGlyphPath(seed: number): string {
  const variants = ["M0,0 L10,0 L10,14 L0,14 Z", "M5,0 L10,10 L0,10 Z", "M0,2 A6,6 0 1 1 11,2 A6,6 0 1 1 0,2 Z", "M0,0 L10,14 M10,0 L0,14"];
  return variants[seed % variants.length];
}

export const EP4_B106_MeroiticScript: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const rowH = 90;
  const startY = height / 2 - (ROW_COUNT * rowH) / 2;
  const startX = width * 0.18;
  const glyphGap = (width * 0.64) / GLYPHS_PER_ROW;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {Array.from({ length: ROW_COUNT }).map((_, row) => {
          const rowY = startY + row * rowH;
          const isKnown = KNOWN_ROWS.includes(row);
          return (
            <g key={row}>
              {Array.from({ length: GLYPHS_PER_ROW }).map((_, col) => {
                const seed = row * 7 + col;
                const glyphDelay = fps * (0.3 + (row * GLYPHS_PER_ROW + col) * 0.025);
                const glyphIn = interpolate(frame, [glyphDelay, glyphDelay + fps * 0.3], [0, 1], {
                  extrapolateLeft: "clamp",
                  extrapolateRight: "clamp",
                });
                // the "known royal name" segment sits in the middle 4 glyphs of its row
                const inKnownSegment = isKnown && col >= 5 && col < 9;
                const finalOpacity = inKnownSegment ? glyphIn : glyphIn * 0.35;
                const color = inKnownSegment ? themeEp4.colors.goldLight : themeEp4.colors.goldDim;
                return (
                  <path
                    key={col}
                    d={pseudoGlyphPath(seed)}
                    transform={`translate(${startX + col * glyphGap}, ${rowY})`}
                    fill={inKnownSegment ? color : "none"}
                    stroke={color}
                    strokeWidth={1.5}
                    opacity={finalOpacity}
                  />
                );
              })}
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
