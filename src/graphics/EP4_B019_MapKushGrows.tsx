import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, EGYPT_BAND_Y, KUSH_BAND_Y, CITY_POS } from "./ep4-map-data";

// MG1 Phase 3: Kush glows warm and widens north; Egypt's rival cities sit dim.
const RIVAL_CITIES: (keyof typeof CITY_POS)[] = ["sais", "memphis", "herakleopolis", "hermopolis", "thebes"];

export const EP4_B019_MapKushGrows: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const kushTop = interpolate(frame, [0, fps * 2.2], [KUSH_BAND_Y[0], 560], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const kushGlow = interpolate(frame, [0, fps * 1.5], [0.3, 0.6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <rect x={600} y={EGYPT_BAND_Y[0]} width={500} height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]} fill={themeEp4.colors.goldDim} opacity={0.25} />
        <rect x={600} y={kushTop} width={500} height={KUSH_BAND_Y[1] - kushTop} fill={themeEp4.colors.ember} opacity={kushGlow} />

        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldLight} strokeWidth={5} strokeLinecap="round" />

        {RIVAL_CITIES.map((key, i) => {
          const c = CITY_POS[key];
          const dotIn = interpolate(frame, [fps * (0.6 + i * 0.3), fps * (1.0 + i * 0.3)], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          return (
            <g key={key} opacity={dotIn * 0.75}>
              <circle cx={c.x} cy={c.y} r={7} fill={themeEp4.colors.textFaint} />
              <text
                x={c.x + 16}
                y={c.y + 5}
                fill={themeEp4.colors.textFaint}
                fontFamily={themeEp4.font.body}
                fontSize={17}
              >
                {c.label}
              </text>
            </g>
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          left: 700,
          top: height * 0.86,
          fontFamily: themeEp4.font.display,
          fontSize: 34,
          letterSpacing: 6,
          color: themeEp4.colors.goldLight,
        }}
      >
        KUSH
      </div>
    </AbsoluteFill>
  );
};
