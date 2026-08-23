# Item 9: science-intensive alternative controls (G01N, G02B, B01D, G21)

Science-control pairs: 817,927 (64,793 patents). Sample (a) treated vs science controls: 1,237,797 pairs. Sample (b) treated vs all 9 mechanical+2 + 4 science controls: 1,247,402 pairs.

## Pairs by class and period, science controls

| class | pre | post |
|---|---:|---:|
| B01D | 39,735 | 11,133 |
| G01N | 580,036 | 92,900 |
| G02B | 72,088 | 14,908 |
| G21 | 5,058 | 2,069 |

## B. Share of citations <= 3y (pp), patent level, filings <= 2024-06-30

| control group | treated pre % | treated post % | control pre % | control post % | DiD | SE | p (class x year) | G | p (wild cluster bootstrap) | N patents |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| science-intensive only (a) | 19.7 | 11.9 | 10.4 | 6.1 | -4.11 | 0.93 | 0.0000 | 8 | 0.1573 | 114,289 |
| all controls (b) | 19.7 | 11.9 | 10.3 | 6.1 | -4.13 | 0.91 | 0.0000 | 13 | 0.1536 | 116,184 |

Baseline vs mechanical controls (paper Table 5): DiD -4.93 pp, p = 0.0012, WCB p = 0.106 (G = 7), 0.093 (G = 9).

## A. Log(1 + lag), pair level, 10-year window

| control group | treated x post | SE | p (class x year) | G | p (wild cluster bootstrap) | N pairs |
|---|---:|---:|---:|---:|---:|---:|
| science-intensive only (a) | +0.101 | 0.025 | 0.0001 | 8 | 0.0971 | 618,928 |
| all controls (b) | +0.102 | 0.025 | 0.0000 | 13 | 0.0921 | 622,720 |

Baseline vs mechanical controls: +0.201, p = 0.0002, WCB p = 0.111 (G = 7), 0.087 (G = 9).

## Raw fresh-science shares of the control classes (citation-weighted, %, filings <= 2024-06-30)

| class | pre-2023 | post-2023 |
|---|---:|---:|
| B01D | 13.6 | 10.1 |
| G01N | 9.5 | 5.2 |
| G02B | 15.4 | 8.3 |
| G21 | 15.3 | 10.7 |
