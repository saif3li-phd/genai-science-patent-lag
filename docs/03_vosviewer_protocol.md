# Step 8 Protocol: VOSviewer Descriptive Maps (supporting evidence only)

Tool: VOSviewer (van Eck, N.J. & Waltman, L. (2010). Software survey: VOSviewer,
a computer program for bibliometric mapping. Scientometrics 84(2), 523-538.
Official site: https://www.vosviewer.com).

Role in the paper: descriptive illustration of the homogenization question (RQ2),
NOT statistical inference. State this explicitly in the paper.

## Procedure

1. From the Lens treated-group patent exports, build two corpora of titles+abstracts:
   PRE  = filings 2018-2022,  POST = filings 2023-2025.
2. VOSviewer -> Create map based on text data -> import each corpus
   (Lens exports are directly importable in VOSviewer; otherwise use the
   generic CSV/RIS route).
3. Term extraction settings (record them): binary counting; minimum term
   occurrences set so each map keeps roughly 300-800 terms; relevance
   threshold at the default 60%.
4. Produce one term co-occurrence map per corpus with identical settings.
   Identical settings across PRE/POST is what makes the panels comparable.
5. Read-out for the paper: qualitative comparison of cluster structure and
   term concentration between panels. If POST shows visibly fewer, denser
   clusters around model-related vocabulary, present it as descriptive
   evidence consistent with (not proof of) semantic convergence.
6. Export both maps (PNG for the talk, and the VOSviewer map/network files
   for the replication archive).

## Files to archive

- vos_pre_map.txt / vos_pre_network.txt
- vos_post_map.txt / vos_post_network.txt
- settings_log.md (every parameter used, so a reviewer can reproduce the maps)
