import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Simplified line-art of Pillar 43's relief (not the photograph - this plays
// right after the real archival photo, as its own annotated-diagram beat),
// with a constellation-line overlay for the contested reading.
const STARS = [
  { x: 500, y: 140 }, // disc
  { x: 560, y: 190 }, // wing tip
  { x: 440, y: 190 },
  { x: 420, y: 320 }, // scorpion L
  { x: 580, y: 320 }, // scorpion R
  { x: 500, y: 380 }, // headless figure
];

const CONNECTIONS: [number, number][] = [
  [0, 1],
  [0, 2],
  [1, 4],
  [2, 3],
  [3, 5],
  [4, 5],
];

export const EP2_S19_VultureStoneOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const carvingIn = interpolate(frame, [0, fps * 1.2], [0, 1], { extrapolateRight: "clamp" });
  const starsIn = interpolate(frame, [fps * 2.5, fps * 4.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const linesIn = interpolate(frame, [fps * 4.2, fps * 7.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(frame, [fps * 1.6, fps * 2.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.ink, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 550" width={width * 0.7} height={height * 0.72}>
        <g opacity={carvingIn} stroke={theme.colors.ashGray} strokeWidth={2.5} fill="none">
          {/* disc */}
          <circle cx={500} cy={140} r={38} />
          {/* wings */}
          <path d="M462,160 C420,150 380,170 350,200" />
          <path d="M538,160 C580,150 620,170 650,200" />
          {/* body / headless figure */}
          <line x1={500} y1={178} x2={500} y2={360} />
          <path d="M500,360 L470,400 M500,360 L530,400" />
          {/* scorpions, simplified */}
          <path d="M400,310 C410,300 430,300 440,315 L445,330" />
          <path d="M600,310 C590,300 570,300 560,315 L555,330" />
          {/* bird row along the top */}
          {[380, 440, 560, 620].map((x) => (
            <path key={x} d={`M${x - 10},90 Q${x},78 ${x + 10},90`} />
          ))}
        </g>

        {/* constellation overlay */}
        <g opacity={linesIn}>
          {CONNECTIONS.map(([a, b], i) => (
            <line
              key={i}
              x1={STARS[a].x}
              y1={STARS[a].y}
              x2={STARS[b].x}
              y2={STARS[b].y}
              stroke={theme.colors.glacialBlue}
              strokeWidth={1.5}
              strokeDasharray="5 5"
            />
          ))}
        </g>
        <g opacity={starsIn}>
          {STARS.map((s, i) => (
            <circle key={i} cx={s.x} cy={s.y} r={5} fill={theme.colors.glacialBlue} />
          ))}
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          top: height * 0.1,
          width: "100%",
          textAlign: "center",
          opacity: labelOpacity,
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 2,
          color: theme.colors.terracotta,
        }}
      >
        PROPOSED INTERPRETATION — CONTESTED
      </div>
      <div
        style={{
          position: "absolute",
          bottom: height * 0.08,
          width: "100%",
          textAlign: "center",
          opacity: linesIn,
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 1,
          color: theme.colors.textFaint,
        }}
      >
        Sweatman &amp; Tsikritsis (2017) — not consensus among archaeologists
      </div>
    </AbsoluteFill>
  );
};
