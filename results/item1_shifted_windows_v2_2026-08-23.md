# Item 1: Shifted-window robustness of the fresh-science result

Spec: patent-level share of citations in each age window ~ treated:post + class FE + filing-year FE; OLS, unweighted (one row per patent); SE clustered by class x filing-year. Group shares are citation-pair-weighted means (as reported in the abstract: 19.7% -> 11.9%). Raw DiD = (treated post - treated pre) - (control post - control pre) on those shares.

Reading rule fixed BEFORE running: the composition result survives if the 2-5y and 3-6y treated:post coefficients are negative and significant and the >=8y coefficient is positive. It collapses into an indexing artifact if the shifted windows are flat or positive.

## A. Main sample (filings 2018-2025, treatment 2023-01-01)

### full (through 2025-12-31)

Pairs: 441,537 | Patents: 57,126

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 20.6 | 11.3 | 7.2 | 4.9 | -7.0 | -4.79 | 1.33 | 0.0003 |
| 2-5y (shifted) | 21.2 | 14.9 | 11.8 | 8.7 | -3.3 | +2.75 | 3.25 | 0.3971 |
| 3-6y (shifted) | 19.1 | 15.5 | 12.9 | 9.8 | -0.5 | +7.24 | 3.75 | 0.0537 |
| 4-8y (shifted) | 22.5 | 21.4 | 18.1 | 14.8 | +2.2 | +8.57 | 2.95 | 0.0037 |
| >=8y (old stock) | 49.8 | 62.6 | 70.3 | 77.7 | +5.3 | -6.59 | 4.06 | 0.1043 |

### mature 2024-06-30

Pairs: 426,270 | Patents: 55,539

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 20.6 | 11.9 | 7.2 | 5.4 | -6.9 | -5.56 | 1.58 | 0.0004 |
| 2-5y (shifted) | 21.2 | 16.1 | 11.8 | 9.5 | -2.9 | +1.41 | 3.94 | 0.7209 |
| 3-6y (shifted) | 19.1 | 16.8 | 12.9 | 10.4 | +0.2 | +6.17 | 4.36 | 0.1566 |
| 4-8y (shifted) | 22.5 | 23.5 | 18.1 | 15.6 | +3.5 | +8.52 | 3.54 | 0.0161 |
| >=8y (old stock) | 49.8 | 59.6 | 70.3 | 76.2 | +3.9 | -5.17 | 4.85 | 0.2867 |

### mature 2024-12-31

Pairs: 434,550 | Patents: 56,352

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 20.6 | 11.5 | 7.2 | 5.0 | -6.9 | -4.64 | 1.25 | 0.0002 |
| 2-5y (shifted) | 21.2 | 15.3 | 11.8 | 9.1 | -3.2 | +2.27 | 3.47 | 0.5139 |
| 3-6y (shifted) | 19.1 | 16.0 | 12.9 | 10.2 | -0.4 | +6.82 | 3.96 | 0.0852 |
| 4-8y (shifted) | 22.5 | 22.2 | 18.1 | 15.4 | +2.4 | +8.25 | 3.14 | 0.0085 |
| >=8y (old stock) | 49.8 | 61.5 | 70.3 | 76.9 | +5.1 | -6.08 | 4.32 | 0.1590 |

### Treated group: share of citation pairs by cited-paper publication year (%)

| pub_year | pre-2023 filings | post-2023 filings |
|---|---:|---:|
| 2008 | 4.6 | 3.9 |
| 2009 | 4.9 | 4.2 |
| 2010 | 4.8 | 4.2 |
| 2011 | 5.0 | 4.6 |
| 2012 | 5.2 | 4.8 |
| 2013 | 4.9 | 5.1 |
| 2014 | 5.1 | 5.1 |
| 2015 | 6.0 | 5.7 |
| 2016 | 7.1 | 6.0 |
| 2017 | 7.0 | 5.9 |
| 2018 | 6.8 | 6.1 |
| 2019 | 5.1 | 5.4 |
| 2020 | 3.3 | 5.1 |
| 2021 | 1.6 | 5.2 |
| 2022 | 0.2 | 3.4 |
| 2023 | 0.0 | 1.2 |
| 2024 | 0.0 | 0.1 |

Top-5 cited publication years in post-2023 treated filings: 2018 (6.1%), 2016 (6.0%), 2017 (5.9%), 2015 (5.7%), 2019 (5.4%)

### Fine age-bin decomposition (same spec)

| age bin | treated pre % | treated post % | control pre % | control post % | patent-level DiD (pp) | p |
|---|---:|---:|---:|---:|---:|---:|
| 0-1y | 4.8 | 2.4 | 1.2 | 0.8 | -2.21 | 0.0014 |
| 1-2y | 7.9 | 4.3 | 2.9 | 1.8 | -1.28 | 0.1270 |
| 2-3y | 7.8 | 5.2 | 3.1 | 2.8 | -2.06 | 0.1197 |
| 3-4y | 7.1 | 5.0 | 4.4 | 2.8 | +2.21 | 0.2049 |
| 4-5y | 6.3 | 5.9 | 4.3 | 4.0 | +1.26 | 0.5211 |
| 5-6y | 5.7 | 6.0 | 4.2 | 3.7 | +2.71 | 0.1696 |
| 6-8y | 10.4 | 11.7 | 9.6 | 8.0 | +4.55 | 0.0004 |
| 8-12y | 19.0 | 20.3 | 20.3 | 20.6 | -7.25 | 0.0000 |
| 12-99y | 30.9 | 39.3 | 50.1 | 55.6 | +2.09 | 0.6170 |

## B. Placebo sample (filings 2015-2019, fake treatment 2017-01-01)

### placebo, all filings 2015-2019

Pairs: 231,929 | Patents: 24,791

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 16.1 | 20.1 | 9.8 | 7.5 | +6.3 | +13.19 | 3.61 | 0.0003 |
| 2-5y (shifted) | 20.9 | 21.0 | 14.8 | 12.9 | +2.0 | -1.82 | 2.25 | 0.4196 |
| 3-6y (shifted) | 21.4 | 19.3 | 16.8 | 15.6 | -0.9 | -5.48 | 2.45 | 0.0256 |
| 4-8y (shifted) | 28.0 | 24.5 | 24.7 | 22.7 | -1.5 | -4.36 | 1.89 | 0.0208 |
| >=8y (old stock) | 48.9 | 48.4 | 60.6 | 65.3 | -5.1 | -6.47 | 2.39 | 0.0069 |
