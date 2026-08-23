# Step 1 Output: CPC Field Selection (Treated vs. Control)

Study: Accelerating the Science-to-Technology Transition (GenAI and corporate innovation)
Design: Difference-in-Differences (DiD). Treatment = high GenAI exposure; Post = filings from 2023-01-01.

Single authoritative source for all classification definitions: the official Cooperative
Patent Classification (CPC) scheme and definitions jointly maintained by the USPTO and EPO,
published at uspto.gov. Each code below links to its official definition page.

## Treated group (high GenAI exposure)

| CPC | Official title (abridged) | Official definition source | Justification (one line) |
|---|---|---|---|
| G06N | Computing arrangements based on specific computational models (neural networks, machine learning, AI) | https://www.uspto.gov/web/patents/classification/cpc/html/defG06N.html | The direct technological core of GenAI itself. |
| G16B | Bioinformatics: ICT specially adapted for genetic or protein-related data processing in computational molecular biology | https://www.uspto.gov/web/patents/classification/cpc/html/defG16B.html | Field most visibly transformed by protein/molecule foundation models (e.g., structure prediction, protein design). |
| G16C | Computational theoretical chemistry, chemoinformatics, and computational materials science | https://www.uspto.gov/web/patents/classification/cpc/html/defG16C.html | Generative models for materials and molecule discovery. |
| C40B | Combinatorial chemistry; chemical/biological libraries and screening methods | https://www.uspto.gov/web/patents/classification/cpc/html/defC40B.html | Virtual screening is an early industrial GenAI application in pharma. |

## Control group (low GenAI exposure)

| CPC | Official title (abridged) | Official definition source | Justification (one line) |
|---|---|---|---|
| F16B | Devices for fastening or securing constructional elements or machine parts (nails, bolts, clamps, joints) | https://www.uspto.gov/web/patents/classification/cpc/html/defF16B.html | Mature structural mechanical engineering; historically low reliance on recent scientific literature. |
| F16H | Gearing (toothed, friction, fluid, change-speed, differential; details and control thereof) | https://www.uspto.gov/web/patents/classification/cpc/html/defF16H.html | Same rationale: incremental mechanical domain, weak GenAI channel from papers to patents. |
| B65D | Containers for storage or transport (bags, barrels, bottles, boxes, cartons); closures, packaging elements | https://www.uspto.gov/web/patents/classification/cpc/html/defB65D.html | Packaging engineering: mature, low science-intensity domain. |

## Methodological cautions (recorded at selection time)

1. Pair-count check required. Mechanical control classes cite scientific papers at much
   lower base rates than the treated classes. Before any analysis, count patent-paper
   citation pairs per class in Lens. If control-group pairs are too sparse, widen the
   control set (candidates to consider, pending the same official-definition check:
   additional mature mechanical subclasses).
2. Treatment definition. Treatment here is defined by the patent's own technology class.
   An alternative definition (exposure via the type of science cited) exists and should be
   listed in the paper as a planned sensitivity analysis.
3. Citation-practice drift. Han & Magee (Scientometrics, 2018; arXiv:1705.00258) caution
   that rising patent-to-paper citation intensity can reflect changing citation practices
   rather than a tighter science-technology link. The DiD design absorbs practice drift
   that is common to both groups; drift specific to the treated group post-2023 (e.g.,
   AI-assisted examiner search) is addressed by the inventor-only robustness test
   (see analysis protocol).

## Addendum 2026-08-22: control-group expansion candidates (item 3b)

Selected by the same rule as the original controls: mature mechanical domains with historically
low reliance on recent scientific literature and no plausible GenAI channel from papers to patents.
Definitions from the official CPC scheme (USPTO/EPO), checked before export.

| CPC | Official title (abridged) | Official definition source | Justification (one line) |
|---|---|---|---|
| E05B | Locks; accessories therefor; handcuffs | https://www.uspto.gov/web/patents/classification/cpc/html/defE05B.html | Mature mechanical security hardware; incremental design domain. |
| B25B | Tools or bench devices not otherwise provided for, for fastening, connecting, disengaging or holding (wrenches, pliers, vises, screwdrivers) | https://www.uspto.gov/web/patents/classification/cpc/html/defB25B.html | Hand tools; mature, low science intensity. |

Pair-count check applies as before: if either class yields very few patent-paper pairs, report it
and keep it in the pooled control group only (class-year cells will be thin).

## Addendum 2026-08-23: science-intensive alternative control classes (researcher decision)

Purpose: a second control group that cites science at meaningful rates, unlike the mechanical
controls, to test whether the post-2023 composition shift survives a counterfactual built from
science-citing fields. Selection rule declared BEFORE any export: science-intensive class,
outside AI and molecular chemistry, with no plausible channel from generative models to the
inventive step in 2023-2024. Chosen ex ante on 2026-08-23:

| CPC | Official title (abridged) | Official definition source | Justification (one line) |
|---|---|---|---|
| G01N | Investigating or analysing materials by determining their chemical or physical properties | https://www.uspto.gov/web/patents/classification/cpc/html/defG01N.html | Instrument- and method-driven; among the most science-citing classes outside pharma and computing; classical engineering design. |
| G02B | Optical elements, systems or apparatus | https://www.uspto.gov/web/patents/classification/cpc/html/defG02B.html | Cites physics literature; optical design relies on classical simulation software. |
| B01D | Separation (filtration, distillation, membranes) | https://www.uspto.gov/web/patents/classification/cpc/html/defB01D.html | Process engineering with moderate science citation; physical processes, no generative modeling channel. |
| G21 | Nuclear physics; nuclear engineering | https://www.uspto.gov/web/patents/classification/cpc/html/defG21.html | Physics-citation-intensive; small, regulated, slow-moving domain. |

Known limitation, recorded ex ante: G01N includes subgroup G01N33 (biological/immunological
analysis), adjacent to medical diagnostics where some machine-learning use exists. The full class
is exported; a sensitivity check dropping G01N33 can be run without re-export because CPC codes
ship with the export.

Role in the analysis (declared ex ante): these classes form an ALTERNATIVE control group.
Estimates to report: (a) treated vs science-intensive controls only; (b) treated vs all controls
(mechanical + science-intensive). Cleaning rules R1-R4 unchanged. Cluster count rises from 9 to 13
for the wild cluster bootstrap. The reading rule is fixed in advance: the composition result is
supported if the DiD on the <=3y share against science-intensive controls is negative and of
broadly similar magnitude to the mechanical-control baseline; a sign flip or collapse toward zero
is reported as a failure of the robustness test, not explained away.
