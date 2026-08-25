# Item 6: replication on Reliance on Science (indexing-independent source)

RoS pairs: 603,758 (48,851 patents). Lens pairs: 441,537 (57,126 patents). Patents present in both: 34,986.

## Pairs by class and period, RoS

| class | pre | post |
|---|---:|---:|
| B65D | 6,892 | 799 |
| C40B | 69,045 | 10,173 |
| F16B | 793 | 86 |
| F16H | 4,769 | 630 |
| G06N | 324,377 | 48,644 |
| G16B | 115,569 | 18,865 |
| G16C | 2,974 | 142 |

## B. Share of citations <=3y, patent level, filings <= 2024-06-30 (pp)

| source | sample | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RoS | all RoS patents | 23.1 | 9.9 | 4.8 | 2.9 | -12.22 | 1.62 | 0.0000 | 48,218 |
| RoS | common patents | 22.3 | 9.4 | 4.7 | 2.7 | -11.86 | 1.43 | 0.0000 | 34,508 |
| Lens | common patents | 18.3 | 7.8 | 6.3 | 3.5 | -10.07 | 1.63 | 0.0000 | 34,508 |
| Lens | all Lens patents (baseline) | 20.6 | 11.9 | 7.2 | 5.4 | -5.56 | 1.58 | 0.0004 | 55,539 |

## Shifted windows, RoS, patent level, filings <= 2024-06-30 (pp)

| window | RoS DiD | SE | p | Lens DiD (same patents) | p |
|---|---:|---:|---:|---:|---:|
| <=3y | -11.86 | 1.43 | 0.0000 | -10.07 | 0.0000 |
| 2-5y | +1.40 | 1.87 | 0.4559 | +2.55 | 0.1937 |
| 3-6y | +8.98 | 2.75 | 0.0011 | +7.93 | 0.0235 |
| 4-8y | +15.11 | 3.31 | 0.0000 | +11.56 | 0.0112 |
| >=8y | -5.44 | 2.95 | 0.0648 | -4.36 | 0.3412 |

## A. Log lag, pair level, 10-year window

| source | sample | treated x post | SE | p | N pairs |
|---|---|---:|---:|---:|---:|
| RoS | all | +0.325 | 0.072 | 0.0000 | 367,239 |
| RoS | common patents | +0.337 | 0.073 | 0.0000 | 339,392 |
| Lens | common patents | +0.263 | 0.074 | 0.0004 | 200,212 |

Patent-level fresh-share agreement between sources (common patents): Pearson r = 0.822, mean RoS 34.1% vs Lens 36.1%.
Top-5 cited publication years, RoS, post-2023 treated filings: 2017 (7.5%), 2016 (7.5%), 2018 (6.8%), 2019 (6.2%), 2015 (6.1%)
