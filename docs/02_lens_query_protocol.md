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
