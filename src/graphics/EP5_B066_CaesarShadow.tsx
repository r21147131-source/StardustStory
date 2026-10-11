import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG11 phase 1: Caesar's Long Shadow. Typography on dark stone, modeled on
// Episode 4's Kandake treatment: CAESAR carves itself in gold, then splits
// and regrows into KAISER and TSAR branching to either side.
export const EP5_B066_CaesarShadow: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const caesarOpacity = interpolate(frame, [fps * 0.3, fps * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const caesarFade = interpolate(frame, [fps * 3, fps * 4], [1, 0.3], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const splitT = interpolate(frame, [fps * 3.4, fps * 5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const kaiserOpacity = interpolate(frame, [fps * 4, fps * 5.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const tsarOpacity = interpolate(frame, [fps * 4, fps * 5.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", textAlign: "center" }}>
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 76,
            letterSpacing: 10,
            color: themeEp5.colors.gold,
            opacity: caesarOpacity * caesarFade,
          }}
        >
          CAESAR
        </div>

        <div
          style={{
            position: "absolute",
            left: `calc(50% - ${350 * splitT}px)`,
            top: 110,
            transform: "translateX(-50%)",
            fontFamily: themeEp5.font.display,
            fontSize: 56,
            letterSpacing: 6,
            color: themeEp5.colors.goldLight,
            opacity: kaiserOpacity,
          }}
        >
          KAISER
        </div>
        <div
          style={{
            position: "absolute",
            left: `calc(50% + ${350 * splitT}px)`,
            top: 110,
            transform: "translateX(-50%)",
            fontFamily: themeEp5.font.display,
            fontSize: 56,
            letterSpacing: 6,
            color: themeEp5.colors.goldLight,
            opacity: tsarOpacity,
          }}
        >
          TSAR
        </div>
      </div>
    </AbsoluteFill>
  );
};
