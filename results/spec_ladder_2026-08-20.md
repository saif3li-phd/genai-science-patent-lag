# Truncation-Treatment Specification Ladder (preliminary, pre-controls)

Model: log(1+lag_days) ~ treated:post + class FE + year FE, SE clustered class-year.
Date run: 2026-08-20. Data: 7/7 classes, complete exports.

| spec | truncation guard | N pairs | coef (treated x post) | p |
|---|---|---:|---:|---:|
| 1 | none (baseline) | 429,111 | +0.110 | 0.092 |
| 2 | drop filings > 2024-12-31 | 422,124 | +0.126 | 0.056 |
| 3 | uniform 10y citation window | 243,036 | +0.201 | 0.0002 |
| 4 | 2 + 3 combined | 240,752 | +0.197 | 0.0002 |
| 5 | strictest: >2024-06-30 dropped, 8y window | 196,169 | +0.191 | 0.0005 |

## Reading (recorded honestly, before paper-level controls)

The sign is POSITIVE and it strengthens, not weakens, as truncation guards
tighten. Preliminary direction: the paper-to-patent lag LENGTHENED more in
GenAI-exposed classes after 2023 relative to mechanical controls.

Interpretation is premature before paper-level controls (basicness/novelty
mix may have shifted post-2023 in treated fields, e.g., a surge of citations
to older foundational AI papers would mechanically lengthen measured lags).
Candidate mechanism to test: post-2023 patents citing canonical older
literature (attention/transformer-era classics) rather than the newest science.

Next modeling steps: paper-age composition control, cited-paper-year FE,
then placebo (needs 2015-2017 exports).
