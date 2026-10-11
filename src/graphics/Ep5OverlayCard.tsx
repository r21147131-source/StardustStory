import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { themeEp5 } from "../theme-ep5";

// Lower-third name card (kind="name") or corner year stamp (kind="year"),
// shown on a person's first mention or a narration-stated date change.
// Rendered against solid chroma-key green and composited over the
// underlying footage with ffmpeg's colorkey filter at assembly time (see
// production/pantheon-ep5-render-overlays.py and
// pantheon-ep5-apply-overlays.py) -- same workaround as Ep.4's
// Ep4NameCard, for the same reason (this sandbox's alpha-channel video
// export isn't reliable). Every element is kept fully opaque and animated
// by position only, never CSS opacity, so no pixel is a part-green blend
// colorkey can't cleanly key.
export const Ep5OverlayCard: React.FC<{ kind: "name" | "year"; line1: string; line2?: string }> = ({
  kind,
  line1,
  line2,
}) => {
  const frame = useCurrentFrame();

  const slideIn = interpolate(frame, [0, 10], [360, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const slideOut = interpolate(frame, [92, 108], [0, 360], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const offsetX = Math.max(slideIn, slideOut) * (kind === "year" ? -1 : 1);
  const barWidth = interpolate(frame, [2, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  if (kind === "year") {
    return (
      <AbsoluteFill style={{ backgroundColor: "#00FF00" }}>
        <div
          style={{
            position: "absolute",
            right: 120,
            top: 100,
            transform: `translateX(-${offsetX}px)`,
            textAlign: "right",
          }}
        >
          <div
            style={{
              display: "inline-block",
              padding: "14px 30px",
              background: "#0A0908",
              borderRight: `3px solid ${themeEp5.colors.goldLight}`,
            }}
          >
            <div
              style={{
                fontFamily: themeEp5.font.display,
                fontSize: 34,
                letterSpacing: 5,
                fontWeight: 700,
                color: themeEp5.colors.goldLight,
                whiteSpace: "nowrap",
              }}
            >
              {line1}
            </div>
          </div>
          <div
            style={{
              height: 3,
              width: `${barWidth * 260}px`,
              background: themeEp5.colors.goldLight,
              marginTop: 10,
              marginLeft: "auto",
            }}
          />
        </div>
      </AbsoluteFill>
    );
  }

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
            background: themeEp5.colors.goldLight,
            marginBottom: 14,
          }}
        />
        <div
          style={{
            display: "inline-block",
            padding: "18px 36px",
            background: "#0A0908",
            borderLeft: `3px solid ${themeEp5.colors.goldLight}`,
          }}
        >
          <div
            style={{
              fontFamily: themeEp5.font.display,
              fontSize: 38,
              letterSpacing: 4,
              fontWeight: 700,
              color: themeEp5.colors.goldLight,
              textTransform: "uppercase",
              whiteSpace: "nowrap",
            }}
          >
            {line1}
          </div>
          {line2 && (
            <div
              style={{
                fontFamily: themeEp5.font.body,
                fontStyle: "italic",
                fontSize: 22,
                color: themeEp5.colors.parchment,
                marginTop: 6,
                whiteSpace: "nowrap",
              }}
            >
              {line2}
            </div>
          )}
        </div>
      </div>
    </AbsoluteFill>
  );
};
