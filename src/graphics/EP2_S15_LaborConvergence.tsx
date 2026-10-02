import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Scattered hunter-gatherer bands (dots) converging from the edges toward a
// central point (the enclosure), each leaving a radiating travel line behind.
const BANDS = [
  { angle: 20, dist: 0.42, delay: 0 },
  { angle: 70, dist: 0.38, delay: 0.3 },
  { angle: 125, dist: 0.44, delay: 0.1 },
  { angle: 170, dist: 0.4, delay: 0.5 },
  { angle: 210, dist: 0.46, delay: 0.2 },
  { angle: 255, dist: 0.39, delay: 0.4 },
  { angle: 300, dist: 0.43, delay: 0.15 },
  { angle: 340, dist: 0.41, delay: 0.35 },
];

export const EP2_S15_LaborConvergence: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const cx = width * 0.5;
  const cy = height * 0.48;
  const R = Math.min(width, height) * 0.38;

  const centerIn = spring({ frame, fps, config: { damping: 14 } });
  const convergeStart = fps * 1.0;
  const convergeDur = fps * 4.5;
  const converge = interpolate(frame, [convergeStart, convergeStart + convergeDur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const labelOpacity = interpolate(frame, [fps * 6.5, fps * 7.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {BANDS.map((b, i) => {
          const rad = (b.angle * Math.PI) / 180;
          const startX = cx + Math.cos(rad) * R;
          const startY = cy + Math.sin(rad) * R * 0.6;

          const bandT = interpolate(frame, [convergeStart + b.delay * fps, convergeStart + b.delay * fps + convergeDur * 0.7], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const curX = interpolate(bandT, [0, 1], [startX, cx]);
          const curY = interpolate(bandT, [0, 1], [startY, cy]);

          return (
            <g key={i}>
              <line
                x1={startX}
                y1={startY}
                x2={curX}
                y2={curY}
                stroke={theme.colors.ashGrayDim}
                strokeWidth={1.5}
                strokeDasharray="4 5"
                opacity={0.6}
              />
              <circle cx={curX} cy={curY} r={6} fill={theme.colors.glacialBlue} opacity={interpolate(bandT, [0, 0.1], [0, 1], { extrapolateLeft: "clamp" })} />
            </g>
          );
        })}

        {/* central enclosure marker */}
        <g transform={`translate(${cx}, ${cy}) scale(${centerIn})`} style={{ transformOrigin: `${cx}px ${cy}px` }}>
          <circle r={22} fill="none" stroke={theme.colors.terracotta} strokeWidth={3} />
          <circle r={5} fill={theme.colors.terracotta} />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.12,
          width: "100%",
          textAlign: "center",
          opacity: labelOpacity,
          fontFamily: theme.font.display,
          fontSize: 20,
          color: theme.colors.text,
        }}
      >
        scattered bands, one gathering place
      </div>
    </AbsoluteFill>
  );
};
