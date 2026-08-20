"""
OpenAlex pilot: pull a trial sample of papers (2018-2025) for the
GenAI science-to-technology lag study.

What it does
------------
1. Queries the OpenAlex /works endpoint for journal articles in a chosen
   research field, split into two cohorts:
       pre-GenAI  : 2018-01-01 .. 2022-12-31
       post-GenAI : 2023-01-01 .. 2025-12-31
2. Keeps only records with a DOI (needed later to match patent NPL
   references in Google Patents / Reliance on Science).
3. Saves one CSV per cohort plus a combined CSV with the fields you need
   downstream: id, doi, title, publication_date, cohort, field, type,
   cited_by_count.

How to run (on your own machine, not inside a restricted environment)
---------------------------------------------------------------------
    pip install requests
    python openalex_pilot.py --email your.email@example.org
Optional:
    python openalex_pilot.py --email you@... --field "artificial intelligence" --n 500

Notes
-----
- The --email flag puts you in OpenAlex's "polite pool" (faster, more
  reliable). No API key is needed; OpenAlex is free.
- Start small (default 500 papers per cohort). Scale up only after the
  pipeline works end to end.
"""

import argparse
import csv
import sys
import time

import requests

BASE = "https://api.openalex.org/works"


def find_field_id(field_name: str, email: str) -> tuple[str, str]:
    """Resolve a free-text field name to an OpenAlex concept ID."""
    r = requests.get(
        "https://api.openalex.org/concepts",
        params={"search": field_name, "per-page": 1, "mailto": email},
        timeout=30,
    )
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        sys.exit(f"No OpenAlex concept found for '{field_name}'.")
    top = results[0]
    concept_id = top["id"].rsplit("/", 1)[-1]  # e.g. C154945302
    print(f"Field resolved: '{top['display_name']}' -> {concept_id}")
    return concept_id, top["display_name"]


def fetch_cohort(concept_id: str, date_from: str, date_to: str,
                 n_target: int, email: str, cohort_label: str) -> list[dict]:
    """Cursor-paginate through /works until n_target records are collected."""
    rows: list[dict] = []
    cursor = "*"
    per_page = min(200, n_target)
    filters = ",".join([
        f"concepts.id:{concept_id}",
        f"from_publication_date:{date_from}",
        f"to_publication_date:{date_to}",
        "type:article",
        "has_doi:true",
    ])

    while len(rows) < n_target and cursor:
        params = {
            "filter": filters,
            "per-page": per_page,
            "cursor": cursor,
            "select": "id,doi,title,publication_date,type,cited_by_count",
            "mailto": email,
        }
        for attempt in range(4):
            try:
                r = requests.get(BASE, params=params, timeout=60)
                if r.status_code == 429:
                    wait = 2 ** attempt
                    print(f"  rate-limited, waiting {wait}s ...")
                    time.sleep(wait)
                    continue
                r.raise_for_status()
                break
            except requests.RequestException as exc:
                if attempt == 3:
                    raise
                print(f"  retrying after error: {exc}")
                time.sleep(2 ** attempt)

        payload = r.json()
        for w in payload.get("results", []):
            rows.append({
                "openalex_id": w["id"].rsplit("/", 1)[-1],
                "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                "title": (w.get("title") or "").strip(),
                "publication_date": w.get("publication_date", ""),
                "type": w.get("type", ""),
                "cited_by_count": w.get("cited_by_count", 0),
                "cohort": cohort_label,
            })
            if len(rows) >= n_target:
                break

        cursor = payload.get("meta", {}).get("next_cursor")
        print(f"  {cohort_label}: {len(rows)}/{n_target}")
        time.sleep(0.2)  # stay well under rate limits

    return rows


def write_csv(path: str, rows: list[dict]) -> None:
    if not rows:
        print(f"WARNING: no rows for {path}")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="OpenAlex pilot sampler")
    ap.add_argument("--email", required=True,
                    help="Your email (OpenAlex polite pool)")
    ap.add_argument("--field", default="artificial intelligence",
                    help="Research field to sample (free text)")
    ap.add_argument("--n", type=int, default=500,
                    help="Papers per cohort (default 500)")
    args = ap.parse_args()

    concept_id, field_name = find_field_id(args.field, args.email)

    pre = fetch_cohort(concept_id, "2018-01-01", "2022-12-31",
                       args.n, args.email, "pre_genai")
    post = fetch_cohort(concept_id, "2023-01-01", "2025-12-31",
                        args.n, args.email, "post_genai")

    for row in pre + post:
        row["field"] = field_name

    write_csv("openalex_pre_genai.csv", pre)
    write_csv("openalex_post_genai.csv", post)
    write_csv("openalex_pilot_combined.csv", pre + post)

    print("\nDone. Next step: match the DOIs in the combined CSV against "
          "non-patent literature references in Google Patents Public Data "
          "(BigQuery) to compute publication-to-filing lags.")


if __name__ == "__main__":
    main()
