# R3 winsorization sensitivity for the lag outcome

Date: 2026-09-03. Script: `code/winsorization_sensitivity.py`. Data: `data/clean/lag_pairs_v2.csv.gz`.

## Why

Cleaning rule R3 winsorizes `lag_days` at the 99th percentile within CPC class. The paper
declared the rule but never showed what the lag estimate does under other choices. A referee
can reasonably ask whether the result is an artifact of that rule. This file answers it.

## Method

`lag_pairs_v2.csv.gz` stores the winsorized `lag_days`, but it also stores `filing_date` and
`pub_date`, so the unclipped lag is recoverable exactly as their difference in days. We
recomputed it and re-applied R3 at four thresholds, then re-ran every specification of the
paper's Table 6.

Reconstruction check: the recomputed raw lag equals the stored `lag_days` for 98.99 percent of
the 441,537 pairs. The 4,442 differing rows are all rows where the stored value is smaller,
that is, exactly the winsorized top one percent. Their per-class caps differ slightly from a
recomputed 99th percentile because the original build applied the quantile before the final
deduplication step, so the quantile was taken over a marginally larger set. This is a property
of the build order, not a discrepancy in the data.

## Result

Treated x Post on log(1 + lag), class and filing-year fixed effects, SE clustered by class-year.

| R3 rule | 1 none | 2 filings <= 2024-12-31 | 3 uniform 10-year window | 4 specs 2 and 3 | 5 <= 2024-06-30, 8-year window |
|---|---:|---:|---:|---:|---:|
| no winsorization | +0.1211 (0.072) | +0.1383 (0.043) | +0.2136 (<0.0001) | +0.2094 (<0.0001) | +0.2039 (0.0002) |
| 95th percentile | +0.1235 (0.064) | +0.1398 (0.040) | +0.2136 (<0.0001) | +0.2094 (<0.0001) | +0.2039 (0.0002) |
| 99th percentile (paper) | +0.1211 (0.072) | +0.1383 (0.043) | +0.2136 (<0.0001) | +0.2094 (<0.0001) | +0.2039 (0.0002) |
| 99.5th percentile | +0.1210 (0.072) | +0.1382 (0.043) | +0.2136 (<0.0001) | +0.2094 (<0.0001) | +0.2039 (0.0002) |

N pairs: 441,537 / 434,550 / 253,301 / 251,017 / 205,617, identical across rules.

## Reading

Specifications 3 to 5, which include the headline +0.214, are identical to four decimal places
under all four rules. The reason is mechanical: the uniform ten-year window keeps only pairs
with a lag at or below 3,652.5 days, which is far below every class cap, so once the window is
imposed the winsorization has nothing left to clip. Only the two windowless specifications move,
and only in the third decimal, with p between 0.064 and 0.072 throughout.

## Scope, stated so the result is not overread

Winsorizing the upper tail cannot move the primary outcome. The fresh-science share is an
indicator for a lag of three years or less; clipping the longest lags leaves it unchanged. The
script confirms this rather than asserting it: the share of pairs three years old or younger is
18.6021 percent under all four rules, identical to four decimal places. This robustness bears on
H1, the secondary outcome, and on it alone.
