import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";

// MG10 phase 2: the western map relights, now divided into small successor
// kingdoms (Gaul, Hispania, Italia — the real provinces that became France,
// Spain, Italy). Beneath it, the word LATIN splits and regrows into
// FRANÇAIS, ESPAÑOL, ITALIANO branching outward like roots, each rooted at
// its real region on the map.
export const EP5_B063_MapSuccessorKingdoms: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const mapRelight = interpolate(frame, [fps * 0.3, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const latinOpacity = interpolate(frame, [fps * 5, fps * 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rootsDraw = interpolate(frame, [fps * 6.4, fps * 8.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wordsOpacity = interpolate(frame, [fps * 8, fps * 9.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const latinX = 650;
  const latinY = 230;
  const targets = [
    { label: "FRANÇAIS", x: 650, y: 440 },
    { label: "ESPAÑOL", x: 380, y: 660 },
    { label: "ITALIANO", x: 900, y: 600 },
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="west" opacity={mapRelight} />

      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        {targets.map((t, i) => (
          <path
            key={i}
            d={`M ${latinX},${latinY} Q ${(latinX + t.x) / 2},${(latinY + t.y) / 2 + 20} ${t.x},${t.y}`}
            fill="none"
            stroke={themeEp5.colors.goldLight}
            strokeWidth={2.5}
            pathLength={1}
            strokeDasharray={1}
            strokeDashoffset={1 - rootsDraw}
          />
        ))}
      </svg>

      <div
        style={{
          position: "absolute",
          left: latinX - 150,
          top: latinY - 36,
          width: 300,
          textAlign: "center",
          fontFamily: themeEp5.font.display,
          fontSize: 48,
          letterSpacing: 8,
          color: themeEp5.colors.gold,
          opacity: latinOpacity,
        }}
      >
        LATIN
      </div>

      {targets.map((t, i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: t.x - 120,
            top: t.y - 14,
            width: 240,
            textAlign: "center",
            fontFamily: themeEp5.font.display,
            fontSize: 24,
            letterSpacing: 2,
            color: themeEp5.colors.goldLight,
            textShadow: "0 0 12px rgba(0,0,0,0.9)",
            opacity: wordsOpacity,
          }}
        >
          {t.label}
        </div>
      ))}
    </AbsoluteFill>
  );
};
