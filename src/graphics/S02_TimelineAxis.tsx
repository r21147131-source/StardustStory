import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Timeline spans 20,000 BCE (left) to present (right); marker lands on 12,800 BP.
const START_YEAR = -20000;
const END_YEAR = 2026;
const MARK_YEAR = -12800;

const yearToX = (year: number, width: number, margin: number) =>
  margin + ((year - START_YEAR) / (END_YEAR - START_YEAR)) * (width - margin * 2);

export const S02_TimelineAxis: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const margin = width * 0.08;
  const lineY = height * 0.55;

  const clockSpin = interpolate(frame, [0, fps * 2.5], [0, -1080], {
    extrapolateRight: "clamp",
  });
  const clockSettle = spring({ frame: frame - fps * 2.2, fps, config: { damping: 14 } });
  const clockAngle = clockSpin + clockSettle * 40;

  const markerX = yearToX(MARK_YEAR, width, margin);
  const markerIn = spring({ frame: frame - fps * 2.6, fps, config: { damping: 16 } });
  const lineDraw = interpolate(frame, [fps * 0.2, fps * 2.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(frame, [fps * 2.8, fps * 3.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ticks = [];
  for (let y = -20000; y <= 2000; y += 2000) {
    ticks.push(y);
  }

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* base axis line, drawing in */}
        <line
          x1={margin}
          y1={lineY}
          x2={margin + (width - margin * 2) * lineDraw}
          y2={lineY}
          stroke={theme.colors.ashGrayDim}
          strokeWidth={2}
        />

        {/* tick marks */}
        {ticks.map((y) => {
          const x = yearToX(y, width, margin);
          if (x > margin + (width - margin * 2) * lineDraw) return null;
          return (
            <g key={y}>
              <line x1={x} y1={lineY - 10} x2={x} y2={lineY + 10} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />
              <text
                x={x}
                y={lineY + 34}
                fill={theme.colors.textFaint}
                fontFamily={theme.font.mono}
                fontSize={16}
                textAnchor="middle"
              >
                {y <= 0 ? `${Math.abs(y)} BCE` : "NOW"}
              </text>
            </g>
          );
        })}

        {/* clock, spinning backward then settling */}
        <g transform={`translate(${width * 0.5}, ${height * 0.28})`}>
          <circle r={54} fill="none" stroke={theme.colors.glacialBlueDim} strokeWidth={2} />
          <line
            x1={0}
            y1={0}
            x2={0}
            y2={-40}
            stroke={theme.colors.glacialBlue}
            strokeWidth={3}
            strokeLinecap="round"
            transform={`rotate(${clockAngle})`}
          />
          <circle r={4} fill={theme.colors.glacialBlue} />
        </g>

        {/* 12,800 BCE marker */}
        <g
          transform={`translate(${markerX}, ${lineY}) scale(${markerIn})`}
          style={{ transformOrigin: `${markerX}px ${lineY}px` }}
        >
          <line x1={0} y1={-46} x2={0} y2={10} stroke={theme.colors.terracotta} strokeWidth={3} />
          <circle cy={-46} r={6} fill={theme.colors.terracotta} />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          left: markerX,
          top: lineY - 110,
          transform: "translateX(-50%)",
          opacity: labelOpacity,
          textAlign: "center",
          fontFamily: theme.font.display,
        }}
      >
        <div style={{ color: theme.colors.terracotta, fontSize: 30, fontWeight: 700 }}>12,800 BCE</div>
        <div style={{ color: theme.colors.textDim, fontSize: 16, marginTop: 4 }}>the impact</div>
      </div>
    </AbsoluteFill>
  );
};
