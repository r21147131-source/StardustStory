import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { CITY_POS, MAP_BOX } from "./ep5-map-data";

const SEAM_X = 1040;

// MG2 phase 1-3: the gold fill cracks into two separate fields, East and
// West. A walled-city icon and CONSTANTINOPLE label appear in the east,
// glowing brighter. The western field dims to a duller bronze.
export const EP5_B013_MapEmpireSplits: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const seamDraw = interpolate(frame, [fps * 0.3, fps * 1.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const mapReveal = interpolate(frame, [fps * 0.6, fps * 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const cityOpacity = interpolate(frame, [fps * 4, fps * 5.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const westDim = interpolate(frame, [fps * 7, fps * 9.5], [1, 0.45], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const c = CITY_POS.constantinopolis;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="west" opacity={mapReveal * westDim} />
      <Ep5MapBackground layer="east" opacity={mapReveal} />

      <svg width={width} height={height} style={{ position: "absolute" }}>
        <line
          x1={SEAM_X}
          y1={MAP_BOX.y}
          x2={SEAM_X}
          y2={MAP_BOX.y + MAP_BOX.height}
          stroke={themeEp5.colors.bg}
          strokeWidth={10}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - seamDraw}
        />
        <line
          x1={SEAM_X}
          y1={MAP_BOX.y}
          x2={SEAM_X}
          y2={MAP_BOX.y + MAP_BOX.height}
          stroke={themeEp5.colors.goldLight}
          strokeWidth={2}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - seamDraw}
          opacity={0.8}
        />

        {/* walled-city icon at Constantinople */}
        <g opacity={cityOpacity}>
          <rect x={c.x - 16} y={c.y - 14} width={32} height={24} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={3} />
          <rect x={c.x - 22} y={c.y - 22} width={6} height={10} fill={themeEp5.colors.goldLight} />
          <rect x={c.x + 16} y={c.y - 22} width={6} height={10} fill={themeEp5.colors.goldLight} />
          <rect x={c.x - 3} y={c.y - 24} width={6} height={12} fill={themeEp5.colors.goldLight} />
          <circle cx={c.x} cy={c.y} r={30} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={1.5} opacity={0.5} />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          left: c.x - 160,
          top: c.y + 30,
          width: 320,
          textAlign: "center",
          fontFamily: themeEp5.font.display,
          fontSize: 24,
          letterSpacing: 5,
          color: themeEp5.colors.goldLight,
          opacity: cityOpacity,
        }}
      >
        CONSTANTINOPLE
      </div>
    </AbsoluteFill>
  );
};
