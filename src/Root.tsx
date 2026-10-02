import { Composition } from "remotion";
import { S02_TimelineAxis } from "./graphics/S02_TimelineAxis";
import { S06_IceSheetMap } from "./graphics/S06_IceSheetMap";
import { S09_ImpactDiagram } from "./graphics/S09_ImpactDiagram";
import { S11_ExtinctionChart } from "./graphics/S11_ExtinctionChart";
import { S14_ClimatePlunge } from "./graphics/S14_ClimatePlunge";
import { S16_AMOCDiagram } from "./graphics/S16_AMOCDiagram";
import { S19_PopulationMap } from "./graphics/S19_PopulationMap";
import { S21_MythMontage } from "./graphics/S21_MythMontage";
import { S25_NeolithicTimeline } from "./graphics/S25_NeolithicTimeline";
import { S28_StatCards } from "./graphics/S28_StatCards";
import { S31_CitationCrawl } from "./graphics/S31_CitationCrawl";
import { S30_LogoCard } from "./graphics/S30_LogoCard";
import { EP2_S02_BridgeTimeline } from "./graphics/EP2_S02_BridgeTimeline";
import { EP2_S06_TasTepelerMap } from "./graphics/EP2_S06_TasTepelerMap";
import { EP2_S10_ComparativeTimeline } from "./graphics/EP2_S10_ComparativeTimeline";
import { EP2_S11_InvertedSequenceBars } from "./graphics/EP2_S11_InvertedSequenceBars";
import { EP2_S15_LaborConvergence } from "./graphics/EP2_S15_LaborConvergence";
import { EP2_S19_VultureStoneOverlay } from "./graphics/EP2_S19_VultureStoneOverlay";
import { EP2_S23_AgricultureSpreadMap } from "./graphics/EP2_S23_AgricultureSpreadMap";
import { EP2_S24_EinkornComparison } from "./graphics/EP2_S24_EinkornComparison";
import { EP2_S28_ClosingStatCard } from "./graphics/EP2_S28_ClosingStatCard";
import { EP2_S29_LogoCard } from "./graphics/EP2_S29_LogoCard";
import { EP2_S30_CitationCrawl } from "./graphics/EP2_S30_CitationCrawl";

// Duration in frames = ceil(final_dur_seconds * 30), taken from
// production/pantheon-ep1-shot-list-final.json (voiceover-reconciled timing).
const COMPOSITIONS: { id: string; component: React.FC; durationInFrames: number }[] = [
  { id: "S02-TimelineAxis", component: S02_TimelineAxis, durationInFrames: 468 },
  { id: "S06-IceSheetMap", component: S06_IceSheetMap, durationInFrames: 137 },
  { id: "S09-ImpactDiagram", component: S09_ImpactDiagram, durationInFrames: 507 },
  { id: "S11-ExtinctionChart", component: S11_ExtinctionChart, durationInFrames: 897 },
  { id: "S14-ClimatePlunge", component: S14_ClimatePlunge, durationInFrames: 995 },
  { id: "S16-AMOCDiagram", component: S16_AMOCDiagram, durationInFrames: 135 },
  { id: "S19-PopulationMap", component: S19_PopulationMap, durationInFrames: 234 },
  { id: "S21-MythMontage", component: S21_MythMontage, durationInFrames: 1365 },
  { id: "S25-NeolithicTimeline", component: S25_NeolithicTimeline, durationInFrames: 527 },
  { id: "S28-StatCards", component: S28_StatCards, durationInFrames: 1131 },
  { id: "S31-CitationCrawl", component: S31_CitationCrawl, durationInFrames: 800 },
  { id: "S30-LogoCard", component: S30_LogoCard, durationInFrames: 120 },

  // Pantheon Ep.2 — Göbekli Tepe. Frames taken from
  // production/pantheon-ep2-shot-list-final.json (voiceover-reconciled timing).
  { id: "EP2-S02-BridgeTimeline", component: EP2_S02_BridgeTimeline, durationInFrames: 754 },
  { id: "EP2-S06-TasTepelerMap", component: EP2_S06_TasTepelerMap, durationInFrames: 449 },
  { id: "EP2-S10-ComparativeTimeline", component: EP2_S10_ComparativeTimeline, durationInFrames: 585 },
  { id: "EP2-S11-InvertedSequenceBars", component: EP2_S11_InvertedSequenceBars, durationInFrames: 1156 },
  { id: "EP2-S15-LaborConvergence", component: EP2_S15_LaborConvergence, durationInFrames: 851 },
  { id: "EP2-S19-VultureStoneOverlay", component: EP2_S19_VultureStoneOverlay, durationInFrames: 887 },
  { id: "EP2-S23-AgricultureSpreadMap", component: EP2_S23_AgricultureSpreadMap, durationInFrames: 778 },
  { id: "EP2-S24-EinkornComparison", component: EP2_S24_EinkornComparison, durationInFrames: 828 },
  { id: "EP2-S28-ClosingStatCard", component: EP2_S28_ClosingStatCard, durationInFrames: 390 },
  { id: "EP2-S29-LogoCard", component: EP2_S29_LogoCard, durationInFrames: 150 },
  { id: "EP2-S30-CitationCrawl", component: EP2_S30_CitationCrawl, durationInFrames: 300 },
];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {COMPOSITIONS.map((c) => (
        <Composition
          key={c.id}
          id={c.id}
          component={c.component}
          durationInFrames={c.durationInFrames}
          fps={30}
          width={1920}
          height={1080}
        />
      ))}
    </>
  );
};
