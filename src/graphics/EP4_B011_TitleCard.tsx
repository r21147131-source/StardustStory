import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG6 title card: a hollow cartouche on dark stone; the title carves itself in beside it.
export const EP4_B011_TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const cx = width * 0.3;
  const cy = height / 2;
  const w = 220;
  const h = 320;

  const ovalDraw = interpolate(frame, [0, fps * 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const titleDraw = interpolate(frame, [fps * 0.8, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <rect
          x={cx - w / 2}
          y={cy - h / 2}
          width={w}
          height={h}
          rx={w / 2}
          fill="none"
          stroke={themeEp4.colors.goldDim}
          strokeWidth={5}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - ovalDraw}
        />
        <line
          x1={cx - w / 2 - 20}
          y1={cy + h / 2 + 10}
          x2={cx + w / 2 + 20}
          y2={cy + h / 2 + 10}
          stroke={themeEp4.colors.goldDim}
          strokeWidth={5}
          opacity={ovalDraw}
        />
      </svg>

      <div
        style={{
          position: "absolute",
          left: cx + w / 2 + 70,
          top: cy - 100,
          width: width * 0.5,
          opacity: titleDraw,
        }}
      >
        <div style={{ fontFamily: themeEp4.font.display, fontSize: 44, lineHeight: 1.25, color: themeEp4.colors.goldLight }}>
          The Pharaohs
          <br />
          Egypt Tried to Erase
        </div>
      </div>
    </AbsoluteFill>
  );
};
