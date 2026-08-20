# GenAI and the Science-to-Technology Lag - Full Research Package

Study: Does generative AI accelerate the transition from science to corporate
patents? Difference-in-Differences design; treated = GenAI-exposed CPC classes
(G06N, G16B, G16C, C40B); control = low-exposure mechanical classes
(F16B, F16H, B65D); treatment period from 2023-01-01.

Target: AI4SciSci 2026 extended abstract (EasyChair, deadline 2026-09-07),
then full paper (Journal of Informetrics / Scientometrics tier).

## Folder map

    README.md                          <- this file: map + run order
    docs/
      01_cpc_codes_documented.md       CPC classes + official USPTO definition URLs
      02_lens_query_protocol.md        how every Lens query/export is done
      03_vosviewer_protocol.md         reproducible descriptive-map settings
      04_export_log_filled.md          ACTUAL collection log: counts, deltas, flags
    code/
      build_lag_dataset.py             raw exports -> data/clean/lag_pairs.csv
      did_analysis.py                  main DiD, --placebo, --inventor-only
      openalex_pilot.py                optional paper-level controls sampler
    data/
      raw/                             Lens exports EXACTLY as downloaded (never edited)
      clean/lag_pairs.csv              analysis dataset (regenerable from raw/)
    latex/
      extended-abstract.tex/.pdf       ANONYMIZED submission version
      extended-abstract-named.tex/.pdf named version (camera-ready only)
      ceurart.cls, ccicons.sty         CEUR template files
    results/                           regression tables + figures (filled after analysis)

## Reproduction order

    1. Queries + exports:     follow docs/02, log into docs/04
    2. cd code && python3 build_lag_dataset.py     (reads ../data/raw)
    3. python3 did_analysis.py                     (main estimate)
    4. python3 did_analysis.py --placebo
    5. python3 did_analysis.py --inventor-only
    6. VOSviewer maps: follow docs/03
    7. Update latex/ with results; compile with pdflatex (twice)

## Status at packaging time

- Data COMPLETE: 429,111 main pairs (7/7 classes) + 100,032 placebo pairs (2015-2017).
- Results in results/: main DiD, truncation spec ladder, placebo (clean), patent-level check.
- Abstract in findings form (latex/), anonymized replication archive published.

## Integrity policy

Raw exports are never hand-edited; every cleaning rule is declared in code
(R1-R4 in build_lag_dataset.py) and every run prints the full record flow.
Classification sources: official USPTO/EPO CPC definitions (docs/01).
