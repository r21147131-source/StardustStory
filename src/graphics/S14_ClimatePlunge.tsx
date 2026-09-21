import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Schematic Greenland-ice-core-style temperature curve: gradual post-glacial
// warming, then the Younger Dryas plunge, then recovery. Shape is illustrative,
// not plotted from a dataset.
const CURVE: [number, number][] = [
  [0.0, 0.75],
  [0.12, 0.68],
  [0.24, 0.55],
  [0.34, 0.42],
  [0.4, 0.4],
  [0.44, 0.72], // the plunge
  [0.46, 0.78],
  [0.6, 0.8],
  [0.72, 0.79],
  [0.82, 0.55], // recovery begins
  [0.92, 0.3],
  [1.0, 0.22],
];

export const S14_ClimatePlunge: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const margin = width * 0.1;
  const chartW = width - margin * 2;
  const chartTop = height * 0.2;
  const chartBottom = height * 0.78;
  const chartH = chartBottom - chartTop;

  const drawFrac = interpolate(frame, [fps * 0.3, fps * 7], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const pts = CURVE.filter((p) => p[0] <= drawFrac).map(
    ([fx, fy]) => [margin + chartW * fx, chartTop + chartH * fy] as [number, number]
  );
  const pathD = pts.map((p, i) => `${i === 0 ? "M" : "L"}${p[0]},${p[1]}`).join(" ");

  const bandX0 = margin + chartW * 0.4;
  const bandX1 = margin + chartW * 0.72;
  const bandIn = interpolate(frame, [fps * 3.2, fps * 4.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const labelIn = interpolate(frame, [fps * 4.4, fps * 5.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* Younger Dryas shaded band */}
        <rect
          x={bandX0}
          y={chartTop}
          width={(bandX1 - bandX0) * bandIn}
          height={chartBottom - chartTop}
          fill={theme.colors.glacialBlueDim}
          opacity={0.25}
        />

        <line x1={margin} y1={chartBottom} x2={width - margin} y2={chartBottom} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />
        <line x1={margin} y1={chartTop} x2={margin} y2={chartBottom} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />

        <path d={pathD} fill="none" stroke={theme.colors.glacialBlue} strokeWidth={3} />

        <text x={margin - 16} y={chartTop + 8} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={13} textAnchor="end">
          warmer
        </text>
        <text x={margin - 16} y={chartBottom} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={13} textAnchor="end">
          colder
        </text>
        <text x={margin} y={chartBottom + 30} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={14}>
          ~14,700 BP
        </text>
        <text x={width - margin} y={chartBottom + 30} fill={theme.colors.textFaint} fontFamily={theme.font.body} fontSize={14} textAnchor="end">
          ~11,700 BP
        </text>
      </svg>

      <div
        style={{
          position: "absolute",
          left: (bandX0 + bandX1) / 2,
          top: chartTop - 50,
          transform: "translateX(-50%)",
          opacity: labelIn,
          textAlign: "center",
          fontFamily: theme.font.display,
        }}
      >
        <div style={{ color: theme.colors.text, fontSize: 24, fontWeight: 700 }}>The Younger Dryas</div>
        <div style={{ color: theme.colors.textDim, fontSize: 15, marginTop: 2 }}>~1,000 years, ~10°C drop</div>
      </div>
    </AbsoluteFill>
  );
};
