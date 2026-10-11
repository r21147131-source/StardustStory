import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG11 phase 2 (continuation of B066): caption fades in beneath the three
// words — IT HAD NOT DIED. IT HAD STOPPED BELONGING TO ANY ONE THRONE.
export const EP5_B067_CaesarCaption: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const captionOpacity = interpolate(frame, [fps * 0.3, fps * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", textAlign: "center" }}>
        <div style={{ fontFamily: themeEp5.font.display, fontSize: 56, letterSpacing: 6, color: themeEp5.colors.goldLight, opacity: 0.35 }}>
          <span style={{ marginRight: 170 }}>KAISER</span>
          <span style={{ marginLeft: 170 }}>TSAR</span>
        </div>

        <div
          style={{
            marginTop: 60,
            fontFamily: themeEp5.font.body,
            fontStyle: "italic",
            fontSize: 30,
            color: themeEp5.colors.textDim,
            opacity: captionOpacity,
          }}
        >
          IT HAD NOT DIED. IT HAD STOPPED BELONGING TO ANY ONE THRONE.
        </div>
      </div>
    </AbsoluteFill>
  );
};
