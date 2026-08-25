# Item 2: incumbents-only re-estimation

Incumbent = applicant with at least one patent filed before 2020-01-01 in the seven-class sample (4,224 distinct normalised applicants). Patent is incumbent if any applicant is incumbent.

## Share of patents filed by incumbents (%)

| group | pre-2023 | post-2023 |
|---|---:|---:|
| treated | 85.3 | 68.8 |
| control | 73.5 | 51.1 |

(The pre-2023 share is mechanically high because incumbency is defined on pre-2020 filings.)

## A. Log lag, pair level, uniform 10-year window

| sample | N pairs | treated x post | SE | p |
|---|---:|---:|---:|---:|
| all | 253,301 | +0.214 | 0.054 | 0.0001 |
| incumbents only | 223,095 | +0.242 | 0.055 | 0.0000 |
| entrants only | 30,206 | +0.013 | 0.058 | 0.8253 |

## B. Share of citations <= 3y, patent level, filings <= 2024-06-30 (pp)

| sample | N patents | treated x post | SE | p |
|---|---:|---:|---:|---:|
| all | 55,539 | -5.56 | 1.58 | 0.0004 |
| incumbents only | 46,063 | -5.64 | 2.06 | 0.0061 |
| entrants only | 9,476 | -3.30 | 2.44 | 0.1758 |

## Treated classes: citation-weighted share <= 3y by incumbency (%)

| | pre-2023 | post-2023 |
|---|---:|---:|
| incumbents | 19.8 | 10.1 |
| entrants | 29.3 | 21.7 |
