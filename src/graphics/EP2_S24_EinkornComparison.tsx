import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Simple diagrammatic wheat spike: a stem with spikelets. Wild einkorn's
// rachis (stem) is brittle and shatters at a joint; domesticated stays whole.
const SPIKELET_COUNT = 7;

const Spike: React.FC<{ cx: number; shatter: number; color: string }> = ({ cx, shatter, color }) => {
  const stemTop = 120;
  const stemBottom = 360;
  const breakY = stemTop + (stemBottom - stemTop) * 0.55;
  const breakOffset = shatter * 50;
  const breakRotate = shatter * 28;

  const spikelets = Array.from({ length: SPIKELET_COUNT }, (_, i) => {
    const frac = i / (SPIKELET_COUNT - 1);
    const y = stemTop + 20 + frac * (stemBottom - stemTop - 40);
    const below = y > breakY;
    const dy = below ? breakOffset : 0;
    const side = i % 2 === 0 ? -1 : 1;
    return { y: y + dy, side, below };
  });

  return (
    <g>
      {/* upper stem segment (always fixed) */}
      <line x1={cx} y1={stemTop} x2={cx} y2={breakY} stroke={color} strokeWidth={3} />
      {/* lower stem segment, rotates/falls away when shattered */}
      <g
        transform={`translate(${cx}, ${breakY}) rotate(${breakRotate}) translate(${-cx}, ${-breakY})`}
        style={{ transformOrigin: `${cx}px ${breakY}px` }}
      >
        <line x1={cx} y1={breakY} x2={cx} y2={stemBottom + breakOffset} stroke={color} strokeWidth={3} />
      </g>
      {spikelets.map((s, i) => {
        const x = cx + s.side * 26;
        const rotate = s.below ? breakRotate : 0;
        return (
          <g
            key={i}
            transform={s.below ? `translate(${cx}, ${breakY}) rotate(${rotate}) translate(${-cx}, ${-breakY})` : undefined}
          >
            <ellipse cx={x} cy={s.y} rx={16} ry={9} fill="none" stroke={color} strokeWidth={2} transform={`rotate(${s.side * 20}, ${x}, ${s.y})`} />
          </g>
        );
      })}
    </g>
  );
};

export const EP2_S24_EinkornComparison: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const panelsIn = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateRight: "clamp" });
  const shatter = interpolate(frame, [fps * 2.5, fps * 4.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(frame, [fps * 1.0, fps * 1.6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const mechanismOpacity = interpolate(frame, [fps * 3.2, fps * 3.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const footerOpacity = interpolate(frame, [fps * 5.5, fps * 6.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }} opacity={panelsIn}>
        <line x1={width / 2} y1={height * 0.14} x2={width / 2} y2={height * 0.78} stroke={theme.colors.ashGrayDark} strokeWidth={1} />
        <g transform={`translate(0, ${height * 0.1})`}>
          <Spike cx={width * 0.27} shatter={shatter} color={theme.colors.terracotta} />
        </g>
        <g transform={`translate(0, ${height * 0.1})`}>
          <Spike cx={width * 0.73} shatter={0} color={theme.colors.glacialBlue} />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          left: 0,
          top: height * 0.14,
          width: "50%",
          textAlign: "center",
          opacity: labelOpacity,
          fontFamily: theme.font.display,
          fontSize: 22,
          color: theme.colors.terracotta,
          letterSpacing: 1,
        }}
      >
        WILD EINKORN
      </div>
      <div
        style={{
          position: "absolute",
          right: 0,
          top: height * 0.14,
          width: "50%",
          textAlign: "center",
          opacity: labelOpacity,
          fontFamily: theme.font.display,
          fontSize: 22,
          color: theme.colors.glacialBlue,
          letterSpacing: 1,
        }}
      >
        DOMESTICATED EINKORN
      </div>

      <div
        style={{
          position: "absolute",
          left: 0,
          bottom: height * 0.2,
          width: "50%",
          textAlign: "center",
          opacity: mechanismOpacity,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textDim,
        }}
      >
        brittle rachis — shatters, scatters seed
      </div>
      <div
        style={{
          position: "absolute",
          right: 0,
          bottom: height * 0.2,
          width: "50%",
          textAlign: "center",
          opacity: mechanismOpacity,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textDim,
        }}
      >
        non-brittle rachis — ear stays intact
      </div>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.07,
          width: "100%",
          textAlign: "center",
          opacity: footerOpacity,
          fontFamily: theme.font.body,
          fontSize: 14,
          letterSpacing: 1.5,
          color: theme.colors.textFaint,
        }}
      >
        DOMESTICATION TRACED TO THE KARACADAĞ MOUNTAINS, SE TURKEY
      </div>
    </AbsoluteFill>
  );
};
