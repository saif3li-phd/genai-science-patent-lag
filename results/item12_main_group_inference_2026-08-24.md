# Item 12: inference at the CPC main-group level (133 clusters)

Own-class main groups: 133 total, 29 treated, 104 control. Treatment definition unchanged (the patent's own class); the cluster dimension and, in specification (ii), the fixed effects move to the main-group level. Wild cluster bootstrap: Webb weights, 9,999 draws, null imposed.

| outcome | FE | coef | CR1 SE (cluster = main group) | G | p (wild cluster bootstrap) | N |
|---|---|---:|---:|---:|---:|---:|
| share <= 3y (pp) | class FE | -5.560 | 2.953 | 129 | 0.1055 | 55,539 |
| share <= 3y (pp) | main-group FE | -5.116 | 2.971 | 129 | 0.1393 | 55,539 |
| log lag (10y window) | class FE | +0.214 | 0.070 | 123 | 0.0138 | 253,301 |
| log lag (10y window) | main-group FE | +0.202 | 0.076 | 123 | 0.0321 | 253,301 |

Reference: class-level wild bootstrap p-values are 0.109 (share) and 0.115 (lag) with G = 7, and 0.093 / 0.089 with G = 9 (v2 numbers).
