import { themeEp5 } from "../theme-ep5";
import {
  REGION_BRITANNIA,
  REGION_GAUL_HISPANIA,
  REGION_ITALIA,
  REGION_SICILIA,
  REGION_BALKANS_GREECE,
  REGION_ASIA_MINOR,
  REGION_SYRIA_LEVANT,
  REGION_NORTH_AFRICA,
} from "./ep5-map-data";

// Shared stylized "flat ink-and-gold" Mediterranean-world backdrop used
// behind every map-style motion graphic in Ep.5. See ep5-map-data.ts.
export const Ep5MapBackground: React.FC<{ fillOpacity?: number; strokeOpacity?: number }> = ({
  fillOpacity = 0.14,
  strokeOpacity = 0.5,
}) => {
  const regions = [
    REGION_BRITANNIA,
    REGION_GAUL_HISPANIA,
    REGION_ITALIA,
    REGION_SICILIA,
    REGION_BALKANS_GREECE,
    REGION_ASIA_MINOR,
    REGION_SYRIA_LEVANT,
    REGION_NORTH_AFRICA,
  ];
  return (
    <svg width={1920} height={1080} style={{ position: "absolute" }}>
      {regions.map((d, i) => (
        <path
          key={i}
          d={d}
          fill={themeEp5.colors.bronze}
          fillOpacity={fillOpacity}
          stroke={themeEp5.colors.bronze}
          strokeOpacity={strokeOpacity}
          strokeWidth={2}
        />
      ))}
    </svg>
  );
};
