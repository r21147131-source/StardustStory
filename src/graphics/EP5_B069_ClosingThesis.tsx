import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

const LINES = ["EVERYONE KEPT THE NAME.", "ALMOST NO ONE KEPT", "THE THING THE NAME ONCE MEANT."];

// MG12: Closing thesis card. On black, gold serif text builds line by line.
export const EP5_B069_ClosingThesis: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000", alignItems: "center", justifyContent: "center" }}>
      <div style={{ textAlign: "center", maxWidth: 1400 }}>
        {LINES.map((line, i) => {
          const start = fps * 0.4 + i * fps * 0.9;
          const op = interpolate(frame, [start, start + fps * 0.7], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div
              key={i}
              style={{
                fontFamily: themeEp5.font.display,
                fontSize: 48,
                letterSpacing: 3,
                lineHeight: 1.5,
                color: themeEp5.colors.gold,
                opacity: op,
              }}
            >
              {line}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
