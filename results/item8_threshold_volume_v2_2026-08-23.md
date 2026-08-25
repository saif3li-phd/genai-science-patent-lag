# Item 8: cumulative thresholds and citation volume versus composition

Pairs with filing <= 2024-06-30: 426,270; patents: 55,539.

## (a) Share of citations to papers at most k years old, patent level (pp)

| threshold | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <= 2 years | 28.2 | 20.7 | 8.6 | 4.1 | -3.50 | 0.95 | 0.0002 | 55,539 |
| <= 3 years | 41.7 | 32.9 | 13.2 | 9.4 | -5.56 | 1.58 | 0.0004 | 55,539 |
| <= 4 years | 52.3 | 42.8 | 21.1 | 14.5 | -3.31 | 2.43 | 0.1733 | 55,539 |
| <= 5 years | 60.4 | 51.7 | 28.2 | 21.4 | -2.09 | 3.73 | 0.5748 | 55,539 |

## (b) Citations per patent: volume versus composition

| group | period | patents | mean citations per patent | mean <= 3y per patent | mean > 3y per patent | median total |
|---|---|---:|---:|---:|---:|---:|
| treated | pre-2023 | 46,061 | 7.64 | 1.57 | 6.07 | 2 |
| treated | post-2023 | 7,720 | 8.48 | 1.01 | 7.47 | 2 |
| control | pre-2023 | 1,502 | 5.37 | 0.39 | 4.99 | 1 |
| control | post-2023 | 256 | 3.82 | 0.21 | 3.62 | 1 |

DiD on log(1 + count), patent level, class FE + year FE, SE clustered class x year:

| outcome | treated x post | SE | p | approx. % change |
|---|---:|---:|---:|---:|
| all citations per patent | +0.055 | 0.054 | 0.3093 | +5.6% |
| citations <= 3y per patent | -0.119 | 0.025 | 0.0000 | -11.2% |
| citations > 3y per patent | +0.117 | 0.059 | 0.0485 | +12.4% |
