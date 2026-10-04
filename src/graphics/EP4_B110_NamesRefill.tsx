import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { CARTOUCHE_GRID, KING_NAMES } from "./ep4-cartouche-data";

// MG6 reversed: hollow ovals fill in gold, reading PIYE, TAHARQA, TANTAMANI, AMANIRENAS.
const NAME_CELLS = [1, 2, 3, 4]; // central-ish cells to carry the four names

export const EP4_B110_NamesRefill: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {CARTOUCHE_GRID.map((c, i) => {
          const nameIdx = NAME_CELLS.indexOf(i);
          const fillStart = fps * (0.3 + Math.max(0, nameIdx) * 0.9);
          const filled = interpolate(frame, [fillStart, fillStart + fps * 0.6], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <g key={i}>
              <rect
                x={c.x}
                y={c.y}
                width={c.w}
                height={c.h}
                rx={c.w / 2}
                fill="none"
                stroke={themeEp4.colors.goldDim}
                strokeWidth={3}
              />
              {nameIdx >= 0 && (
                <rect
                  x={c.x}
                  y={c.y}
                  width={c.w}
                  height={c.h}
                  rx={c.w / 2}
                  fill={themeEp4.colors.gold}
                  fillOpacity={filled * 0.9}
                />
              )}
            </g>
          );
        })}
      </svg>

      {NAME_CELLS.map((cellIdx, i) => {
        const c = CARTOUCHE_GRID[cellIdx];
        const fillStart = fps * (0.3 + i * 0.9);
        const textOpacity = interpolate(frame, [fillStart + fps * 0.3, fillStart + fps * 0.7], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={cellIdx}
            style={{
              position: "absolute",
              left: c.x - 20,
              top: c.y + c.h / 2 - 10,
              width: c.w + 40,
              textAlign: "center",
              transform: "rotate(-90deg)",
              fontFamily: themeEp4.font.display,
              fontSize: 15,
              letterSpacing: 2,
              color: themeEp4.colors.bg,
              fontWeight: 700,
              opacity: textOpacity,
            }}
          >
            {KING_NAMES[i]}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
