import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const STATS = [
  { label: "GÖBEKLI TEPE", value: "earliest enclosures, c. 9600 BCE" },
  { label: "PREDATES", value: "pottery, writing, the wheel, agriculture (this region)" },
  { label: "SCALE", value: "20+ enclosures identified; most still unexcavated" },
  { label: "EINKORN WHEAT", value: "domesticated within centuries, Karacadağ hills" },
];

export const EP2_S28_ClosingStatCard: React.FC = () => {
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
              borderLeft: `3px solid ${theme.colors.glacialBlue}`,
              paddingLeft: 24,
            }}
          >
            <div style={{ fontFamily: theme.font.body, fontSize: 14, letterSpacing: 2, color: theme.colors.textFaint }}>
              {s.label}
            </div>
            <div style={{ fontFamily: theme.font.display, fontSize: 28, color: theme.colors.text, marginTop: 4 }}>
              {s.value}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
