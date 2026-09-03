# Sensitivity to violations of parallel trends (relative magnitudes)

Patent-level fresh-science share, filings through 2024-06-30, class and filing-year fixed effects, standard errors clustered by class x filing year. Method: the relative-magnitudes restriction of Rambachan and Roth (2023), conservative plug-in version. The construct, the simplification and the declared reading rule are in `code/honest_did_sensitivity.py`.

## Event-study coefficients (treated x year, relative to 2022)

| filing year | coef (pp) | SE |
|---|---:|---:|
| 2018 | +0.09 | 2.40 |
| 2019 | +2.97 | 1.93 |
| 2020 | -1.22 | 2.01 |
| 2021 | +3.59 | 2.39 |
| 2022 (reference) | +0.00 | 0.00 |
| 2023 | -3.68 | 2.23 |
| 2024 | -7.09 | 3.23 |

## Pre-treatment first differences

The restriction is expressed in units of the largest year-to-year change in the differential that the pre-period actually shows.

| transition | change (pp) |
|---|---:|
| 2018->2019 | +2.87 |
| 2019->2020 | -4.19 |
| 2020->2021 | +4.82 |
| 2021->2022 | -3.59 |

Worst pre-treatment first difference: **4.82 pp** (2020->2021).

## Robust identified sets by Mbar

For post period t, the accumulated bound is `t * Mbar * 4.81 pp`. The reported interval widens the identified set by the sampling uncertainty of the coefficient (1.96 SE), which is conservative.

| Mbar | 2023 robust interval | excludes 0 | 2024 robust interval | excludes 0 |
|---:|---|---|---|---|
| 0.00 | [-8.04, +0.68] | no | [-13.43, -0.76] | yes |
| 0.25 | [-9.24, +1.89] | no | [-15.83, +1.65] | no |
| 0.50 | [-10.45, +3.09] | no | [-18.24, +4.06] | no |
| 0.75 | [-11.65, +4.30] | no | [-20.65, +6.46] | no |
| 1.00 | [-12.86, +5.50] | no | [-23.06, +8.87] | no |
| 1.50 | [-15.27, +7.91] | no | [-27.88, +13.69] | no |
| 2.00 | [-17.67, +10.32] | no | [-32.69, +18.51] | no |

## Breakdown values

| period | ignoring sampling error | including sampling error |
|---|---:|---:|
| 2023 | Mbar = 0.76 | Mbar = 0.00 |
| 2024 | Mbar = 0.74 | Mbar = 0.08 |

## Reading

**The estimate does not survive a violation the size of the worst one already in the data.** Including sampling error it excludes zero only up to Mbar = 0.00, meaning the counterfactual differential would have to drift by less than 0.00 times the worst pre-2023 year-to-year movement (4.82 pp) for the effect to be signed with confidence. Ignoring sampling error the breakdown values are 0.76 for 2023 and 0.74 for 2024.

This is a negative result and it is reported as one. It says the pre-period in this design is too unsettled to license a confident causal reading of the event-study coefficients on their own. It does not overturn the point estimate, which is stable across every specification in the paper, and it does not bear on the within-G06N and within-firm evidence, which does not rest on a between-class parallel-trends assumption at all. The correct conclusion is the one the paper already reaches by a different route: the between-class difference-in-differences is descriptive framing, and the inferential weight belongs elsewhere.

