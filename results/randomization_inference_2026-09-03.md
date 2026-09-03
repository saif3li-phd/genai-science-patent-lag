# Randomization inference on the fresh-science composition estimate

Patent-level share of citations to papers three years old or younger, filings through 2024-06-30, class and filing-year fixed effects. For every way of choosing four classes from the pool as the treated set, the same specification is re-estimated. The reported p-value is the share of assignments producing an estimate at least as extreme as the one the actual assignment produces.

The construct and its declared reading rule are in `code/randomization_inference.py`.

### A. Baseline pool: four treated plus three mechanical controls

- Classes in the pool: 7 (B65D, C40B, F16B, F16H, G06N, G16B, G16C)
- Patents: 55,539
- Assignments evaluated: 35 of 35 (a split with no post-period variation is dropped)
- True estimate: **-5.51 pp**
- Rank of the true estimate, most negative first: **5 of 35**
- One-sided randomization p (as negative or more): **0.1429** (5/35)
- Two-sided randomization p (magnitude): **0.2000** (7/35)
- Finest attainable p in this pool: 0.0286
- Placebo distribution: mean -0.77, sd 4.68, min -12.94, max +7.97

| rank | treated set | DiD (pp) |
|---:|---|---:|
| 1 | B65D, C40B, G06N, G16B | -12.94 |
| 2 | C40B, F16H, G06N, G16B | -7.79 |
| 3 | C40B, F16B, G06N, G16B | -7.56 |
| 4 | B65D, F16B, G06N, G16B | -5.55 |
| 5 | C40B, G06N, G16B, G16C **<- actual** | -5.51 |
| 6 | B65D, F16H, G06N, G16B | -5.50 |
| 7 | F16B, F16H, G06N, G16B | -4.36 |
| 8 | B65D, C40B, F16B, G06N | -3.95 |
| 9 | B65D, C40B, F16H, G06N | -3.80 |
| 10 | C40B, F16B, F16H, G06N | -3.51 |
| 11 | B65D, G06N, G16B, G16C | -3.40 |
| 12 | F16B, G06N, G16B, G16C | -2.96 |
| 13 | B65D, C40B, G06N, G16C | -2.73 |
| 14 | B65D, F16B, F16H, G06N | -2.73 |
| 15 | F16H, G06N, G16B, G16C | -2.68 |
| 16 | C40B, F16B, G06N, G16C | -2.64 |
| 17 | C40B, F16H, G06N, G16C | -2.44 |
| 18 | B65D, F16B, G06N, G16C | -1.89 |
| 19 | F16B, F16H, G06N, G16C | -1.77 |
| 20 | B65D, F16H, G06N, G16C | -1.66 |
| 21 | B65D, C40B, F16B, G16B | +2.11 |
| 22 | C40B, F16B, F16H, G16B | +2.27 |
| 23 | B65D, C40B, F16H, G16B | +2.28 |
| 24 | B65D, C40B, G16B, G16C | +2.98 |
| 25 | B65D, F16B, F16H, G16B | +3.01 |
| 26 | C40B, F16B, G16B, G16C | +3.08 |
| 27 | C40B, F16H, G16B, G16C | +3.24 |
| 28 | B65D, C40B, F16B, F16H | +3.51 |
| 29 | B65D, F16B, G16B, G16C | +3.85 |
| 30 | B65D, F16H, G16B, G16C | +3.97 |
| 31 | F16B, F16H, G16B, G16C | +4.33 |
| 32 | B65D, C40B, F16B, G16C | +4.83 |
| 33 | B65D, C40B, F16H, G16C | +4.94 |
| 34 | C40B, F16B, F16H, G16C | +6.08 |
| 35 | B65D, F16B, F16H, G16C | +7.97 |

### B. Plus the two auxiliary mechanical classes (E05B, B25B)

- Classes in the pool: 9 (B25B, B65D, C40B, E05B, F16B, F16H, G06N, G16B, G16C)
- Patents: 55,650
- Assignments evaluated: 126 of 126 (a split with no post-period variation is dropped)
- True estimate: **-5.16 pp**
- Rank of the true estimate, most negative first: **13 of 126**
- One-sided randomization p (as negative or more): **0.1032** (13/126)
- Two-sided randomization p (magnitude): **0.2222** (28/126)
- Finest attainable p in this pool: 0.0079
- Placebo distribution: mean +0.59, sd 4.63, min -11.32, max +13.29

Ten most negative placebo splits, for inspection:

| rank | treated set | DiD (pp) |
|---:|---|---:|
| 1 | B65D, C40B, G06N, G16B | -11.32 |
| 2 | C40B, E05B, G06N, G16B | -8.34 |
| 3 | C40B, F16H, G06N, G16B | -7.25 |
| 4 | B25B, C40B, G06N, G16B | -7.13 |
| 5 | C40B, F16B, G06N, G16B | -7.10 |
| 6 | B65D, E05B, G06N, G16B | -6.49 |
| 7 | B25B, B65D, G06N, G16B | -5.35 |
| 8 | B25B, E05B, G06N, G16B | -5.33 |
| 9 | B65D, F16B, G06N, G16B | -5.26 |
| 10 | E05B, F16B, G06N, G16B | -5.26 |
| 13 | C40B, G06N, G16B, G16C **<- actual** | -5.16 |

### C. Full pool: plus the four science-intensive controls

- Classes in the pool: 13 (B01D, B25B, B65D, C40B, E05B, F16B, F16H, G01N, G02B, G06N, G16B, G16C, G21)
- Patents: 115,338
- Assignments evaluated: 715 of 715 (a split with no post-period variation is dropped)
- True estimate: **-4.87 pp**
- Rank of the true estimate, most negative first: **64 of 715**
- One-sided randomization p (as negative or more): **0.0895** (64/715)
- Two-sided randomization p (magnitude): **0.2028** (145/715)
- Finest attainable p in this pool: 0.0014
- Placebo distribution: mean +0.76, sd 3.71, min -5.76, max +10.95

Ten most negative placebo splits, for inspection:

| rank | treated set | DiD (pp) |
|---:|---|---:|
| 1 | C40B, G02B, G06N, G16B | -5.76 |
| 2 | E05B, G02B, G06N, G16B | -5.67 |
| 3 | B65D, G02B, G06N, G16B | -5.62 |
| 4 | B25B, G02B, G06N, G16B | -5.56 |
| 5 | F16B, G02B, G06N, G16B | -5.55 |
| 6 | C40B, E05B, G02B, G06N | -5.54 |
| 7 | F16H, G02B, G06N, G16B | -5.53 |
| 8 | B65D, C40B, G02B, G06N | -5.48 |
| 9 | B25B, C40B, G02B, G06N | -5.44 |
| 10 | G02B, G06N, G16B, G21 | -5.43 |
| 64 | C40B, G06N, G16B, G16C **<- actual** | -4.87 |

## Reading

The wild cluster bootstrap and this test answer different questions and both belong in the paper. The bootstrap asks how much sampling variation the estimator has when only seven clusters carry the treatment, and its answer is: enough that the estimate is not significant at five percent. That answer stands and Section 6.5 keeps it. This test asks how unusual the observed treated-versus-control contrast is among all the contrasts these classes could have produced, and it is exact in finite samples.

Neither test rescues the other. Reported together they say what the paper can honestly claim: a stable point estimate whose class-level significance is marginal, sitting at a specific and reportable place in the distribution of alternative class splits.

