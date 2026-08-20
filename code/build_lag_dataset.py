"""
Steps 4-5: Build the analysis dataset from Lens.org exports (REAL format).

Input (data/raw/), one or more batch files per class:
  patents_<CLASS>*.csv     Lens patent export (contains 'NPL Resolved Lens ID(s)')
  citations_<CLASS>*.csv   Lens 'Cited Scholarly Works' export (work-level)

The patent->paper link comes from the patent file itself: the
'NPL Resolved Lens ID(s)' column lists cited scholarly Lens IDs separated
by ';;'. We explode it into pairs and join publication dates from the
scholarly export.

Output: data/clean/lag_pairs.csv, one row per (patent, cited paper) pair.

Cleaning rules:
  R1. Drop pairs with missing filing date or missing paper publication date.
  R2. Drop negative lags.
  R3. Winsorize lags above the class-level 99th percentile.
  R4. One row per unique (patent_id, paper_id).
"""

from pathlib import Path

import pandas as pd

RAW = Path("../data/raw")
CLEAN = Path("../data/clean")

TREATED = {"G06N", "G16B", "G16C", "C40B"}
CONTROL = {"F16B", "F16H", "B65D"}
POST_CUTOFF = "2023-01-01"

P_ID = "Lens ID"
P_FILING = "Application Date"
P_NPL = "NPL Resolved Lens ID(s)"
P_APPLICANT = "Applicants"
P_STATUS = "Legal Status"
W_ID = "Lens ID"
W_PUB = "Date Published"
W_DOI = "DOI"


def read_batches(prefix: str, cls: str) -> pd.DataFrame:
    files = sorted(RAW.glob(f"{prefix}_{cls}*.csv"))
    if not files:
        return pd.DataFrame()
    df = pd.concat([pd.read_csv(f, dtype=str) for f in files], ignore_index=True)
    print(f"  {cls}: {len(files)} {prefix} file(s), {len(df)} rows")
    return df


def load_class(cls: str) -> pd.DataFrame:
    patents = read_batches("patents", cls)
    works = read_batches("citations", cls)
    if patents.empty or works.empty:
        return pd.DataFrame()

    for col in (P_ID, P_FILING, P_NPL):
        if col not in patents.columns:
            raise SystemExit(f"[{cls}] patents file missing column: {col!r}")
    for col in (W_ID, W_PUB):
        if col not in works.columns:
            raise SystemExit(f"[{cls}] citations file missing column: {col!r}")

    p = patents[[P_ID, P_FILING, P_NPL]
                + [c for c in (P_APPLICANT, P_STATUS) if c in patents.columns]].copy()
    p.columns = ["patent_id", "filing_date", "npl_ids"] + (
        ["assignee"] if P_APPLICANT in patents.columns else []) + (
        ["legal_status"] if P_STATUS in patents.columns else [])

    p = p.dropna(subset=["npl_ids"])
    p["paper_id"] = p["npl_ids"].str.split(";;")
    pairs = p.explode("paper_id").drop(columns=["npl_ids"])
    pairs["paper_id"] = pairs["paper_id"].str.strip()
    pairs = pairs[pairs["paper_id"] != ""]

    w = works[[W_ID, W_PUB] + ([W_DOI] if W_DOI in works.columns else [])].copy()
    w.columns = ["paper_id", "pub_date"] + (["doi"] if W_DOI in works.columns else [])
    w = w.drop_duplicates(subset=["paper_id"])

    df = pairs.merge(w, on="paper_id", how="inner")
    df["cpc_class"] = cls
    return df


def main() -> None:
    frames = [d for c in sorted(TREATED | CONTROL)
              if not (d := load_class(c)).empty]
    if not frames:
        raise SystemExit(f"No usable class files found in {RAW}/")
    df = pd.concat(frames, ignore_index=True)

    n0 = len(df)
    df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
    df["pub_date"] = pd.to_datetime(df["pub_date"], errors="coerce")
    df = df.dropna(subset=["filing_date", "pub_date"])
    n1 = len(df)

    df["lag_days"] = (df["filing_date"] - df["pub_date"]).dt.days
    df = df[df["lag_days"] >= 0]
    n2 = len(df)

    p99 = df.groupby("cpc_class")["lag_days"].transform(lambda s: s.quantile(0.99))
    df["lag_days"] = df["lag_days"].clip(upper=p99)
    df = df.drop_duplicates(subset=["patent_id", "paper_id"])
    n3 = len(df)

    df["treated"] = df["cpc_class"].isin(TREATED).astype(int)
    df["post"] = (df["filing_date"] >= pd.Timestamp(POST_CUTOFF)).astype(int)
    df["filing_year"] = df["filing_date"].dt.year

    CLEAN.mkdir(parents=True, exist_ok=True)
    out = CLEAN / "lag_pairs.csv"
    df.to_csv(out, index=False)

    print(f"\npairs exploded          : {n0}")
    print(f"after R1 missing dates  : {n1}")
    print(f"after R2 negative lags  : {n2}")
    print(f"after R3+R4 final       : {n3}")
    print(f"written -> {out}")
    print("\nPair counts by class x post:")
    print(df.pivot_table(index="cpc_class", columns="post",
                         values="patent_id", aggfunc="count", fill_value=0))
    print("\nMedian lag (days) by class x post:")
    print(df.pivot_table(index="cpc_class", columns="post",
                         values="lag_days", aggfunc="median"))


if __name__ == "__main__":
    main()
