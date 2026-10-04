import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, CITY_POS } from "./ep4-map-data";

// MG2 Phase 2: Memphis flips to Tefnakht's color; Herakleopolis is ringed by besiegers.
export const EP4_B027_MapMemphisHerakleopolis: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const memphis = CITY_POS.memphis;
  const herak = CITY_POS.herakleopolis;

  const memphisFlip = interpolate(frame, [fps * 0.4, fps * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ringProgress = interpolate(frame, [fps * 2, fps * 4.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldDim} strokeWidth={4} strokeLinecap="round" opacity={0.6} />

        <circle
          cx={memphis.x}
          cy={memphis.y}
          r={12}
          fill={themeEp4.colors.gold}
          opacity={1}
          style={{ filter: `grayscale(${1 - memphisFlip})` }}
        />
        <circle cx={memphis.x} cy={memphis.y} r={12} fill={themeEp4.colors.ember} opacity={memphisFlip} />
        <text x={memphis.x + 20} y={memphis.y + 5} fill={themeEp4.colors.text} fontFamily={themeEp4.font.body} fontSize={20}>
          Memphis
        </text>

        <circle cx={herak.x} cy={herak.y} r={9} fill={themeEp4.colors.gold} />
        <text x={herak.x + 18} y={herak.y + 5} fill={themeEp4.colors.text} fontFamily={themeEp4.font.body} fontSize={20}>
          Herakleopolis
        </text>
        <circle
          cx={herak.x}
          cy={herak.y}
          r={28}
          fill="none"
          stroke={themeEp4.colors.ember}
          strokeWidth={3}
          strokeDasharray="8 6"
          pathLength={1}
          style={{
            strokeDashoffset: 0,
            opacity: ringProgress,
            transform: `scale(${0.6 + ringProgress * 0.4})`,
            transformOrigin: `${herak.x}px ${herak.y}px`,
          }}
        />
      </svg>
    </AbsoluteFill>
  );
};
