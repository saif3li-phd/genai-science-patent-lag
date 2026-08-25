# Item 10: rebuild with corrected G06N exports, and the R1 year-based sensitivity

Old pairs: 429,111. Rebuilt pairs: 441,537 (+12,426 gained, 0 lost; gains come from works resolved by the corrected 2020a and 2021b G06N citation exports; some multi-class pairs move their class label to G06N because R4 keeps the first class in the fixed alphabetical concatenation, the same rule as the original build).
Year-based file: 737,032 pairs (67 percent more than full-date, recovering works that carry a publication year but no full date).

## Pair counts by class and period, old vs rebuilt

| class | old pre | old post | v2 pre | v2 post |
|---|---:|---:|---:|---:|
| B65D | 5,428 | 781 | 5,428 | 781 |
| C40B | 61,164 | 11,312 | 61,164 | 11,312 |
| F16B | 562 | 77 | 562 | 77 |
| F16H | 2,083 | 310 | 2,083 | 310 |
| G06N | 171,301 | 40,689 | 185,258 | 40,689 |
| G16B | 103,872 | 28,170 | 102,748 | 28,170 |
| G16C | 3,010 | 352 | 2,603 | 352 |

## B. Share <= 3y, patent level, filings <= 2024-06-30 (pp)

| dataset | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| old (paper Table 5) | 19.7 | 11.9 | 7.2 | 5.4 | -4.93 | 1.52 | 0.0012 | 52,559 |
| rebuilt v2 | 20.6 | 11.9 | 7.2 | 5.4 | -5.56 | 1.58 | 0.0004 | 55,539 |
| v2, R1 = publication year | 27.0 | 14.1 | 8.3 | 5.5 | -10.10 | 2.98 | 0.0007 | 78,447 |

## A. Log(1 + lag), pair level, 10-year window

| dataset | treated x post | SE | p | N pairs |
|---|---:|---:|---:|---:|
| old (paper Table 4 spec 3) | +0.201 | 0.054 | 0.0002 | 243,036 |
| rebuilt v2 | +0.214 | 0.054 | 0.0001 | 253,301 |

Item 3 (G16B dedup accounting, from the build log): the two G16B citation batches load 66,772 work rows; 13,620 are the same works exported in both windows; 53,152 distinct works remain and are the merge base. The same rule (one row per work, then one row per patent-paper pair) applies to every class; G06N drops 119,700 cross-batch duplicate work rows across its ten files.
