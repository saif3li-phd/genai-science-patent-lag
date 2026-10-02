# CPC scheme-change robustness (Reviewer 1, point 3)

Mature sample, filings through 2024-06-30. G06N patents with at least one dated citation: 47,302. Fresh share uses half-open age [0, 3).

## A. Share of G06N patents carrying each code, by filing year (%)

| filing year | N | 3/045 combinations | 3/0455 encoder-decoder | 3/0475 generative | any of the three | any 3/04* | HIGH |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 4,644 | 37.9 | 9.6 | 5.2 | 40.0 | 57.3 | 91.1 |
| 2019 | 7,464 | 39.1 | 10.2 | 6.2 | 41.3 | 57.6 | 91.3 |
| 2020 | 9,685 | 44.7 | 12.0 | 7.3 | 46.5 | 60.0 | 92.1 |
| 2021 | 10,703 | 38.9 | 12.9 | 7.4 | 43.3 | 59.0 | 91.7 |
| 2022 | 7,784 | 32.1 | 11.1 | 6.0 | 38.9 | 55.7 | 89.8 |
| 2023 | 5,454 | 33.5 | 11.9 | 7.2 | 41.1 | 55.3 | 90.4 |
| 2024 | 1,568 | 33.0 | 10.2 | 7.8 | 40.2 | 53.6 | 91.4 |

## B. Within HIGH G06N: each code against the rest of HIGH (share <=3y, pp)

| code group | patents with code (pre / post) | DiD | SE grp x yr | p | SE firm | p firm | firm clusters |
|---|---|---:|---:|---:|---:|---:|---:|
| any of the three (published GENERATIVE) | 17,118 / 2,874 | -6.80 | 1.33 | 0.0000 | 1.61 | 0.0000 | 6,996 |
| 3/045 combinations of networks only | 15,660 / 2,342 | -11.62 | 1.64 | 0.0000 | 1.54 | 0.0000 | 6,996 |
| 3/0455 encoder-decoder only | 4,615 / 811 | -4.08 | 0.99 | 0.0000 | 1.86 | 0.0286 | 6,996 |
| 3/0475 generative networks only | 2,673 / 513 | -5.77 | 3.32 | 0.0822 | 3.69 | 0.1175 | 6,996 |

## C. Scheme-stable definition: HIGH (main groups G06N3, G06N20)

| contrast | DiD | SE class x yr | p | SE firm | p firm | N |
|---|---:|---:|---:|---:|---:|---:|
| HIGH G06N vs mechanical controls | -6.21 | 1.74 | 0.0003 | 2.27 | 0.0062 | 44,896 |
| LOW G06N vs mechanical controls | -0.45 | 1.71 | 0.7907 | 2.92 | 0.8766 | 5,922 |
| HIGH vs LOW inside G06N | -5.51 | 3.02 | 0.0684 | 1.96 | 0.0050 | 47,302 |

