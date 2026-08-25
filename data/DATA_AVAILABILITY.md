# Data Availability (anonymized replication archive)

The FULL raw Lens.org exports (all columns) are excluded from this archive for
size and licensing reasons; they are fully regenerable from a Lens.org account
by the protocol below. The SLIM versions of every raw export (the columns the
build scripts read: patents = Lens ID, Application Date, NPL Resolved Lens
ID(s), Applicants, Legal Status, CPC Classifications; citations = Lens ID,
Date Published, Publication Year) ARE included, in data/raw_full_slim/ (50
files, main + placebo windows) and data/raw_sci_slim/ (38 files, science
controls), so the entire pipeline from raw export to every published estimate
runs from this repository as-is (see results/repro_check_2026-08-25.md).
To regenerate the full exports:

1. Follow docs/02_lens_query_protocol.md for the queries
   (class_cpc.symbol:<CLASS>*, Filed 2018-01-01..2025-12-31, US):
   seven main classes (treated G06N, G16B, G16C, C40B; mechanical controls
   F16B, F16H, B65D), the two auxiliary controls (E05B, B25B), the four
   science-intensive alternative controls (G01N, G02B, B01D, G21, addendum
   in docs/01 and docs/02), plus the placebo window 2015-01-01..2017-12-31.
2. Export batch sizes and completeness checks are logged in
   docs/04_export_log_filled.md and in the docs/02 addenda.
3. v1 build: place exports in data/raw/ (main) and data/raw_placebo/
   (placebo), then run code/build_lag_dataset.py.
   v2 build (current): code/build_lag_dataset_v2.py on data/raw_full_slim/.
   Science controls: code/build_sci_controls.py on data/raw_sci_slim/.
   A full reproduction check (rebuild from these slim exports, content-hash
   comparison, headline estimates) is in results/repro_check_2026-08-25.md:
   zero discrepancies.

Cleaned analysis datasets included directly in data/clean/:

- lag_pairs_v2.csv.gz        current main dataset, 441,537 pairs
                             (corrected G06N citation batches)
- lag_pairs_v2_year.csv.gz   year-based dating rule, 737,032 pairs
- lag_pairs_9classes_v2.csv.gz  with E05B/B25B, bootstrap use only
- lag_pairs_sci.csv.gz       science-intensive controls, 817,927 pairs
- placebo_pairs_v2.csv.gz    2015-2017 filings, 233,081 pairs including the
                             2018-2019 slice of the main build; rebuilt
                             2026-08-25 with the complete G16C citation
                             re-export (6,130 works; the original export was
                             truncated at 1,000 rows)
- lag_pairs.csv, placebo_pairs.csv  the v1 files, kept for the v1-vs-v2
                             comparison in results/item10
- data/g06n_cpc.csv.gz       patent-level CPC codes for G06N (dose,
                             item 11 and item 13 scripts)
