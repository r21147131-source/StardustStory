import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, EGYPT_BAND_Y, KUSH_BAND_Y } from "./ep4-map-data";

// MG1 Phase 2: Egypt's gold fill splinters into rival fragments. Date c. 1070 BCE.
const FRACTURE_LINES = [
  "M 600,180 L 1100,220",
  "M 650,320 L 1050,300",
  "M 620,420 L 1080,440",
  "M 680,560 L 1020,540",
  "M 630,650 L 1070,680",
];

export const EP4_B017_MapEgyptCracks: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const egyptFill = 0.55;
  const crackProgress = interpolate(frame, [fps * 0.3, fps * 2.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const jitter = interpolate(frame, [fps * 2.2, fps * 3], [0, 6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const dateOpacity = interpolate(frame, [fps * 3.2, fps * 4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <clipPath id="egyptBand2">
            <rect x={0} y={EGYPT_BAND_Y[0]} width={width} height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]} />
          </clipPath>
        </defs>

        <g style={{ transform: `translate(${jitter}px, 0)` }}>
          <rect
            x={600}
            y={EGYPT_BAND_Y[0]}
            width={500}
            height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]}
            fill={themeEp4.colors.goldDim}
            opacity={egyptFill}
          />
        </g>
        <rect
          x={600}
          y={KUSH_BAND_Y[0]}
          width={500}
          height={KUSH_BAND_Y[1] - KUSH_BAND_Y[0]}
          fill="none"
          stroke={themeEp4.colors.ember}
          strokeWidth={3}
          strokeDasharray="10 8"
          opacity={0.5}
        />

        <g clipPath="url(#egyptBand2)">
          {FRACTURE_LINES.map((d, i) => (
            <path
              key={i}
              d={d}
              fill="none"
              stroke={themeEp4.colors.bg}
              strokeWidth={10}
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - Math.min(1, Math.max(0, crackProgress - i * 0.08))}
            />
          ))}
        </g>

        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldLight} strokeWidth={5} strokeLinecap="round" />
      </svg>

      <div
        style={{
          position: "absolute",
          left: 740,
          top: EGYPT_BAND_Y[0] + 40,
          fontFamily: themeEp4.font.display,
          fontSize: 34,
          letterSpacing: 6,
          color: themeEp4.colors.cream,
        }}
      >
        EGYPT
      </div>
      <div
        style={{
          position: "absolute",
          bottom: height * 0.08,
          width: "100%",
          textAlign: "center",
          fontFamily: themeEp4.font.body,
          fontStyle: "italic",
          fontSize: 26,
          color: themeEp4.colors.goldLight,
          opacity: dateOpacity,
        }}
      >
        c. 1070 BCE
      </div>
    </AbsoluteFill>
  );
};
