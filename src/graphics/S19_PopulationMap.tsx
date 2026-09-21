import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const LANDMASS_PATH =
  "M120,260 C160,180 260,140 360,150 C420,120 520,110 600,150 C680,120 780,140 820,200 " +
  "C880,190 940,220 950,280 C920,340 840,360 760,340 C700,380 600,400 520,370 " +
  "C440,400 340,390 280,350 C200,360 130,330 120,260 Z";

// Pre-impact population grid: denser in the north (upper rows), matching the
// "population collapsed in the north" narration.
const GRID: { x: number; y: number; preDensity: number; postDensity: number }[] = [];
for (let row = 0; row < 6; row++) {
  for (let col = 0; col < 10; col++) {
    const x = 150 + col * 75;
    const y = 160 + row * 35;
    const northern = row < 3;
    GRID.push({
      x,
      y,
      preDensity: northern ? 0.9 : 0.5,
      postDensity: northern ? 0.15 : 0.45,
    });
  }
}

export const S19_PopulationMap: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const mapIn = interpolate(frame, [0, fps * 0.3], [0, 1], { extrapolateRight: "clamp" });
  const dotsIn = interpolate(frame, [fps * 0.3, fps * 0.9], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const collapse = interpolate(frame, [fps * 2.0, fps * 3.4], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(frame, [fps * 2.2, fps * 2.8], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <svg viewBox="0 0 1000 500" width={width * 0.75} height={height * 0.6}>
        <path d={LANDMASS_PATH} fill={theme.colors.ashGrayDark} opacity={mapIn} />
        <clipPath id="popclip">
          <path d={LANDMASS_PATH} />
        </clipPath>
        <g clipPath="url(#popclip)">
          {GRID.map((d, i) => {
            const density = interpolate(collapse, [0, 1], [d.preDensity, d.postDensity]);
            return <circle key={i} cx={d.x} cy={d.y} r={5} fill={theme.colors.terracotta} opacity={density * dotsIn} />;
          })}
        </g>
      </svg>

      <div
        style={{
          position: "absolute",
          bottom: height * 0.16,
          opacity: labelOpacity,
          textAlign: "center",
          fontFamily: theme.font.display,
        }}
      >
        <div style={{ color: theme.colors.text, fontSize: 22 }}>Before → After</div>
        <div style={{ color: theme.colors.textDim, fontSize: 15, marginTop: 2 }}>population decline concentrated in the north</div>
      </div>
    </AbsoluteFill>
  );
};
