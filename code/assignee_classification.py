"""
Item 5: assignee classification (firm / university-research / government / individual)
and assignee fixed effects.

Threat (self-critique #5): the title says "corporate" but the sample mixes firms,
universities and individuals, and nothing holds the applicant fixed.

Rules (fixed before running, applied to normalised applicant names; a patent takes the
highest-priority type among its applicants: university > government > firm > individual):
  UNIVERSITY/RESEARCH : UNIV, UNIVERSITY, COLLEGE, INSTITUTE, INST, SCHOOL, ACADEMY, HOSPITAL,
                        MEDICAL CENTER, FOUNDATION, RESEARCH, CNRS, CSIC, FRAUNHOFER, MAX PLANCK,
                        RIKEN, KAIST, ETRI, POLYTECH, LABORATORY (non-firm)
  GOVERNMENT          : GOVERNMENT, MINISTRY, DEPARTMENT OF, US ARMY, US NAVY, AIR FORCE, NASA,
                        NATIONAL LABORATORY, SECRETARY OF, AGENCY
  FIRM                : corporate suffix (INC, LLC, LTD, CORP, CO, GMBH, AG, SA, SAS, BV, NV, PLC,
                        KK, KABUSHIKI KAISHA, HOLDINGS, TECHNOLOGIES, LIMITED, PTY, OY, AB, SRL,
                        SPA, SE, LP, LLP, COMPANY, GROUP, LABS, SYSTEMS, SOLUTIONS, NETWORKS)
  INDIVIDUAL          : none of the above (person names carry no suffix in Lens exports)

Estimates:
  A/B baseline specs on the FIRM sample; and with assignee fixed effects (within-applicant
  demeaning) on the firm sample, so the treated x post contrast is identified from changes
  inside the same applicant.
Output: ../results/item5_assignee_2026-08-21.md and ../data/clean/patent_assignee_type.csv
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs.csv")
OUT = Path("../results/item5_assignee_2026-08-21.md")
OUT_TYPES = Path("../data/clean/patent_assignee_type.csv")

UNI = r"\b(UNIV|UNIVERSITY|UNIVERSITE|UNIVERSITAT|UNIVERSIDAD|COLLEGE|INSTITUTE|INST|SCHOOL|ACADEMY|HOSPITAL|MEDICAL CENTER|FOUNDATION|RESEARCH|CNRS|CSIC|FRAUNHOFER|MAX PLANCK|RIKEN|KAIST|ETRI|POLYTECH|POLYTECHNIC|LABORATORY|CENTRE|CENTER)\b"
GOV = r"\b(GOVERNMENT|MINISTRY|DEPARTMENT OF|US ARMY|US NAVY|UNITED STATES OF AMERICA|AIR FORCE|NASA|NATIONAL LAB|NATIONAL LABORATORY|SECRETARY OF|AGENCY|ADMINISTRATION)\b"
FIRM = r"\b(INC|LLC|LTD|CORP|CORPORATION|CO|GMBH|AG|SA|SAS|BV|NV|PLC|KK|KABUSHIKI KAISHA|HOLDINGS|HOLDING|TECHNOLOGIES|TECHNOLOGY|LIMITED|PTY|OY|AB|SRL|SPA|SE|LP|LLP|COMPANY|GROUP|LABS|SYSTEMS|SOLUTIONS|NETWORKS|ELECTRONICS|PHARMACEUTICALS|THERAPEUTICS|BIOSCIENCES|INDUSTRIES|ENTERPRISES|INTERNATIONAL|MOTORS|BANK)\b"


def norm(s):
    s = re.sub(r"[^\w\s]", " ", str(s).upper())
    return re.sub(r"\s+", " ", s).strip()


def classify(name):
    n = norm(name)
    if re.search(UNI, n) and not re.search(r"\b(INC|LLC|CORP|GMBH)\b", n):
        return "university"
    if re.search(GOV, n):
        return "government"
    if re.search(FIRM, n):
        return "firm"
    return "individual"


PRIORITY = {"university": 0, "government": 1, "firm": 2, "individual": 3}


def fit(d, y, level, fe_assignee=False):
    d = d.copy()
    d["T"] = d["treated"] * d["post"]
    if level == "pair":
        d = d[d["lag_days"] <= 10 * 365.25]
        scale = 1
    else:
        d = d[d["filing_date"] <= "2024-06-30"]
        d = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster", "assignee_key"]).agg(
            **{y: (y, "mean")}, T=("T", "first")).reset_index()
        scale = 100
    if not fe_assignee:
        m = smf.ols(f"{y} ~ T + C(cpc_class) + C(filing_year)", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["cluster"]})
        return m.params["T"] * scale, m.bse["T"] * scale, m.pvalues["T"], int(m.nobs)
    # within-assignee demeaning of y, T and the class/year dummies
    X = pd.get_dummies(d[["cpc_class", "filing_year"]].astype(str), drop_first=True).astype(float)
    X["T"] = d["T"].astype(float)
    Y = d[y].astype(float)
    g = d["assignee_key"]
    Xd = X - X.groupby(g).transform("mean")
    Yd = Y - Y.groupby(g).transform("mean")
    Xd = Xd.loc[:, Xd.std() > 0]
    m = sm.OLS(Yd, Xd).fit(cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    return m.params["T"] * scale, m.bse["T"] * scale, m.pvalues["T"], int(m.nobs)


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["age_y"] = df["lag_days"] / 365.25
    df["fresh3"] = (df["age_y"] <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    df["cluster"] = df["cpc_class"] + "_" + df["filing_year"].astype(str)

    pat = df.drop_duplicates("patent_id")[["patent_id", "assignee", "cpc_class", "treated", "post", "filing_date"]].copy()
    pat["apps"] = pat["assignee"].fillna("").str.split(";;")
    pat["types"] = pat["apps"].apply(lambda L: [classify(a) for a in L if a.strip()])
    pat["atype"] = pat["types"].apply(lambda L: min(L, key=lambda t: PRIORITY[t]) if L else "individual")
    pat["assignee_key"] = pat["apps"].apply(lambda L: norm(L[0]) if L and L[0].strip() else "UNKNOWN")
    pat[["patent_id", "atype", "assignee_key"]].to_csv(OUT_TYPES, index=False)
    df = df.merge(pat[["patent_id", "atype", "assignee_key"]], on="patent_id", how="left")

    lines = ["# Item 5: assignee classification and assignee fixed effects", ""]
    lines.append("## Patent composition by applicant type (%), patents with at least one citation\n")
    lines.append("| group | period | firm | university/research | government | individual | N |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for g, glab in [(1, "treated"), (0, "control")]:
        for p, plab in [(0, "pre-2023"), (1, "post-2023")]:
            s = pat[(pat["treated"] == g) & (pat["post"] == p)]["atype"].value_counts(normalize=True) * 100
            lines.append(f"| {glab} | {plab} | {s.get('firm',0):.1f} | {s.get('university',0):.1f} | {s.get('government',0):.1f} | {s.get('individual',0):.1f} | {len(pat[(pat['treated']==g)&(pat['post']==p)]):,} |")

    lines.append("\n## Fresh-science share (<=3y) by applicant type, treated classes, citation-weighted (%)\n")
    lines.append("| type | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    t = df[(df["treated"] == 1) & (df["filing_date"] <= "2024-06-30")]
    for ty in ["firm", "university", "government", "individual"]:
        s = t[t["atype"] == ty].groupby("post")["fresh3"].mean() * 100
        lines.append(f"| {ty} | {s.get(0, float('nan')):.1f} | {s.get(1, float('nan')):.1f} |")

    samples = [("all applicants", df), ("firms only", df[df["atype"] == "firm"]),
               ("universities/research only", df[df["atype"] == "university"])]
    for y, lab, level in [("log_lag", "A. log lag (10-year window)", "pair"), ("fresh3", "B. share <=3y (pp), patent level, filings <= 2024-06-30", "patent")]:
        lines.append(f"\n## {lab}: treated x post\n")
        lines.append("| sample | assignee FE | N | coef | SE | p |")
        lines.append("|---|---|---:|---:|---:|---:|")
        for sl, d in samples:
            b, se, p, n = fit(d, y, level)
            lines.append(f"| {sl} | no | {n:,} | {b:+.3f} | {se:.3f} | {p:.4f} |")
        for sl, d in samples[1:2]:
            b, se, p, n = fit(d, y, level, fe_assignee=True)
            lines.append(f"| {sl} | yes (within-applicant) | {n:,} | {b:+.3f} | {se:.3f} | {p:.4f} |")

    n_firms = pat[pat["atype"] == "firm"]["assignee_key"].nunique()
    lines.append(f"\nDistinct firm applicants (first-listed, normalised): {n_firms:,}. "
                 "Firm sample with assignee FE identifies treated x post from changes within the same applicant.")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
