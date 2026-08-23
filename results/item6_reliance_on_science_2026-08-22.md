# Item 6: replication on Reliance on Science (indexing-independent source)

RoS pairs: 603,758 (48,851 patents). Lens pairs: 429,111 (54,009 patents). Patents present in both: 33,362.

## Pairs by class and period, RoS

| class | pre | post |
|---|---:|---:|
| B65D | 6,892 | 799 |
| C40B | 69,045 | 10,173 |
| F16B | 793 | 86 |
| F16H | 4,769 | 630 |
| G06N | 324,377 | 48,644 |
| G16B | 115,569 | 18,865 |
| G16C | 2,974 | 142 |

## B. Share of citations <=3y, patent level, filings <= 2024-06-30 (pp)

| source | sample | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RoS | all RoS patents | 23.1 | 9.9 | 4.8 | 2.9 | -12.22 | 1.62 | 0.0000 | 48,218 |
| RoS | common patents | 22.0 | 9.4 | 4.7 | 2.7 | -11.53 | 1.40 | 0.0000 | 32,884 |
| Lens | common patents | 17.6 | 7.8 | 6.3 | 3.5 | -9.42 | 1.52 | 0.0000 | 32,944 |
| Lens | all Lens patents (baseline) | 19.7 | 11.9 | 7.2 | 5.4 | -4.93 | 1.52 | 0.0012 | 52,559 |

## Shifted windows, RoS, patent level, filings <= 2024-06-30 (pp)

| window | RoS DiD | SE | p | Lens DiD (same patents) | p |
|---|---:|---:|---:|---:|---:|
| <=3y | -11.53 | 1.40 | 0.0000 | -9.42 | 0.0000 |
| 2-5y | +1.27 | 1.90 | 0.5042 | +2.02 | 0.3206 |
| 3-6y | +8.75 | 2.77 | 0.0016 | +7.37 | 0.0358 |
| 4-8y | +14.89 | 3.32 | 0.0000 | +11.30 | 0.0130 |
| >=8y | -5.54 | 2.95 | 0.0602 | -4.52 | 0.3236 |

## A. Log lag, pair level, 10-year window

| source | sample | treated x post | SE | p | N pairs |
|---|---|---:|---:|---:|---:|
| RoS | all | +0.325 | 0.072 | 0.0000 | 367,239 |
| RoS | common patents | +0.335 | 0.074 | 0.0000 | 333,653 |
| Lens | common patents | +0.251 | 0.073 | 0.0006 | 193,246 |

Patent-level fresh-share agreement between sources (common patents): Pearson r = 0.816, mean RoS 33.6% vs Lens 35.3%.
Top-5 cited publication years, RoS, post-2023 treated filings: 2017 (7.5%), 2016 (7.5%), 2018 (6.8%), 2019 (6.2%), 2015 (6.1%)

## Verdict (against the reading rule fixed before running)

1. The composition result replicates on the independent source, and it is larger, not
   smaller. On the 33,362 patents present in both sources the RoS-based DiD on the <=3y share
   is -11.5 pp (p < 0.0001) against -9.4 pp (p < 0.0001) from Lens on the same patents.
   Patent-level fresh shares from the two sources correlate at r = 0.82.
2. The shifted-window pattern is the same in both sources: no change at 2-5 years, gains at
   3-6 and 4-8 years (+8.8 and +14.9 pp in RoS), and a negative coefficient at >=8 years.
   The modal cited publication years in post-2023 treated patents are again 2015-2019.
   The displaced citations went to transformer-era papers in both datasets.
3. The indexing explanation is rejected as the driver of the result. RoS matches
   non-patent references to OpenAlex with its own pipeline, independent of Lens resolution,
   and reproduces the decline. A residual caveat remains: any matcher resolves the very
   newest papers less completely, so the LEVEL of the fresh share is understated in both
   sources; what the replication shows is that the post-2023 CHANGE is not a Lens artefact.
4. Why the effect is larger on the common patents (-9.4 Lens, -11.5 RoS) than in the Lens
   baseline (-4.9): RoS covers granted USPTO patents, so the common set is the granted
   subset. The decline in fresh-science intake is sharper among granted patents than among
   applications. This is worth a sentence in the paper and a granted-only row in Table 5.
5. The lag result also replicates at the pair level (+0.33 RoS, +0.25 Lens on common
   patents), with the same interpretation as before (between-applicant composition; see
   item 5).
6. Limits: 26% of RoS citation rows lack a publication date (11,179 OpenAlex ids not found,
   and Lens-MAG joins without dates); RoS v65 flags almost all citations as applicant-added
   (846 examiner rows in 34.8 million), so the inventor-only contrast cannot be run on this
   version; RoS is granted-patent based, so applications filed in 2024-2025 and not yet
   granted are absent.

Consequence for the paper: Section 6.3 becomes "Replication on an independent citation
source" with the table above; the indexing reading moves from "open" to "rejected as the
driver, with a level caveat"; Section 8 drops the Reliance on Science item.
