import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { MARCH_LOOP_1, MARCH_LOOP_2, MARCH_LOOP_3, MARCH_FINAL, CITY_POS } from "./ep5-map-data";

// MG5 phase 2-3 (continuation of B027): the first three march-lines toward
// Rome fade out one by one (dotted, failing). A fourth line runs solid and
// unbroken to the city, and the date 410 CE stamps in large.
export const EP5_B030_MapFourthMarch: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const oldFade = interpolate(frame, [0, fps * 1.2], [0.75, 0.12], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const finalDraw = interpolate(frame, [fps * 0.5, fps * 2.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dateOpacity = interpolate(frame, [fps * 2.6, fps * 3.4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const r = CITY_POS.roma;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path d={MARCH_LOOP_1} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6" opacity={oldFade} />
        <path d={MARCH_LOOP_2} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6" opacity={oldFade} />
        <path d={MARCH_LOOP_3} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6" opacity={oldFade} />

        <path
          d={MARCH_FINAL}
          fill="none"
          stroke={themeEp5.colors.crimsonLight}
          strokeWidth={4}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - finalDraw}
        />
        <circle cx={r.x} cy={r.y} r={10} fill={themeEp5.colors.goldLight} />
        <text x={r.x + 16} y={r.y + 5} fontFamily={themeEp5.font.display} fontSize={22} letterSpacing={3} fill={themeEp5.colors.goldLight}>
          ROMA
        </text>
      </svg>

      <div
        style={{
          position: "absolute",
          left: "50%",
          top: 160,
          transform: "translateX(-50%)",
          fontFamily: themeEp5.font.display,
          fontSize: 56,
          letterSpacing: 8,
          color: themeEp5.colors.crimsonLight,
          opacity: dateOpacity,
        }}
      >
        410 CE
      </div>
    </AbsoluteFill>
  );
};
