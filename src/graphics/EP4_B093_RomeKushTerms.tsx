import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp4 } from "../theme-ep4";
import { RIVER_PATH, BORDER_Y, CITY_POS, MAP_BOX } from "./ep4-map-data";
import { Ep4RealMapBackground } from "./Ep4RealMapBackground";

// MG8: map of Roman Egypt and Kush; envoy ships cross to Samos; terms appear as
// a Kush-independent border line and a struck-out tribute mark.
export const EP4_B093_RomeKushTerms: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const napata = CITY_POS.napata;

  const shipProgress = interpolate(frame, [fps * 0.3, fps * 3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const borderDraw = interpolate(frame, [fps * 4, fps * 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const tributeStrike = interpolate(frame, [fps * 7, fps * 8.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const shipX = interpolate(shipProgress, [0, 1], [napata.x, width * 0.86]);
  const shipY = interpolate(shipProgress, [0, 1], [napata.y - 40, height * 0.3]);

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp4.colors.bg }}>
      <Ep4RealMapBackground />
      <svg width={width} height={height} style={{ position: "absolute" }}>
        <rect x={MAP_BOX.x} y={MAP_BOX.y} width={MAP_BOX.width} height={BORDER_Y - MAP_BOX.y} fill={themeEp4.colors.romeRegion} opacity={0.3} />
        <rect x={MAP_BOX.x} y={BORDER_Y} width={MAP_BOX.width} height={MAP_BOX.y + MAP_BOX.height - BORDER_Y} fill={themeEp4.colors.ember} opacity={0.35} />
        <path d={RIVER_PATH} fill="none" stroke={themeEp4.colors.goldLight} strokeWidth={4} strokeLinecap="round" opacity={0.7} />

        <circle cx={shipX} cy={shipY} r={6} fill={themeEp4.colors.cream} opacity={shipProgress > 0 ? 1 : 0} />
        <line
          x1={napata.x}
          y1={napata.y - 40}
          x2={shipX}
          y2={shipY}
          stroke={themeEp4.colors.cream}
          strokeWidth={2}
          strokeDasharray="4 4"
          opacity={shipProgress}
        />

        <line
          x1={MAP_BOX.x}
          y1={BORDER_Y}
          x2={MAP_BOX.x + MAP_BOX.width * borderDraw}
          y2={BORDER_Y}
          stroke={themeEp4.colors.goldLight}
          strokeWidth={4}
        />
      </svg>

      <div
        style={{
          position: "absolute",
          right: width * 0.08,
          top: height * 0.2,
          fontFamily: themeEp4.font.body,
          fontStyle: "italic",
          fontSize: 20,
          color: themeEp4.colors.cream,
          opacity: shipProgress,
        }}
      >
        to Samos, in the Aegean
      </div>

      <div
        style={{
          position: "absolute",
          left: 620,
          top: BORDER_Y + 30,
          fontFamily: themeEp4.font.display,
          fontSize: 26,
          letterSpacing: 3,
          color: themeEp4.colors.goldLight,
          opacity: borderDraw,
        }}
      >
        KUSH — INDEPENDENT
      </div>

      <div
        style={{
          position: "absolute",
          left: 620,
          top: 90,
          fontFamily: themeEp4.font.body,
          fontSize: 22,
          color: themeEp4.colors.textDim,
          opacity: tributeStrike > 0 ? 1 : 0,
          position2: "relative",
        } as React.CSSProperties}
      >
        <span style={{ position: "relative" }}>
          annual tribute
          <span
            style={{
              position: "absolute",
              left: 0,
              right: 0,
              top: "50%",
              height: 3,
              backgroundColor: themeEp4.colors.ember,
              transform: `scaleX(${tributeStrike})`,
              transformOrigin: "left",
              display: "inline-block",
            }}
          />
        </span>
      </div>
    </AbsoluteFill>
  );
};
