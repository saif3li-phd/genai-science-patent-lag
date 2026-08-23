# Item 1: Shifted-window robustness of the fresh-science result

Spec: patent-level share of citations in each age window ~ treated:post + class FE + filing-year FE; OLS, unweighted (one row per patent); SE clustered by class x filing-year. Group shares are citation-pair-weighted means (as reported in the abstract: 19.7% -> 11.9%). Raw DiD = (treated post - treated pre) - (control post - control pre) on those shares.

Reading rule fixed BEFORE running: the composition result survives if the 2-5y and 3-6y treated:post coefficients are negative and significant and the >=8y coefficient is positive. It collapses into an indexing artifact if the shifted windows are flat or positive.

## A. Main sample (filings 2018-2025, treatment 2023-01-01)

### full (through 2025-12-31)

Pairs: 429,111 | Patents: 54,146

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 19.7 | 11.3 | 7.2 | 4.9 | -6.1 | -4.17 | 1.25 | 0.0009 |
| 2-5y (shifted) | 21.0 | 14.9 | 11.8 | 8.7 | -3.0 | +2.13 | 3.30 | 0.5187 |
| 3-6y (shifted) | 19.1 | 15.5 | 12.9 | 9.8 | -0.4 | +6.63 | 3.79 | 0.0805 |
| 4-8y (shifted) | 22.6 | 21.4 | 18.1 | 14.8 | +2.1 | +8.27 | 2.94 | 0.0049 |
| >=8y (old stock) | 50.8 | 62.6 | 70.3 | 77.7 | +4.4 | -6.66 | 4.07 | 0.1019 |

### mature 2024-06-30

Pairs: 413,844 | Patents: 52,559

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 19.7 | 11.9 | 7.2 | 5.4 | -6.0 | -4.93 | 1.52 | 0.0012 |
| 2-5y (shifted) | 21.0 | 16.1 | 11.8 | 9.5 | -2.6 | +0.78 | 3.98 | 0.8444 |
| 3-6y (shifted) | 19.1 | 16.8 | 12.9 | 10.4 | +0.3 | +5.55 | 4.39 | 0.2058 |
| 4-8y (shifted) | 22.6 | 23.5 | 18.1 | 15.6 | +3.5 | +8.22 | 3.53 | 0.0199 |
| >=8y (old stock) | 50.8 | 59.6 | 70.3 | 76.2 | +2.9 | -5.25 | 4.86 | 0.2808 |

### mature 2024-12-31

Pairs: 422,124 | Patents: 53,372

| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <=3y (baseline) | 19.7 | 11.5 | 7.2 | 5.0 | -6.0 | -4.01 | 1.16 | 0.0006 |
| 2-5y (shifted) | 21.0 | 15.3 | 11.8 | 9.1 | -2.9 | +1.64 | 3.52 | 0.6405 |
| 3-6y (shifted) | 19.1 | 16.0 | 12.9 | 10.2 | -0.4 | +6.20 | 4.00 | 0.1207 |
| 4-8y (shifted) | 22.6 | 22.2 | 18.1 | 15.4 | +2.3 | +7.95 | 3.12 | 0.0109 |
| >=8y (old stock) | 50.8 | 61.5 | 70.3 | 76.9 | +4.2 | -6.15 | 4.33 | 0.1554 |

### Treated group: share of citation pairs by cited-paper publication year (%)

| pub_year | pre-2023 filings | post-2023 filings |
|---|---:|---:|
| 2008 | 4.7 | 3.9 |
| 2009 | 5.0 | 4.2 |
| 2010 | 4.9 | 4.2 |
| 2011 | 5.0 | 4.6 |
| 2012 | 5.2 | 4.8 |
| 2013 | 5.0 | 5.1 |
| 2014 | 5.1 | 5.1 |
| 2015 | 6.0 | 5.7 |
| 2016 | 7.1 | 6.0 |
| 2017 | 7.0 | 5.9 |
| 2018 | 6.5 | 6.1 |
| 2019 | 4.7 | 5.4 |
| 2020 | 3.0 | 5.1 |
| 2021 | 1.4 | 5.2 |
| 2022 | 0.3 | 3.4 |
| 2023 | 0.0 | 1.2 |
| 2024 | 0.0 | 0.1 |

Top-5 cited publication years in post-2023 treated filings: 2018 (6.1%), 2016 (6.0%), 2017 (5.9%), 2015 (5.7%), 2019 (5.4%)

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

## C. Fine age-bin decomposition (mature 2024-06-30; added after seeing A, recorded as post-hoc)

Same patent-level DiD spec, one-year bins of cited-paper age. Where did the mass lost from <=3y go?

| age bin | T pre % | T post % | C pre % | C post % | DiD pp | p |
|---|---:|---:|---:|---:|---:|---:|
| 0-1y | 4.4 | 2.4 | 1.2 | 0.8 | -1.70 | 0.0046 |
| 1-2y | 7.6 | 4.3 | 2.9 | 1.8 | -1.02 | 0.2375 |
| 2-3y | 7.6 | 5.2 | 3.1 | 2.8 | -2.21 | 0.0947 |
| 3-4y | 7.0 | 5.0 | 4.4 | 2.8 | +1.96 | 0.2646 |
| 4-5y | 6.3 | 5.9 | 4.3 | 4.0 | +1.03 | 0.6039 |
| 5-6y | 5.7 | 6.0 | 4.2 | 3.7 | +2.57 | 0.1937 |
| 6-8y | 10.5 | 11.7 | 9.6 | 8.0 | +4.62 | 0.0002 |
| 8-12y | 19.2 | 20.3 | 20.3 | 20.6 | -7.25 | <0.0001 |
| 12y+ | 31.5 | 39.3 | 50.1 | 55.6 | +2.00 | 0.6316 |

Reading: the relative decline is spread over the whole 0-3y range (not only the most
indexing-sensitive 0-1y bin), the gain is concentrated in 6-8y (for 2023-2024 filings this is
papers published 2015-2018), and 8-12y FALLS. The ">=8y old stock" framing is not supported
at the patent level; the ">=8y" rise in the raw pair-weighted shares (50.8% -> 59.6%) is
matched by a larger rise in the control group (70.3% -> 76.2%).

## D. Direct indexing diagnostic: Lens NPL resolution rate by class x filing year

Source: raw Lens patent exports (data/raw), columns `NPL Citation Count` and
`NPL Resolved Citation Count`, summed per class x application year
(rate = resolved / total NPL, %). Computed 2026-08-21 on the researcher's machine
(Lens/npl_resolution_by_class_year.csv holds the patent-level counts).

| filing year | B65D | C40B | F16B | F16H | G06N | G16B | G16C |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 12.0 | 58.4 | 7.1 | 13.0 | 37.2 | 66.7 | 65.9 |
| 2019 | 6.5 | 72.9 | 2.4 | 7.4 | 37.2 | 70.4 | 63.7 |
| 2020 | 7.7 | 72.5 | 3.6 | 11.7 | 39.4 | 70.5 | 62.2 |
| 2021 | 8.0 | 75.4 | 3.4 | 13.7 | 39.8 | 69.3 | 66.3 |
| 2022 | 6.0 | 75.0 | 2.5 | 12.4 | 37.5 | 72.6 | 61.3 |
| 2023 | 5.4 | 76.9 | 2.5 | 7.4 | 37.6 | 70.2 | 62.3 |
| 2024 | 3.5 | 83.9 | 1.1 | 11.0 | 36.5 | 67.8 | 58.0 |
| 2025 | 5.0 | 82.6 | 1.1 | 3.5 | 43.9 | 61.0 | 69.0 |

Reading: no post-2023 collapse in NPL resolution in the treated classes (G06N flat at
37-40% through 2024; G16B and G16C dip 2-4 points in 2024 only). This weakens, but does not
eliminate, the indexing explanation: the rate is for all NPL, not for fresh papers
specifically, and G06N resolves only ~37% of its NPL in every year (arXiv-heavy
citations), so a constant under-resolution of preprints is present in both periods.

## E. Verdict against the pre-specified reading rule

1. The <=3y decline itself is robust: -4.0 to -4.9 pp, p <= 0.0012, in all three samples.
2. The shifted windows FAIL the pre-specified survival test: 2-5y is flat (+0.8 pp, p=0.84)
   and 3-6y is positive (+5.6 pp, p=0.21); 4-8y is positive and significant (+8.2 pp, p=0.02).
   The >=8y coefficient is negative (-5.3 pp, p=0.28), the opposite of the "old canonical
   stock" prediction.
3. Placebo (2015-2019, fake 2017): the <=3y share shows a LARGE positive fake-post effect
   (+13.2 pp, p=0.0003). This is the "rising pre-trend" the abstract presents as a trend
   reversal. For identification it is a parallel-trends violation on exactly the <=3y
   outcome: treated and control were not on parallel paths before 2023, so the -4.9 pp
   cannot be read as a clean causal effect without an explicit trend control.
4. Net: the central finding survives as "fresh-science share fell relative to controls",
   but NOT as "reorientation toward the old canonical stock". The mass moved to the
   4-8y window (2015-2019 publications for 2023-2024 filings). That pattern is consistent
   with a shift toward transformer-era classics AND with slower resolution of the newest
   papers; the shifted-window design cannot separate the two. Section D argues against a
   sharp indexing break, but not against a level effect.

## F. Consequences for the paper (to be decided at the evaluation pause)

- Abstract sentences to revise: "reorientation ... toward the older canonical stock",
  "mid-2010s deep-learning classics absorbing the difference" (partly supported: 6-8y bin),
  and the old-stock (>=8y) statistic, which does not hold at the patent level.
- Required addition: a group-specific linear pre-trend control (or event-study with
  2018-2022 leads) for the <=3y outcome, given the placebo result in B.
- Decisive indexing test needs an indexing-neutral source: Reliance on Science
  (item 6) or OpenAlex resolution of the raw NPL strings.
