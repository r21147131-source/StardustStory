import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Approximate years-before-present, rounded for a clean illustrative bar chart
// (not a precision claim - matches the script's own relative framing).
const ITEMS = [
  { label: "Stonehenge", years: 5000 },
  { label: "Great Pyramid", years: 4600 },
  { label: "Writing (cuneiform)", years: 5400 },
  { label: "The Wheel", years: 5500 },
  { label: "Pottery (regional)", years: 8000 },
  { label: "Göbekli Tepe", years: 11600, highlight: true },
];

const MAX_YEARS = 12500;

export const EP2_S10_ComparativeTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const margin = width * 0.1;
  const labelW = width * 0.22;
  const chartLeft = margin + labelW;
  const chartW = width - chartLeft - margin * 0.6;
  const rowH = height * 0.12;
  const startY = height * 0.14;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      {ITEMS.map((item, i) => {
        const t = frame - i * fps * 0.35;
        const barFrac = interpolate(t, [0, fps * 1.1], [0, item.years / MAX_YEARS], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const opacity = interpolate(t, [0, fps * 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
        const y = startY + i * rowH;
        const barW = chartW * barFrac;

        return (
          <div key={item.label} style={{ position: "absolute", top: y, left: 0, width: "100%", opacity }}>
            <div
              style={{
                position: "absolute",
                left: margin,
                top: 0,
                width: labelW - 16,
                textAlign: "right",
                fontFamily: theme.font.body,
                fontSize: item.highlight ? 20 : 16,
                color: item.highlight ? theme.colors.text : theme.colors.textDim,
                lineHeight: 1.2,
              }}
            >
              {item.label}
            </div>
            <div
              style={{
                position: "absolute",
                left: chartLeft,
                top: 6,
                width: barW,
                height: rowH * 0.42,
                backgroundColor: item.highlight ? theme.colors.terracotta : theme.colors.glacialBlueDim,
                borderRadius: 2,
              }}
            />
            {barFrac > 0.02 && (
              <div
                style={{
                  position: "absolute",
                  left: chartLeft + barW + 12,
                  top: 2,
                  fontFamily: theme.font.mono,
                  fontSize: 15,
                  color: item.highlight ? theme.colors.terracotta : theme.colors.textFaint,
                }}
              >
                ~{item.years.toLocaleString()} yrs ago
              </div>
            )}
          </div>
        );
      })}

      <div
        style={{
          position: "absolute",
          bottom: height * 0.08,
          width: "100%",
          textAlign: "center",
          fontFamily: theme.font.body,
          fontSize: 15,
          letterSpacing: 1.5,
          color: theme.colors.textFaint,
          opacity: interpolate(frame, [fps * 3.2, fps * 3.8], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        OLDER THAN WRITING · THE WHEEL · POTTERY · THE PYRAMIDS
      </div>
    </AbsoluteFill>
  );
};
