"""
Item 2: incumbents-only re-estimation.

Threat (self-critique #1): after ChatGPT a wave of new entrants filed in the treated
classes; if entrants cite differently (e.g., fewer fresh papers), the treated x post
coefficient could reflect a change in WHO patents rather than a change in HOW incumbents
draw on science.

Definition (fixed before running): an assignee is an INCUMBENT if it appears on at least
one patent filed before 2020-01-01 in our seven-class sample (any class). A patent is an
incumbent patent if at least one of its applicants is an incumbent. Applicant strings are
normalised (upper case, punctuation stripped, multiple applicants split on ';;').
Cutoff 2020 leaves a three-year buffer before the treatment date.

Estimates (same specs as the baseline):
  A. log lag, pair level, uniform 10-year window            (baseline +0.201, p=0.0002)
  B. share <=3y, patent level, filings <= 2024-06-30        (baseline -4.93 pp, p=0.0012)
each on: all patents | incumbents only | entrants only.
Output: ../results/item2_incumbents_2026-08-21.md
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs.csv")
OUT = Path("../results/item2_incumbents_2026-08-21.md")
CUTOFF = pd.Timestamp("2020-01-01")


def norm(s):
    s = str(s).upper()
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\b(INC|LLC|LTD|CORP|CORPORATION|CO|GMBH|AG|SA|SAS|BV|PLC|LIMITED|COMPANY|KK|KABUSHIKI KAISHA)\b", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["age_y"] = df["lag_days"] / 365.25
    df["fresh3"] = (df["age_y"] <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    df["cluster"] = df["cpc_class"] + "_" + df["filing_year"].astype(str)

    # applicant lists per patent
    pat = df.drop_duplicates("patent_id")[["patent_id", "assignee", "filing_date", "treated", "post", "cpc_class"]].copy()
    pat["apps"] = pat["assignee"].fillna("").str.split(";;").apply(lambda L: [norm(a) for a in L if norm(a)])
    early = pat[pat["filing_date"] < CUTOFF].explode("apps")["apps"].dropna().unique()
    incumbents = set(early)
    pat["incumbent"] = pat["apps"].apply(lambda L: any(a in incumbents for a in L))
    df = df.merge(pat[["patent_id", "incumbent"]], on="patent_id", how="left")

    lines = ["# Item 2: incumbents-only re-estimation", "",
             f"Incumbent = applicant with at least one patent filed before {CUTOFF.date()} in the seven-class sample "
             f"({len(incumbents):,} distinct normalised applicants). Patent is incumbent if any applicant is incumbent.", ""]

    # composition of the post period
    comp = pat.groupby(["treated", "post"])["incumbent"].mean().unstack() * 100
    lines.append("## Share of patents filed by incumbents (%)\n")
    lines.append("| group | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    for g, lab in [(1, "treated"), (0, "control")]:
        lines.append(f"| {lab} | {comp.loc[g, 0]:.1f} | {comp.loc[g, 1]:.1f} |")
    lines.append("\n(The pre-2023 share is mechanically high because incumbency is defined on pre-2020 filings.)\n")

    def run_lag(d):
        d = d[d["lag_days"] <= 10 * 365.25]
        m = smf.ols("log_lag ~ treated:post + C(cpc_class) + C(filing_year)", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["cluster"]})
        return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], int(m.nobs)

    def run_share(d):
        d = d[d["filing_date"] <= "2024-06-30"]
        pl = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"])["fresh3"].mean().reset_index()
        m = smf.ols("fresh3 ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
            cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
        return m.params["treated:post"] * 100, m.bse["treated:post"] * 100, m.pvalues["treated:post"], int(m.nobs)

    lines.append("## A. Log lag, pair level, uniform 10-year window\n")
    lines.append("| sample | N pairs | treated x post | SE | p |")
    lines.append("|---|---:|---:|---:|---:|")
    for lab, d in [("all", df), ("incumbents only", df[df["incumbent"]]), ("entrants only", df[~df["incumbent"]])]:
        b, se, p, n = run_lag(d)
        lines.append(f"| {lab} | {n:,} | {b:+.3f} | {se:.3f} | {p:.4f} |")

    lines.append("\n## B. Share of citations <= 3y, patent level, filings <= 2024-06-30 (pp)\n")
    lines.append("| sample | N patents | treated x post | SE | p |")
    lines.append("|---|---:|---:|---:|---:|")
    for lab, d in [("all", df), ("incumbents only", df[df["incumbent"]]), ("entrants only", df[~df["incumbent"]])]:
        b, se, p, n = run_share(d)
        lines.append(f"| {lab} | {n:,} | {b:+.2f} | {se:.2f} | {p:.4f} |")

    # incumbents: treated-group raw shares
    t = df[(df["treated"] == 1) & (df["filing_date"] <= "2024-06-30")]
    g = t.groupby(["incumbent", "post"])["fresh3"].mean().unstack() * 100
    lines.append("\n## Treated classes: citation-weighted share <= 3y by incumbency (%)\n")
    lines.append("| | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    for k, lab in [(True, "incumbents"), (False, "entrants")]:
        if k in g.index:
            lines.append(f"| {lab} | {g.loc[k, 0]:.1f} | {g.loc[k, 1]:.1f} |")

    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
