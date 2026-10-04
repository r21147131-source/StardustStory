import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, CITY_POS } from "./ep4-map-data";
import { Ep4RealMapBackground } from "./Ep4RealMapBackground";

// MG2 Phase 3: the army arrow runs from Napata north; Piye's own arrow follows.
export const EP4_B030_MapArmyFollowsPiye: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const napata = CITY_POS.napata;
  const thebes = CITY_POS.thebes;

  const armyDraw = interpolate(frame, [0, fps * 1.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const piyeDraw = interpolate(frame, [fps * 1.8, fps * 3.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <Ep4RealMapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <marker id="arrowB030a" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill={themeEp4.colors.goldLight} />
          </marker>
          <marker id="arrowB030b" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill={themeEp4.colors.gold} />
          </marker>
        </defs>
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldDim} strokeWidth={4} strokeLinecap="round" opacity={0.6} />

        <circle cx={napata.x} cy={napata.y} r={9} fill={themeEp4.colors.goldLight} />
        <text x={napata.x - 110} y={napata.y + 5} fill={themeEp4.colors.text} fontFamily={themeEp4.font.body} fontSize={20}>
          Napata
        </text>

        <path
          d={`M ${napata.x - 10},${napata.y - 15} L ${thebes.x + 15},${thebes.y + 10}`}
          fill="none"
          stroke={themeEp4.colors.goldLight}
          strokeWidth={5}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - armyDraw}
          markerEnd="url(#arrowB030a)"
        />
        <path
          d={`M ${napata.x + 15},${napata.y - 5} L ${thebes.x + 40},${thebes.y + 25}`}
          fill="none"
          stroke={themeEp4.colors.gold}
          strokeWidth={3}
          strokeDasharray="6 5"
          pathLength={1}
          strokeDashoffset={1 - piyeDraw}
          markerEnd="url(#arrowB030b)"
          opacity={piyeDraw}
        />
      </svg>
    </AbsoluteFill>
  );
};
