import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { DANUBE_PATH } from "./ep5-map-data";

// MG3 phase 3-4 (continuation of B020): the converted icons mass into a
// single army marker south of the river; a date stamp 378 CE appears beside
// it.
export const EP5_B021_MapArmyMasses: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const massT = interpolate(frame, [fps * 0.2, fps * 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const dateOpacity = interpolate(frame, [fps * 2.6, fps * 3.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const massX = 1010;
  const massY = 590;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="full" />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path d={DANUBE_PATH} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={5} strokeLinecap="round" opacity={0.7} />

        {/* army marker: a cluster of diamonds converging and settling */}
        {Array.from({ length: 7 }).map((_, i) => {
          const angle = (i / 7) * Math.PI * 2;
          const scatterR = 90;
          const sx = massX + Math.cos(angle) * scatterR;
          const sy = massY + Math.sin(angle) * scatterR * 0.6;
          const x = sx + (massX - sx) * massT;
          const y = sy + (massY - sy) * massT;
          return (
            <path
              key={i}
              d="M 0,-10 L 4,0 L 0,10 L -4,0 Z"
              fill={themeEp5.colors.crimsonLight}
              transform={`translate(${x},${y})`}
            />
          );
        })}
        <circle cx={massX} cy={massY} r={interpolate(massT, [0, 1], [0, 34])} fill="none" stroke={themeEp5.colors.crimsonLight} strokeWidth={2} opacity={massT * 0.6} />
      </svg>

      <div
        style={{
          position: "absolute",
          left: massX + 70,
          top: massY - 20,
          fontFamily: themeEp5.font.display,
          fontSize: 36,
          letterSpacing: 6,
          color: themeEp5.colors.goldLight,
          opacity: dateOpacity,
        }}
      >
        378 CE
      </div>
    </AbsoluteFill>
  );
};
