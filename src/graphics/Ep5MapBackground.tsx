import { Img, staticFile } from "remotion";
import { MAP_BOX } from "./ep5-map-data";

const LAYER_FILES = {
  full: "pantheon-ep5-assets/roman-empire-map.png",
  west: "pantheon-ep5-assets/roman-empire-map-west.png",
  east: "pantheon-ep5-assets/roman-empire-map-east.png",
  sea: "pantheon-ep5-assets/roman-empire-map-sea.png",
} as const;

// Shared real-geography map backdrop (the actual 395 AD East/West Roman
// Empire boundary map, recolored to the Pantheon Ep.5 palette) used behind
// every map-style motion graphic in Ep.5. `layer` selects the full map or
// an isolated west/east/sea cutout so beats can animate the empire split
// independently. See ep5-map-data.ts for sourcing/calibration notes.
export const Ep5MapBackground: React.FC<{ layer?: keyof typeof LAYER_FILES; opacity?: number }> = ({
  layer = "full",
  opacity = 1,
}) => {
  return (
    <Img
      src={staticFile(LAYER_FILES[layer])}
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
