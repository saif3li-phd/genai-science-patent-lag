# Item 5: assignee classification and assignee fixed effects

## Patent composition by applicant type (%), patents with at least one citation

| group | period | firm | university/research | government | individual | N |
|---|---|---:|---:|---:|---:|---:|
| treated | pre-2023 | 75.1 | 11.6 | 0.2 | 13.1 | 42,944 |
| treated | post-2023 | 79.8 | 11.8 | 0.1 | 8.3 | 9,256 |
| control | pre-2023 | 79.3 | 7.6 | 0.7 | 12.4 | 1,502 |
| control | post-2023 | 84.4 | 6.5 | 0.0 | 9.1 | 307 |

## Fresh-science share (<=3y) by applicant type, treated classes, citation-weighted (%)

| type | pre-2023 | post-2023 |
|---|---:|---:|
| firm | 18.8 | 12.0 |
| university | 18.2 | 9.4 |
| government | 25.6 | 26.9 |
| individual | 34.2 | 26.0 |

## A. log lag (10-year window): treated x post

| sample | assignee FE | N | coef | SE | p |
|---|---|---:|---:|---:|---:|
| all applicants | no | 243,036 | +0.201 | 0.054 | 0.0002 |
| firms only | no | 174,411 | +0.137 | 0.058 | 0.0187 |
| universities/research only | no | 50,067 | +0.543 | 0.168 | 0.0012 |
| firms only | yes (within-applicant) | 174,411 | -0.022 | 0.052 | 0.6680 |

## B. share <=3y (pp), patent level, filings <= 2024-06-30: treated x post

| sample | assignee FE | N | coef | SE | p |
|---|---|---:|---:|---:|---:|
| all applicants | no | 52,559 | -4.926 | 1.517 | 0.0012 |
| firms only | no | 39,942 | -6.385 | 2.181 | 0.0034 |
| universities/research only | no | 6,017 | -5.326 | 7.837 | 0.4967 |
| firms only | yes (within-applicant) | 39,942 | -4.603 | 1.958 | 0.0187 |

Distinct firm applicants (first-listed, normalised): 5,973. Firm sample with assignee FE identifies treated x post from changes within the same applicant.

## Verdict

1. Composition result: survives every cut. Firms only: -6.4 pp (p = 0.003). Firms with
   assignee fixed effects, i.e. identified from changes inside the same applicant: -4.6 pp
   (p = 0.019). The fresh-science decline is a within-firm change in how established
   companies draw on science, which is exactly the claim the word "corporate" in the title
   requires. Universities show the same raw drop (18.2% -> 9.4%) but the university sample is
   too small for a precise estimate (-5.3 pp, p = 0.50).
2. Lag result: does NOT survive assignee fixed effects. On the firm sample without FE the
   lag lengthening is +0.137 (p = 0.019); within the same firm it is -0.022 (p = 0.67). The
   pair-level lag lengthening is therefore a between-applicant composition effect (which
   applicants patent, and how much universities, whose lag effect is +0.54, weigh in the
   treated post period), not a within-firm slowdown. This is consistent with the earlier
   patent-level null and with item 4 (no dose gradient on the lag margin).
3. Paper consequence, stated plainly: the headline should be the composition result. The
   lag result stays in the paper as a pair-level descriptive fact with its decomposition
   (between-applicant, no within-firm counterpart), not as a causal finding about firm
   behaviour. The abstract sentence "the effect is a composition effect, not a slowdown of
   the average patent" was already correct; it now has a mechanism: applicant mix.
4. Applicant-type mix moved little (firms 75% -> 80% of treated patents), so the
   composition result is not an artefact of type mix either.
5. Caveats: rule-based classification on names (no external register); the first-listed
   applicant defines the assignee key; "individual" is a residual category that also
   catches unusual corporate names.
