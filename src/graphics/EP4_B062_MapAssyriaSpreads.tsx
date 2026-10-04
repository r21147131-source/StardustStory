import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH } from "./ep4-map-data";
import { Ep4RealMapBackground } from "./Ep4RealMapBackground";

// MG5 Phase 1: Assyria's territory spreads west across the map like ink toward the Nile.
export const EP4_B062_MapAssyriaSpreads: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const inkSpread = interpolate(frame, [fps * 0.5, fps * 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const labelOpacity = interpolate(frame, [fps * 0.3, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <Ep4RealMapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.gold} strokeWidth={6} strokeLinecap="round" opacity={0.7} />

        <g style={{ opacity: inkSpread }}>
          <path
            d={`M 1920,120 C 1500,160 ${1300 - inkSpread * 300},220 ${900 + (1 - inkSpread) * 400},280
                C ${700 + (1 - inkSpread) * 400},340 1400,400 1920,420 Z`}
            fill={themeEp4.colors.assyriaRegion}
            opacity={0.55}
          />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          right: 80,
          top: height * 0.18,
          fontFamily: themeEp4.font.display,
          fontSize: 30,
          letterSpacing: 5,
          color: "#c98b8b",
          opacity: labelOpacity,
        }}
      >
        ASSYRIA
      </div>
    </AbsoluteFill>
  );
};
