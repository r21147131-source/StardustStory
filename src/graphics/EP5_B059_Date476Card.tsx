import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG9 phase 2 (continuation of B058): big date card on black — 476 CE, THE
// WESTERN ROMAN EMPIRE ENDS.
export const EP5_B059_Date476Card: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const dateOpacity = interpolate(frame, [fps * 0.2, fps * 1.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const lineOpacity = interpolate(frame, [fps * 1.3, fps * 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const subOpacity = interpolate(frame, [fps * 2.2, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", alignItems: "center", justifyContent: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 100,
            letterSpacing: 10,
            color: themeEp5.colors.goldLight,
            opacity: dateOpacity,
            textShadow: `0 0 60px rgba(237,220,184,${0.35 * dateOpacity})`,
          }}
        >
          476 CE
        </div>
        <div
          style={{
            width: 300,
            height: 2,
            background: themeEp5.colors.bronzeDim,
            margin: "24px auto",
            opacity: lineOpacity,
          }}
        />
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 38,
            letterSpacing: 4,
            color: themeEp5.colors.crimsonLight,
            opacity: subOpacity,
          }}
        >
          THE WESTERN ROMAN EMPIRE ENDS
        </div>
      </div>
    </AbsoluteFill>
  );
};
