# Item 14: cited-publication-year fixed effects on the lag (partial response to Ke 2020)

Pair level, ten-year window, v2 data. Adding cited-publication-year fixed effects to the
baseline lag specification (class FE + filing-year FE, SE clustered class x year):

| specification | treated x post | SE | p | N pairs |
|---|---:|---:|---:|---:|
| baseline | +0.214 | 0.054 | 0.0001 | 253,301 |
| + cited-publication-year FE | +0.065 | 0.047 | 0.166 | 253,301 |

Reading: conditional on the vintage of the cited paper, treated patents are not slower to
cite it. The lag lengthening is carried by WHICH vintages get cited (older ones), not by a
slowdown in citing any given vintage. This completes the compositional reading of the lag
result: between applicants (Section 6.4) and between cited vintages (here). Paper-level
basicness and novelty controls from OpenAlex remain future work.
