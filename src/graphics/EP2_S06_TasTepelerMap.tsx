import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Simplified schematic outline of the Taş Tepeler region (SE Anatolia / N Syria).
const REGION_PATH =
  "M160,180 C220,120 340,100 440,130 C520,100 620,110 680,160 " +
  "C740,150 800,190 790,250 C840,260 860,320 810,360 " +
  "C760,410 660,420 580,390 C500,430 390,420 330,380 " +
  "C250,400 170,370 150,300 C120,270 120,220 160,180 Z";

const SITES = [
  { name: "Göbekli Tepe", x: 420, y: 230, delay: 0 },
  { name: "Karahan Tepe", x: 540, y: 270, delay: 0.6 },
  { name: "Nevalı Çori", x: 320, y: 300, delay: 1.2 },
];

export const EP2_S06_TasTepelerMap: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const mapIn = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: "clamp" });
  const labelOpacity = interpolate(frame, [fps * 3.6, fps * 4.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 500" width={width * 0.75} height={height * 0.6}>
        <path d={REGION_PATH} fill={theme.colors.ashGrayDark} opacity={mapIn} stroke={theme.colors.ashGrayDim} strokeWidth={1.5} />

        {SITES.map((s) => {
          const pinIn = spring({ frame: frame - fps * (0.6 + s.delay), fps, config: { damping: 15 } });
          const textOpacity = interpolate(frame, [fps * (1.0 + s.delay), fps * (1.4 + s.delay)], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <g key={s.name}>
              <circle
                cx={s.x}
                cy={s.y}
                r={9 * pinIn}
                fill={s.name === "Göbekli Tepe" ? theme.colors.terracotta : theme.colors.glacialBlue}
              />
              <circle
                cx={s.x}
                cy={s.y}
                r={18 * pinIn}
                fill="none"
                stroke={s.name === "Göbekli Tepe" ? theme.colors.terracotta : theme.colors.glacialBlue}
                strokeWidth={1.5}
                opacity={0.5}
              />
              <text
                x={s.x}
                y={s.y - 24}
                fill={theme.colors.text}
                fontFamily={theme.font.display}
                fontSize={18}
                textAnchor="middle"
                opacity={textOpacity}
              >
                {s.name}
              </text>
            </g>
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.14,
          opacity: labelOpacity,
          textAlign: "center",
          fontFamily: theme.font.body,
          fontSize: 15,
          letterSpacing: 1.5,
          color: theme.colors.textFaint,
        }}
      >
        THE TAŞ TEPELER CLUSTER · SOUTHEASTERN ANATOLIA
      </div>
    </AbsoluteFill>
  );
};
