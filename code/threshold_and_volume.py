"""
Item 8: (a) cumulative fresh-science thresholds and (b) citation volume versus composition.

(a) Answers "why three years?": the patent-level DiD on the share of citations to papers
    at most k years old, for k = 2, 3, 5 (and 4 for completeness). Same spec as the
    baseline: filings <= 2024-06-30, class FE + filing-year FE, SE clustered class x year.
(b) Answers "did citation volume change, or only its age composition?": per-patent counts
    of (i) all scientific citations in the dataset, (ii) citations <= 3y, (iii) citations
    > 3y, treated vs control, pre vs post, plus a DiD on log(1 + count) for each.
    Reading rule (fixed): the result is a composition effect if the DiD on the share is
    negative while the DiD on total citations per patent is not negative of similar
    relative size.
Input : ../data/clean/lag_pairs.csv   Output: ../results/item8_threshold_volume_2026-08-22.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs.csv")
OUT = Path("../results/item8_threshold_volume_2026-08-22.md")


def did(pl, y):
    m = smf.ols(f"{y} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], int(m.nobs)


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df = df[df["filing_date"] <= "2024-06-30"].copy()
    df["age_y"] = df["lag_days"] / 365.25
    df["cluster"] = df["cpc_class"] + "_" + df["filing_year"].astype(str)
    keys = ["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"]
    lines = ["# Item 8: cumulative thresholds and citation volume versus composition", "",
             f"Pairs with filing <= 2024-06-30: {len(df):,}; patents: {df['patent_id'].nunique():,}.", ""]

    lines.append("## (a) Share of citations to papers at most k years old, patent level (pp)\n")
    lines.append("| threshold | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for k in [2, 3, 4, 5]:
        df[f"s{k}"] = (df["age_y"] <= k).astype(int)
        pl = df.groupby(keys)[f"s{k}"].mean().reset_index()
        g = pl.groupby(["treated", "post"])[f"s{k}"].mean() * 100
        b, se, p, n = did(pl, f"s{k}")
        lines.append(f"| <= {k} years | {g[(1,0)]:.1f} | {g[(1,1)]:.1f} | {g[(0,0)]:.1f} | {g[(0,1)]:.1f} | {b*100:+.2f} | {se*100:.2f} | {p:.4f} | {n:,} |")

    lines.append("\n## (b) Citations per patent: volume versus composition\n")
    df["fresh"] = df["s3"]; df["old"] = 1 - df["s3"]; df["one"] = 1
    pl = df.groupby(keys).agg(total=("one", "sum"), fresh=("fresh", "sum"), old=("old", "sum")).reset_index()
    lines.append("| group | period | patents | mean citations per patent | mean <= 3y per patent | mean > 3y per patent | median total |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for t, tl in [(1, "treated"), (0, "control")]:
        for p_, pl_ in [(0, "pre-2023"), (1, "post-2023")]:
            c = pl[(pl.treated == t) & (pl.post == p_)]
            lines.append(f"| {tl} | {pl_} | {len(c):,} | {c.total.mean():.2f} | {c.fresh.mean():.2f} | {c.old.mean():.2f} | {c.total.median():.0f} |")
    lines.append("\nDiD on log(1 + count), patent level, class FE + year FE, SE clustered class x year:\n")
    lines.append("| outcome | treated x post | SE | p | approx. % change |")
    lines.append("|---|---:|---:|---:|---:|")
    for col, lab in [("total", "all citations per patent"), ("fresh", "citations <= 3y per patent"), ("old", "citations > 3y per patent")]:
        pl[f"l_{col}"] = np.log1p(pl[col])
        b, se, p, n = did(pl, f"l_{col}")
        lines.append(f"| {lab} | {b:+.3f} | {se:.3f} | {p:.4f} | {(np.exp(b)-1)*100:+.1f}% |")
    OUT.write_text("\n".join(lines) + "\n"); print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
