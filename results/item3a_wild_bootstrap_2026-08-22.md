# Item 3a: wild cluster bootstrap (clusters = CPC class, G = 7, Webb weights, B = 9,999, null imposed)

| outcome | sample | coef | CR1 SE (cluster = class) | t | p (cluster = class, t-dist G-1) | p (wild cluster bootstrap) | N |
|---|---|---:|---:|---:|---:|---:|---:|
| share <=3y (pp) | patent level, filings <= 2024-06-30 | -4.93 | 1.75 | -2.82 | 0.0302 | 0.1060 | 52,559 |
| log lag | pair level, 10-year window | +0.201 | 0.063 | 3.20 | 0.0186 | 0.1111 | 243,036 |

Baseline (cluster = class x year) p-values for comparison: share 0.0012; lag 0.0002.

## Verdict (stated plainly)

1. When inference is done at the level at which treatment is assigned (the CPC class, G = 7),
   neither headline estimate reaches conventional significance: wild cluster bootstrap
   p = 0.106 for the fresh-science share and p = 0.111 for the log lag. The class x year
   clustering used in the baseline (p = 0.001 and 0.0002) treats years within a class as
   independent and is optimistic.
2. This does not reverse the point estimates or the pattern of independent confirmations
   (event-study break in 2023, incumbents-only, dose gradient inside G06N, within-firm
   assignee FE, replication on Reliance on Science). It does mean the paper must report
   class-level bootstrap p-values next to the baseline p-values and must say that, with seven
   classes, the design has limited power for class-level inference. Item 3b (two additional
   control classes, E05B and B25B) raises G to 9 and is the direct remedy; the within-G06N
   dose gradient and the within-firm estimates provide inference that does not depend on the
   seven-class structure.
3. Paper consequence: Tables 4 and 5 gain a "wild cluster bootstrap p (G = 7)" column; the
   abstract keeps "robust across specifications" but drops any phrase implying class-level
   significance; Section 8 keeps item 3b as planned.
