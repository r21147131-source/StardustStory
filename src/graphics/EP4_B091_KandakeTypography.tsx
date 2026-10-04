import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG7: pure typography. CANDACE appears as a name, struck through, replaced by
// KANDAKE with a caption, then AMANIRENAS carves into stone.
export const EP4_B091_KandakeTypography: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const candaceOpacity = interpolate(frame, [fps * 0.3, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const strikeDraw = interpolate(frame, [fps * 2, fps * 2.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const candaceFade = interpolate(frame, [fps * 3, fps * 3.8], [1, 0.25], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const kandakeOpacity = interpolate(frame, [fps * 3.6, fps * 4.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const captionOpacity = interpolate(frame, [fps * 4.8, fps * 5.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const amanirenasOpacity = interpolate(frame, [fps * 7.5, fps * 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", textAlign: "center" }}>
        <div
          style={{
            fontFamily: themeEp4.font.display,
            fontSize: 72,
            letterSpacing: 10,
            color: themeEp4.colors.textDim,
            opacity: candaceOpacity * candaceFade,
            position: "relative",
          }}
        >
          CANDACE
          <div
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: "50%",
              height: 4,
              backgroundColor: themeEp4.colors.ember,
              transform: `scaleX(${strikeDraw})`,
              transformOrigin: "left",
            }}
          />
        </div>

        <div
          style={{
            fontFamily: themeEp4.font.display,
            fontSize: 72,
            letterSpacing: 10,
            color: themeEp4.colors.goldLight,
            opacity: kandakeOpacity,
            marginTop: 20,
          }}
        >
          KANDAKE
        </div>
        <div
          style={{
            fontFamily: themeEp4.font.body,
            fontStyle: "italic",
            fontSize: 24,
            color: themeEp4.colors.textDim,
            opacity: captionOpacity,
            marginTop: 14,
          }}
        >
          a title, not a name
        </div>

        <div
          style={{
            fontFamily: themeEp4.font.display,
            fontSize: 44,
            letterSpacing: 8,
            color: themeEp4.colors.gold,
            opacity: amanirenasOpacity,
            marginTop: 50,
          }}
        >
          AMANIRENAS
        </div>
      </div>
    </AbsoluteFill>
  );
};
