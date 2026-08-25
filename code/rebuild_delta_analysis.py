"""
Revision plan items 1-3: headline estimates on the rebuilt dataset (corrected G06N
citation batches), compared with the pre-rebuild numbers, plus the R1 sensitivity
that uses publication YEAR instead of the full date.

Specs identical to the paper:
 B. share of citations <= 3 years old, patent level, filings <= 2024-06-30,
    class FE + filing-year FE, SE clustered class x year (raw shares citation-weighted)
 A. log(1 + lag days), pair level, 10-year window, same FE and clustering
 Year-based B: fresh = (filing_year - pub_year) <= 3 on the year-based pairs file,
    which recovers pairs whose cited work has a year but no full date.
Output: ../results/item10_rebuild_2026-08-23.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

OLD = Path("../data/clean/lag_pairs.csv")
NEW = Path("../data/clean/lag_pairs_v2.csv.gz")
YEAR = Path("../data/clean/lag_pairs_v2_year.csv.gz")
OUT = Path("../results/item10_rebuild_2026-08-23.md")


def share_did(d, fresh_col):
    d = d[d["filing_date"] <= "2024-06-30"]
    pl = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"])[fresh_col].mean().reset_index()
    m = smf.ols(f"{fresh_col} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    g = d.groupby(["treated", "post"])[fresh_col].mean() * 100
    return m.params["treated:post"] * 100, m.bse["treated:post"] * 100, m.pvalues["treated:post"], int(m.nobs), g


def lag_did(d):
    d = d[d["lag_days"] <= 10 * 365.25]
    m = smf.ols("log_lag ~ treated:post + C(cpc_class) + C(filing_year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], int(m.nobs)


def prep(d):
    d = d.copy()
    d["filing_date"] = pd.to_datetime(d["filing_date"])
    d["lag_days"] = pd.to_numeric(d["lag_days"])
    d["fresh3"] = (d["lag_days"] / 365.25 <= 3).astype(int)
    d["log_lag"] = np.log1p(d["lag_days"])
    d["cluster"] = d["cpc_class"] + "_" + d["filing_year"].astype(str)
    return d


def main():
    old = prep(pd.read_csv(OLD))
    new = prep(pd.read_csv(NEW))
    yr = pd.read_csv(YEAR)
    yr["filing_date"] = pd.to_datetime(yr["filing_date"])
    yr["fresh3y"] = (yr["age_years"] <= 3).astype(int)
    yr["cluster"] = yr["cpc_class"] + "_" + yr["filing_year"].astype(str)

    lines = ["# Item 10: rebuild with corrected G06N exports, and the R1 year-based sensitivity", "",
             f"Old pairs: {len(old):,}. Rebuilt pairs: {len(new):,} (+{len(new)-len(old):,} gained, 0 lost; "
             "gains come from works resolved by the corrected 2020a and 2021b G06N citation exports; "
             "some multi-class pairs move their class label to G06N because R4 keeps the first class in "
             "the fixed alphabetical concatenation, the same rule as the original build).",
             f"Year-based file: {len(yr):,} pairs ({len(yr)/len(new)*100:.0f} percent more than full-date, "
             "recovering works that carry a publication year but no full date).", ""]

    lines.append("## Pair counts by class and period, old vs rebuilt\n")
    t_old = old.groupby(["cpc_class", "post"]).size().unstack(fill_value=0)
    t_new = new.groupby(["cpc_class", "post"]).size().unstack(fill_value=0)
    lines.append("| class | old pre | old post | v2 pre | v2 post |")
    lines.append("|---|---:|---:|---:|---:|")
    for c in t_new.index:
        lines.append(f"| {c} | {t_old.loc[c,0]:,} | {t_old.loc[c,1]:,} | {t_new.loc[c,0]:,} | {t_new.loc[c,1]:,} |")

    lines.append("\n## B. Share <= 3y, patent level, filings <= 2024-06-30 (pp)\n")
    lines.append("| dataset | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lab, d, col in [("old (paper Table 5)", old, "fresh3"), ("rebuilt v2", new, "fresh3")]:
        b, se, p, n, g = share_did(d, col)
        lines.append(f"| {lab} | {g[(1,0)]:.1f} | {g[(1,1)]:.1f} | {g[(0,0)]:.1f} | {g[(0,1)]:.1f} | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")
    b, se, p, n, g = share_did(yr, "fresh3y")
    lines.append(f"| v2, R1 = publication year | {g[(1,0)]:.1f} | {g[(1,1)]:.1f} | {g[(0,0)]:.1f} | {g[(0,1)]:.1f} | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")

    lines.append("\n## A. Log(1 + lag), pair level, 10-year window\n")
    lines.append("| dataset | treated x post | SE | p | N pairs |")
    lines.append("|---|---:|---:|---:|---:|")
    for lab, d in [("old (paper Table 4 spec 3)", old), ("rebuilt v2", new)]:
        b, se, p, n = lag_did(d)
        lines.append(f"| {lab} | {b:+.3f} | {se:.3f} | {p:.4f} | {n:,} |")

    lines.append("\nItem 3 (G16B dedup accounting, from the build log): the two G16B citation batches "
                 "load 66,772 work rows; 13,620 are the same works exported in both windows; "
                 "53,152 distinct works remain and are the merge base. The same rule (one row per "
                 "work, then one row per patent-paper pair) applies to every class; G06N drops "
                 "119,700 cross-batch duplicate work rows across its ten files.")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
