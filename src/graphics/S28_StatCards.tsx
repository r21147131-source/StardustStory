import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const STATS = [
  { label: "THE YOUNGER DRYAS IMPACT", value: "12,800 years before present" },
  { label: "EXTINCTION EVENT", value: "35+ megafauna genera, North America" },
  { label: "CLIMATE ANOMALY", value: "1,000 years of unexpected glaciation" },
  { label: "HUMAN RESPONSE", value: "The beginning of civilization" },
];

export const S28_StatCards: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const rowH = height * 0.16;
  const startY = height * 0.22;
  const stagger = fps * 1.6;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      {STATS.map((s, i) => {
        const t = frame - i * stagger;
        const enter = spring({ frame: t, fps, config: { damping: 16 } });
        const x = interpolate(enter, [0, 1], [-60, 0]);
        const opacity = interpolate(t, [0, fps * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

        return (
          <div
            key={s.label}
            style={{
              position: "absolute",
              top: startY + i * rowH,
              left: width * 0.1,
              transform: `translateX(${x}px)`,
              opacity,
              borderLeft: `3px solid ${theme.colors.terracotta}`,
              paddingLeft: 24,
            }}
          >
            <div style={{ fontFamily: theme.font.body, fontSize: 14, letterSpacing: 2, color: theme.colors.textFaint }}>
              {s.label}
            </div>
            <div style={{ fontFamily: theme.font.display, fontSize: 30, color: theme.colors.text, marginTop: 4 }}>
              {s.value}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
