import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG-TITLE: THE LAST ROMAN carves itself into a weathered marble slab in
// gold, cracks already running through the stone; then the crack widens and
// a fragment falls away, leaving the title legible but visibly broken.
export const EP5_B006_TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const cx = width / 2;
  const cy = height / 2;

  const slabOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const titleDraw = interpolate(frame, [fps * 0.3, fps * 2.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const crackDraw = interpolate(frame, [fps * 0.5, fps * 1.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const crackWiden = interpolate(frame, [fps * 3, fps * 4.2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fragmentFall = interpolate(frame, [fps * 3.4, fps * 5.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const fragmentOpacity = interpolate(frame, [fps * 3.4, fps * 4, fps * 5.5], [1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg, alignItems: "center", justifyContent: "center" }}>
      {/* weathered slab */}
      <div
        style={{
          position: "absolute",
          left: cx - 620,
          top: cy - 220,
          width: 1240,
          height: 440,
          background: `linear-gradient(135deg, ${themeEp5.colors.stone}, ${themeEp5.colors.stoneLight})`,
          opacity: slabOpacity,
          boxShadow: "0 0 120px rgba(0,0,0,0.6) inset",
        }}
      />

      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* base hairline crack, always faintly present */}
        <path
          d={`M ${cx - 560},${cy - 190} C ${cx - 300},${cy - 60} ${cx - 80},${cy + 40} ${cx + 180},${cy - 20} C ${cx + 360},${cy - 70} ${cx + 520},${cy + 60} ${cx + 580},${cy + 190}`}
          fill="none"
          stroke={themeEp5.colors.bg}
          strokeWidth={interpolate(crackWiden, [0, 1], [3, 14])}
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={1 - crackDraw}
          opacity={slabOpacity}
        />
      </svg>

      {/* falling fragment */}
      <div
        style={{
          position: "absolute",
          left: cx + 300,
          top: cy - 150,
          width: 220,
          height: 260,
          background: themeEp5.colors.stoneLight,
          opacity: fragmentOpacity,
          transform: `translateY(${fragmentFall * 420}px) rotate(${fragmentFall * 18}deg)`,
          clipPath: "polygon(0% 0%, 100% 10%, 85% 100%, 10% 90%)",
        }}
      />

      <div
        style={{
          position: "relative",
          fontFamily: themeEp5.font.display,
          fontSize: 92,
          letterSpacing: 10,
          color: themeEp5.colors.gold,
          textAlign: "center",
          opacity: titleDraw,
          textShadow: `0 0 40px rgba(217,191,140,${0.25 * titleDraw})`,
        }}
      >
        THE LAST ROMAN
      </div>
    </AbsoluteFill>
  );
};
