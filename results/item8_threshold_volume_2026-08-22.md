# Item 8: cumulative thresholds and citation volume versus composition

Pairs with filing <= 2024-06-30: 413,844; patents: 52,422.

## (a) Share of citations to papers at most k years old, patent level (pp)

| threshold | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| <= 2 years | 27.2 | 20.7 | 8.6 | 4.1 | -2.72 | 0.90 | 0.0026 | 52,559 |
| <= 3 years | 40.7 | 32.9 | 13.2 | 9.4 | -4.93 | 1.52 | 0.0012 | 52,559 |
| <= 4 years | 51.4 | 42.8 | 21.1 | 14.5 | -2.93 | 2.45 | 0.2314 | 52,559 |
| <= 5 years | 59.7 | 51.7 | 28.2 | 21.4 | -1.94 | 3.73 | 0.6037 | 52,559 |

## (b) Citations per patent: volume versus composition

| group | period | patents | mean citations per patent | mean <= 3y per patent | mean > 3y per patent | median total |
|---|---|---:|---:|---:|---:|---:|
| treated | pre-2023 | 43,081 | 7.88 | 1.55 | 6.33 | 2 |
| treated | post-2023 | 7,720 | 8.48 | 1.01 | 7.47 | 2 |
| control | pre-2023 | 1,502 | 5.37 | 0.39 | 4.99 | 1 |
| control | post-2023 | 256 | 3.82 | 0.21 | 3.62 | 1 |

DiD on log(1 + count), patent level, class FE + year FE, SE clustered class x year:

| outcome | treated x post | SE | p | approx. % change |
|---|---:|---:|---:|---:|
| all citations per patent | +0.061 | 0.055 | 0.2640 | +6.3% |
| citations <= 3y per patent | -0.107 | 0.026 | 0.0001 | -10.1% |
| citations > 3y per patent | +0.116 | 0.060 | 0.0525 | +12.3% |
