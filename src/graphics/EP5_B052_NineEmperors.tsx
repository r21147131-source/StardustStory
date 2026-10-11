import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

const EMPERORS = [
  { reign: "1 yr", struck: false },
  { reign: "4 yr", struck: true },
  { reign: "4 yr", struck: true },
  { reign: "5 yr", struck: true },
  { reign: "7 mo", struck: true },
  { reign: "1 yr", struck: false },
  { reign: "1 yr", struck: true },
  { reign: "1 yr", struck: false },
  { reign: "1 yr", struck: false },
];

// MG8: Nine Emperors, Twenty-One Years. A ticker of nine small
// coin-portrait medallions drops down one by one, each stamped with a
// reign-length; several are struck through with a red/iron mark as they
// land.
export const EP5_B052_NineEmperors: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, fps } = useVideoConfig();

  const n = EMPERORS.length;
  const spacing = (width - 320) / (n - 1);
  const startX = 160;
  const landY = 480;

  const titleOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 140,
          textAlign: "center",
          fontFamily: themeEp5.font.display,
          fontSize: 44,
          letterSpacing: 6,
          color: themeEp5.colors.gold,
          opacity: titleOpacity,
        }}
      >
        NINE EMPERORS, TWENTY-ONE YEARS
      </div>

      <svg width={width} height={1080} style={{ position: "absolute" }}>
        {EMPERORS.map((e, i) => {
          const delay = fps * 0.8 + i * 9;
          const dropT = interpolate(frame, [delay, delay + fps * 0.5], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const y = -80 + (landY - -80) * dropT;
          const x = startX + i * spacing;
          const strikeT = e.struck
            ? interpolate(frame, [delay + fps * 0.6, delay + fps * 1.1], [0, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
              })
            : 0;
          return (
            <g key={i} opacity={dropT}>
              <circle cx={x} cy={y} r={44} fill={themeEp5.colors.stoneLight} stroke={themeEp5.colors.bronze} strokeWidth={3} />
              <circle cx={x} cy={y} r={44} fill="none" stroke={themeEp5.colors.gold} strokeWidth={1} opacity={0.5} />
              <text x={x} y={y + 8} textAnchor="middle" fontFamily={themeEp5.font.display} fontSize={16} fill={themeEp5.colors.textDim}>
                {e.reign}
              </text>
              {e.struck && (
                <line
                  x1={x - 44}
                  y1={y - 30}
                  x2={x - 44 + 88 * strikeT}
                  y2={y - 30 + 60 * strikeT}
                  stroke={themeEp5.colors.crimsonLight}
                  strokeWidth={5}
                />
              )}
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
