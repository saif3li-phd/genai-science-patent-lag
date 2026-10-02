# Camera-ready tables (AI4SciSci 2026)

All age windows half-open [lo, hi). Mature sample: filings through 2024-06-30.

## Table 1. Dataset statistics by class and period

| class | group | patents pre | patents post | pairs pre | pairs post | assignees pre | assignees post | fresh share pre % | fresh share post % |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| G06N | treated | 40,280 | 7,022 | 185,258 | 35,746 | 6,697 | 2,112 | 31.8 | 18.6 |
| G16B | treated | 3,845 | 456 | 102,748 | 22,584 | 1,456 | 237 | 9.4 | 4.4 |
| G16C | treated | 425 | 58 | 2,603 | 229 | 252 | 47 | 16.7 | 21.0 |
| C40B | treated | 1,511 | 184 | 61,164 | 6,886 | 676 | 95 | 5.7 | 1.4 |
| F16B | control | 159 | 24 | 562 | 66 | 106 | 20 | 14.8 | 16.7 |
| F16H | control | 301 | 63 | 2,083 | 220 | 148 | 44 | 5.3 | 6.4 |
| B65D | control | 1,042 | 169 | 5,428 | 693 | 496 | 101 | 7.1 | 4.0 |
| **All treated** | | 46,061 | 7,720 | 351,773 | 65,445 | 8,314 | 2,389 | 20.6 | 11.9 |
| **All control** | | 1,502 | 256 | 8,073 | 979 | 725 | 163 | 7.2 | 5.4 |

Mature sample totals: 55,539 patents, 426,270 citation pairs, 9,860 distinct assignees, 128,643 distinct cited papers. Full sample through 2025: 57,126 patents, 441,537 pairs.

## Table 2. Main results: treated x post, patent level

| outcome | unit | DiD | SE | p | N patents |
|---|---|---:|---:|---:|---:|
| share, age [0, 3) | pp | -5.56 | 1.58 | 0.0004 | 55,539 |
| share, age [2, 5) | pp | +1.41 | 3.94 | 0.7209 | 55,539 |
| share, age [3, 6) | pp | +6.17 | 4.36 | 0.1566 | 55,539 |
| share, age [4, 8) | pp | +8.52 | 3.54 | 0.0161 | 55,539 |
| share, age [8, inf) | pp | -5.17 | 4.85 | 0.2867 | 55,539 |
| mean age of cited papers | years | +0.140 | 0.783 | 0.8583 | 55,539 |
| median age of cited papers | years | +0.352 | 0.757 | 0.6418 | 55,539 |
| CV of cited-paper age (NEW, patents with 2+ citations) | ratio | -0.0537 | 0.0295 | 0.0689 | 31,902 |

Mean CV: treated pre 0.631, post 0.525; control pre 0.491, post 0.427.

