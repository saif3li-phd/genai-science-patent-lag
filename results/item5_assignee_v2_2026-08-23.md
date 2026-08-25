# Item 5: assignee classification and assignee fixed effects

## Patent composition by applicant type (%), patents with at least one citation

| group | period | firm | university/research | government | individual | N |
|---|---|---:|---:|---:|---:|---:|
| treated | pre-2023 | 74.8 | 11.7 | 0.2 | 13.3 | 46,061 |
| treated | post-2023 | 79.8 | 11.8 | 0.1 | 8.3 | 9,256 |
| control | pre-2023 | 79.3 | 7.6 | 0.7 | 12.4 | 1,502 |
| control | post-2023 | 84.4 | 6.5 | 0.0 | 9.1 | 307 |

## Fresh-science share (<=3y) by applicant type, treated classes, citation-weighted (%)

| type | pre-2023 | post-2023 |
|---|---:|---:|
| firm | 19.7 | 12.0 |
| university | 19.0 | 9.4 |
| government | 25.9 | 26.9 |
| individual | 35.5 | 26.0 |

## A. log lag (10-year window): treated x post

| sample | assignee FE | N | coef | SE | p |
|---|---|---:|---:|---:|---:|
| all applicants | no | 253,301 | +0.214 | 0.054 | 0.0001 |
| firms only | no | 180,990 | +0.152 | 0.058 | 0.0090 |
| universities/research only | no | 52,222 | +0.548 | 0.168 | 0.0011 |
| firms only | yes (within-applicant) | 180,990 | -0.023 | 0.052 | 0.6633 |

## B. share <=3y (pp), patent level, filings <= 2024-06-30: treated x post

| sample | assignee FE | N | coef | SE | p |
|---|---|---:|---:|---:|---:|
| all applicants | no | 55,539 | -5.560 | 1.577 | 0.0004 |
| firms only | no | 42,036 | -6.955 | 2.206 | 0.0016 |
| universities/research only | no | 6,406 | -6.557 | 7.886 | 0.4057 |
| firms only | yes (within-applicant) | 42,036 | -4.505 | 1.925 | 0.0193 |

Distinct firm applicants (first-listed, normalised): 6,259. Firm sample with assignee FE identifies treated x post from changes within the same applicant.
