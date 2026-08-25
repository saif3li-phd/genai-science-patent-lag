"""
Revision plan item 6: a firm-level GenAI exposure measure, built from the patent data
itself (external measures such as hiring or disclosures would need new data collection
and are left as future work).

Exposure definition (declared before running):
  A firm is an ADOPTER if it files at least one GENERATIVE-coded G06N patent
  (G06N3/045, 3/0455, 3/0475) in 2023-2024. A continuous version uses the generative share of
  the firm's 2023-2024 treated-class patents. Because exposure is measured in the post
  period, estimates are associations between adoption and citation behavior, not causal
  effects of adoption.

Test, reading rule fixed before running: the within-firm behavioral channel is supported
if adopters reduce their fresh-science share in their NON-GENERATIVE treated-class
patents more than non-adopters after 2023 (exposure x post < 0, significant, firm and
year fixed effects, SE clustered by firm). A null says the residual decline is not
explained by measured firm adoption, consistent with the subject-matter reading of
item 11.

Sample: firm patents (first-listed applicant, same rules as item 5) in treated classes,
excluding generative-coded patents, filings <= 2024-06-30, patent level.
Output: ../results/item13_firm_exposure_2026-08-24.md
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA = Path("../data/clean/lag_pairs_v2.csv.gz")
CPC = Path("../data/g06n_cpc.csv.gz")
OUT = Path("../results/item13_firm_exposure_2026-08-24.md")
GEN_PAT = r"G06N3/045\b|G06N3/0455|G06N3/0475"
FIRM = r"\b(INC|LLC|LTD|CORP|CORPORATION|CO|GMBH|AG|SA|SAS|BV|NV|PLC|KK|KABUSHIKI KAISHA|HOLDINGS|HOLDING|TECHNOLOGIES|TECHNOLOGY|LIMITED|PTY|OY|AB|SRL|SPA|SE|LP|LLP|COMPANY|GROUP|LABS|SYSTEMS|SOLUTIONS|NETWORKS|ELECTRONICS|PHARMACEUTICALS|THERAPEUTICS|BIOSCIENCES|INDUSTRIES|ENTERPRISES|INTERNATIONAL|MOTORS|BANK)\b"
UNI = r"\b(UNIV|UNIVERSITY|UNIVERSITE|COLLEGE|INSTITUTE|INST|SCHOOL|ACADEMY|HOSPITAL|FOUNDATION|RESEARCH|CNRS|CSIC|FRAUNHOFER|MAX PLANCK|RIKEN|KAIST|ETRI|POLYTECH|LABORATORY|CENTRE|CENTER)\b"


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", str(s).upper())).strip()


def fit_fe(pl, xcol):
    pl = pl.copy()
    pl["XP"] = pl[xcol] * pl["post"]
    X = pd.get_dummies(pl[["cpc_class", "filing_year"]].astype(str), drop_first=True).astype(float)
    X["post"] = pl["post"].astype(float)
    X["XP"] = pl["XP"].astype(float)
    Y = pl["fresh3"].astype(float)
    g = pl["firm"]
    Xd = X - X.groupby(g).transform("mean")
    Yd = Y - Y.groupby(g).transform("mean")
    Xd = Xd.loc[:, Xd.std() > 0]
    m = sm.OLS(Yd, Xd).fit(cov_type="cluster", cov_kwds={"groups": g})
    return m.params["XP"] * 100, m.bse["XP"] * 100, m.pvalues["XP"], int(len(pl))


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df = df[df["treated"] == 1]
    df["fresh3"] = (df["lag_days"] / 365.25 <= 3).astype(int)
    cpc = pd.read_csv(CPC, dtype=str).rename(columns={"Lens ID": "patent_id", "CPC Classifications": "codes"})
    cpc["generative"] = cpc["codes"].str.contains(GEN_PAT, regex=True, na=False)
    df = df.merge(cpc[["patent_id", "generative"]], on="patent_id", how="left")
    df["generative"] = df["generative"].fillna(False).astype(bool)
    first = df["assignee"].fillna("").str.split(";;").str[0].map(norm)
    df["firm"] = first
    df = df[first.str.contains(FIRM, regex=True) & ~first.str.contains(UNI, regex=True)]

    pat = df.drop_duplicates("patent_id")[["patent_id", "firm", "cpc_class", "filing_year", "filing_date", "post", "generative"]]
    post_pat = pat[(pat["filing_year"] >= 2023) & (pat["filing_year"] <= 2024)]
    expo = post_pat.groupby("firm")["generative"].agg(["mean", "max", "count"]).rename(
        columns={"mean": "gen_share", "max": "adopter", "count": "n_post"})
    expo["adopter"] = expo["adopter"].astype(int)

    # analysis sample: non-generative firm patents, mature window, firms observed pre AND post
    d = df[~df["generative"] & (df["filing_date"] <= "2024-06-30")]
    pl = d.groupby(["patent_id", "firm", "cpc_class", "filing_year", "treated", "post"])["fresh3"].mean().reset_index()
    both = pl.groupby("firm")["post"].nunique()
    keep = both[both == 2].index
    pl = pl[pl["firm"].isin(keep)].merge(expo, on="firm", how="left")
    pl["adopter"] = pl["adopter"].fillna(0).astype(int)
    pl["gen_share"] = pl["gen_share"].fillna(0.0)

    n_firms = pl["firm"].nunique()
    n_adopt = pl[pl.adopter == 1]["firm"].nunique()
    raw = pl.groupby(["adopter", "post"])["fresh3"].mean() * 100

    lines = ["# Item 13: firm-level GenAI exposure (adoption measured inside the patent data)", "",
             "Exposure: adopter = files at least one GENERATIVE-coded patent in 2023-2024; continuous "
             "version = generative share of the firm's 2023-2024 treated-class patents. Exposure is "
             "measured post, so estimates are associations, not causal effects of adoption. Sample: "
             "NON-generative treated-class firm patents, filings <= 2024-06-30, firms observed both "
             "before and after 2023. Firm, class and filing-year fixed effects; SE clustered by firm.", "",
             f"Firms in sample: {n_firms:,}, of which adopters: {n_adopt:,}.", ""]
    lines.append("## Raw fresh-science shares on non-generative patents (%, citation-weighted at patent level)\n")
    lines.append("| group | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    for a, albl in [(1, "adopters"), (0, "non-adopters")]:
        lines.append(f"| {albl} | {raw.get((a,0), float('nan')):.1f} | {raw.get((a,1), float('nan')):.1f} |")

    lines.append("\n## Within-firm estimates on non-generative patents, share <= 3y (pp)\n")
    lines.append("| exposure measure | exposure x post | SE | p | N patents |")
    lines.append("|---|---:|---:|---:|---:|")
    for xcol, xlbl in [("adopter", "adopter (0/1)"), ("gen_share", "generative share (0-1)")]:
        b, se, p, n = fit_fe(pl, xcol)
        lines.append(f"| {xlbl} | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
