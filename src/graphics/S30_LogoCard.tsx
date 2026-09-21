import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

export const S30_LogoCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scale = spring({ frame, fps, config: { damping: 14 } });
  const glow = interpolate(frame, [0, fps * 1.2, fps * 4], [0, 1, 0.6], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const subOpacity = interpolate(frame, [fps * 0.8, fps * 1.6], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: theme.colors.ink,
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <div
        style={{
          transform: `scale(${scale})`,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontFamily: theme.font.display,
            fontSize: 88,
            letterSpacing: 12,
            color: theme.colors.text,
            textShadow: `0 0 ${40 * glow}px ${theme.colors.terracotta}`,
          }}
        >
          PANTHEON
        </div>
        <div
          style={{
            marginTop: 18,
            fontFamily: theme.font.body,
            fontSize: 20,
            letterSpacing: 6,
            color: theme.colors.glacialBlue,
            opacity: subOpacity,
          }}
        >
          EPISODE ONE
        </div>
      </div>
    </AbsoluteFill>
  );
};
