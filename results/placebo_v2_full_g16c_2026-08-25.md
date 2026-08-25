# Placebo 2017, rebuilt with the complete G16C citation export (2026-08-25)

The original citations-g16c-placebo export was truncated by the export tool at
exactly 1,000 rows. The complete re-export (6,130 works vs 6,136 on the Lens
screen, a 0.1 percent discrepancy, within the 1.5 percent tolerance) replaces
it; the truncated file is quarantined in _wrong_exports/. G16C 2015-2017 pairs
rise from 727 to 1,428; placebo_pairs_v2.csv.gz now holds 233,081 pairs
(2015-2017: 101,184 + 2018-2019 from the main v2 build: 131,897).

Design unchanged: false treatment 2017-01-01 on the 2015-2019 window, class FE +
filing-year FE, SE clustered class x year.

## Lag placebo (log lag)

| spec | coef (treated x fake-post) | p | N pairs | previous (truncated G16C) |
|---|---:|---:|---:|---|
| baseline | -0.069 | 0.4373 | 233,081 | -0.066, p 0.46 |
| 10y citation window | -0.087 | 0.2656 | 144,095 | -0.085, p 0.28 |

No placebo effect on the lag; unchanged.

## Composition placebo (share <= 3y, patent level)

| quantity | value | previous |
|---|---:|---|
| treated 2015-2016 (citation-weighted) | 15.9% | 16.1% |
| treated 2017-2019 | 20.0% | 20.1% |
| control 2015-2016 | 9.8% | 9.8% |
| control 2017-2019 | 7.5% | 7.5% |
| placebo DiD | +13.55 pp | +13.2 |
| p | 0.0001 | 0.0003 |
| N patents | 24,871 | |

Reading: identical conclusions. The pre-2018 rise in treated fresh-science
intake is confirmed on the complete data; the post-2023 decline remains a
trend reversal. Paper sections 4.4 and 6.1 updated (v0.6.2).
