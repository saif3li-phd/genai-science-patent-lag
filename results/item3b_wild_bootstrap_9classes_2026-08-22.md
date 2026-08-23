# Item 3a: wild cluster bootstrap (clusters = CPC class, G = 9, Webb weights, B = 9,999, null imposed)

| outcome | sample | coef | CR1 SE (cluster = class) | t | p (cluster = class, t-dist G-1) | p (wild cluster bootstrap) | N |
|---|---|---:|---:|---:|---:|---:|---:|
| share <=3y (pp) | patent level, filings <= 2024-06-30 | -4.39 | 1.58 | -2.78 | 0.0238 | 0.0934 | 52,696 |
| log lag | pair level, 10-year window | +0.202 | 0.058 | 3.51 | 0.0080 | 0.0868 | 243,239 |

Baseline (cluster = class x year) p-values for comparison: share 0.0012; lag 0.0002.

## Item 3b: control group widened to E05B (locks) and B25B (hand tools)

Exports received 2026-08-22 (US, filings 2018-2025, same query protocol): E05B 15,019 patents,
186 cited works, 138 patents with resolved NPL; B25B 12,001 patents, 349 cited works, 122 patents
with resolved NPL. After rules R1-R4: 364 pairs (E05B 157 pre / 24 post; B25B 144 / 39).
Raw files are kept in data/raw_new/ and were appended to the seven-class analysis set as
data/clean/lag_pairs_9classes.csv (429,475 pairs, 9 classes). build_lag_dataset.py should be
rerun with CONTROL extended once the raw folder is consolidated on the researcher's machine.

Baseline (cluster = class x year), 9 classes: share -4.39 pp (p = 0.002); lag +0.202 (p = 0.0001).

## Verdict

1. The two extra classes add clusters but almost no citation pairs (364 of 429,475), exactly
   the sparsity risk recorded in docs/01 at selection time. They raise G from 7 to 9 and move
   the wild cluster bootstrap p-values from 0.106 to 0.093 (share) and from 0.111 to 0.087
   (lag). Point estimates are unchanged (-4.4 pp; +0.20).
2. Honest reading: class-level inference remains marginal (p about 0.09) even with nine
   classes, because mechanical control classes cite science so rarely that they contribute
   clusters without information. The paper should report both clusterings, state that
   class-level inference is limited by the number of science-citing control classes, and
   rest the causal case on the within-design evidence that does not depend on the seven
   classes: the 2023 break in the event study, the dose gradient inside G06N, the
   within-firm assignee-FE estimate, the incumbents-only estimate, and the independent
   replication on Reliance on Science.
3. Possible next step if a referee insists on class-level inference: add science-citing
   control classes outside AI and chemistry (candidates would need the same official
   definition check and a plausibility argument of no GenAI channel), or move to a
   finer treatment definition (CPC main groups) so that G rises into the dozens.
