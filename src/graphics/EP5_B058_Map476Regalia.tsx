import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { CITY_POS } from "./ep5-map-data";

// MG9 phase 1: a small regalia-icon travels by ship from Ravenna/Rome to
// Constantinople across the map. The western half of the earlier split-map
// goes fully dark.
export const EP5_B058_Map476Regalia: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const travelT = interpolate(frame, [fps * 0.4, fps * 3.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const westDark = interpolate(frame, [fps * 3.6, fps * 4.8], [1, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const from = CITY_POS.ravenna;
  const to = CITY_POS.constantinopolis;
  const shipX = from.x + (to.x - from.x) * travelT;
  const shipY = from.y + (to.y - from.y) * travelT - Math.sin(travelT * Math.PI) * 40;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="west" opacity={westDark} />
      <Ep5MapBackground layer="east" opacity={1} />

      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path
          d={`M ${from.x},${from.y} Q ${(from.x + to.x) / 2},${Math.min(from.y, to.y) - 80} ${to.x},${to.y}`}
          fill="none"
          stroke={themeEp5.colors.textFaint}
          strokeWidth={1.5}
          strokeDasharray="4 6"
          opacity={0.6}
        />

        {/* travelling regalia icon: a small crown */}
        <g transform={`translate(${shipX},${shipY})`} opacity={travelT > 0 && travelT < 1 ? 1 : travelT}>
          <path
            d="M -12,6 L -12,-2 L -6,4 L 0,-6 L 6,4 L 12,-2 L 12,6 Z"
            fill={themeEp5.colors.goldLight}
          />
        </g>

        <circle cx={from.x} cy={from.y} r={8} fill={themeEp5.colors.textFaint} opacity={westDark} />
        <circle cx={to.x} cy={to.y} r={8} fill={themeEp5.colors.goldLight} />
      </svg>
    </AbsoluteFill>
  );
};
