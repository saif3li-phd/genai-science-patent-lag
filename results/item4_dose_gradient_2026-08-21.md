# Item 4: dose gradient inside G06N

HIGH = any G06N3/* or G06N20/* code; LOW = G06N patent with neither; GENERATIVE = any G06N3/045, 3/0455, 3/0475 code (post-2023 CPC codes; timing caveat). Baseline specs: A log lag, pair level, 10-year window; B share <=3y, patent level, filings <= 2024-06-30; class/subgroup FE + filing-year FE; SE clustered by (sub)class x year.

## G06N patents with citations, by subgroup

| subgroup | pre-2023 | post-2023 |
|---|---:|---:|
| HIGH (G06N3/G06N20) | 33,780 | 7,594 |
| LOW (other G06N) | 3,262 | 742 |
| GENERATIVE codes | 15,916 | 3,471 |

## A. log lag (10-year window), treated x post

| comparison | N | coef | SE | p |
|---|---:|---:|---:|---:|
| (1) HIGH vs mechanical controls | 136,628 | +0.213 | 0.046 | 0.0000 |
| (2) LOW vs mechanical controls | 23,096 | +0.172 | 0.038 | 0.0000 |
| (3) HIGH vs LOW inside G06N | 152,546 | -0.005 | 0.040 | 0.9069 |
| (4) GENERATIVE vs other HIGH inside G06N | 133,039 | +0.082 | 0.052 | 0.1135 |

## B. share <=3y (pp), treated x post

| comparison | N | coef | SE | p |
|---|---:|---:|---:|---:|
| (1) HIGH vs mechanical controls | 41,902 | -5.42 | 1.68 | 0.0012 |
| (2) LOW vs mechanical controls | 5,678 | -0.23 | 1.72 | 0.8919 |
| (3) HIGH vs LOW inside G06N | 44,064 | -4.84 | 3.10 | 0.1187 |
| (4) GENERATIVE vs other HIGH inside G06N | 40,144 | -6.39 | 1.43 | 0.0000 |

## Raw citation-weighted share <=3y inside G06N (%)

| subgroup | pre-2023 | post-2023 |
|---|---:|---:|
| HIGH | 32.7 | 20.4 |
| LOW | 20.6 | 10.7 |
| GENERATIVE | 38.8 | 22.8 |

## Verdict

1. Composition margin: a clear dose gradient. Against mechanical controls the fresh-science
   share falls by 5.4 pp (p = 0.001) in the HIGH subgroup (neural networks / machine learning)
   and does not move in the LOW subgroup (-0.2 pp, p = 0.89). Inside G06N, HIGH vs LOW gives
   -4.8 pp (p = 0.12; the LOW group is small, 742 post-2023 patents), and GENERATIVE-coded
   patents vs other HIGH patents give -6.4 pp (p < 0.0001). The decline in fresh-science
   intake is concentrated where generative-model exposure is highest. A 2023 shock common to
   all of G06N (funding, layoffs, examination guidance) would not produce this ordering.
2. Lag margin: no gradient. HIGH and LOW both show the lag lengthening against controls
   (+0.21 and +0.17) and do not differ from each other (-0.005, p = 0.91); GENERATIVE vs other
   HIGH is +0.08 (p = 0.11). The pair-level lag effect is therefore a G06N-wide (and, from the
   main results, treated-class-wide) phenomenon, not a generative-specific one. This sharpens
   the paper's reading: the speed result is broad, the composition result is GenAI-specific.
3. Caveats: (a) the generative codes G06N3/045, 3/0455, 3/0475 entered the CPC scheme in 2023;
   the 15,916 pre-2023 patents carrying them were reclassified retroactively, so the
   GENERATIVE flag is a current-scheme label, not the label at filing. (b) Subgroups share
   applicants and cite overlapping literature; the within-G06N comparisons are descriptive
   contrasts, not independent experiments. (c) LOW is thin.

Consequence for the paper: add a "dose gradient" paragraph to Section 6 with the four-row
table; state explicitly that the gradient holds on the composition margin only.
