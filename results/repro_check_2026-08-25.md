# Full reproduction check of data/clean (2026-08-25)

Requested by the researcher: rebuild every cleaned analysis dataset from the raw
slim exports in an isolated directory and verify, row by row and estimate by
estimate, that the published files and numbers reproduce exactly.

## Step 1-2: dataset reconstruction (content hash on sorted rows, md5)

| file | published rows | rebuilt rows | content hash match |
|---|---:|---:|---|
| lag_pairs_v2.csv.gz | 441,537 | 441,537 | IDENTICAL |
| lag_pairs_9classes_v2.csv.gz | 441,859 | 441,859 | IDENTICAL |
| lag_pairs_v2_year.csv.gz | 737,032 | 737,032 | IDENTICAL |
| placebo_pairs_v2.csv.gz | 233,081 | 233,081 | IDENTICAL |
| lag_pairs_sci.csv.gz | 817,927 | 817,927 | IDENTICAL |

The class x post pair-count table printed by the rebuild matches Table item10
exactly (G06N 185,258/40,689; G16B 102,748/28,170; G16C 2,603/352; C40B
61,164/11,312; F16B 562/77; F16H 2,083/310; B65D 5,428/781).

## Step 4: headline estimates on the REBUILT files vs the paper

| estimate | rebuilt | published (v0.6.2) |
|---|---|---|
| share <= 3y, patent level, mature | -5.56 (SE 1.58, p 0.0004, N 55,539) | identical |
| log lag, 10y window | +0.214 (SE 0.054, p 0.0001, N 253,301) | identical |
| year-based dating rule | -10.10 (SE 2.98, p 0.0007, N 78,447) | identical |
| vs science controls, share | -4.78 (SE 0.90, p < 0.0001, N 117,269) | identical |
| vs science controls, lag | +0.114 (SE 0.029, p 0.0001, N 629,193) | identical |
| placebo 2017 lag / 10y / share | -0.069 (0.44) / -0.087 (0.27) / +13.55 (0.0001) | identical (same file hash) |

## Verdict

Every cleaned dataset and every headline estimate reproduces exactly from the
raw exports with the declared rules R1-R4. Zero discrepancies. The stale
truncation NOTE inside build_lag_dataset_v2.py was updated to record the
complete G16C re-export.
