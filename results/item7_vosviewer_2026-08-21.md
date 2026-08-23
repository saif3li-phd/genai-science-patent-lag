# Item 7: VOSviewer term maps, G06N patents before and after 2023 (descriptive evidence for RQ2)

Role in the paper: descriptive illustration only, not statistical inference (docs/03).
Date: 2026-08-21. Files: vosviewer/ (corpora, map/network files, PNGs, settings_log.md).

## 1. Corpus construction

Source: Lens G06N patent exports (US, filed 2018-2025, 8 yearly files).
PRE = Application Date 2018-01-01..2022-12-31; POST = 2023-01-01..2025-12-31.
Rows without abstract dropped; duplicates on Lens ID dropped.

Rule D1 (added after round 1, applied to both periods): keep one document per identical
title + abstract text (case- and whitespace-insensitive). Lens exports applications, grants
and continuations of the same text as separate records; one continuation family alone
contributed 349 identical abstracts to POST and produced a spurious outlier cluster.

| corpus | raw docs | after D1 | duplicates removed |
|---|---:|---:|---:|
| PRE 2018-2022 | 166,990 | 96,831 | 70,159 (42.0%) |
| POST 2023-2025 | 58,620 | 43,177 | 15,443 (26.3%) |

Corpus line = title + ". " + abstract (VOSviewer corpus-file route).

## 2. VOSviewer settings (identical across panels, threshold scaled to corpus size)

Counting: binary. Relevance selection: default 60% most relevant terms.
Minimum occurrences: PRE 200 (797 terms meet it, 478 selected);
POST 89 = round(200 / 2.24) (798 meet it, 479 selected). Size ratio PRE/POST = 2.24.
Clustering: VOSviewer defaults (resolution 1.00). No manual term exclusion.

Discarded runs, recorded for transparency: round 1 without D1 (PRE 350 -> 777 terms;
POST 123 -> 810 terms) and a POST run at threshold 200 (226 terms, not size-scaled).

## 3. Comparable statistics from the map files

| statistic | PRE | POST |
|---|---:|---:|
| terms in map | 478 | 479 |
| clusters (VOSviewer default) | 6 | 7 |
| cluster sizes | 174 / 113 / 103 / 42 / 31 / 15 | 154 / 126 / 124 / 37 / 20 / 15 / 3 |
| share of occurrences in top-10 terms | 16.8% | 18.7% |
| share of occurrences in top-50 terms | 41.9% | 43.5% |
| term overlap with the other panel | 371 of 478 | 371 of 479 |
| Jaccard similarity of term sets | 0.633 | |

Network density (links / possible links) is 0.778 in PRE and 0.615 in POST, but this is
not interpretable: with a smaller corpus fewer term pairs co-occur at all, so density falls
mechanically. It is NOT reported as evidence.

## 4. Cluster content (top terms by occurrence)

PRE: C1 applications/user (user, learning model, action, score, request, content);
C2 neural architecture and hardware (neural network, memory, state, signal, layer, vector);
C3 computer vision (image, object, region, electronic device, storage medium, label);
C4 apparatus-style filings (unit, program, basis, target, processing device);
C5 sensing/vehicles (sensor, vehicle, sensor data, command, terminal, robot);
C6 reinforcement learning (computer program, agent, policy, reinforcement learning, trajectory).

POST: C1 applications/user, now organised around response and request
(learning model, user, response, request, action, content; contains LLM, prompt, chatbot,
generative AI, language model, knowledge graph, ai agent);
C2 hardware and quantum (memory, layer, unit, signal, weight, circuit, qubit);
C3 vision merged with generic neural-network and apparatus vocabulary
(apparatus, image, neural network, object, medium, sensor; contains diffusion model,
transformer, latent space);
C4 graph/network and messaging (graph, message, edge, report, terminal, transmission);
C5 claim boilerplate (program product, first set, second set, first/second machine learning model);
C6 reinforcement learning (unchanged); C7 residual (internet, thing, iot).

## 5. Vocabulary shift (occurrences per 1,000 documents; "below threshold" = fewer than
200 occurrences in PRE, i.e. under 2.1 per 1,000)

| term | PRE | POST |
|---|---:|---:|
| large language model | below threshold | 28.6 |
| llm | below threshold | 20.2 |
| language model | 3.9 | 17.4 |
| embedding | 12.5 | 22.1 |
| token | 7.0 | 14.2 |
| generative artificial intelligence | below threshold | 9.9 |
| prompt | below threshold | 9.5 |
| transformer | below threshold | 8.8 |
| generative ai model | below threshold | 5.3 |
| fine tuning | below threshold | 5.1 |
| diffusion model | below threshold | 4.3 |
| ai agent | below threshold | 3.7 |
| synthetic data | below threshold | 3.6 |
| chatbot | below threshold | 3.4 |

Largest new terms in POST (absent from the PRE map): apparatus, response, medium, engine,
program product, large language model, item, llm, measurement, problem, patient, ai model,
tool, generative artificial intelligence, prompt, transformer.
Largest PRE terms absent from the POST map: state, vector, score, server, input data, label,
map, communication, rule, resource, recognition, class, target, real time, profile, metric.

## 6. Reading for the paper (descriptive, stated with its limits)

1. What changed is the vocabulary, not the number of clusters. Under identical, size-scaled
   settings both panels resolve into the same three large blocks (applications/user,
   neural architecture/hardware, vision/perception) plus small satellites. The count of
   clusters is 6 vs 7. The "fewer, denser clusters" pattern anticipated in docs/03 is not
   observed.
2. A generative-AI vocabulary that was below the mapping threshold before 2023 is now
   prominent (LLM, prompt, generative AI, transformer, diffusion model, fine tuning,
   chatbot, AI agent), and it sits inside the applications cluster, which reorganises
   around response/request/query rather than user/service/action.
3. Mild concentration: the top-10 and top-50 terms absorb slightly more of all term
   occurrences after 2023 (+1.9 and +1.6 points). Term-set overlap between panels is
   63% (Jaccard). This is consistent with, but far from proof of, convergence.
4. Vision vocabulary loses relative weight: in PRE the vision cluster is the largest
   distinct block; in POST vision terms merge with generic neural-network and
   apparatus vocabulary.
5. Caveats to state explicitly: (a) the maps describe G06N only, not all treated classes;
   (b) term maps cannot separate firms, so they say nothing about cross-firm similarity
   (that requires item 5 assignee classification plus embeddings); (c) "apparatus",
   "medium", "program product" are claim-drafting boilerplate whose rise reflects drafting
   style and applicant mix (e.g. Japanese and Korean filers), not technology;
   (d) POST includes 2025 filings that are incompletely published, so late-2024/2025
   vocabulary is under-represented.

Bottom line for RQ2 wording: "descriptive evidence of a vocabulary shift toward
generative-model terms and a mild concentration of term usage after 2023; no evidence of
structural collapse into fewer clusters." Replace any stronger homogenization language.
