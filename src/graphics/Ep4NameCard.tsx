import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { themeEp4 } from "../theme-ep4";

// Lower-third name card, shown once on a person's first mention in the
// narration. Rendered against a solid chroma-key green and composited over
// the underlying footage with ffmpeg's colorkey filter at assembly time
// (see production/pantheon-ep4-render-namecards.py and
// production/pantheon-ep4-apply-namecards.py) — this sandbox's webm/vp8
// alpha export did not actually come out transparent when tested, so this
// is a deliberate workaround, not a real alpha channel. Every element here
// is kept fully opaque and animated by position only (never CSS opacity),
// so no pixel is ever a part-green blend that colorkey can't cleanly key.
export const Ep4NameCard: React.FC<{ name: string; role: string }> = ({ name, role }) => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, 10], [360, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const slideOut = interpolate(frame, [92, 108], [0, 360], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const offsetX = Math.max(slideIn, slideOut);
  const barWidth = interpolate(frame, [2, 14], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#00FF00" }}>
      <div
        style={{
          position: "absolute",
          left: 120,
          bottom: 140,
          transform: `translateX(-${offsetX}px)`,
        }}
      >
        <div
          style={{
            height: 3,
            width: `${barWidth * 420}px`,
            background: themeEp4.colors.goldLight,
            marginBottom: 14,
          }}
        />
        <div
          style={{
            display: "inline-block",
            padding: "18px 36px",
            // Opaque, not translucent: this box renders against a solid
            // chroma-key green backdrop (see note above), so any alpha
            // here would bake a green tint into the box instead of
            // blending with the real footage underneath at composite time.
            background: "#0A0908",
            borderLeft: `3px solid ${themeEp4.colors.goldLight}`,
          }}
        >
          <div
            style={{
              fontFamily: themeEp4.font.display,
              fontSize: 38,
              letterSpacing: 4,
              fontWeight: 700,
              color: themeEp4.colors.goldLight,
              textTransform: "uppercase",
              whiteSpace: "nowrap",
            }}
          >
            {name}
          </div>
          <div
            style={{
              fontFamily: themeEp4.font.body,
              fontStyle: "italic",
              fontSize: 22,
              color: themeEp4.colors.cream,
              marginTop: 6,
              whiteSpace: "nowrap",
            }}
          >
            {role}
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};
