import { Img, staticFile } from "remotion";
import { MAP_IMAGE, MAP_BOX } from "./ep4-map-data";

// Shared real-geography map backdrop (traced from a public-domain Nile
// basin map, recolored to the Pantheon palette) used behind every map-style
// motion graphic in Ep.4. See ep4-map-data.ts for sourcing/calibration notes.
export const Ep4RealMapBackground: React.FC<{ opacity?: number }> = ({ opacity = 1 }) => {
  return (
    <Img
      src={staticFile(MAP_IMAGE)}
      style={{
        position: "absolute",
        left: MAP_BOX.x,
        top: MAP_BOX.y,
        width: MAP_BOX.width,
        height: MAP_BOX.height,
        objectFit: "cover",
        opacity,
        filter: "drop-shadow(0 0 40px rgba(0,0,0,0.6))",
      }}
    />
  );
};
