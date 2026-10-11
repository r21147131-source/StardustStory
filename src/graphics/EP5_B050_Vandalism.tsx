import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG7: Vandalism. Typography reveal on dark stone: VANDAL carves itself in
// gold. A line strikes beneath it and VANDALISM grows out from the same
// letters, larger, with the caption "a word that outlived the kingdom."
export const EP5_B050_Vandalism: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const vandalOpacity = interpolate(frame, [fps * 0.3, fps * 1.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const strikeDraw = interpolate(frame, [fps * 2, fps * 2.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const vandalShrink = interpolate(frame, [fps * 3.4, fps * 4.4], [1, 0.55], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const vandalFade = interpolate(frame, [fps * 3.4, fps * 4.4], [1, 0.4], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ismScale = interpolate(frame, [fps * 3.6, fps * 5], [0.6, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const ismOpacity = interpolate(frame, [fps * 3.6, fps * 4.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const captionOpacity = interpolate(frame, [fps * 9, fps * 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ textAlign: "center" }}>
        <div style={{ position: "relative", display: "inline-block" }}>
          <div
            style={{
              fontFamily: themeEp5.font.display,
              fontSize: 96,
              letterSpacing: 10,
              color: themeEp5.colors.gold,
              opacity: vandalOpacity * vandalFade,
              transform: `scale(${vandalShrink})`,
              transformOrigin: "center",
            }}
          >
            VANDAL
          </div>
          <div
            style={{
              position: "absolute",
              left: "8%",
              right: "8%",
              top: "52%",
              height: 4,
              backgroundColor: themeEp5.colors.crimsonLight,
              transform: `scaleX(${strikeDraw})`,
              transformOrigin: "left",
              opacity: 1 - (vandalShrink < 0.9 ? 0.5 : 0),
            }}
          />
        </div>

        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 112,
            letterSpacing: 8,
            color: themeEp5.colors.goldLight,
            opacity: ismOpacity,
            transform: `scale(${ismScale})`,
            marginTop: 10,
            textShadow: `0 0 50px rgba(217,191,140,${0.3 * ismOpacity})`,
          }}
        >
          VANDALISM
        </div>

        <div
          style={{
            fontFamily: themeEp5.font.body,
            fontStyle: "italic",
            fontSize: 28,
            color: themeEp5.colors.textDim,
            opacity: captionOpacity,
            marginTop: 26,
          }}
        >
          a word that outlived the kingdom
        </div>
      </div>
    </AbsoluteFill>
  );
};
