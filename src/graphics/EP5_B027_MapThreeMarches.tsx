import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { MARCH_LOOP_1, MARCH_LOOP_2, MARCH_LOOP_3, CITY_POS } from "./ep5-map-data";

// MG5 phase 1: Three Marches, One Sack. An army icon wanders through the
// Balkans and Greece over several loops, a faint trail marking two decades
// of movement.
export const EP5_B027_MapThreeMarches: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const loop1 = interpolate(frame, [fps * 0.3, fps * 4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const loop2 = interpolate(frame, [fps * 4, fps * 7.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const loop3 = interpolate(frame, [fps * 7.5, fps * 11], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const caption = interpolate(frame, [fps * 11.2, fps * 12.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const r = CITY_POS.roma;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <circle cx={r.x} cy={r.y} r={10} fill={themeEp5.colors.goldLight} />
        <text x={r.x + 16} y={r.y + 5} fontFamily={themeEp5.font.display} fontSize={22} letterSpacing={3} fill={themeEp5.colors.goldLight}>
          ROMA
        </text>

        <path d={MARCH_LOOP_1} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6"
          pathLength={1} strokeDashoffset={1 - loop1} opacity={0.75} />
        <path d={MARCH_LOOP_2} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6"
          pathLength={1} strokeDashoffset={1 - loop2} opacity={0.75} />
        <path d={MARCH_LOOP_3} fill="none" stroke={themeEp5.colors.textFaint} strokeWidth={2.5} strokeDasharray="8 6"
          pathLength={1} strokeDashoffset={1 - loop3} opacity={0.75} />
      </svg>

      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 110,
          textAlign: "center",
          fontFamily: themeEp5.font.body,
          fontStyle: "italic",
          fontSize: 26,
          color: themeEp5.colors.textDim,
          opacity: caption,
        }}
      >
        twenty years, searching for a settlement Rome never honored
      </div>
    </AbsoluteFill>
  );
};
