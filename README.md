# Foundation over Frontier: Replication Package

Study: how the age of the science cited by US patents changed after generative AI diffused, and
whether the lag from publication to patent citation shortened. Difference-in-differences design;
treated = GenAI-exposed CPC classes (G06N, G16B, G16C, C40B); control = low-exposure mechanical
classes (F16B, F16H, B65D); science-intensive alternative controls (G01N, G02B, B01D, G21);
treatment period from 2023-01-01, read as a diffusion threshold.

Paper: "Foundation over Frontier: The Age of Science Cited by Patents after the Diffusion of
Generative AI". Accepted at AI4SciSci 2026, the 3rd International Workshop on Artificial
Intelligence for the Science of Science (co-located with JCDL 2026), CEUR Workshop Proceedings.
A longer journal version is in preparation.

## Folder map

    README.md                          this file: map + run order
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
      instrument_vs_subject.py         item 11: excluding architecture-coded patents
      main_group_inference.py          item 12: wild cluster bootstrap at 133 CPC main groups
      firm_exposure.py                 item 13: firm-level adoption measure
      randomization_inference.py       randomization inference over class assignments
      honest_did_sensitivity.py        Rambachan-Roth relative-magnitudes sensitivity
      identification_hardening.py      identification checks (2026-09-03)
      winsorization_sensitivity.py     lag winsorization at alternative thresholds
      cpc_scheme_robustness.py         CPC 2023.01 scheme-change test, code by code
      camera_ready_tables.py           Tables 1 and 2 of the workshop paper (half-open windows)
      camera_ready_figure.py           Figure 1 of the workshop paper (event study, cited years)
      (+ event study, dose gradient, incumbents, assignee FE, RoS replication,
         thresholds/volume, wild cluster bootstrap 7/9, RQ2 similarity, OpenAlex pilot)
    data/
      raw_full_slim/, raw_sci_slim/    slim Lens exports (columns the build scripts read)
      g06n_cpc.csv.gz                  patent-level CPC codes for G06N
      clean/                           analysis datasets (regenerable from the slim exports):
                                       lag_pairs.csv (v1), lag_pairs_v2.csv.gz (current),
                                       lag_pairs_9classes_v2.csv.gz, lag_pairs_v2_year.csv.gz,
                                       lag_pairs_sci.csv.gz, placebo_pairs(_v2).csv.gz
      DATA_AVAILABILITY.md             what is included and how to regenerate the full exports
    latex/
      extended-abstract.tex/.pdf       anonymized version as submitted for review
      ceurart.cls, ccicons.sty         CEUR template files
    results/                           regression tables + figures

## Reproduction order

    1. Queries + exports:  follow docs/02, log into docs/04
    2. cd code && python3 build_lag_dataset_v2.py      (reads ../data/raw_full_slim)
    3. python3 rebuild_delta_analysis.py               (headline estimates, v1 vs v2)
    4. robustness battery: event study, dose, incumbents, assignee FE, RoS, thresholds,
       wild cluster bootstrap, science controls ("_v2" results files)
    5. decomposition: instrument_vs_subject.py, main_group_inference.py, firm_exposure.py
    6. inference: randomization_inference.py, honest_did_sensitivity.py
    7. workshop paper: cpc_scheme_robustness.py, camera_ready_tables.py, camera_ready_figure.py
    8. VOSviewer maps: follow docs/03

## Workshop paper (camera-ready, 2026-10-02)

The camera-ready answers the reviews. Changes visible in this repository:

- All age windows are half-open, [lo, hi). Earlier shifted-window code used closed intervals, so
  51 of 426,270 pairs aged exactly 8.00 years fell in two windows; the [4, 8) estimate moves from
  +8.524 to +8.517 with an unchanged p-value (results/camera_ready_tables_2026-10-02.md).
- CPC scheme check (results/cpc_scheme_robustness_2026-10-02.md). The three codes previously
  labelled "generative" (G06N3/045, 3/0455, 3/0475) belong to the 2023.01 reorganization of
  G06N3/04. Only 3/0475 is titled "Generative networks"; 3/045 is "Combinations of networks" and
  3/0455 "Auto-encoder networks; Encoder-decoder networks". They are now called architecture
  codes. The codes appear on about 40 percent of G06N patents in every filing year from 2018 to
  2024, so there is no labelling break at 2023 and no rise in their share. The within-G06N effect
  is carried mainly by 3/045; 3/0475 alone is not significant. Scheme-stable main-group contrasts
  reproduce the published estimates.
- New outcome: coefficient of variation of cited-paper age, -0.054 (p = 0.069), reported as
  imprecise.

## Status (v2 data)

Current dataset: lag_pairs_v2.csv.gz, 441,537 pairs (corrected G06N citation batches; +12,426
pairs vs v1, 0 lost). Year-based file: 737,032 pairs.

Headline: fresh-science share DiD -5.56 pp (p = 0.0004); -10.1 under the year-based dating rule;
lag +0.214 (compositional: halves vs science controls, zero within firms, collapses under
cited-publication-year FE, item 14). Inference at the level of treatment assignment (wild
cluster bootstrap, randomization inference) is not significant at the five percent level.

Decomposition: roughly half the share decline is carried by architecture-coded patents
(item 11); firms filing architecture-coded patents in 2023-2024 RETAIN fresh science better in
their other patents (+4.54 pp, p = 0.021, item 13); 133-main-group wild cluster bootstrap in
item 12.

Closed gap (2026-08-25): the citations-g16c-placebo export had been truncated by the export tool
at exactly 1,000 rows. The complete re-export is in place (6,130 works against 6,136 on the Lens
screen, a 0.1 percent discrepancy); G16C 2015-2017 pairs rise from 727 to 1,428 and
placebo_pairs_v2.csv.gz now holds 233,081 pairs. See results/placebo_v2_full_g16c_2026-08-25.md.

## Integrity policy

Raw exports are never hand-edited; every cleaning rule is declared in code (R1-R4 in
build_lag_dataset*.py) and every run prints the full record flow. The architecture-code
definition is the same in every script: G06N3/045, G06N3/0455, G06N3/0475 (current-scheme
codes). Classification sources: official USPTO/EPO CPC definitions (docs/01).
