import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { themeEp5 as _t } from "../theme-ep5";
import { DANUBE_PATH } from "./ep5-map-data";

// Seven crossing points sampled along the Danube path, north bank -> south.
const CROSSERS = [
  { startX: 690, startY: 395, endX: 705, endY: 445, delay: 0 },
  { startX: 740, startY: 390, endX: 755, endY: 440, delay: 4 },
  { startX: 790, startY: 395, endX: 805, endY: 445, delay: 8 },
  { startX: 840, startY: 410, endX: 850, endY: 455, delay: 12 },
  { startX: 890, startY: 420, endX: 900, endY: 465, delay: 16 },
  { startX: 940, startY: 435, endX: 950, endY: 478, delay: 20 },
  { startX: 985, startY: 450, endX: 995, endY: 488, delay: 24 },
];

// MG3 phase 1-2: a wave of small refugee-wagon icons crosses the river into
// Roman territory; the icons flip from pale (refugee) to a weapon icon
// (armed), rippling outward.
export const EP5_B020_MapCrossingRiver: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const riverDraw = interpolate(frame, [0, fps * 0.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <svg width={1920} height={1080} viewBox="550 300 650 350" style={{ position: "absolute", width: "100%", height: "100%" }}>
        <rect x={550} y={300} width={650} height={350} fill={_t.colors.crimson} opacity={0.06} />
        <path
          d={DANUBE_PATH}
          fill="none"
          stroke={themeEp5.colors.goldLight}
          strokeWidth={6}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - riverDraw}
        />
        <text x={720} y={380} fontFamily={themeEp5.font.body} fontStyle="italic" fontSize={20} fill={themeEp5.colors.textDim} opacity={riverDraw}>
          Danuvius
        </text>

        {CROSSERS.map((c, i) => {
          const localFrame = Math.max(0, frame - c.delay - fps * 0.5);
          const crossT = interpolate(localFrame, [0, fps * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const flipT = interpolate(localFrame, [fps * 1.6, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const x = c.startX + (c.endX - c.startX) * crossT;
          const y = c.startY + (c.endY - c.startY) * crossT;
          const opacity = interpolate(localFrame, [0, fps * 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <g key={i} opacity={opacity} transform={`translate(${x},${y})`}>
              {/* pale refugee wagon icon, fading out as it flips */}
              <g opacity={1 - flipT}>
                <rect x={-7} y={-4} width={14} height={8} rx={2} fill={themeEp5.colors.textFaint} />
                <circle cx={-5} cy={5} r={2.5} fill={themeEp5.colors.textFaint} />
                <circle cx={5} cy={5} r={2.5} fill={themeEp5.colors.textFaint} />
              </g>
              {/* armed weapon icon, fading in */}
              <g opacity={flipT}>
                <path d="M 0,-9 L 3,0 L 0,9 L -3,0 Z" fill={themeEp5.colors.crimsonLight} />
              </g>
              {/* ripple ring at the moment of flip */}
              <circle r={14 * flipT} fill="none" stroke={themeEp5.colors.crimsonLight} strokeWidth={1.5} opacity={(1 - flipT) * 0.7} />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
