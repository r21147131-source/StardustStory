import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";
import { Ep5MapBackground } from "./Ep5MapBackground";
import { CITY_POS } from "./ep5-map-data";

// MG2 phase 4 (continuation of B013): both halves are labeled ROMA, then the
// western label flickers and fades while the eastern one holds steady.
export const EP5_B014_MapEmpireSplitsLabels: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const labelsIn = interpolate(frame, [fps * 0.2, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const flicker = Math.abs(Math.sin(frame / 2.3));
  const westFlicker = interpolate(frame, [fps * 1.6, fps * 3.2], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) * (0.4 + 0.6 * flicker);
  const westFinal = interpolate(frame, [fps * 3.2, fps * 4], [1, 0.45], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const roma = CITY_POS.roma;
  const c = CITY_POS.constantinopolis;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg }}>
      <Ep5MapBackground layer="west" opacity={westFinal} />
      <Ep5MapBackground layer="east" opacity={1} />

      <svg width={1920} height={1080} style={{ position: "absolute" }}>
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
          left: roma.x - 90,
          top: roma.y - 70,
          fontFamily: themeEp5.font.display,
          fontSize: 40,
          letterSpacing: 7,
          color: themeEp5.colors.crimsonLight,
          opacity: labelsIn * westFlicker,
        }}
      >
        ROMA
      </div>
      <div
        style={{
          position: "absolute",
          left: c.x - 90,
          top: c.y + 40,
          fontFamily: themeEp5.font.display,
          fontSize: 40,
          letterSpacing: 7,
          color: themeEp5.colors.goldLight,
          opacity: labelsIn,
        }}
      >
        ROMA
      </div>
    </AbsoluteFill>
  );
};
