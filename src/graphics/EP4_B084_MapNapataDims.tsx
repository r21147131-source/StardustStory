import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, CITY_POS } from "./ep4-map-data";
import { Ep4RealMapBackground } from "./Ep4RealMapBackground";

// MG4 contraction: an army arrow runs south to Napata, which dims.
export const EP4_B084_MapNapataDims: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const thebes = CITY_POS.thebes;
  const napata = CITY_POS.napata;

  const riverGlow = interpolate(frame, [0, fps * 0.5], [0.85, 0.85]);
  const arrowDraw = interpolate(frame, [fps * 0.4, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const napataDim = interpolate(frame, [fps * 3.2, fps * 5], [1, 0.15], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <Ep4RealMapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <marker id="arrowB084" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill={themeEp4.colors.textFaint} />
          </marker>
        </defs>
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.gold} strokeWidth={6} strokeLinecap="round" opacity={riverGlow} />

        <path
          d={`M ${thebes.x + 10},${thebes.y + 10} L ${napata.x - 5},${napata.y - 20}`}
          fill="none"
          stroke={themeEp4.colors.textFaint}
          strokeWidth={4}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - arrowDraw}
          markerEnd="url(#arrowB084)"
        />

        <circle cx={napata.x} cy={napata.y} r={10} fill={themeEp4.colors.goldLight} opacity={napataDim} />
        <text x={napata.x - 110} y={napata.y + 5} fill={themeEp4.colors.text} fontFamily={themeEp4.font.body} fontSize={20} opacity={napataDim + 0.3}>
          Napata
        </text>
      </svg>
    </AbsoluteFill>
  );
};
