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
import { EP4_B008_MapEgyptKush } from "./graphics/EP4_B008_MapEgyptKush";
import { EP4_B017_MapEgyptCracks } from "./graphics/EP4_B017_MapEgyptCracks";
import { EP4_B019_MapKushGrows } from "./graphics/EP4_B019_MapKushGrows";
import { EP4_B022_MapAlaraKashta } from "./graphics/EP4_B022_MapAlaraKashta";
import { EP4_B026_MapCoalitionMarches } from "./graphics/EP4_B026_MapCoalitionMarches";
import { EP4_B027_MapMemphisHerakleopolis } from "./graphics/EP4_B027_MapMemphisHerakleopolis";
import { EP4_B030_MapArmyFollowsPiye } from "./graphics/EP4_B030_MapArmyFollowsPiye";
import { EP4_B039_MemphisHarborSchematic } from "./graphics/EP4_B039_MemphisHarborSchematic";
import { EP4_B056_MapEmpireGlows } from "./graphics/EP4_B056_MapEmpireGlows";
import { EP4_B084_MapNapataDims } from "./graphics/EP4_B084_MapNapataDims";
import { EP4_B062_MapAssyriaSpreads } from "./graphics/EP4_B062_MapAssyriaSpreads";
import { EP4_B069_AssyrianTimeline } from "./graphics/EP4_B069_AssyrianTimeline";
import { EP4_B011_TitleCard } from "./graphics/EP4_B011_TitleCard";
import { EP4_B083_ErasureSequence } from "./graphics/EP4_B083_ErasureSequence";
import { EP4_B103_ErasureRepeat } from "./graphics/EP4_B103_ErasureRepeat";
import { EP4_B110_NamesRefill } from "./graphics/EP4_B110_NamesRefill";
import { EP4_B091_KandakeTypography } from "./graphics/EP4_B091_KandakeTypography";
import { EP4_B093_RomeKushTerms } from "./graphics/EP4_B093_RomeKushTerms";
import { EP4_B102_KingListScroll } from "./graphics/EP4_B102_KingListScroll";
import { EP4_B106_MeroiticScript } from "./graphics/EP4_B106_MeroiticScript";

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

  // Pantheon Ep.4 — Kush. Frames are voiceover-reconciled (real VO 759.43s,
  // scale 0.97164x applied to narration_words/150wpm estimates) — see
  // production/pantheon-ep4-shot-list-final.json and pantheon-ep4-allocate.py.
  { id: "EP4-B008-MapEgyptKush", component: EP4_B008_MapEgyptKush, durationInFrames: 210 },
  { id: "EP4-B017-MapEgyptCracks", component: EP4_B017_MapEgyptCracks, durationInFrames: 221 },
  { id: "EP4-B019-MapKushGrows", component: EP4_B019_MapKushGrows, durationInFrames: 198 },
  { id: "EP4-B022-MapAlaraKashta", component: EP4_B022_MapAlaraKashta, durationInFrames: 362 },
  { id: "EP4-B026-MapCoalitionMarches", component: EP4_B026_MapCoalitionMarches, durationInFrames: 210 },
  { id: "EP4-B027-MapMemphisHerakleopolis", component: EP4_B027_MapMemphisHerakleopolis, durationInFrames: 210 },
  { id: "EP4-B030-MapArmyFollowsPiye", component: EP4_B030_MapArmyFollowsPiye, durationInFrames: 128 },
  { id: "EP4-B039-MemphisHarborSchematic", component: EP4_B039_MemphisHarborSchematic, durationInFrames: 58 },
  { id: "EP4-B056-MapEmpireGlows", component: EP4_B056_MapEmpireGlows, durationInFrames: 175 },
  { id: "EP4-B084-MapNapataDims", component: EP4_B084_MapNapataDims, durationInFrames: 256 },
  { id: "EP4-B062-MapAssyriaSpreads", component: EP4_B062_MapAssyriaSpreads, durationInFrames: 268 },
  { id: "EP4-B069-AssyrianTimeline", component: EP4_B069_AssyrianTimeline, durationInFrames: 245 },
  { id: "EP4-B011-TitleCard", component: EP4_B011_TitleCard, durationInFrames: 128 },
  { id: "EP4-B083-ErasureSequence", component: EP4_B083_ErasureSequence, durationInFrames: 152 },
  { id: "EP4-B103-ErasureRepeat", component: EP4_B103_ErasureRepeat, durationInFrames: 70 },
  { id: "EP4-B110-NamesRefill", component: EP4_B110_NamesRefill, durationInFrames: 140 },
  { id: "EP4-B091-KandakeTypography", component: EP4_B091_KandakeTypography, durationInFrames: 408 },
  { id: "EP4-B093-RomeKushTerms", component: EP4_B093_RomeKushTerms, durationInFrames: 350 },
  { id: "EP4-B102-KingListScroll", component: EP4_B102_KingListScroll, durationInFrames: 210 },
  { id: "EP4-B106-MeroiticScript", component: EP4_B106_MeroiticScript, durationInFrames: 338 },
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
