import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, EGYPT_BAND_Y, KUSH_BAND_Y, CITY_POS } from "./ep4-map-data";

// MG1 Phase 4: ALARA, then KASHTA carve in; an arrow reaches from Napata to Upper Egypt.
export const EP4_B022_MapAlaraKashta: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const alaraOpacity = interpolate(frame, [fps * 0.3, fps * 1.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const kashtaOpacity = interpolate(frame, [fps * 2.2, fps * 3.2], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const arrowDraw = interpolate(frame, [fps * 4.5, fps * 7.5], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const napata = CITY_POS.napata;
  const thebes = CITY_POS.thebes;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <marker id="arrowheadB022" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill={themeEp4.colors.ember} />
          </marker>
        </defs>

        <rect x={600} y={EGYPT_BAND_Y[0]} width={500} height={EGYPT_BAND_Y[1] - EGYPT_BAND_Y[0]} fill={themeEp4.colors.goldDim} opacity={0.25} />
        <rect x={600} y={560} width={500} height={KUSH_BAND_Y[1] - 560} fill={themeEp4.colors.ember} opacity={0.4} />

        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldLight} strokeWidth={5} strokeLinecap="round" />

        <circle cx={napata.x} cy={napata.y} r={9} fill={themeEp4.colors.goldLight} />
        <circle cx={thebes.x} cy={thebes.y} r={6} fill={themeEp4.colors.textFaint} opacity={0.6} />

        <path
          d={`M ${napata.x - 15},${napata.y - 15} L ${thebes.x + 20},${thebes.y + 15}`}
          fill="none"
          stroke={themeEp4.colors.ember}
          strokeWidth={4}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - arrowDraw}
          markerEnd="url(#arrowheadB022)"
        />
      </svg>

      <div
        style={{
          position: "absolute",
          left: napata.x - 140,
          top: napata.y + 30,
          width: 280,
          textAlign: "center",
          fontFamily: themeEp4.font.display,
          fontSize: 26,
          letterSpacing: 3,
          color: themeEp4.colors.gold,
          opacity: alaraOpacity,
        }}
      >
        ALARA
      </div>
      <div
        style={{
          position: "absolute",
          left: napata.x - 140,
          top: napata.y + 70,
          width: 280,
          textAlign: "center",
          fontFamily: themeEp4.font.display,
          fontSize: 26,
          letterSpacing: 3,
          color: themeEp4.colors.goldLight,
          opacity: kashtaOpacity,
        }}
      >
        KASHTA
      </div>
    </AbsoluteFill>
  );
};
