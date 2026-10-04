import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { CARTOUCHE_GRID } from "./ep4-cartouche-data";

// MG6 short repeat: a handful of cartouches erase (the wall starts already mostly hollow).
export const EP4_B103_ErasureRepeat: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {CARTOUCHE_GRID.map((c, i) => {
          const isLastFew = i >= CARTOUCHE_GRID.length - 4;
          if (!isLastFew) {
            return (
              <rect
                key={i}
                x={c.x}
                y={c.y}
                width={c.w}
                height={c.h}
                rx={c.w / 2}
                fill="none"
                stroke={themeEp4.colors.goldDim}
                strokeWidth={3}
              />
            );
          }
          const idx = i - (CARTOUCHE_GRID.length - 4);
          const eraseStart = fps * (0.2 + idx * 0.4);
          const erased = interpolate(frame, [eraseStart, eraseStart + fps * 0.3], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <rect
              key={i}
              x={c.x}
              y={c.y}
              width={c.w}
              height={c.h}
              rx={c.w / 2}
              fill={themeEp4.colors.gold}
              fillOpacity={1 - erased}
              stroke={themeEp4.colors.goldDim}
              strokeWidth={3}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
