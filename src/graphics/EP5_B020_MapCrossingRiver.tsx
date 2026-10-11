import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { DANUBE_PATH } from "./ep5-map-data";

// Seven crossing points sampled along the real Danube frontier path, north
// bank (free Gothic lands) -> south (Roman territory).
const CROSSERS = [
  { x: 860, midY: 486, delay: 0 },
  { x: 910, midY: 483, delay: 4 },
  { x: 960, midY: 495, delay: 8 },
  { x: 1010, midY: 515, delay: 12 },
  { x: 1060, midY: 530, delay: 16 },
  { x: 1110, midY: 540, delay: 20 },
  { x: 1160, midY: 555, delay: 24 },
];

// MG3 phase 1-2: a wave of small refugee-wagon icons crosses the river into
// Roman territory; the icons flip from pale (refugee) to a weapon icon
// (armed), rippling outward.
export const EP5_B020_MapCrossingRiver: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const mapReveal = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const riverDraw = interpolate(frame, [fps * 0.2, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="full" opacity={mapReveal} />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path
          d={DANUBE_PATH}
          fill="none"
          stroke={themeEp5.colors.goldLight}
          strokeWidth={5}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - riverDraw}
        />
        <text x={880} y={465} fontFamily={themeEp5.font.body} fontStyle="italic" fontSize={18} fill={themeEp5.colors.textDim} opacity={riverDraw}>
          Danuvius
        </text>

        {CROSSERS.map((c, i) => {
          const localFrame = Math.max(0, frame - c.delay - fps * 0.5);
          const crossT = interpolate(localFrame, [0, fps * 1.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const flipT = interpolate(localFrame, [fps * 1.6, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const y = c.midY - 40 + 80 * crossT;
          const opacity = interpolate(localFrame, [0, fps * 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <g key={i} opacity={opacity} transform={`translate(${c.x},${y})`}>
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
