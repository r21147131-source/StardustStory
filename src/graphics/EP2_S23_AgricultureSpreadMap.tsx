import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Broader Fertile Crescent outline, with expanding rings radiating outward
// from the Taş Tepeler origin point to suggest agriculture's spread.
const CRESCENT_PATH =
  "M140,300 C160,200 260,130 380,120 C480,90 620,90 720,130 " +
  "C820,120 900,180 880,260 C920,300 900,370 830,390 " +
  "C760,440 640,450 540,410 C460,450 340,440 280,390 " +
  "C200,410 130,370 140,300 Z";

const ORIGIN = { x: 430, y: 220 };

export const EP2_S23_AgricultureSpreadMap: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const mapIn = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: "clamp" });
  const originIn = interpolate(frame, [fps * 0.5, fps * 1.0], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const rings = [0, 1, 2].map((i) => {
    const t = interpolate(frame, [fps * (1.4 + i * 1.0), fps * (1.4 + i * 1.0 + 5.5)], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
    return { r: interpolate(t, [0, 1], [10, 520]), opacity: interpolate(t, [0, 0.15, 1], [0, 0.55, 0]) };
  });

  const labelOpacity = interpolate(frame, [fps * 5.5, fps * 6.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 550" width={width * 0.78} height={height * 0.68}>
        <defs>
          <clipPath id="agclip">
            <path d={CRESCENT_PATH} />
          </clipPath>
        </defs>
        <path d={CRESCENT_PATH} fill={theme.colors.ashGrayDark} opacity={mapIn} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />

        <g clipPath="url(#agclip)">
          {rings.map((r, i) => (
            <circle key={i} cx={ORIGIN.x} cy={ORIGIN.y} r={r.r} fill="none" stroke={theme.colors.terracotta} strokeWidth={3} opacity={r.opacity} />
          ))}
        </g>

        <circle cx={ORIGIN.x} cy={ORIGIN.y} r={10 * originIn} fill={theme.colors.terracotta} />
        <text
          x={ORIGIN.x}
          y={ORIGIN.y - 24}
          fill={theme.colors.text}
          fontFamily={theme.font.display}
          fontSize={16}
          textAnchor="middle"
          opacity={originIn}
        >
          Taş Tepeler
        </text>
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.1,
          width: "100%",
          textAlign: "center",
          opacity: labelOpacity,
          fontFamily: theme.font.body,
          fontSize: 15,
          letterSpacing: 1.5,
          color: theme.colors.textFaint,
        }}
      >
        AGRICULTURE SPREADING OUTWARD ACROSS THE FERTILE CRESCENT
      </div>
    </AbsoluteFill>
  );
};
