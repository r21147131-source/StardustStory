import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG9: a scroll of royal names scrolls down; the 25th Dynasty names fill in,
// Piye's slot stays a blank outline.
const NAMES = ["SHABAKA", "SHEBITKU", "[ — ]", "TAHARQA", "TANTAMANI"];

export const EP4_B102_KingListScroll: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const scrollY = interpolate(frame, [0, fps * 6], [height * 0.5, -height * 0.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg, overflow: "hidden" }}>
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: scrollY,
          transform: "translateX(-50%)",
          textAlign: "center",
        }}
      >
        {NAMES.map((name, i) => {
          const rowIn = interpolate(frame, [fps * (0.5 + i * 0.8), fps * (1.1 + i * 0.8)], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const isBlank = name === "[ — ]";
          return (
            <div
              key={i}
              style={{
                fontFamily: themeEp4.font.display,
                fontSize: 36,
                letterSpacing: 4,
                marginBottom: 46,
                opacity: rowIn,
                color: isBlank ? "transparent" : themeEp4.colors.goldLight,
                border: isBlank ? `2px dashed ${themeEp4.colors.textFaint}` : "none",
                padding: isBlank ? "6px 30px" : 0,
                display: "block",
              }}
            >
              {isBlank ? "PIYE?" : name}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
