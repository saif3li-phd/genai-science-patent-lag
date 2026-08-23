"""
Item 9 (step 1): build the science-intensive alternative control dataset.

Input: slim extracts of the Lens exports for G01N, G02B, B01D, G21 (chosen ex ante,
docs/01 addendum 2026-08-23), staged from the researcher's machine. Columns:
patents: Lens ID, Application Date, NPL Resolved Lens ID(s), Applicants, Legal Status
citations: Lens ID, Date Published.

Same pipeline as build_lag_dataset.py: explode NPL Resolved Lens ID(s) on ';;', join
publication dates, R1 drop missing dates, R2 drop negative lags, R3 winsorize at the
class-level p99, R4 one row per (patent, paper). All four classes are controls
(treated = 0); post = filing >= 2023-01-01.

Output: ../data/clean/lag_pairs_sci.csv.gz (same columns as lag_pairs.csv).
"""

from pathlib import Path
import pandas as pd

RAW = Path("../data/raw_sci_slim")
OUT = Path("../data/clean/lag_pairs_sci.csv.gz")
CLASSES = ["g01n", "g02b", "b01d", "g21"]


def load_class(cls):
    pf = sorted(RAW.glob(f"patents-{cls}-*.slim.csv.gz")) + sorted(RAW.glob(f"patents-{cls}.slim.csv.gz"))
    cf = sorted(RAW.glob(f"citations-{cls}-*.slim.csv.gz")) + sorted(RAW.glob(f"citations-{cls}.slim.csv.gz"))
    p = pd.concat([pd.read_csv(f, dtype=str) for f in pf], ignore_index=True)
    w = pd.concat([pd.read_csv(f, dtype=str) for f in cf], ignore_index=True)
    print(f"{cls.upper()}: {len(pf)} patent files ({len(p):,} rows), {len(cf)} citation files ({len(w):,} rows)")
    p = p.rename(columns={"Lens ID": "patent_id", "Application Date": "filing_date",
                          "NPL Resolved Lens ID(s)": "npl_ids", "Applicants": "assignee",
                          "Legal Status": "legal_status"})
    p = p.drop_duplicates("patent_id").dropna(subset=["npl_ids"])
    p["paper_id"] = p["npl_ids"].str.split(";;")
    pairs = p.explode("paper_id").drop(columns=["npl_ids"])
    pairs["paper_id"] = pairs["paper_id"].str.strip()
    pairs = pairs[pairs["paper_id"] != ""]
    w = w.rename(columns={"Lens ID": "paper_id", "Date Published": "pub_date"})
    w = w.drop_duplicates("paper_id")
    df = pairs.merge(w, on="paper_id", how="inner")
    df["cpc_class"] = cls.upper()
    return df


def main():
    df = pd.concat([load_class(c) for c in CLASSES], ignore_index=True)
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
    df["doi"] = ""
    df["treated"] = 0
    df["post"] = (df["filing_date"] >= pd.Timestamp("2023-01-01")).astype(int)
    df["filing_year"] = df["filing_date"].dt.year
    cols = ["patent_id", "filing_date", "assignee", "legal_status", "paper_id", "pub_date",
            "doi", "cpc_class", "lag_days", "treated", "post", "filing_year"]
    df[cols].to_csv(OUT, index=False)
    print(f"\nexploded {n0:,} -> R1 {n1:,} -> R2 {n2:,} -> R3+R4 {n3:,}")
    print(df.pivot_table(index="cpc_class", columns="post", values="patent_id",
                         aggfunc="count", fill_value=0))
    print("median lag days:")
    print(df.pivot_table(index="cpc_class", columns="post", values="lag_days", aggfunc="median"))
    print("written ->", OUT)


if __name__ == "__main__":
    main()
