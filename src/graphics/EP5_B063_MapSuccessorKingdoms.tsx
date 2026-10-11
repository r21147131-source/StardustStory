import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";

// MG10 phase 2: the western map relights, now divided into small successor
// kingdoms, each still faintly gold at the edges. Beneath it, the word LATIN
// splits and regrows into FRANÇAIS, ESPAÑOL, ITALIANO branching outward
// like roots.
export const EP5_B063_MapSuccessorKingdoms: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, fps } = useVideoConfig();

  const mapRelight = interpolate(frame, [fps * 0.3, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const partitionsDraw = interpolate(frame, [fps * 1, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const latinOpacity = interpolate(frame, [fps * 5, fps * 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const rootsDraw = interpolate(frame, [fps * 6.4, fps * 8.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wordsOpacity = interpolate(frame, [fps * 8, fps * 9.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const latinX = width / 2;
  const latinY = 760;
  const targets = [
    { label: "FRANÇAIS", x: latinX - 320, y: 900 },
    { label: "ESPAÑOL", x: latinX - 20, y: 950 },
    { label: "ITALIANO", x: latinX + 300, y: 900 },
  ];

  // Internal partitions within the western landmass, suggesting small
  // successor kingdoms (Visigothic Hispania, Frankish Gaul, Ostrogothic
  // Italy) replacing one imperial field.
  const partitions = [
    "M 360,380 C 420,460 450,560 420,660",
    "M 560,330 C 600,420 610,520 590,610",
  ];

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground fillOpacity={0.1 * mapRelight} strokeOpacity={0.4 * mapRelight} />
      <svg width={width} height={1080} style={{ position: "absolute" }}>
        {partitions.map((d, i) => (
          <path key={i} d={d} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={2}
            pathLength={1} strokeDasharray={1} strokeDashoffset={1 - partitionsDraw} opacity={0.6 * mapRelight} />
        ))}

        {/* roots from LATIN to each descendant language */}
        {targets.map((t, i) => (
          <path
            key={i}
            d={`M ${latinX},${latinY} Q ${(latinX + t.x) / 2},${(latinY + t.y) / 2 + 20} ${t.x},${t.y}`}
            fill="none"
            stroke={themeEp5.colors.bronze}
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
            top: t.y - 18,
            width: 240,
            textAlign: "center",
            fontFamily: themeEp5.font.display,
            fontSize: 28,
            letterSpacing: 3,
            color: themeEp5.colors.goldLight,
            opacity: wordsOpacity,
          }}
        >
          {t.label}
        </div>
      ))}
    </AbsoluteFill>
  );
};
