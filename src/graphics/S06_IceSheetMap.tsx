import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Stylized/schematic northern-hemisphere silhouette — not cartographically
// accurate, intended as a documentary-graphic abstraction only.
const LANDMASS_PATH =
  "M120,260 C160,180 260,140 360,150 C420,120 520,110 600,150 C680,120 780,140 820,200 " +
  "C880,190 940,220 950,280 C920,340 840,360 760,340 C700,380 600,400 520,370 " +
  "C440,400 340,390 280,350 C200,360 130,330 120,260 Z";

const POPULATION_DOTS = [
  { x: 300, y: 240 },
  { x: 420, y: 200 },
  { x: 560, y: 230 },
  { x: 680, y: 260 },
  { x: 780, y: 230 },
];

export const S06_IceSheetMap: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const landIn = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateRight: "clamp" });
  const iceIn = interpolate(frame, [fps * 0.3, fps * 1.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const habitableIn = interpolate(frame, [fps * 1.0, fps * 1.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const dotsIn = interpolate(frame, [fps * 1.6, fps * 2.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const pulse = 0.6 + 0.4 * Math.sin(frame / 6);

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 500" width={width * 0.75} height={height * 0.6}>
        <path d={LANDMASS_PATH} fill={theme.colors.ashGrayDark} opacity={landIn} />

        {/* ice sheet extent, upper portion of landmass */}
        <clipPath id="landclip">
          <path d={LANDMASS_PATH} />
        </clipPath>
        <g clipPath="url(#landclip)" opacity={iceIn}>
          <rect x={0} y={100} width={1000} height={140} fill={theme.colors.glacialBlue} opacity={0.75} />
        </g>

        {/* habitable green band */}
        <g clipPath="url(#landclip)" opacity={habitableIn}>
          <rect x={0} y={240} width={1000} height={160} fill="#4a7a5a" opacity={0.35} />
        </g>

        {/* population concentration dots */}
        {POPULATION_DOTS.map((d, i) => (
          <circle
            key={i}
            cx={d.x}
            cy={d.y}
            r={8 * pulse}
            fill={theme.colors.terracotta}
            opacity={dotsIn}
          />
        ))}
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.12,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textFaint,
          letterSpacing: 1,
        }}
      >
        ICE SHEET EXTENT · HABITABLE ZONES · POPULATION CONCENTRATIONS
      </div>
    </AbsoluteFill>
  );
};
