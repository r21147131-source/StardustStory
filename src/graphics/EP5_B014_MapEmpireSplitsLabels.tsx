import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { CITY_POS } from "./ep5-map-data";

const SEAM_X = 870;

// MG2 phase 4 (continuation of B013): both halves are labeled ROMA, then the
// western label flickers and fades while the eastern one holds steady.
export const EP5_B014_MapEmpireSplitsLabels: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const labelsIn = interpolate(frame, [fps * 0.2, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const flicker = Math.abs(Math.sin(frame / 2.3));
  const westFlicker = interpolate(frame, [fps * 1.6, fps * 3.2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) * (0.4 + 0.6 * flicker);
  const westFinal = interpolate(frame, [fps * 3.2, fps * 4], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const c = CITY_POS.constantinopolis;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground fillOpacity={0.08} />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <rect x={0} y={120} width={SEAM_X} height={760} fill={themeEp5.colors.crimson} opacity={0.16 * westFinal} />
        <rect x={SEAM_X} y={120} width={width - SEAM_X} height={760} fill={themeEp5.colors.gold} opacity={0.4} />
        <line x1={SEAM_X} y1={120} x2={SEAM_X} y2={880} stroke={themeEp5.colors.goldLight} strokeWidth={2} opacity={0.8} />

        <g>
          <rect x={c.x - 16} y={c.y - 14} width={32} height={24} fill="none" stroke={themeEp5.colors.goldLight} strokeWidth={3} />
          <rect x={c.x - 22} y={c.y - 22} width={6} height={10} fill={themeEp5.colors.goldLight} />
          <rect x={c.x + 16} y={c.y - 22} width={6} height={10} fill={themeEp5.colors.goldLight} />
          <rect x={c.x - 3} y={c.y - 24} width={6} height={12} fill={themeEp5.colors.goldLight} />
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          left: 220,
          top: 480,
          fontFamily: themeEp5.font.display,
          fontSize: 56,
          letterSpacing: 10,
          color: themeEp5.colors.crimsonLight,
          opacity: labelsIn * westFlicker,
        }}
      >
        ROMA
      </div>
      <div
        style={{
          position: "absolute",
          left: 1120,
          top: 480,
          fontFamily: themeEp5.font.display,
          fontSize: 56,
          letterSpacing: 10,
          color: themeEp5.colors.goldLight,
          opacity: labelsIn,
        }}
      >
        ROMA
      </div>
    </AbsoluteFill>
  );
};
