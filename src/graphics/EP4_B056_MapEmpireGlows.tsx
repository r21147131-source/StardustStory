import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH } from "./ep4-map-data";

// MG4 expansion: the Nile glows gold from the Delta to deep in Kush.
export const EP4_B056_MapEmpireGlows: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const glowDraw = interpolate(frame, [0, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const labelOpacity = interpolate(frame, [fps * 2.6, fps * 3.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path
          d={RIVER_PATH}
          fill="none"
          stroke={themeEp4.colors.goldLight}
          strokeWidth={14}
          strokeLinecap="round"
          opacity={0.85}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - glowDraw}
        />
        <path
          d={RIVER_PATH}
          fill="none"
          stroke={themeEp4.colors.gold}
          strokeWidth={6}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - glowDraw}
        />
      </svg>

      <div
        style={{
          position: "absolute",
          top: height * 0.1,
          width: "100%",
          textAlign: "center",
          opacity: labelOpacity,
        }}
      >
        <div style={{ fontFamily: themeEp4.font.display, fontSize: 32, letterSpacing: 5, color: themeEp4.colors.goldLight }}>
          THE 25TH DYNASTY
        </div>
        <div style={{ fontFamily: themeEp4.font.body, fontStyle: "italic", fontSize: 22, color: themeEp4.colors.textDim, marginTop: 8 }}>
          c. 690 BCE
        </div>
      </div>
    </AbsoluteFill>
  );
};
