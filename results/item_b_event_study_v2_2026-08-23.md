# Option (b): event-study on the fresh-science share and the log lag

Coefficients are treated x filing-year, relative to 2022 (last pre-treatment year); class FE + filing-year FE; SE clustered by class x filing-year. Share model is patent level (one row per patent); lag model is patent level on the median log lag. Joint F-test: all pre-2023 coefficients (2018-2021) equal zero.


## Sample: mature (filings <= 2024-06-30)  (patents = 55,539)

### Outcome: share of citations <= 3y (pp)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.09 | 2.40 | 0.970 |
| 2019 | +2.97 | 1.93 | 0.125 |
| 2020 | -1.22 | 2.01 | 0.542 |
| 2021 | +3.59 | 2.39 | 0.132 |
| 2022 | 0 (ref) | | |
| 2023 | -3.68 | 2.23 | 0.098 |
| 2024 | -7.09 | 3.23 | 0.028 |

Joint test pre-2023 = 0: F = 7.35, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): -5.65 (SE 2.78, p = 0.042); fitted treated trend per year +0.03 (p = 0.963)

### Outcome: median log lag (log points)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.10 | 0.04 | 0.011 |
| 2019 | -0.02 | 0.04 | 0.601 |
| 2020 | -0.07 | 0.03 | 0.021 |
| 2021 | -0.08 | 0.04 | 0.057 |
| 2022 | 0 (ref) | | |
| 2023 | +0.08 | 0.09 | 0.381 |
| 2024 | -0.05 | 0.08 | 0.508 |

Joint test pre-2023 = 0: F = 6.89, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): +0.16 (SE 0.09, p = 0.084); fitted treated trend per year -0.03 (p = 0.105)


## Sample: full sample  (patents = 57,126)

### Outcome: share of citations <= 3y (pp)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.10 | 2.47 | 0.967 |
| 2019 | +2.96 | 1.97 | 0.132 |
| 2020 | -1.20 | 2.06 | 0.561 |
| 2021 | +3.61 | 2.38 | 0.129 |
| 2022 | 0 (ref) | | |
| 2023 | -3.68 | 2.24 | 0.100 |
| 2024 | -2.96 | 2.19 | 0.176 |
| 2025 | -6.02 | 10.35 | 0.561 |
| 2026 | -6.94 | 1.30 | 0.000 |

Joint test pre-2023 = 0: F = 7.08, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): -5.02 (SE 2.69, p = 0.062); fitted treated trend per year +0.07 (p = 0.913)

### Outcome: median log lag (log points)

| filing year | coef | SE | p |
|---|---:|---:|---:|
| 2018 | +0.10 | 0.04 | 0.021 |
| 2019 | -0.02 | 0.04 | 0.625 |
| 2020 | -0.07 | 0.03 | 0.029 |
| 2021 | -0.08 | 0.04 | 0.057 |
| 2022 | 0 (ref) | | |
| 2023 | +0.08 | 0.10 | 0.385 |
| 2024 | -0.12 | 0.06 | 0.032 |
| 2025 | -0.08 | 0.29 | 0.796 |
| 2026 | +0.33 | 0.03 | 0.000 |

Joint test pre-2023 = 0: F = 6.54, p = 0.000

Trend-adjusted treated x post (treated-specific linear trend included): +0.14 (SE 0.09, p = 0.124); fitted treated trend per year -0.03 (p = 0.081)

