# Item 4: dose gradient inside G06N

HIGH = any G06N3/* or G06N20/* code; LOW = G06N patent with neither; GENERATIVE = any G06N3/045, 3/0455, 3/0475 code (post-2023 CPC codes; timing caveat). Baseline specs: A log lag, pair level, 10-year window; B share <=3y, patent level, filings <= 2024-06-30; class/subgroup FE + filing-year FE; SE clustered by (sub)class x year.

## G06N patents with citations, by subgroup

| subgroup | pre-2023 | post-2023 |
|---|---:|---:|
| HIGH (G06N3/G06N20) | 36,774 | 7,594 |
| LOW (other G06N) | 3,506 | 742 |
| GENERATIVE codes | 17,118 | 3,471 |

## A. log lag (10-year window), treated x post

| comparison | N | coef | SE | p |
|---|---:|---:|---:|---:|
| (1) HIGH vs mechanical controls | 146,756 | +0.232 | 0.042 | 0.0000 |
| (2) LOW vs mechanical controls | 24,373 | +0.172 | 0.038 | 0.0000 |
| (3) HIGH vs LOW inside G06N | 163,951 | +0.015 | 0.034 | 0.6676 |
| (4) GENERATIVE vs other HIGH inside G06N | 143,167 | +0.079 | 0.051 | 0.1217 |

## B. share <=3y (pp), treated x post

| comparison | N | coef | SE | p |
|---|---:|---:|---:|---:|
| (1) HIGH vs mechanical controls | 44,896 | -6.21 | 1.74 | 0.0003 |
| (2) LOW vs mechanical controls | 5,922 | -0.45 | 1.71 | 0.7907 |
| (3) HIGH vs LOW inside G06N | 47,302 | -5.51 | 3.02 | 0.0684 |
| (4) GENERATIVE vs other HIGH inside G06N | 43,138 | -6.80 | 1.33 | 0.0000 |

## Raw citation-weighted share <=3y inside G06N (%)

| subgroup | pre-2023 | post-2023 |
|---|---:|---:|
| HIGH | 33.8 | 20.4 |
| LOW | 21.1 | 10.7 |
| GENERATIVE | 39.9 | 22.8 |
