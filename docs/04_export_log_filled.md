# Export Log (filled) — Lens.org Data Collection

Query template: `class_cpc.symbol:<CLASS>*`
Fixed filters on every query: Filing Date 2018-01-01 to 2025-12-31; Jurisdiction = US.
Export cap on this account: 50,000 records per export.
Collection date: 2026-08-20.

## A. Query counts (recorded from Lens result screens)

| class | group | patents (Lens) | cited scholarly works (Lens) |
|---|---|---:|---:|
| G06N | treated | 227,436 | 172,880 |
| G16B | treated | 14,390 | 52,683 |
| G16C | treated | 4,326 | 11,895 |
| C40B | treated | 4,079 | 22,197 |
| F16B | control | 23,114 | 938 |
| F16H | control | 31,739 | 1,512 |
| B65D | control | 50,643 | 4,882 |

## B. Export batches received and completeness checks

| class | file(s) | rows loaded | Lens count | delta | note |
|---|---|---:|---:|---|---|
| G16C | patents_G16C.csv | 4,326 | 4,326 | 0 | complete |
| G16C | citations_G16C.csv | 11,722 | 11,895 | -173 (1.5%) | export/indexing gap, accepted |
| C40B | patents_C40B.csv | 4,103 | 4,079 | +24 | boundary-date drift, accepted |
| C40B | citations_C40B.csv | 22,514 | 22,197 | +317 | same, accepted |
| F16B | patents_F16B.csv | 23,114 | 23,114 | 0 | complete |
| F16B | citations_F16B.csv | 938 | 938 | 0 | complete |
| F16H | patents_F16H.csv (re-export) | 31,739 | 31,739 | 0 | complete; earlier 11%-short export replaced 2026-08-20 |
| F16H | citations_F16H.csv | 1,518 | 1,512 | +6 | accepted |
| B65D | patents_B65D_2018-2021 + 2022-2025 | 50,643 | 50,643 | 0 | two batches, complete |
| B65D | citations_B65D.csv | 4,935 | 4,882 | +53 | accepted |
| G16B | patents_G16B.csv | 14,390 | 14,390 | 0 | complete |
| G16B | citations_G16B_2018-2021 + 2022-2025 | 66,772 | 52,683 | +14,089 | expected: works cited in both windows appear twice pre-dedup; deduplicated in pipeline |
| G06N | patents_G06N_2018 ... 2025 (8 files) | 225,627 | 227,436 | -1,809 (0.8%) | year-boundary/unindexed filing dates, accepted |
| G06N | citations_G06N_2018...2024 (10 files incl. 2020a/b, 2021a/b) | 271,645 pre-dedup | 172,880 | dedup in pipeline | complete |

## C. Pipeline flow (auto-printed by build_lag_dataset.py on every run)

State at last run (6 of 7 classes; G06N citations pending):

| stage | rows |
|---|---:|
| pairs exploded from patent NPL links | 347,902 |
| after R1 drop missing dates | 275,285 |
| after R2 drop negative lags | 273,369 |
| after R3 winsorize p99 + R4 dedupe | 251,845 |

Pair counts by class x post (0 = filed before 2023-01-01):

| class | pre | post |
|---|---:|---:|
| B65D | 5,428 | 781 |
| C40B | 61,164 | 11,312 |
| F16B | 562 | 77 |
| F16H | 1,792 | 310 |
| G16B | 130,887 | 34,222 |
| G16C | 4,665 | 645 |

Control-group total: 8,950 pairs — adequate for pooled DiD; thin for
class-year cells (documented decision: expansion candidates E05B, B25B
if needed, pending official CPC definition checks).

## D. Recorded methodological notes

1. Cross-classification: many patents carry more than one of our CPC codes
   (notably G16B+G16C, and C40B+G16C). The pipeline keeps one row per
   (patent, paper) pair; class assignment for dual-coded patents currently
   follows load order. To verify before analysis: no patent appears in both
   a treated and a control class.
2. F16H patents export was 11% short; RESOLVED by re-export (now complete).
3. G06N filing-year histogram peaks ~38k (2023): every yearly patent batch
   is under the 50k cap.
