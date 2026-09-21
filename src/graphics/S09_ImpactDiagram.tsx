import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const LANDMASS_PATH =
  "M120,260 C160,180 260,140 360,150 C420,120 520,110 600,150 C680,120 780,140 820,200 " +
  "C880,190 940,220 950,280 C920,340 840,360 760,340 C700,380 600,400 520,370 " +
  "C440,400 340,390 280,350 C200,360 130,330 120,260 Z";

// Fragment landing points on the schematic landmass (northern impact swarm).
const IMPACT_POINTS = [
  { x: 340, y: 210, delay: 0 },
  { x: 430, y: 180, delay: 4 },
  { x: 540, y: 200, delay: 8 },
  { x: 640, y: 175, delay: 5 },
  { x: 730, y: 210, delay: 10 },
];

export const S09_ImpactDiagram: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const mapIn = interpolate(frame, [0, fps * 0.4], [0, 1], { extrapolateRight: "clamp" });
  const streakStart = fps * 0.5;
  const streakDur = fps * 1.1;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 500" width={width * 0.8} height={height * 0.65}>
        <path d={LANDMASS_PATH} fill={theme.colors.ashGrayDark} opacity={mapIn} />

        {IMPACT_POINTS.map((p, i) => {
          const t0 = streakStart + p.delay;
          const streakProgress = interpolate(frame, [t0, t0 + streakDur], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const originX = p.x - 180;
          const originY = p.y - 220;
          const curX = interpolate(streakProgress, [0, 1], [originX, p.x]);
          const curY = interpolate(streakProgress, [0, 1], [originY, p.y]);

          const impactStart = t0 + streakDur;
          const impactProgress = interpolate(frame, [impactStart, impactStart + fps * 0.9], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const ringR = interpolate(impactProgress, [0, 1], [4, 70]);
          const ringOpacity = interpolate(impactProgress, [0, 1], [0.9, 0]);
          const flashOpacity = interpolate(frame, [impactStart, impactStart + 4, impactStart + 14], [0, 1, 0], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });

          return (
            <g key={i}>
              {streakProgress > 0 && streakProgress < 1 && (
                <line
                  x1={originX}
                  y1={originY}
                  x2={curX}
                  y2={curY}
                  stroke={theme.colors.ember}
                  strokeWidth={3}
                  strokeLinecap="round"
                />
              )}
              {impactProgress > 0 && (
                <>
                  <circle cx={p.x} cy={p.y} r={ringR} fill="none" stroke={theme.colors.ember} strokeWidth={3} opacity={ringOpacity} />
                  <circle cx={p.x} cy={p.y} r={16} fill={theme.colors.ember} opacity={flashOpacity} />
                </>
              )}
            </g>
          );
        })}
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.1,
          fontFamily: theme.font.body,
          fontSize: 15,
          color: theme.colors.textFaint,
          letterSpacing: 1,
        }}
      >
        FRAGMENTED IMPACT SWARM · AIRBURST SCENARIO, NORTH AMERICA
      </div>
    </AbsoluteFill>
  );
};
