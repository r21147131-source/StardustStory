import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

const CROWN_PATH = "M -24,12 L -24,-4 L -12,8 L 0,-14 L 12,8 L 24,-4 L 24,12 Z";

// MG10 phase 3: a single gold crown icon on black shatters into a dozen
// smaller crown icons that scatter outward and settle, each still faintly
// glowing gold.
export const EP5_B065_CrownShatters: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const cx = width / 2;
  const cy = height / 2 - 40;

  const bigOpacity = interpolate(frame, [fps * 0.2, fps * 0.8, fps * 2.4, fps * 3], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const scatterT = interpolate(frame, [fps * 2.6, fps * 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const settleGlow = interpolate(frame, [fps * 5, fps * 6.5], [0.4, 0.75], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const shards = Array.from({ length: 12 }).map((_, i) => {
    const angle = (i / 12) * Math.PI * 2 + 0.2;
    const dist = 260 + (i % 3) * 60;
    return { x: cx + Math.cos(angle) * dist, y: cy + Math.sin(angle) * dist * 0.62, scale: 0.4 + (i % 3) * 0.08, rot: (i * 37) % 360 };
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <g transform={`translate(${cx},${cy}) scale(2.2)`} opacity={bigOpacity}>
          <path d={CROWN_PATH} fill={themeEp5.colors.goldLight} />
        </g>

        {shards.map((s, i) => {
          const x = cx + (s.x - cx) * scatterT;
          const y = cy + (s.y - cy) * scatterT;
          const op = interpolate(scatterT, [0, 0.15, 1], [0, 1, 1]);
          return (
            <g key={i} transform={`translate(${x},${y}) scale(${s.scale}) rotate(${s.rot * scatterT})`} opacity={op}>
              <path d={CROWN_PATH} fill={themeEp5.colors.gold} opacity={settleGlow} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
