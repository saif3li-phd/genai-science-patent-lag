# Item 13: firm-level GenAI exposure (adoption measured inside the patent data)

Exposure: adopter = files at least one GENERATIVE-coded patent in 2023-2024; continuous version = generative share of the firm's 2023-2024 treated-class patents. Exposure is measured post, so estimates are associations, not causal effects of adoption. Sample: NON-generative treated-class firm patents, filings <= 2024-06-30, firms observed both before and after 2023. Firm, class and filing-year fixed effects; SE clustered by firm.

Firms in sample: 820, of which adopters: 259.

## Raw fresh-science shares on non-generative patents (%, citation-weighted at patent level)

| group | pre-2023 | post-2023 |
|---|---:|---:|
| adopters | 40.4 | 33.6 |
| non-adopters | 26.4 | 14.4 |

## Within-firm estimates on non-generative patents, share <= 3y (pp)

| exposure measure | exposure x post | SE | p | N patents |
|---|---:|---:|---:|---:|
| adopter (0/1) | +4.54 | 1.97 | 0.0211 | 16,505 |
| generative share (0-1) | +6.69 | 4.44 | 0.1320 | 16,505 |
