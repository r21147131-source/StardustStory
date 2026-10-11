import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { ROAD_PATH, CITY_POS } from "./ep5-map-data";

// MG1: Roads and Rule. Phase 1: a single road network lights up gold from
// Britain to the Euphrates. Phase 2: coin icons pulse at major ports from
// Spain to Syria. Phase 3: caption ROMA AETERNA fades in beneath.
export const EP5_B009_MapRoadsRule: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const roadDraw = interpolate(frame, [fps * 0.3, fps * 3.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const portPulse = interpolate(frame, [fps * 3, fps * 4.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const captionOpacity = interpolate(frame, [fps * 5.5, fps * 6.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const ports: Array<keyof typeof CITY_POS> = ["hispalis", "roma", "antiochia"];

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path
          d={ROAD_PATH}
          fill="none"
          stroke={themeEp5.colors.gold}
          strokeWidth={4}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - roadDraw}
        />
        {ports.map((key) => {
          const p = CITY_POS[key];
          const pulseR = 10 + Math.sin(frame / 6) * 4 * portPulse;
          return (
            <g key={key} opacity={portPulse}>
              <circle cx={p.x} cy={p.y} r={pulseR} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={2} opacity={0.6} />
              <circle cx={p.x} cy={p.y} r={6} fill={themeEp5.colors.goldLight} />
            </g>
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 110,
          textAlign: "center",
          fontFamily: themeEp5.font.display,
          fontSize: 48,
          letterSpacing: 10,
          color: themeEp5.colors.gold,
          opacity: captionOpacity,
        }}
      >
        ROMA AETERNA
      </div>
    </AbsoluteFill>
  );
};
