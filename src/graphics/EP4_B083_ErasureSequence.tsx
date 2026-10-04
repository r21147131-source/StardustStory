import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { CARTOUCHE_GRID } from "./ep4-cartouche-data";

// MG6 erasure: a wall of golden cartouches vanish one by one, leaving hollow ovals.
export const EP4_B083_ErasureSequence: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const wallOpacity = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }} opacity={wallOpacity}>
        {CARTOUCHE_GRID.map((c, i) => {
          const eraseStart = fps * (0.6 + i * 0.1);
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
              strokeWidth={erased > 0 ? 3 : 0}
              strokeOpacity={erased}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
