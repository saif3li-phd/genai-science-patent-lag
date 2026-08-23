"""
Option (b): Event-study on the fresh-science share and on the log lag.

Why: the 2015-2019 placebo showed a large positive fake-post coefficient on the
<=3y share (treated classes were gaining fresh-science share before 2023), so the
single treated x post coefficient cannot be read causally without looking at the
year-by-year path. An event study estimates one treated x year coefficient per
filing year relative to 2022 (the last pre-treatment year).

Model (patent level for the share; pair level for the lag):
  y = sum_{t != 2022} b_t * (treated x 1[filing_year = t]) + class FE + year FE + e
  SE clustered by class x filing-year.
Reading rule (fixed before running):
  - pre-2023 coefficients (2018-2021) jointly indistinguishable from zero and without
    a monotone trend  -> parallel trends plausible, post coefficients read as effects.
  - pre-2023 coefficients rising monotonically -> the 2023 break is a reversal of a
    trend; report it as such and add a group-specific linear trend as a second spec.
Also estimated: the same model with a treated x linear-year trend (2018-2022 fitted),
so the post coefficients are deviations from the treated group's own pre-trend.

Samples: mature (filings <= 2024-06-30) as in the baseline, plus full sample.
Output: ../results/item_b_event_study_<date>.md and a PNG figure.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path("../data/clean/lag_pairs.csv")
OUT_MD = Path("../results/item_b_event_study_2026-08-21.md")
OUT_PNG = Path("../results/item_b_event_study_2026-08-21.png")
BASE_YEAR = 2022


def prep(df):
    df = df.copy()
    df["age_y"] = df["lag_days"] / 365.25
    df["fresh3"] = (df["age_y"] <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    return df


def patent_level(df):
    keys = ["patent_id", "cpc_class", "filing_year", "treated"]
    pl = df.groupby(keys).agg(fresh3=("fresh3", "mean"), log_lag=("log_lag", "median")).reset_index()
    pl["cluster"] = pl["cpc_class"] + "_" + pl["filing_year"].astype(str)
    return pl


def event_study(d, y, years):
    """Return dict year -> (coef, se, p) relative to BASE_YEAR."""
    d = d.copy()
    terms = []
    for t in years:
        if t == BASE_YEAR:
            continue
        col = f"tx{t}"
        d[col] = ((d["treated"] == 1) & (d["filing_year"] == t)).astype(int)
        terms.append(col)
    f = f"{y} ~ " + " + ".join(terms) + " + C(cpc_class) + C(filing_year)"
    m = smf.ols(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    res = {t: (m.params[f"tx{t}"], m.bse[f"tx{t}"], m.pvalues[f"tx{t}"]) for t in years if t != BASE_YEAR}
    # joint test of pre-period coefficients
    pre = [f"tx{t}" for t in years if t < BASE_YEAR]
    ftest = m.f_test(" = ".join(pre) + " = 0") if len(pre) > 1 else None
    return res, (float(ftest.fvalue), float(ftest.pvalue)) if ftest is not None else None, int(m.nobs)


def trend_adjusted(d, y):
    """treated x post with a treated-specific linear trend fitted on all years."""
    d = d.copy()
    d["post"] = (d["filing_year"] >= 2023).astype(int)
    d["t_trend"] = d["treated"] * (d["filing_year"] - BASE_YEAR)
    f = f"{y} ~ treated:post + t_trend + C(cpc_class) + C(filing_year)"
    m = smf.ols(f, data=d).fit(cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], m.params["t_trend"], m.pvalues["t_trend"]


def main():
    df = prep(pd.read_csv(DATA, parse_dates=["filing_date"]))
    lines = ["# Option (b): event-study on the fresh-science share and the log lag",
             "",
             "Coefficients are treated x filing-year, relative to 2022 (last pre-treatment year); "
             "class FE + filing-year FE; SE clustered by class x filing-year. Share model is patent level "
             "(one row per patent); lag model is patent level on the median log lag. "
             "Joint F-test: all pre-2023 coefficients (2018-2021) equal zero.", ""]
    panels = {}
    for sname, mature in [("mature (filings <= 2024-06-30)", "2024-06-30"), ("full sample", None)]:
        d = df if mature is None else df[df["filing_date"] <= mature]
        years = sorted(d["filing_year"].unique())
        pl = patent_level(d)
        lines.append(f"\n## Sample: {sname}  (patents = {len(pl):,})\n")
        for y, lab, scale in [("fresh3", "share of citations <= 3y (pp)", 100), ("log_lag", "median log lag (log points)", 1)]:
            res, ft, n = event_study(pl, y, years)
            lines.append(f"### Outcome: {lab}\n")
            lines.append("| filing year | coef | SE | p |")
            lines.append("|---|---:|---:|---:|")
            for t in years:
                if t == BASE_YEAR:
                    lines.append(f"| {t} | 0 (ref) | | |")
                else:
                    b, se, p = res[t]
                    lines.append(f"| {t} | {b*scale:+.2f} | {se*scale:.2f} | {p:.3f} |")
            if ft:
                lines.append(f"\nJoint test pre-2023 = 0: F = {ft[0]:.2f}, p = {ft[1]:.3f}")
            b, se, p, tr, ptr = trend_adjusted(pl, y)
            lines.append(f"\nTrend-adjusted treated x post (treated-specific linear trend included): "
                         f"{b*scale:+.2f} (SE {se*scale:.2f}, p = {p:.3f}); fitted treated trend per year "
                         f"{tr*scale:+.2f} (p = {ptr:.3f})\n")
            panels[(sname, y)] = (years, res, scale, lab)

    # figure: mature sample, both outcomes
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, y in zip(axes, ["fresh3", "log_lag"]):
        years, res, scale, lab = panels[("mature (filings <= 2024-06-30)", y)]
        xs, bs, es = [], [], []
        for t in years:
            if t == BASE_YEAR:
                xs.append(t); bs.append(0); es.append(0)
            else:
                b, se, p = res[t]; xs.append(t); bs.append(b*scale); es.append(1.96*se*scale)
        ax.errorbar(xs, bs, yerr=es, fmt="o-", color="#1f4e79", capsize=3)
        ax.axhline(0, color="grey", lw=0.8); ax.axvline(2022.5, color="grey", ls="--", lw=0.8)
        ax.set_title(lab); ax.set_xlabel("filing year (ref. 2022)")
    fig.tight_layout(); fig.savefig(OUT_PNG, dpi=200)
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT_MD, OUT_PNG)


if __name__ == "__main__":
    main()
