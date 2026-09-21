import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

const LINES = [
  { culture: "SUMER", text: "The Sumerians spoke of the great flood that wiped the earth clean.", tint: "#8a4f34" },
  { culture: "GREECE", text: "The Greeks told of Deucalion and the deluge that drowned the world.", tint: "#2c4a5c" },
  { culture: "INDIA", text: "The Hindus preserved the memory in the fire and water of the Pralaya.", tint: "#7a5324" },
  { culture: "MAYA", text: "The Maya carved the story into stone — a world cycle ending in catastrophic destruction.", tint: "#2f4a3a" },
  { culture: "AMERICAS", text: "Indigenous peoples of the Americas held stories of the sky falling, of ice returning.", tint: "#3d3428" },
];

export const S21_MythMontage: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();

  const segmentFrames = Math.floor((fps * 45.49) / LINES.length);
  const index = Math.min(LINES.length - 1, Math.floor(frame / segmentFrames));
  const localFrame = frame - index * segmentFrames;
  const line = LINES[index];

  const charCount = Math.max(0, Math.min(line.text.length, Math.floor((localFrame - fps * 0.2) * 1.6)));
  const visibleText = line.text.slice(0, charCount);

  const bgOpacity = interpolate(localFrame, [0, fps * 0.4, segmentFrames - fps * 0.5, segmentFrames], [0, 1, 1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const labelOpacity = interpolate(localFrame, [0, fps * 0.3], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cursorBlink = Math.floor(frame / 15) % 2 === 0;

  return (
    <AbsoluteFill style={{ backgroundColor: theme.colors.bg }}>
      <AbsoluteFill style={{ backgroundColor: line.tint, opacity: bgOpacity * 0.35 }} />

      <div
        style={{
          position: "absolute",
          top: height * 0.32,
          left: width * 0.1,
          right: width * 0.1,
        }}
      >
        <div
          style={{
            opacity: labelOpacity,
            fontFamily: theme.font.body,
            fontSize: 16,
            letterSpacing: 4,
            color: theme.colors.terracotta,
            marginBottom: 18,
          }}
        >
          {line.culture}
        </div>
        <div
          style={{
            fontFamily: theme.font.display,
            fontSize: 40,
            lineHeight: 1.35,
            color: theme.colors.text,
          }}
        >
          {visibleText}
          {charCount < line.text.length && cursorBlink ? "|" : ""}
        </div>
      </div>

      {/* progress dots */}
      <div style={{ position: "absolute", bottom: height * 0.1, width: "100%", display: "flex", justifyContent: "center", gap: 10 }}>
        {LINES.map((_, i) => (
          <div
            key={i}
            style={{
              width: 8,
              height: 8,
              borderRadius: 4,
              backgroundColor: i === index ? theme.colors.terracotta : theme.colors.ashGrayDim,
            }}
          />
        ))}
      </div>
    </AbsoluteFill>
  );
};
