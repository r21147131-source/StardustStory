import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, EGYPT_BAND_Y, KUSH_BAND_Y, MAP_BOX } from "./ep4-map-data";
import { Ep4RealMapBackground } from "./Ep4RealMapBackground";

// MG1 Phase 1: Egypt in the north (gold-filled), Kush in the south (outlined only).
export const EP4_B008_MapEgyptKush: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const riverDraw = interpolate(frame, [0, fps * 1.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const egyptFill = interpolate(frame, [fps * 1.2, fps * 2.4], [0, 0.55], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const kushOutline = interpolate(frame, [fps * 1.8, fps * 3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(frame, [fps * 2.2, fps * 3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <Ep4RealMapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <clipPath id="egyptBand">
            <rect x={0} y={EGYPT_BAND_Y[0]} width={width} height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]} />
          </clipPath>
          <clipPath id="kushBand">
            <rect x={0} y={KUSH_BAND_Y[0]} width={width} height={KUSH_BAND_Y[1] - KUSH_BAND_Y[0]} />
          </clipPath>
        </defs>

        <rect
          x={MAP_BOX.x}
          y={EGYPT_BAND_Y[0]}
          width={MAP_BOX.width}
          height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]}
          fill={themeEp4.colors.gold}
          opacity={egyptFill}
        />
        <rect
          x={MAP_BOX.x}
          y={KUSH_BAND_Y[0]}
          width={MAP_BOX.width}
          height={KUSH_BAND_Y[1] - KUSH_BAND_Y[0]}
          fill="none"
          stroke={themeEp4.colors.ember}
          strokeWidth={3}
          strokeDasharray="10 8"
          opacity={kushOutline}
        />

        <path
          d={RIVER_PATH}
          fill="none"
          stroke={themeEp4.colors.goldLight}
          strokeWidth={5}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - riverDraw}
        />
      </svg>

      <div
        style={{
          position: "absolute",
          left: 740,
          top: EGYPT_BAND_Y[0] + 40,
          fontFamily: themeEp4.font.display,
          fontSize: 34,
          letterSpacing: 6,
          color: themeEp4.colors.bg,
          fontWeight: 700,
          opacity: labelOpacity,
        }}
      >
        EGYPT
      </div>
      <div
        style={{
          position: "absolute",
          left: 700,
          top: KUSH_BAND_Y[1] - 90,
          fontFamily: themeEp4.font.display,
          fontSize: 34,
          letterSpacing: 6,
          color: themeEp4.colors.ember,
          fontWeight: 700,
          opacity: labelOpacity,
        }}
      >
        KUSH
      </div>
    </AbsoluteFill>
  );
};
