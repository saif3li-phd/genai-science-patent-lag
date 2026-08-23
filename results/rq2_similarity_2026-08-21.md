# RQ2: cross-firm similarity of patent abstracts (TF-IDF cosine)

Firm patents in the fixed-seed sample: 44,190; vocabulary 83,788 terms. Cells = class x filing year (min 30 patents). M1 = mean cross-firm cosine (random pairs, <=20k per cell); M2 = mean nearest cross-firm neighbour cosine; M3 = mean within-firm cosine.

## Cell means (treated classes pooled vs control classes pooled, unweighted)

| group | period | M1 cross-firm | M2 nearest neighbour | M3 within-firm | cells |
|---|---|---:|---:|---:|---:|
| treated | 2018-2022 | 0.0222 | 0.1662 | 0.1656 | 20 |
| treated | 2023-2025 | 0.0241 | 0.1640 | 0.1142 | 12 |
| control | 2018-2022 | 0.0176 | 0.1744 | 0.1205 | 15 |
| control | 2023-2025 | 0.0189 | 0.1719 | 0.1138 | 9 |

## Difference-in-differences on cell means (class FE + year FE, SE clustered by class)

| measure | treated x post | SE | p | cells |
|---|---:|---:|---:|---:|
| M1 | +0.0006 | 0.0012 | 0.597 | 56 |
| M2 | +0.0003 | 0.0116 | 0.982 | 56 |
| M3 | -0.0446 | 0.0387 | 0.249 | 56 |

Excluding 2025 filings:

| measure | treated x post | SE | p |
|---|---:|---:|---:|
| M1 | +0.0011 | 0.0012 | 0.371 |
| M2 | +0.0013 | 0.0099 | 0.894 |
| M3 | -0.0461 | 0.0421 | 0.273 |

## Per class and year: M1 cross-firm similarity

| class | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B65D | 0.0155 | 0.0155 | 0.0158 | 0.0153 | 0.0154 | 0.0152 | 0.0155 | 0.0162 |
| C40B | 0.0282 | 0.0323 | 0.0302 | 0.0298 | 0.0311 | 0.0302 | 0.0332 | 0.0281 |
| F16B | 0.0163 | 0.0163 | 0.0164 | 0.0169 | 0.0165 | 0.0172 | 0.0169 | 0.0179 |
| F16H | 0.0206 | 0.0207 | 0.0214 | 0.0205 | 0.0211 | 0.0230 | 0.0240 | 0.0237 |
| G06N | 0.0201 | 0.0206 | 0.0211 | 0.0214 | 0.0221 | 0.0218 | 0.0221 | 0.0234 |
| G16B | 0.0183 | 0.0188 | 0.0190 | 0.0187 | 0.0186 | 0.0198 | 0.0213 | 0.0205 |
| G16C | 0.0168 | 0.0163 | 0.0196 | 0.0199 | 0.0219 | 0.0225 | 0.0239 | 0.0227 |

## Verdict (against the reading rule fixed before running)

1. No cross-firm homogenisation is detectable. The treated x post coefficient is zero on both
   cross-firm measures (M1 +0.0006, p = 0.60; M2 +0.0003, p = 0.98) and stays zero when 2025
   filings are excluded. Cross-firm similarity in G06N drifts upward slowly over the whole
   period (0.020 in 2018 to 0.023 in 2025), but so does similarity in F16H and G16C, and the
   drift starts before 2023.
2. Within-firm similarity (M3) falls in treated classes after 2023 (0.166 to 0.114) more
   than in controls (0.121 to 0.114), although imprecisely (-0.045, p = 0.25). If anything,
   firms' own portfolios became more internally diverse, the opposite of convergence.
3. Reading for the paper: on the lexical measure available here, RQ2 receives a null. The
   vocabulary shift documented with VOSviewer (item 7) is a shift in WHAT treated-class
   patents talk about, not a collapse of distinctiveness BETWEEN firms.
4. Limits: TF-IDF cosine captures shared vocabulary, not meaning; two abstracts describing
   the same idea in different words score low. Transformer embeddings (SciBERT or SPECTER)
   are the planned refinement and must be run on the researcher's machine, where model files
   can be downloaded. The sample caps each class-year at 1,500 patents; firm identity is the
   first-listed applicant after string normalisation; only seven class clusters.
