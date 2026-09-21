import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Schematic Atlantic conveyor loop: warm surface current flows north (top),
// sinks, returns south (bottom) — a stylized ellipse, not a real ocean map.
export const S16_AMOCDiagram: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const cx = width * 0.5;
  const cy = height * 0.5;
  const rx = width * 0.28;
  const ry = height * 0.22;

  const loopIn = interpolate(frame, [0, fps * 0.5], [0, 1], { extrapolateRight: "clamp" });
  const flowOffset = -(frame * 2) % 40;
  const freshwaterIn = interpolate(frame, [fps * 0.6, fps * 1.3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const stallOpacity = interpolate(frame, [fps * 1.4, fps * 2.2], [1, 0.15], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ellipsePath = `M ${cx - rx},${cy} A ${rx},${ry} 0 1,1 ${cx + rx},${cy} A ${rx},${ry} 0 1,1 ${cx - rx},${cy}`;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <path
          d={ellipsePath}
          fill="none"
          stroke={theme.colors.glacialBlue}
          strokeWidth={5}
          strokeDasharray="18 10"
          strokeDashoffset={flowOffset}
          opacity={loopIn * stallOpacity}
        />
        {/* directional arrowheads, top (northward warm flow) and bottom (southward return) */}
        <polygon
          points={`${cx + 6},${cy - ry - 10} ${cx - 6},${cy - ry - 10} ${cx},${cy - ry - 22}`}
          fill={theme.colors.glacialBlue}
          opacity={loopIn * stallOpacity}
        />
        <polygon
          points={`${cx - 6},${cy + ry + 10} ${cx + 6},${cy + ry + 10} ${cx},${cy + ry + 22}`}
          fill={theme.colors.glacialBlue}
          opacity={loopIn * stallOpacity}
        />

        {/* freshwater wedge cutting into the loop from the upper-left */}
        <polygon
          points={`${cx - rx - 40},${cy - ry - 40} ${cx - rx + 60},${cy - ry - 40} ${cx - rx - 10},${cy}`}
          fill={theme.colors.text}
          opacity={freshwaterIn * 0.5}
        />
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.14,
          textAlign: "center",
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textFaint,
          letterSpacing: 1,
        }}
      >
        ATLANTIC OVERTURNING CIRCULATION — FRESHWATER DISRUPTION
      </div>
    </AbsoluteFill>
  );
};
