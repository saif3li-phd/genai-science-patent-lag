# Item 11: instrument versus subject matter (excluding generative-coded patents)

Reading rule fixed before running: the behavioral interpretation is supported if the fresh-science DiD excluding GENERATIVE patents stays negative, significant, and of broadly comparable magnitude; a collapse toward zero reframes the claim as a shift in the direction of invention.

GENERATIVE-coded G06N patents (current-scheme codes G06N3/045, 3/0455, 3/0475): 20,589 of 48,616 G06N patents with citations (42 percent).

## B. Share <= 3y (pp), patent level, filings <= 2024-06-30

| sample | DiD | SE | p | N patents |
|---|---:|---:|---:|---:|
| (0) baseline, all treated | -5.56 | 1.58 | 0.0004 | 55,539 |
| (1) excluding GENERATIVE G06N patents | -2.73 | 1.60 | 0.0879 | 35,547 |
| (2) excluding all HIGH G06N patents | -1.98 | 1.68 | 0.2384 | 12,401 |
| (3) application classes only (G16B, G16C, C40B) | -2.92 | 1.69 | 0.0831 | 8,237 |
| (4) non-generative HIGH G06N vs mechanical | -2.86 | 1.84 | 0.1197 | 24,904 |

## A. Log(1 + lag), pair level, 10-year window

| sample | treated x post | SE | p | N pairs |
|---|---:|---:|---:|---:|
| (0) baseline, all treated | +0.214 | 0.054 | 0.0001 | 253,301 |
| (1) excluding GENERATIVE G06N patents | +0.176 | 0.054 | 0.0012 | 182,732 |
| (2) excluding all HIGH G06N patents | +0.174 | 0.062 | 0.0049 | 110,134 |
| (3) application classes only (G16B, G16C, C40B) | +0.157 | 0.065 | 0.0157 | 89,350 |
| (4) non-generative HIGH G06N vs mechanical | +0.162 | 0.042 | 0.0001 | 76,187 |

## C. Within-firm (assignee fixed effects, first-listed-applicant firm sample), share <= 3y (pp)

| sample | DiD | SE | p | N patents |
|---|---:|---:|---:|---:|
| (5a) all treated | -4.70 | 1.97 | 0.0169 | 41,798 |
| (5b) excluding GENERATIVE G06N patents | -3.01 | 2.11 | 0.1539 | 25,840 |

Note: the firm sample here uses the first-listed-applicant regex classification (as in RQ2 and
item 13), which is slightly smaller than Table 9's priority-rule classification (item 5); the
all-treated within-firm estimate is -4.70 here versus -4.51 there for that reason.

## Verdict under the pre-declared reading rule (canonical GENERATIVE codes G06N3/045, 3/0455, 3/0475)

The result sits between the two poles of the rule, and closer to the subject-matter pole.
Roughly half of the baseline composition effect is carried by generative-coded G06N patents
(42 percent of G06N patents with citations). Outside them the point estimates remain negative
everywhere (-2.0 to -3.0 pp) but none is significant at 5 percent (p between 0.08 and 0.24).
The lag outcome, by contrast, is significant in every exclusion subsample of this file
(without applicant fixed effects). Consequence for the paper: the dominant channel of the
fresh-science decline is the reorientation of inventive output toward generative-model
patents; a residual broader decline of two to three points appears consistently but cannot
be established precisely. The refutation of the acceleration narrative stands in either
reading: no subsample shows a speed-up in the uptake of new science.
