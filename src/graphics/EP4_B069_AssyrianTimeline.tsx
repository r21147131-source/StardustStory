import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG5 Phase 2: timeline of Assyrian campaigns. 671 stamp, Esarhaddon's route ends
// mid-way, Ashurbanipal enters, strip ends on 664.
const MARKS = [
  { x: 0.15, year: "671", label: "Esarhaddon takes Memphis" },
  { x: 0.42, year: "", label: "Esarhaddon dies on the road" },
  { x: 0.68, year: "", label: "Ashurbanipal" },
  { x: 0.92, year: "664", label: "Taharqa dies at Napata" },
];

export const EP4_B069_AssyrianTimeline: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const lineY = height / 2;
  const left = width * 0.08;
  const right = width * 0.92;

  const lineDraw = interpolate(frame, [0, fps * 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <line
          x1={left}
          y1={lineY}
          x2={left + (right - left) * lineDraw}
          y2={lineY}
          stroke={themeEp4.colors.goldDim}
          strokeWidth={3}
        />
        {MARKS.map((m, i) => {
          const markFrame = fps * (0.8 + i * 1.6);
          const markOpacity = interpolate(frame, [markFrame, markFrame + fps * 0.6], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const x = left + (right - left) * m.x;
          const dead = i === 1; // Esarhaddon's route ends mid-way
          return (
            <g key={i} opacity={markOpacity}>
              <circle cx={x} cy={lineY} r={7} fill={dead ? themeEp4.colors.textFaint : themeEp4.colors.ember} />
              {dead && (
                <line x1={x - 10} y1={lineY - 10} x2={x + 10} y2={lineY + 10} stroke={themeEp4.colors.textFaint} strokeWidth={2} />
              )}
            </g>
          );
        })}
      </svg>

      {MARKS.map((m, i) => {
        const markFrame = fps * (0.8 + i * 1.6);
        const markOpacity = interpolate(frame, [markFrame + fps * 0.2, markFrame + fps * 0.8], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });
        const x = left + (right - left) * m.x;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: x - 130,
              top: lineY + 26,
              width: 260,
              textAlign: "center",
              opacity: markOpacity,
            }}
          >
            {m.year && (
              <div style={{ fontFamily: themeEp4.font.body, fontStyle: "italic", fontSize: 20, color: themeEp4.colors.goldLight }}>
                {m.year} BCE
              </div>
            )}
            <div style={{ fontFamily: themeEp4.font.body, fontSize: 16, color: themeEp4.colors.textDim, marginTop: 4 }}>
              {m.label}
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
