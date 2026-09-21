import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const CITATIONS = [
  "Younger Dryas Impact Hypothesis — Firestone et al., 2007–2020",
  "Greenland Ice Core Project",
  "Antarctic Ice Sheet studies",
  "Megafauna extinction timeline — Faith & Surovell, 2009",
  "Global flood myth compilation — Dundes, 1988",
  "Göbekli Tepe archaeology — Schmidt & Banning",
  "Neolithic transition studies",
];

export const S31_CitationCrawl: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const headerOpacity = interpolate(frame, [0, fps * 0.6], [0, 1], { extrapolateRight: "clamp" });
  const rowStagger = fps * 0.9;
  const listStartFrame = fps * 0.8;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg, alignItems: "center" }}>
      <div
        style={{
          marginTop: height * 0.12,
          opacity: headerOpacity,
          fontFamily: theme.font.body,
          fontSize: 16,
          letterSpacing: 3,
          color: theme.colors.terracotta,
        }}
      >
        EVIDENCE AND SOURCES
      </div>

      <div style={{ marginTop: 40, width: width * 0.6 }}>
        {CITATIONS.map((c, i) => {
          const t = frame - listStartFrame - i * rowStagger;
          const opacity = interpolate(t, [0, fps * 0.5], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          const y = interpolate(t, [0, fps * 0.5], [12, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div
              key={c}
              style={{
                opacity,
                transform: `translateY(${y}px)`,
                fontFamily: theme.font.display,
                fontSize: 20,
                color: theme.colors.textDim,
                padding: "10px 0",
                borderBottom: `1px solid ${theme.colors.ashGrayDark}`,
                textAlign: "center",
              }}
            >
              {c}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
