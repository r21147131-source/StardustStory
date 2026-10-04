import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";

// MG3: top-down schematic of Memphis — siege ramp rejected, ships sweep the harbor quay.
export const EP4_B039_MemphisHarborSchematic: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const rampOpacity = interpolate(frame, [0, fps * 0.3, fps * 0.7, fps * 0.9], [0, 1, 1, 0.15], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const strikeOpacity = interpolate(frame, [fps * 0.6, fps * 0.9], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const shipsProgress = interpolate(frame, [fps * 1, fps * 1.8], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const wallGold = interpolate(frame, [fps * 1.4, fps * 2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const cx = width / 2;
  const cy = height / 2;

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {/* city block */}
        <rect
          x={cx - 160}
          y={cy - 120}
          width={320}
          height={240}
          fill="none"
          stroke={themeEp4.colors.goldDim}
          strokeWidth={3}
          opacity={1}
        />
        <rect
          x={cx - 160}
          y={cy - 120}
          width={6}
          height={240}
          fill={themeEp4.colors.gold}
          opacity={wallGold}
        />
        {/* river / harbor on the left */}
        <rect x={cx - 420} y={cy - 200} width={260} height={400} fill="#2b4a5a" opacity={0.25} />
        <text x={cx - 420} y={cy - 220} fill={themeEp4.colors.textFaint} fontFamily={themeEp4.font.body} fontSize={16}>
          the Nile
        </text>

        {/* rejected siege ramp, on the right */}
        <g opacity={rampOpacity}>
          <path
            d={`M ${cx + 170},${cy + 110} L ${cx + 310},${cy - 60}`}
            stroke={themeEp4.colors.textFaint}
            strokeWidth={10}
            fill="none"
          />
          <line
            x1={cx + 150}
            y1={cy - 90}
            x2={cx + 330}
            y2={cy + 90}
            stroke={themeEp4.colors.ember}
            strokeWidth={4}
            opacity={strikeOpacity}
          />
        </g>

        {/* ships sweeping the harbor */}
        {[0, 1, 2, 3].map((i) => {
          const startX = cx - 400 + i * 20;
          const startY = cy - 150 + i * 90;
          const x = interpolate(shipsProgress, [0, 1], [startX, cx - 170]);
          return (
            <polygon
              key={i}
              points={`${x},${startY} ${x - 22},${startY + 10} ${x - 22},${startY - 10}`}
              fill={themeEp4.colors.goldLight}
              opacity={shipsProgress > 0 ? 1 : 0}
            />
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.1,
          width: "100%",
          textAlign: "center",
          fontFamily: themeEp4.font.body,
          fontSize: 16,
          letterSpacing: 2,
          color: themeEp4.colors.textFaint,
        }}
      >
        MEMPHIS — THE HARBOR, NOT THE WALLS
      </div>
    </AbsoluteFill>
  );
};
