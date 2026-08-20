# Data Availability (anonymized replication archive)

Raw Lens.org exports are excluded from this archive for size and licensing
reasons. They are fully regenerable from a Lens.org account:

1. Follow docs/02_lens_query_protocol.md for the seven queries
   (class_cpc.symbol:<CLASS>*, Filed 2018-01-01..2025-12-31, US),
   plus the placebo window 2015-01-01..2017-12-31.
2. Export batch sizes and completeness checks are logged in
   docs/04_export_log_filled.md.
3. Place exports in data/raw/ (main) and data/raw_placebo/ (placebo),
   then run code/build_lag_dataset.py.

The cleaned analysis dataset (data/clean/lag_pairs.csv and
placebo_pairs.csv) is included directly.
