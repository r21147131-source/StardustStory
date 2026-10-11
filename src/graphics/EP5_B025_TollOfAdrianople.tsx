import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { themeEp5 } from "../theme-ep5";

// MG4: The Toll of Adrianople. Stat card on dark ground: TWO-THIRDS of the
// Eastern field army, in one afternoon. Then: the first Roman emperor killed
// in battle by a foreign enemy in over two hundred years.
export const EP5_B025_TollOfAdrianople: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const statOpacity = interpolate(frame, [0, fps * 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const subOpacity = interpolate(frame, [fps * 0.5, fps * 1.1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const line2Opacity = interpolate(frame, [fps * 1.8, fps * 2.6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <AbsoluteFill style={{ backgroundColor: themeEp5.colors.bg, alignItems: "center", justifyContent: "center" }}>
      <div style={{ textAlign: "center", maxWidth: 1300 }}>
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 110,
            letterSpacing: 8,
            color: themeEp5.colors.crimsonLight,
            opacity: statOpacity,
          }}
        >
          TWO-THIRDS
        </div>
        <div
          style={{
            fontFamily: themeEp5.font.body,
            fontStyle: "italic",
            fontSize: 30,
            color: themeEp5.colors.textDim,
            opacity: subOpacity,
            marginTop: 8,
          }}
        >
          of the Eastern field army, in one afternoon
        </div>
        <div
          style={{
            width: 220,
            height: 2,
            background: themeEp5.colors.bronzeDim,
            margin: "34px auto",
            opacity: line2Opacity,
          }}
        />
        <div
          style={{
            fontFamily: themeEp5.font.display,
            fontSize: 32,
            letterSpacing: 2,
            color: themeEp5.colors.gold,
            opacity: line2Opacity,
            lineHeight: 1.4,
          }}
        >
          THE FIRST ROMAN EMPEROR KILLED IN BATTLE
          <br />
          BY A FOREIGN ENEMY IN OVER TWO HUNDRED YEARS
        </div>
      </div>
    </AbsoluteFill>
  );
};
