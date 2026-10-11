import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

const QUOTE = "...with your right hand, you have cut off your left.";
const WORDS = QUOTE.split(" ");

// MG6: The Hand That Was Cut Off. Phase 1: quote card, gold serif text on
// dark marble, the courtier's line appears word by word. Phase 2: the quote
// dissolves; new text fades in beneath it.
export const EP5_B045_HandCutOff: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const quoteDissolve = interpolate(frame, [fps * 5.2, fps * 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const line2Opacity = interpolate(frame, [fps * 6.4, fps * 7.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(160deg, ${themeEp5.colors.stone}, ${themeEp5.colors.bg})`,
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div style={{ textAlign: "center", maxWidth: 1400, opacity: quoteDissolve }}>
        <div style={{ fontFamily: themeEp5.font.display, fontSize: 44, lineHeight: 1.5, color: themeEp5.colors.gold }}>
          {WORDS.map((w, i) => {
            const start = fps * 0.4 + i * 4;
            const op = interpolate(frame, [start, start + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
            return (
              <span key={i} style={{ opacity: op, marginRight: 14, display: "inline-block" }}>
                {w}
              </span>
            );
          })}
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          textAlign: "center",
          maxWidth: 1300,
          fontFamily: themeEp5.font.display,
          fontSize: 34,
          letterSpacing: 2,
          lineHeight: 1.5,
          color: themeEp5.colors.crimsonLight,
          opacity: line2Opacity,
        }}
      >
        WITHIN A YEAR, THE EMPEROR TOO WAS DEAD —
        <br />
        KILLED BY AETIUS'S FORMER BODYGUARDS
      </div>
    </AbsoluteFill>
  );
};
