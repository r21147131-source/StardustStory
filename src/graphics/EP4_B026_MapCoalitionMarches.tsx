import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, CITY_POS } from "./ep4-map-data";

// MG2 Phase 1: Delta lords' markers join Sais; a coalition arrow runs south.
const DELTA_LORDS = [
  { x: 640, y: 120 },
  { x: 700, y: 90 },
  { x: 800, y: 110 },
];

export const EP4_B026_MapCoalitionMarches: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const sais = CITY_POS.sais;
  const memphis = CITY_POS.memphis;

  const lordsIn = interpolate(frame, [0, fps * 1.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const arrowDraw = interpolate(frame, [fps * 1.6, fps * 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <defs>
          <marker id="arrowB026" markerWidth="10" markerHeight="10" refX="6" refY="3" orient="auto">
            <path d="M0,0 L6,3 L0,6 Z" fill={themeEp4.colors.ember} />
          </marker>
        </defs>
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldDim} strokeWidth={4} strokeLinecap="round" opacity={0.6} />

        {DELTA_LORDS.map((p, i) => (
          <circle key={i} cx={p.x} cy={p.y} r={7} fill={themeEp4.colors.ember} opacity={lordsIn} />
        ))}
        <circle cx={sais.x} cy={sais.y} r={10} fill={themeEp4.colors.ember} />
        <text x={sais.x + 18} y={sais.y + 5} fill={themeEp4.colors.text} fontFamily={themeEp4.font.body} fontSize={20}>
          Sais
        </text>

        <path
          d={`M ${sais.x},${sais.y + 10} L ${memphis.x - 10},${memphis.y - 10}`}
          fill="none"
          stroke={themeEp4.colors.ember}
          strokeWidth={4}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - arrowDraw}
          markerEnd="url(#arrowB026)"
        />
      </svg>
    </AbsoluteFill>
  );
};
