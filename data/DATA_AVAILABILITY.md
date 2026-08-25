# Data Availability (anonymized replication archive)

Raw Lens.org exports are excluded from this archive for size and licensing
reasons. They are fully regenerable from a Lens.org account:

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
   v2 build (current): slim exports (Lens ID, dates, Publication Year, CPC)
   in data/raw_full_slim/, then code/build_lag_dataset_v2.py.
   Science controls: slim exports in data/raw_sci_slim/, then
   code/build_sci_controls.py.

Cleaned analysis datasets included directly in data/clean/:

- lag_pairs_v2.csv.gz        current main dataset, 441,537 pairs
                             (corrected G06N citation batches)
- lag_pairs_v2_year.csv.gz   year-based dating rule, 737,032 pairs
- lag_pairs_9classes_v2.csv.gz  with E05B/B25B, bootstrap use only
- lag_pairs_sci.csv.gz       science-intensive controls, 817,927 pairs
- placebo_pairs_v2.csv.gz    2015-2017 filings; the G16C citation batch of
                             this window is truncated (exactly 1,000 rows,
                             re-export pending); placebo results rest on the
                             other six classes
- lag_pairs.csv, placebo_pairs.csv  the v1 files, kept for the v1-vs-v2
                             comparison in results/item10
- data/g06n_cpc.csv.gz       patent-level CPC codes for G06N (dose,
                             item 11 and item 13 scripts)
