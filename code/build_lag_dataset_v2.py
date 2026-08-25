"""
Revision plan item 1 (+ groundwork for items 2 and 5): rebuild the analysis dataset
from slim extracts that include the CORRECTED G06N citation batches (2020a, 2021b),
plus two new columns kept for later steps:
  pub_year   (Publication Year of the cited work; present for ~98 percent of works)
  main_group (the patent's own-class CPC main group, e.g. G06N3, F16B5, parsed from
              CPC Classifications; empty when no code of the own class appears)

Inputs: /mnt/user-data/uploads/.../data/raw_full_slim/*.slim.csv.gz
  patents:  Lens ID, Application Date, NPL Resolved Lens ID(s), Applicants,
            Legal Status, CPC Classifications
  citations: Lens ID, Date Published, Publication Year

Outputs (../data/clean/):
  lag_pairs_v2.csv.gz          7 classes, cleaning rules R1-R4 unchanged (R1 = full date)
  lag_pairs_9classes_v2.csv.gz + E05B, B25B
  lag_pairs_v2_year.csv.gz     R1 relaxed to publication YEAR (item 2 sensitivity):
                               pairs whose work has a year but possibly no full date;
                               age_years = filing_year - pub_year; negatives dropped;
                               one row per (patent, paper)
  placebo_pairs_v2.csv.gz      2015-2017 filings + 2018-2019 from the main build
Also prints the G16B dedup accounting explicitly (item 3).
"""

import re
from pathlib import Path
import pandas as pd

RAW = Path("/mnt/user-data/uploads/Researchs/GenAI-Sci2Tech/sci-tech-lag-C45D/data/raw_full_slim")
CLEAN = Path("../data/clean")
TREATED = {"G06N", "G16B", "G16C", "C40B"}
CONTROL7 = {"F16B", "F16H", "B65D"}
EXTRA = {"E05B", "B25B"}
POST = pd.Timestamp("2023-01-01")


def main_group(codes, cls):
    if not isinstance(codes, str):
        return ""
    for c in codes.split(";;"):
        c = c.strip()
        if c.startswith(cls):
            m = re.match(rf"({cls}\s?\d+)", c)
            if m:
                return m.group(1).replace(" ", "")
    return ""


def load_class(cls, placebo=False):
    tag = "-placebo" if placebo else ""
    pf = sorted(RAW.glob(f"patents-{cls.lower()}{tag}-*.slim.csv.gz")) + sorted(RAW.glob(f"patents-{cls.lower()}{tag}*.slim.csv.gz"))
    cf = sorted(RAW.glob(f"citations-{cls.lower()}{tag}-*.slim.csv.gz")) + sorted(RAW.glob(f"citations-{cls.lower()}{tag}*.slim.csv.gz"))
    pf = sorted(set(pf)); cf = sorted(set(cf))
    if placebo:
        pf = [f for f in pf if "placebo" in f.name]; cf = [f for f in cf if "placebo" in f.name]
    else:
        pf = [f for f in pf if "placebo" not in f.name]; cf = [f for f in cf if "placebo" not in f.name]
    p = pd.concat([pd.read_csv(f, dtype=str) for f in pf], ignore_index=True)
    w = pd.concat([pd.read_csv(f, dtype=str) for f in cf], ignore_index=True)
    w_raw = len(w)
    p = p.rename(columns={"Lens ID": "patent_id", "Application Date": "filing_date",
                          "NPL Resolved Lens ID(s)": "npl_ids", "Applicants": "assignee",
                          "Legal Status": "legal_status", "CPC Classifications": "cpc_codes"})
    p = p.drop_duplicates("patent_id")
    p["main_group"] = p["cpc_codes"].map(lambda s: main_group(s, cls))
    p = p.drop(columns=["cpc_codes"]).dropna(subset=["npl_ids"])
    p["paper_id"] = p["npl_ids"].str.split(";;")
    pairs = p.explode("paper_id").drop(columns=["npl_ids"])
    pairs["paper_id"] = pairs["paper_id"].str.strip()
    pairs = pairs[pairs["paper_id"] != ""]
    w = w.rename(columns={"Lens ID": "paper_id", "Date Published": "pub_date",
                          "Publication Year": "pub_year"})
    w = w.drop_duplicates("paper_id")
    print(f"  {cls}{tag}: {len(pf)}p/{len(cf)}c files; works {w_raw:,} -> {len(w):,} after dedup "
          f"({w_raw - len(w):,} cross-batch duplicates removed)")
    df = pairs.merge(w, on="paper_id", how="inner")
    df["cpc_class"] = cls
    return df


def clean(df, post=POST):
    n0 = len(df)
    df["filing_date"] = pd.to_datetime(df["filing_date"], errors="coerce")
    df["pub_dt"] = pd.to_datetime(df["pub_date"], errors="coerce")
    df["pub_year_n"] = pd.to_numeric(df["pub_year"], errors="coerce")
    df = df.dropna(subset=["filing_date"])
    # full-date branch (R1 as in the paper)
    full = df.dropna(subset=["pub_dt"]).copy()
    full["lag_days"] = (full["filing_date"] - full["pub_dt"]).dt.days
    full = full[full["lag_days"] >= 0]
    p99 = full.groupby("cpc_class")["lag_days"].transform(lambda s: s.quantile(0.99))
    full["lag_days"] = full["lag_days"].clip(upper=p99)
    full = full.drop_duplicates(subset=["patent_id", "paper_id"])
    # year branch (item 2)
    yr = df.dropna(subset=["pub_year_n"]).copy()
    yr["filing_year"] = yr["filing_date"].dt.year
    yr["age_years"] = yr["filing_year"] - yr["pub_year_n"]
    yr = yr[yr["age_years"] >= 0]
    yr = yr.drop_duplicates(subset=["patent_id", "paper_id"])
    for d in (full, yr):
        d["treated"] = d["cpc_class"].isin(TREATED).astype(int)
        d["post"] = (d["filing_date"] >= post).astype(int)
        d["filing_year"] = d["filing_date"].dt.year
    full = full.rename(columns={"pub_dt": "pub_date_parsed"})
    print(f"  exploded {n0:,}; full-date pairs {len(full):,}; year-based pairs {len(yr):,}")
    return full, yr


def main():
    CLEAN.mkdir(parents=True, exist_ok=True)
    print("Loading main window classes:")
    frames = {c: load_class(c) for c in sorted(TREATED | CONTROL7 | EXTRA)}
    cols = ["patent_id", "filing_date", "assignee", "legal_status", "main_group",
            "paper_id", "pub_date", "pub_year", "cpc_class", "lag_days",
            "treated", "post", "filing_year"]
    # 7-class dataset: dedup within the 7 classes only, so no pair is claimed by E05B/B25B
    df7 = pd.concat([frames[c] for c in sorted(TREATED | CONTROL7)], ignore_index=True)
    full7, yr7 = clean(df7)
    full7[cols].to_csv(CLEAN / "lag_pairs_v2.csv.gz", index=False)
    ycols = ["patent_id", "filing_date", "assignee", "main_group", "paper_id",
             "pub_year", "age_years", "cpc_class", "treated", "post", "filing_year"]
    yr7[ycols].to_csv(CLEAN / "lag_pairs_v2_year.csv.gz", index=False)
    df9 = pd.concat([frames[c] for c in sorted(TREATED | CONTROL7 | EXTRA)], ignore_index=True)
    full9, _ = clean(df9)
    full9[cols].to_csv(CLEAN / "lag_pairs_9classes_v2.csv.gz", index=False)

    print("\nPair counts by class x post (v2, full-date, 7 classes):")
    print(full7.pivot_table(index="cpc_class", columns="post", values="patent_id", aggfunc="count", fill_value=0))

    print("\nLoading placebo window classes:")
    pl = pd.concat([load_class(c, placebo=True) for c in sorted(TREATED | CONTROL7)], ignore_index=True)
    plf, _ = clean(pl, post=pd.Timestamp("2017-01-01"))
    main1819 = full7[full7["filing_year"].isin([2018, 2019])].copy()
    main1819["post"] = 1  # placebo convention: recomputed downstream; keep window flag
    plc = pd.concat([plf[cols], main1819[cols]], ignore_index=True)
    plc.to_csv(CLEAN / "placebo_pairs_v2.csv.gz", index=False)
    print(f"placebo_pairs_v2: {len(plc):,} pairs (2015-2017: {len(plf):,} + 2018-2019: {len(main1819):,})")
    print("NOTE: built with the complete citations-g16c-placebo re-export of 2026-08-25 (6,130 works).")


if __name__ == "__main__":
    main()
