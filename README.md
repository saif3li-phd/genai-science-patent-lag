# GenAI and the Science-to-Technology Lag - Full Research Package

Study: Does generative AI accelerate the transition from science to corporate
patents? Difference-in-Differences design; treated = GenAI-exposed CPC classes
(G06N, G16B, G16C, C40B); control = low-exposure mechanical classes
(F16B, F16H, B65D); science-intensive alternative controls (G01N, G02B, B01D, G21);
treatment period from 2023-01-01.

Target: AI4SciSci 2026 extended abstract (EasyChair #14, under review,
notification 2026-09-21), then full paper (Journal of Informetrics /
Scientometrics tier).

## Folder map

    README.md                          <- this file: map + run order
    docs/
      01_cpc_codes_documented.md       CPC classes + official USPTO definition URLs
                                       (incl. ex-ante science-controls addendum)
      02_lens_query_protocol.md        how every Lens query/export is done
      03_vosviewer_protocol.md         reproducible descriptive-map settings
      04_export_log_filled.md          ACTUAL collection log: counts, deltas, flags
    code/
      build_lag_dataset.py             raw exports -> data/clean/lag_pairs.csv (v1)
      build_lag_dataset_v2.py          slim exports -> lag_pairs_v2.csv.gz (441,537 pairs,
                                       corrected G06N batches, + year-based file)
      build_sci_controls.py            science-controls exports -> lag_pairs_sci.csv.gz
      did_analysis.py                  main DiD, --placebo (2021 in-sample cut), --inventor-only
      rebuild_delta_analysis.py        item 10: v1 vs v2 headline comparison + year-based rule
      instrument_vs_subject.py         item 11: excluding generative-coded patents
      main_group_inference.py          item 12: wild cluster bootstrap at 133 CPC main groups
      firm_exposure.py                 item 13: firm-level GenAI adoption measure
      (+ event study, dose gradient, incumbents, assignee FE, RoS replication,
       thresholds/volume, wild cluster bootstrap 7/9, RQ2 similarity, OpenAlex pilot)
    data/
      raw/                             Lens exports EXACTLY as downloaded (never edited)
      g06n_cpc.csv.gz                  patent-level CPC codes for G06N
      clean/                           analysis datasets (regenerable from raw/):
                                       lag_pairs.csv (v1), lag_pairs_v2.csv.gz (current),
                                       lag_pairs_9classes_v2.csv.gz, lag_pairs_v2_year.csv.gz,
                                       lag_pairs_sci.csv.gz, placebo_pairs(_v2).csv.gz
    latex/
      extended-abstract.tex/.pdf       ANONYMIZED submission version (frozen during review)
      ceurart.cls, ccicons.sty         CEUR template files
    results/                           regression tables + figures

## Reproduction order

    1. Queries + exports:     follow docs/02, log into docs/04
    2. cd code && python3 build_lag_dataset_v2.py   (reads ../data/raw_full_slim)
    3. python3 rebuild_delta_analysis.py            (headline estimates, v1 vs v2)
    4. robustness battery: event study, dose, incumbents, assignee FE, RoS,
       thresholds, wild cluster bootstrap, science controls ("_v2" results files)
    5. decomposition: instrument_vs_subject.py, main_group_inference.py, firm_exposure.py
    6. VOSviewer maps: follow docs/03

## Status (v2, 2026-08-25)

- Current dataset: lag_pairs_v2.csv.gz, 441,537 pairs (corrected G06N citation
  batches; +12,426 pairs vs v1, 0 lost). Year-based file: 737,032 pairs.
- Headline: fresh-science share DiD -5.56 pp (p=0.0004); -10.1 under the
  year-based dating rule; lag +0.214 (compositional: halves vs science controls,
  zero within firms, collapses under cited-publication-year FE, item 14).
- Decomposition: roughly half the share decline is carried by generative-coded
  patents (item 11); adopting firms RETAIN fresh science better in their
  non-generative patents (+4.54 pp, p=0.021, item 13); 133-main-group wild
  cluster bootstrap in item 12.
- Known gap: citations-g16c-placebo export truncated (exactly 1,000 rows);
  re-export pending; placebo unaffected in the other six classes.

## Integrity policy

Raw exports are never hand-edited; every cleaning rule is declared in code
(R1-R4 in build_lag_dataset*.py) and every run prints the full record flow.
GENERATIVE definition unified across all scripts: G06N3/045, G06N3/0455,
G06N3/0475 (current-scheme codes).
Classification sources: official USPTO/EPO CPC definitions (docs/01).
