# Option (b): event-study on the fresh-science share and the log lag

Coefficients are treated x filing-year, relative to 2022 (last pre-treatment year); class FE + filing-year FE; SE clustered by class x filing-year. Share model is patent level (one row per patent); lag model is patent level on the median log lag. Joint F-test: all pre-2023 coefficients (2018-2021) equal zero.


## Sample: mature (filings <= 2024-06-30)  (patents = 52,559)

### Outcome: share of citations <= 3y (pp)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | -0.02 | 2.39 | 0.992 |
| 2019 | +2.91 | 1.95 | 0.134 |
| 2020 | -1.45 | 2.01 | 0.471 |
| 2021 | +1.20 | 2.38 | 0.613 |
| 2022 | 0 (ref) | | |
| 2023 | -3.66 | 2.23 | 0.101 |
| 2024 | -7.08 | 3.21 | 0.027 |

Joint test pre-2023 = 0: F = 7.15, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): -4.24 (SE 2.31, p = 0.067); fitted treated trend per year -0.22 (p = 0.673)

### Outcome: median log lag (log points)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.11 | 0.04 | 0.008 |
| 2019 | -0.02 | 0.04 | 0.629 |
| 2020 | -0.06 | 0.03 | 0.046 |
| 2021 | -0.02 | 0.04 | 0.655 |
| 2022 | 0 (ref) | | |
| 2023 | +0.08 | 0.10 | 0.387 |
| 2024 | -0.05 | 0.08 | 0.508 |

Joint test pre-2023 = 0: F = 6.73, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): +0.13 (SE 0.09, p = 0.145); fitted treated trend per year -0.02 (p = 0.147)


## Sample: full sample  (patents = 54,146)

### Outcome: share of citations <= 3y (pp)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | -0.01 | 2.46 | 0.997 |
| 2019 | +2.91 | 1.98 | 0.142 |
| 2020 | -1.43 | 2.07 | 0.490 |
| 2021 | +1.21 | 2.37 | 0.609 |
| 2022 | 0 (ref) | | |
| 2023 | -3.66 | 2.25 | 0.103 |
| 2024 | -2.97 | 2.16 | 0.169 |
| 2025 | -6.09 | 10.34 | 0.556 |
| 2026 | -7.19 | 1.27 | 0.000 |

Joint test pre-2023 = 0: F = 6.86, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): -3.58 (SE 2.18, p = 0.101); fitted treated trend per year -0.17 (p = 0.739)

### Outcome: median log lag (log points)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.11 | 0.04 | 0.015 |
| 2019 | -0.02 | 0.04 | 0.650 |
| 2020 | -0.06 | 0.03 | 0.058 |
| 2021 | -0.02 | 0.04 | 0.651 |
| 2022 | 0 (ref) | | |
| 2023 | +0.08 | 0.10 | 0.391 |
| 2024 | -0.12 | 0.06 | 0.035 |
| 2025 | -0.07 | 0.29 | 0.800 |
| 2026 | +0.33 | 0.03 | 0.000 |

Joint test pre-2023 = 0: F = 6.37, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): +0.10 (SE 0.08, p = 0.213); fitted treated trend per year -0.03 (p = 0.111)


## Verdict (recorded against the reading rule fixed before running)

1. Fresh-science share, mature sample: the four pre-2023 coefficients are small, alternate in
   sign (-0.02, +2.91, -1.45, +1.20 pp) and are individually indistinguishable from zero; the
   treated-specific linear trend fitted over all years is flat (-0.22 pp per year, p = 0.67).
   There is NO rising pre-trend inside the 2018-2022 estimation window. The post coefficients
   grow with exposure time: -3.66 pp in 2023 (p = 0.10) and -7.08 pp in 2024 (p = 0.027).
   The trend-adjusted treated x post estimate is -4.24 pp (p = 0.067), close to the baseline
   -4.93 pp. Reading: the composition result survives the event-study check. The "rising
   fresh-science share" seen in the 2015-2019 placebo belongs to the years before 2018 and
   does not continue into the estimation window, so the 2023 break is a break, not the
   continuation of a trend.
2. Caveat on the joint F-test: it rejects (p < 0.001) in every panel, including panels whose
   individual pre-coefficients are all near zero. With seven class clusters the cluster-robust
   F-statistic is unreliable (too few clusters), which is exactly the problem item 3 (wild
   cluster bootstrap) is meant to address. Report the individual coefficients and the flat
   fitted trend; do not lean on the F-test in either direction.
3. Median log lag at the patent level: no post-2023 effect in any year (2023 +0.08, 2024 -0.05,
   both n.s.), confirming the earlier patent-level null. The 2018 coefficient (+0.11, p = 0.008)
   is a pre-period wobble that should be mentioned.
4. 2025 and 2026 filings in the full sample are too thin to read (2025: SE 10 pp).

Consequence for the paper: Section 6.1's sentence "pre-trends were not parallel" must be
narrowed to "fresh-science share was rising in treated classes during 2015-2019; within the
2018-2022 window used for estimation the year-by-year coefficients show no trend". The
trend-adjusted estimate (-4.2 pp) joins Table 5.
