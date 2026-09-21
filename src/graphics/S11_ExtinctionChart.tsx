import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const SPECIES = [
  { name: "Woolly Mammoth", y: 0.22 },
  { name: "Giant Ground Sloth", y: 0.38 },
  { name: "Saber-toothed Cat", y: 0.54 },
  { name: "Dire Wolf", y: 0.7 },
];

export const S11_ExtinctionChart: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const margin = width * 0.1;
  const chartW = width - margin * 2;
  const axisY = height * 0.85;
  const topY = height * 0.15;

  // Line draws left (before impact, flat/high count) to right (after, dropping to zero).
  const preImpactFrac = 0.45; // where on the x-axis the impact marker sits
  const impactX = margin + chartW * preImpactFrac;

  const lineDraw = interpolate(frame, [fps * 0.3, fps * 6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const countTop = height * 0.28;
  const countBottom = height * 0.78;

  const linePoints = () => {
    const pts: [number, number][] = [];
    const steps = 60;
    for (let i = 0; i <= steps; i++) {
      const frac = i / steps;
      if (frac > lineDraw) break;
      const x = margin + chartW * frac;
      let y: number;
      if (frac < preImpactFrac) {
        y = countTop;
      } else {
        const dropFrac = Math.min(1, (frac - preImpactFrac) / (1 - preImpactFrac));
        // steep initial drop, matches "in a geological blink" framing
        const eased = 1 - Math.pow(1 - dropFrac, 3);
        y = interpolate(eased, [0, 1], [countTop, countBottom]);
      }
      pts.push([x, y]);
    }
    return pts;
  };

  const points = linePoints();
  const pathD = points.map((p, i) => `${i === 0 ? "M" : "L"}${p[0]},${p[1]}`).join(" ");

  const markerIn = interpolate(frame, [fps * 3.2, fps * 3.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* axes */}
        <line x1={margin} y1={axisY} x2={width - margin} y2={axisY} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />
        <line x1={margin} y1={topY} x2={margin} y2={axisY} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />

        <path d={pathD} fill="none" stroke={theme.colors.glacialBlue} strokeWidth={3} />

        {/* impact marker */}
        <g opacity={markerIn}>
          <line x1={impactX} y1={topY} x2={impactX} y2={axisY} stroke={theme.colors.terracotta} strokeWidth={1.5} strokeDasharray="6 6" />
          <text x={impactX} y={topY - 14} fill={theme.colors.terracotta} fontFamily={theme.font.mono} fontSize={16} textAnchor="middle">
            12,800 BCE
          </text>
        </g>

        <text x={margin} y={axisY + 30} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={14}>
          BEFORE
        </text>
        <text x={width - margin} y={axisY + 30} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={14} textAnchor="end">
          AFTER
        </text>
        <text x={margin - 16} y={countTop} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={13} textAnchor="end">
          thriving
        </text>
        <text x={margin - 16} y={countBottom} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={13} textAnchor="end">
          extinct
        </text>
      </svg>

      {/* species labels, each fading out as the line passes their genus's drop-off point */}
      {SPECIES.map((sp, i) => {
        const dropFrame = fps * (3.4 + i * 0.9);
        const fadeOut = interpolate(frame, [dropFrame, dropFrame + fps * 0.8], [1, 0.25], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const fadeIn = interpolate(frame, [fps * (0.6 + i * 0.15), fps * (1.1 + i * 0.15)], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        return (
          <div
            key={sp.name}
            style={{
              position: "absolute",
              left: margin + chartW * 0.06,
              top: height * sp.y,
              opacity: fadeIn * fadeOut,
              color: theme.colors.text,
              fontFamily: theme.font.display,
              fontSize: 22,
              textDecoration: fadeOut < 0.5 ? "line-through" : "none",
              textDecorationColor: theme.colors.terracotta,
            }}
          >
            {sp.name}
          </div>
        );
      })}

      <div
        style={{
          position: "absolute",
          top: height * 0.05,
          width: "100%",
          textAlign: "center",
          fontFamily: theme.font.body,
          fontSize: 16,
          letterSpacing: 1,
          color: theme.colors.textFaint,
        }}
      >
        35+ MEGAFAUNA GENERA — NORTH AMERICA
      </div>
    </AbsoluteFill>
  );
};
