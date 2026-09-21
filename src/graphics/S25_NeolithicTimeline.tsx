import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Simple abstract glyphs (not literal icon assets): a wandering hunter figure
// (circle head + spear line) crossfades into a settlement glyph (roofed hut).
const HunterGlyph: React.FC<{ opacity: number; color: string }> = ({ opacity, color }) => (
  <g opacity={opacity}>
    <circle cx={0} cy={-18} r={6} fill={color} />
    <line x1={0} y1={-12} x2={0} y2={10} stroke={color} strokeWidth={3} />
    <line x1={0} y1={-4} x2={-10} y2={4} stroke={color} strokeWidth={3} />
    <line x1={0} y1={-4} x2={10} y2={4} stroke={color} strokeWidth={3} />
    <line x1={0} y1={10} x2={-8} y2={24} stroke={color} strokeWidth={3} />
    <line x1={0} y1={10} x2={8} y2={24} stroke={color} strokeWidth={3} />
    <line x1={10} y1={-6} x2={22} y2={-20} stroke={color} strokeWidth={2} />
  </g>
);

const SettlementGlyph: React.FC<{ opacity: number; color: string }> = ({ opacity, color }) => (
  <g opacity={opacity}>
    <polygon points="-16,0 0,-20 16,0" fill="none" stroke={color} strokeWidth={3} />
    <rect x={-12} y={0} width={24} height={20} fill="none" stroke={color} strokeWidth={3} />
    <rect x={-4} y={10} width={8} height={10} fill={color} />
  </g>
);

export const S25_NeolithicTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const margin = width * 0.1;
  const barY = height * 0.55;
  const barW = width - margin * 2;

  const drawFrac = interpolate(frame, [fps * 0.2, fps * 2.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const transition = interpolate(frame, [fps * 2.5, fps * 5.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const positions = [0.1, 0.28, 0.46, 0.64, 0.82];

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <line x1={margin} y1={barY} x2={margin + barW * drawFrac} y2={barY} stroke={theme.colors.ashGrayDim} strokeWidth={2} />

        {positions.map((frac, i) => {
          const x = margin + barW * frac;
          if (frac > drawFrac) return null;
          // later positions convert to settlement glyphs sooner (transition sweeps left to right)
          const localTransition = interpolate(transition, [i * 0.15, i * 0.15 + 0.3], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <g key={i} transform={`translate(${x}, ${barY - 30})`}>
              <HunterGlyph opacity={1 - localTransition} color={theme.colors.ashGray} />
              <SettlementGlyph opacity={localTransition} color={theme.colors.terracotta} />
            </g>
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          left: margin,
          top: barY + 30,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textFaint,
        }}
      >
        HUNTER-GATHERER
      </div>
      <div
        style={{
          position: "absolute",
          right: margin,
          top: barY + 30,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textFaint,
        }}
      >
        SETTLED · AGRICULTURAL
      </div>

      <div
        style={{
          position: "absolute",
          top: height * 0.22,
          width: "100%",
          textAlign: "center",
          fontFamily: theme.font.display,
          fontSize: 26,
          color: theme.colors.text,
          opacity: interpolate(frame, [fps * 0.3, fps * 1.0], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        The Younger Dryas Recovery
      </div>
    </AbsoluteFill>
  );
};
