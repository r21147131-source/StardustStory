import { AbsoluteFill, interpolate, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Two tracks over the same 12,000-years-ago -> present axis: the "old model"
// (farming first, temples follow) vs. what Göbekli Tepe actually shows
// (temple first, a long gap, then farming/cities/writing cluster together).
const START_YEARS_AGO = 12000;
const END_YEARS_AGO = 3000;

const yearsAgoToX = (ya: number, width: number, margin: number) =>
  margin + ((START_YEARS_AGO - ya) / (START_YEARS_AGO - END_YEARS_AGO)) * (width - margin * 2);

const OLD_MODEL = [
  { label: "Farming begins", ya: 10500 },
  { label: "Surplus / settling", ya: 9000 },
  { label: "Villages grow", ya: 7000 },
  { label: "Temples built", ya: 5500 },
];

const ACTUAL = [
  { label: "Temple built\n(Göbekli Tepe)", ya: 11600, early: true },
  { label: "Farming begins\n(einkorn domesticated)", ya: 6500 },
  { label: "First cities", ya: 5500 },
  { label: "Writing", ya: 5400 },
];

export const EP2_S11_InvertedSequenceBars: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const margin = width * 0.08;
  const trackW = width - margin * 2;

  const oldTrackY = height * 0.28;
  const actualTrackY = height * 0.62;

  const oldLineDraw = interpolate(frame, [fps * 0.3, fps * 3.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const actualLineDraw = interpolate(frame, [fps * 4.0, fps * 7.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const gapHighlight = interpolate(frame, [fps * 8.5, fps * 10.5, fps * 13, fps * 14], [0, 1, 1, 0.3], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const titleOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateRight: "clamp" });
  const oldLabelOpacity = interpolate(frame, [fps * 0.6, fps * 1.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const actualLabelOpacity = interpolate(frame, [fps * 3.6, fps * 4.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const calloutOpacity = interpolate(frame, [fps * 15, fps * 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const renderTrack = (
    events: typeof OLD_MODEL,
    trackY: number,
    lineDraw: number,
    color: string,
    revealStart: number
  ) =>
    events.map((e, i) => {
      const x = yearsAgoToX(e.ya, width, margin);
      const segFrac = 1 - (e.ya - END_YEARS_AGO) / (START_YEARS_AGO - END_YEARS_AGO);
      if (segFrac > lineDraw) return null;
      const dotIn = interpolate(frame, [revealStart + i * fps * 0.5, revealStart + i * fps * 0.5 + fps * 0.4], [0, 1], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      });
      return (
        <g key={e.label} opacity={dotIn}>
          <circle cx={x} cy={trackY} r={7} fill={color} />
          <text
            x={x}
            y={trackY + 30}
            fill={theme.colors.textDim}
            fontFamily={theme.font.body}
            fontSize={13}
            textAnchor="middle"
          >
            {e.label.split("\n").map((line, li) => (
              <tspan key={li} x={x} dy={li === 0 ? 0 : 15}>
                {line}
              </tspan>
            ))}
          </text>
        </g>
      );
    });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <OffthreadVideo
        src={staticFile("pantheon-ep2-ai-backgrounds/S11-tracks-bg.mp4")}
        loop
        muted
        style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: 0.45 }}
      />
      <div
        style={{
          position: "absolute",
          top: height * 0.06,
          width: "100%",
          textAlign: "center",
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 2,
          color: theme.colors.textFaint,
          opacity: titleOpacity,
        }}
      >
        12,000 YEARS AGO → 3,000 YEARS AGO
      </div>

      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* old model track */}
        <line
          x1={margin}
          y1={oldTrackY}
          x2={margin + trackW * oldLineDraw}
          y2={oldTrackY}
          stroke={theme.colors.ashGrayDim}
          strokeWidth={2}
        />
        {renderTrack(OLD_MODEL, oldTrackY, oldLineDraw, theme.colors.ashGray, fps * 0.6)}

        {/* actual track, with the gap highlighted */}
        <line
          x1={margin}
          y1={actualTrackY}
          x2={margin + trackW * actualLineDraw}
          y2={actualTrackY}
          stroke={theme.colors.ashGrayDim}
          strokeWidth={2}
        />
        {/* highlighted gap rectangle between temple and the farming/cities/writing cluster */}
        <rect
          x={yearsAgoToX(11600, width, margin)}
          y={actualTrackY - 26}
          width={yearsAgoToX(6500, width, margin) - yearsAgoToX(11600, width, margin)}
          height={52}
          fill={theme.colors.terracottaDark}
          opacity={gapHighlight * 0.35}
        />
        {renderTrack(ACTUAL, actualTrackY, actualLineDraw, theme.colors.terracotta, fps * 4.2)}
      </svg>

      <div
        style={{
          position: "absolute",
          left: margin,
          top: oldTrackY - 50,
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 1.5,
          color: theme.colors.textFaint,
          opacity: oldLabelOpacity,
        }}
      >
        THE OLD MODEL (ASSUMED SEQUENCE)
      </div>
      <div
        style={{
          position: "absolute",
          left: margin,
          top: actualTrackY - 50,
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 1.5,
          color: theme.colors.terracotta,
          opacity: actualLabelOpacity,
        }}
      >
        WHAT GÖBEKLI TEPE SHOWS
      </div>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.06,
          width: "100%",
          textAlign: "center",
          fontFamily: theme.font.display,
          fontSize: 22,
          color: theme.colors.text,
          opacity: calloutOpacity,
        }}
      >
        Here, the temple came first.
      </div>
    </AbsoluteFill>
  );
};
