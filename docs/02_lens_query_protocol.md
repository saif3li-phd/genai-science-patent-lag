# Step 2-3 Protocol: Lens.org Queries and Exports

Data source: The Lens (lens.org), which links patents to the scholarly works they cite
("scholarly citations" / "cited scholarly works" in Lens, also surfaced as
"patent citations" on the scholarly side, called PatCite in Lens tooling).

## Step 2: Patent queries (one query per CPC class)

In Lens Patent Search, for each of the seven classes
(G06N, G16B, G16C, C40B | F16B, F16H, B65D):

1. Structured search -> Classifications -> CPC -> enter the class symbol
   (prefix match so subgroups are included, e.g. "G06N" covers G06N 3/xx, 20/xx ...).
2. Date filter: Earliest Filing Date (priority) OR Filing Date: 2018-01-01 to 2025-12-31.
   Record which of the two you used; use it consistently for every class.
3. Jurisdiction: start with US only (one office keeps examiner practice comparable
   across groups); expand to EP as a robustness set later.
4. Document type: decide once, apply everywhere:
   - Granted patents: cleaner quality bar, but truncates the most recent filings.
   - Applications: fresher signal for 2024-2025, noisier quality.
   Recommendation for the pilot: applications + granted, flag `legal_status`, and
   run the main model on both samples.
5. Record for the protocol log: query string, date run, result count.

## Step 3: Scholarly-citation export

For each patent result set:
1. Export the patent list (CSV) with at least: Lens ID, publication number,
   earliest filing/priority date, applicants/assignees, CPC codes, legal status.
2. Export the cited scholarly works with the patent-to-paper link, with at least:
   citing patent Lens ID, cited work Lens ID / DOI, cited work publication date.
   In Lens this is available via the patent record's "Cites Scholarly Works" data
   and via bulk export depending on subscription tier.
3. Export caps depend on the account tier (institutional vs. free). If capped,
   split exports by class x filing-year so each batch stays under the cap.
4. Keep every raw export unmodified in `data/raw/`. All cleaning happens in code
   (see build_lag_dataset.py), never by hand-editing exports: this is what makes
   the pipeline auditable and repeatable.

## Pilot acceptance checks (before any analysis)

- Pair counts per class per year (the sparsity check from doc 01).
- Share of citations with a usable cited-work publication date.
- Share of patents with at least one scholarly citation, by group:
  expect this to be far higher in treated classes; report it, do not hide it.

## Protocol log template

| date_run | class | filter_used | doc_types | jurisdiction | n_patents | n_citation_pairs | export_file |
|---|---|---|---|---|---|---|---|

## Addendum 2026-08-22: export protocol for the two additional control classes (item 3b)

Run exactly as for the original seven classes. Four exports in total (two per class).

For CLASS in E05B, then B25B:

1. Lens Patent Search -> Query text editor -> enter exactly:  class_cpc.symbol:CLASS*
   (e.g. class_cpc.symbol:E05B* ). Wildcards work only in the text editor.
2. Filters (check them every time; Lens keeps filters from the previous query):
   Filing Date: 2018-01-01 to 2025-12-31. Jurisdiction: US. Document type: all (applications + granted).
3. Record on the result screen: number of patents, number of cited scholarly works. Write both
   into docs/04 table A.
4. Export 1 (patents): Export -> CSV -> all fields. If the count exceeds 50,000, split by filing
   year ranges so each batch is under the cap. Save as:
      Lens/patents 2018 2025/patents-e05b-csv.csv      (or patents-e05b-2018-2021-csv.csv, ...)
      Lens/patents 2018 2025/patents-b25b-csv.csv
5. Export 2 (cited scholarly works): open "Cited Scholarly Works" for the same result set ->
   Export -> CSV -> all fields. Confirm the header starts with "Lens ID, Title, Date Published"
   (a header starting with "Jurisdiction, Kind" means a patent export was saved by mistake;
   this happened for citations-g06n-2020a and citations-g06n-2021b and must be redone). Save as:
      Lens/patents 2018 2025/citations-e05b-csv.csv
      Lens/patents 2018 2025/citations-b25b-csv.csv
6. Completeness check: rows loaded vs Lens count, difference under 1.5 percent accepted; log in
   docs/04 table B.
7. Then: add E05B and B25B to CONTROL in code/build_lag_dataset.py, rerun it, rerun the baseline
   and the wild cluster bootstrap (G = 9).

Also pending from the same session: re-export the G06N cited scholarly works for the two batches
whose files are patent exports (citations-g06n-2020a and citations-g06n-2021b), then rerun
build_lag_dataset.py.

## Addendum 2026-08-23: exports for the science-intensive control classes

Same protocol as the original exports. For each of G01N, G02B, B01D, G21:
1. Patent search query: class_cpc.symbol:G01N*   (then G02B*, B01D*, G21*)
   Filters: filing date 2018-01-01 to 2025-12-31; jurisdiction = United States;
   both applications and granted patents.
2. Record on the result screen: number of patents, number of cited scholarly works.
3. Export patents (CSV, all fields). If over 50,000, split by filing-year ranges. Names:
      Lens/patents 2018 2025/patents-g01n-csv.csv   (or patents-g01n-2018-2020-csv.csv, ...)
      Lens/patents 2018 2025/patents-g02b-csv.csv
      Lens/patents 2018 2025/patents-b01d-csv.csv
      Lens/patents 2018 2025/patents-g21-csv.csv
4. Export cited scholarly works (CSV, all fields). Check the header starts with
   "Lens ID, Title, Date Published" (NOT "Jurisdiction, Kind"). If over 50,000, split the
   patent result set by filing year and export cited works per batch. Names:
      Lens/patents 2018 2025/citations-g01n-csv.csv   (batched: citations-g01n-2018-2020-csv.csv, ...)
      citations-g02b-csv.csv, citations-b01d-csv.csv, citations-g21-csv.csv
5. Completeness check as before (difference under 1.5 percent accepted); log counts.
6. Then: extend build_lag_dataset.py with CONTROL_SCI = {G01N, G02B, B01D, G21}, build
   lag_pairs_sci.csv, run the two declared estimates and the 13-cluster wild bootstrap.

## G01N export completeness log (2026-08-23, verified against per-year Lens screens)

| Year | Patents screen | Patents file | Cited works screen | Citations files (sum, pre-dedup) | Note |
|---|---:|---:|---:|---:|---|
| 2018 | 27,968 | 27,968 | 119,079 | 147,183 (a+b+c) | complete; batch overlap dedups in pipeline |
| 2019 | 28,192 | 28,192 | 111,274 | 137,677 (a+b+c) | complete |
| 2020 | 27,130 | 27,130 | n/r | 88,424 (a+b) | complete (patents match) |
| 2021 | 25,437 | 25,437 | n/r | 112,645 (a+b+c) | complete |
| 2022 | 22,548 | 22,548 | 63,483 | 72,711 (a+b) | first patent export was incomplete (14,532); re-exported, old file in _wrong_exports/ |
| 2023 | 18,502 | 18,502 | 48,335 | 48,315 | first patent export was incomplete (12,875); re-exported. Citations -20 (0.04%), accepted |
| 2024 | 11,904 | 11,904 | 24,373 | 24,528 | +155 (0.6%), accepted |
| 2025 | 7,971 | 7,971 | 7,031 | 7,126 | +95 (1.4%), accepted |
| Total | 169,652 | 169,652 | | 638,609 pre-dedup | pooled screen count matches sum of years exactly |

All 16 citation files verified to carry the scholarly-work header (Lens ID, Title, Date Published).

## G02B export completeness log (2026-08-23)

Pooled screen count 166,670 patents; cited scholarly works 58,283 (whole period).
Patents: 2018: 26,831; 2019: 28,257; 2020: 26,794; 2021: 24,214; 2022-2023: 40,759;
2024-2025: 19,815. Total 166,670 = pooled screen count exactly. Complete.
Citations: 2018-2021: 47,172 (first attempt was a truncated 1,000-row export, kept in
_wrong_exports/); 2022-2025: 23,280. Sum 70,452 pre-dedup vs 58,283 distinct works on
screen; overlap between the two windows dedups in the pipeline. Headers verified.

## B01D export completeness log (2026-08-23)

Pooled screen: 64,041 patents; cited scholarly works 50,572. Files: patents 2018-2022:
48,912; 2023-2025: 14,411; total 63,323 vs 64,041 pooled = -718 (1.1%), within the 1.5%
acceptance rule (pooled-vs-split indexing gap). Citations: 45,545 + 10,769 = 56,314
pre-dedup vs 50,572 distinct on screen; window overlap dedups in the pipeline. Headers verified.

## G21 export completeness log (2026-08-23)

Screen: 9,663 patents; cited scholarly works 8,302. Files: patents 9,663 (exact match);
citations 8,345 (+43, 0.5%, accepted). Headers verified. Single exports, no batching.

Status: all four science-intensive control classes (G01N, G02B, B01D, G21) fully
exported and verified. Next: build lag_pairs_sci.csv and run the declared estimates.
