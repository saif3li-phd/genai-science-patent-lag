# Item 2: incumbents-only re-estimation

Incumbent = applicant with at least one patent filed before 2020-01-01 in the seven-class sample (4,224 distinct normalised applicants). Patent is incumbent if any applicant is incumbent.

## Share of patents filed by incumbents (%)

| group | pre-2023 | post-2023 |
|---|---:|---:|
| treated | 86.1 | 68.8 |
| control | 73.5 | 51.1 |

(The pre-2023 share is mechanically high because incumbency is defined on pre-2020 filings.)

## A. Log lag, pair level, uniform 10-year window

| sample | N pairs | treated x post | SE | p |
|---|---:|---:|---:|---:|
| all | 243,036 | +0.201 | 0.054 | 0.0002 |
| incumbents only | 214,847 | +0.233 | 0.051 | 0.0000 |
| entrants only | 28,189 | +0.004 | 0.059 | 0.9488 |

## B. Share of citations <= 3y, patent level, filings <= 2024-06-30 (pp)

| sample | N patents | treated x post | SE | p |
|---|---:|---:|---:|---:|
| all | 52,559 | -4.93 | 1.52 | 0.0012 |
| incumbents only | 43,868 | -5.13 | 1.96 | 0.0087 |
| entrants only | 8,691 | -2.51 | 2.47 | 0.3105 |

## Treated classes: citation-weighted share <= 3y by incumbency (%)

| | pre-2023 | post-2023 |
|---|---:|---:|
| incumbents | 18.9 | 10.1 |
| entrants | 27.9 | 21.7 |

## Verdict

1. Both results are driven by incumbents, not by entrants. Restricting to applicants active
   before 2020 leaves the lag effect intact and slightly larger (+0.233, p < 0.0001 vs +0.201)
   and leaves the composition effect intact (-5.13 pp, p = 0.009 vs -4.93 pp). Among entrants
   alone neither effect is present (lag +0.004; share -2.5 pp, n.s.).
2. Self-critique #1 (a post-ChatGPT wave of new entrants driving the result) is rejected.
   Entrants in treated classes cite fresher science than incumbents in both periods
   (27.9% vs 18.9% before 2023; 21.7% vs 10.1% after), so the inflow of entrants pushes the
   pooled fresh-science share UP, not down. The decline is a change in how established
   applicants draw on science.
3. Caveats: incumbency is defined within the seven-class sample, so an applicant active before
   2020 only in other classes counts as an entrant (conservative for the incumbent sample,
   noisy for the entrant sample). Applicant-name normalisation is string-based; assignee
   classification and harmonisation (item 5) will refine it. The entrant sample is small
   (8,691 patents) and its estimates are imprecise rather than zero.

Consequence for the paper: add the incumbents-only row to Tables 4 and 5 and a sentence in
Section 6 stating that the effects are located within established applicants.
