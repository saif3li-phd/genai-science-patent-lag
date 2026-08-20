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
