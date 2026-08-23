"""
Item 6: replication of the composition result on an indexing-independent citation source
(Reliance on Science, Marx & Fuegi, Zenodo v65, USPTO citations through 2025).

Build (done on the researcher's machine, reliance-on-science/):
  pcs_oa_uspto.csv  -> rows whose patent number matches one of our 353,942 patents (7 classes)
  -> 900,220 citation rows, 55,022 patents, 261,942 distinct OpenAlex works
  -> publication dates: 143,780 via MAG id = OpenAlex id join to Lens scholarly exports,
     106,983 via the OpenAlex API (11,179 ids not found in OpenAlex), 73.9% of rows dated
  -> same cleaning as the Lens pipeline (drop missing/negative lags, one row per patent-paper)
  -> ros_pairs.csv.gz: 603,758 pairs.

Tests (same specs as the Lens baseline):
  B. share <=3y, patent level, filings <= 2024-06-30, class FE + year FE, cluster class x year
  shifted windows and age bins as in item 1
  A. log lag, pair level, 10-year window
  plus: same estimates on the Lens data restricted to the SAME patents (apples to apples),
  and the correlation of patent-level fresh shares between the two sources.
Reading rule (fixed): the indexing explanation is rejected if the RoS-based DiD on the
<=3y share is negative and of similar size to the Lens-based one on the same patents.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROS = Path("../data/ros_pairs.csv.gz")
LENS = Path("../data/clean/lag_pairs.csv")
OUT = Path("../results/item6_reliance_on_science_2026-08-22.md")
WINDOWS = [("<=3y", 0, 3), ("2-5y", 2, 5), ("3-6y", 3, 6), ("4-8y", 4, 8), (">=8y", 8, None)]


def prep(d):
    d = d.copy()
    d["filing_date"] = pd.to_datetime(d["filing_date"]); d["age_y"] = d["lag_days"] / 365.25
    d["log_lag"] = np.log1p(d["lag_days"]); d["cluster"] = d["cpc_class"] + "_" + d["filing_year"].astype(str)
    for lab, lo, hi in WINDOWS:
        d[lab] = ((d["age_y"] >= lo) & ((d["age_y"] <= hi) if hi else True)).astype(int)
    return d


def share_did(d, col):
    d = d[d["filing_date"] <= "2024-06-30"]
    pl = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"])[col].mean().reset_index()
    m = smf.ols(f"Q('{col}') ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    g = d.groupby(["treated", "post"])[col].mean() * 100
    return m.params["treated:post"] * 100, m.bse["treated:post"] * 100, m.pvalues["treated:post"], int(m.nobs), g


def lag_did(d):
    d = d[d["lag_days"] <= 10 * 365.25]
    m = smf.ols("log_lag ~ treated:post + C(cpc_class) + C(filing_year)", data=d).fit(cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], int(m.nobs)


def main():
    ros = prep(pd.read_csv(ROS))
    lens = prep(pd.read_csv(LENS, parse_dates=["filing_date"]))
    common = set(ros["patent_id"]) & set(lens["patent_id"])
    lens_c = lens[lens["patent_id"].isin(common)]
    ros_c = ros[ros["patent_id"].isin(common)]
    lines = ["# Item 6: replication on Reliance on Science (indexing-independent source)", "",
             f"RoS pairs: {len(ros):,} ({ros['patent_id'].nunique():,} patents). Lens pairs: {len(lens):,} ({lens['patent_id'].nunique():,} patents). "
             f"Patents present in both: {len(common):,}.", ""]
    lines.append("## Pairs by class and period, RoS\n")
    t = ros.groupby(["cpc_class", "post"]).size().unstack(fill_value=0)
    lines.append("| class | pre | post |"); lines.append("|---|---:|---:|")
    for c, r in t.iterrows():
        lines.append(f"| {c} | {r.get(0,0):,} | {r.get(1,0):,} |")

    lines.append("\n## B. Share of citations <=3y, patent level, filings <= 2024-06-30 (pp)\n")
    lines.append("| source | sample | treated pre % | treated post % | control pre % | control post % | DiD | SE | p | N patents |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for src, lab, d in [("RoS", "all RoS patents", ros), ("RoS", "common patents", ros_c), ("Lens", "common patents", lens_c), ("Lens", "all Lens patents (baseline)", lens)]:
        b, se, p, n, g = share_did(d, "<=3y")
        lines.append(f"| {src} | {lab} | {g[(1,0)]:.1f} | {g[(1,1)]:.1f} | {g[(0,0)]:.1f} | {g[(0,1)]:.1f} | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")

    lines.append("\n## Shifted windows, RoS, patent level, filings <= 2024-06-30 (pp)\n")
    lines.append("| window | RoS DiD | SE | p | Lens DiD (same patents) | p |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for lab, lo, hi in WINDOWS:
        b, se, p, n, g = share_did(ros_c, lab)
        b2, se2, p2, n2, g2 = share_did(lens_c, lab)
        lines.append(f"| {lab} | {b:+.2f} | {se:.2f} | {p:.4f} | {b2:+.2f} | {p2:.4f} |")

    lines.append("\n## A. Log lag, pair level, 10-year window\n")
    lines.append("| source | sample | treated x post | SE | p | N pairs |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for src, lab, d in [("RoS", "all", ros), ("RoS", "common patents", ros_c), ("Lens", "common patents", lens_c)]:
        b, se, p, n = lag_did(d)
        lines.append(f"| {src} | {lab} | {b:+.3f} | {se:.3f} | {p:.4f} | {n:,} |")

    # patent-level agreement
    a = ros_c.groupby("patent_id")["<=3y"].mean(); b_ = lens_c.groupby("patent_id")["<=3y"].mean()
    j = pd.concat([a.rename("ros"), b_.rename("lens")], axis=1).dropna()
    lines.append(f"\nPatent-level fresh-share agreement between sources (common patents): Pearson r = {j['ros'].corr(j['lens']):.3f}, "
                 f"mean RoS {j['ros'].mean()*100:.1f}% vs Lens {j['lens'].mean()*100:.1f}%.")
    # cited-year profile RoS treated
    tt = ros[(ros.treated == 1) & (ros.filing_date <= "2024-06-30")].copy(); tt["py"] = pd.to_datetime(tt["pub_date"]).dt.year
    tab = tt.groupby(["post", "py"]).size().unstack(0).fillna(0); tab = tab.div(tab.sum(axis=0), axis=1) * 100
    top = tab[1].sort_values(ascending=False).head(5)
    lines.append("Top-5 cited publication years, RoS, post-2023 treated filings: " + ", ".join(f"{int(y)} ({v:.1f}%)" for y, v in top.items()))
    OUT.write_text("\n".join(lines) + "\n"); print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
