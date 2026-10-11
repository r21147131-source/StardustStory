import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG10 phase 1: What Outlived the Throne. On black, the word ENDING appears
// in large gold type, then a crack splits it and the word reassembles,
// slightly altered, as CONTINUES.
export const EP5_B061_EndingContinues: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, fps } = useVideoConfig();
  const cx = width / 2;

  const endingOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const crackDraw = interpolate(frame, [fps * 1.6, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const endingFade = interpolate(frame, [fps * 2.4, fps * 3], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const continuesOpacity = interpolate(frame, [fps * 2.8, fps * 3.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", alignItems: "center", justifyContent: "center" }}>
      <div style={{ position: "relative", textAlign: "center" }}>
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 110,
            letterSpacing: 10,
            color: themeEp5.colors.gold,
            opacity: endingOpacity * endingFade,
          }}
        >
          ENDING
        </div>
        <svg width={700} height={140} style={{ position: "absolute", left: "50%", top: "50%", transform: "translate(-50%,-50%)" }}>
          <path
            d="M 20,20 C 180,50 280,90 360,60 C 450,30 560,90 680,120"
            fill="none"
            stroke="#000000"
            strokeWidth={10}
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1 - crackDraw}
            opacity={endingFade < 1 ? 1 : crackDraw}
          />
        </svg>
        <div
          style={{
            position: "absolute",
            left: 0,
            right: 0,
            top: 0,
            fontFamily: themeEp5.font.display,
            fontSize: 110,
            letterSpacing: 10,
            color: themeEp5.colors.goldLight,
            opacity: continuesOpacity,
            textShadow: `0 0 50px rgba(237,220,184,${0.3 * continuesOpacity})`,
          }}
        >
          CONTINUES
        </div>
      </div>
    </AbsoluteFill>
  );
};
