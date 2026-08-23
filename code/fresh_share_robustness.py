"""
Item 1: Shifted-window robustness of the fresh-science composition result.

Threat addressed (self-critique #3): the share of citations to papers <= 3 years
old may be contaminated by incomplete indexing / NPL resolution of very recent
papers in Lens. If post-2023 patents cite 2022-2025 papers that Lens has not yet
resolved, the <= 3y share falls mechanically in the post period.

Test: re-estimate the patent-level difference-in-differences on citation-age
shares whose windows sit AWAY from the indexing zone (2-5y, 3-6y, 4-8y), plus
the old-stock share (>= 8y). A genuine reorientation toward the canon predicts
that the 2-5y and 3-6y shares ALSO fall in treated classes relative to controls
and that the >= 8y share rises. An indexing artifact predicts the opposite:
mass lost from <= 3y must reappear in the adjacent windows (2-5y / 3-6y).

Outcome  : patent-level share of citation pairs whose age (filing_date - pub_date)
           falls in the window  [lo, hi] years, age = lag_days / 365.25.
Model    : share ~ treated:post + C(cpc_class) + C(filing_year), OLS, unweighted
           (one row per patent), SE clustered by class x filing-year. This is the
           exact specification behind the -4.9 pp baseline (mature 2024-06-30).
Samples  : full (filings through 2025-12-31), mature 2024-06-30, mature 2024-12-31.
Placebo  : same windows on placebo_pairs.csv (2015-2019, fake treatment 2017-01-01).

Usage (from code/):
  python3 fresh_share_robustness.py   # writes ../results/item1_shifted_windows_auto.md
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

MAIN = Path("../data/clean/lag_pairs.csv")
PLACEBO = Path("../data/clean/placebo_pairs.csv")
OUT = Path("../results/item1_shifted_windows_auto.md")  # machine output; the annotated verdict is item1_shifted_windows_2026-08-21.md

# (label, lo_years, hi_years); hi=None means open-ended
WINDOWS = [
    ("<=3y (baseline)", 0.0, 3.0),
    ("2-5y (shifted)", 2.0, 5.0),
    ("3-6y (shifted)", 3.0, 6.0),
    ("4-8y (shifted)", 4.0, 8.0),
    (">=8y (old stock)", 8.0, None),
]
SAMPLES = [("full (through 2025-12-31)", None),
           ("mature 2024-06-30", "2024-06-30"),
           ("mature 2024-12-31", "2024-12-31")]


def add_windows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["age_y"] = df["lag_days"] / 365.25
    for lab, lo, hi in WINDOWS:
        col = f"w_{lo:g}_{'inf' if hi is None else f'{hi:g}'}"
        df[col] = ((df["age_y"] >= lo) & ((df["age_y"] <= hi) if hi is not None else True)).astype(int)
    return df


def wincols():
    return [(lab, f"w_{lo:g}_{'inf' if hi is None else f'{hi:g}'}") for lab, lo, hi in WINDOWS]


def patent_level(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["patent_id", "cpc_class", "filing_year", "treated", "post"]
    agg = {c: "mean" for _, c in wincols()}
    agg["lag_days"] = "size"
    pl = df.groupby(keys).agg(agg).reset_index().rename(columns={"lag_days": "n_pairs"})
    pl["cluster"] = pl["cpc_class"] + "_" + pl["filing_year"].astype(str)
    return pl


def did(pl: pd.DataFrame, y: str):
    m = smf.ols(f"{y} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    return m.params["treated:post"], m.bse["treated:post"], m.pvalues["treated:post"], int(m.nobs)


def group_means(df: pd.DataFrame, y: str):
    """Pair-level (citation-weighted) shares by treated x post, in percent."""
    g = df.groupby(["treated", "post"])[y].mean() * 100
    return {k: g.get(k, np.nan) for k in [(1, 0), (1, 1), (0, 0), (0, 1)]}


def run_block(df: pd.DataFrame, title: str, lines: list) -> None:
    pl = patent_level(df)
    lines.append(f"\n### {title}\n")
    lines.append(f"Pairs: {len(df):,} | Patents: {len(pl):,}\n")
    lines.append("| window | treated pre % | treated post % | control pre % | control post % | raw DiD (pp) | patent-level DiD (pp) | SE | p |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lab, col in wincols():
        gm = group_means(df, col)
        raw = (gm[(1, 1)] - gm[(1, 0)]) - (gm[(0, 1)] - gm[(0, 0)])
        b, se, p, n = did(pl, col)
        lines.append(f"| {lab} | {gm[(1,0)]:.1f} | {gm[(1,1)]:.1f} | {gm[(0,0)]:.1f} | {gm[(0,1)]:.1f} "
                     f"| {raw:+.1f} | {b*100:+.2f} | {se*100:.2f} | {p:.4f} |")


def cited_year_profile(df: pd.DataFrame, lines: list) -> None:
    """Where did the mass go? Distribution of cited-paper publication years, treated group."""
    t = df[df["treated"] == 1].copy()
    t["pub_year"] = pd.to_datetime(t["pub_date"]).dt.year
    lines.append("\n### Treated group: share of citation pairs by cited-paper publication year (%)\n")
    lines.append("| pub_year | pre-2023 filings | post-2023 filings |")
    lines.append("|---|---:|---:|")
    tab = t.groupby(["post", "pub_year"]).size().unstack(0).fillna(0)
    tab = tab.div(tab.sum(axis=0), axis=1) * 100
    for yr in range(2008, 2026):
        if yr in tab.index:
            lines.append(f"| {yr} | {tab.loc[yr, 0]:.1f} | {tab.loc[yr, 1]:.1f} |")
    top = tab[1].sort_values(ascending=False).head(5)
    lines.append(f"\nTop-5 cited publication years in post-2023 treated filings: "
                 + ", ".join(f"{int(y)} ({v:.1f}%)" for y, v in top.items()))


BINS = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 8), (8, 12), (12, 99)]


def age_bins(df: pd.DataFrame, lines: list) -> None:
    """One-year bins of cited-paper age, same patent-level DiD (added post-hoc, see verdict file)."""
    lines.append("\n### Fine age-bin decomposition (same spec)\n")
    lines.append("| age bin | treated pre % | treated post % | control pre % | control post % | patent-level DiD (pp) | p |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    keys = ["patent_id", "cpc_class", "filing_year", "treated", "post"]
    for lo, hi in BINS:
        d = df.copy()
        d["y"] = ((d["age_y"] >= lo) & (d["age_y"] < hi)).astype(int)
        pl = d.groupby(keys)["y"].mean().reset_index()
        pl["cluster"] = pl["cpc_class"] + "_" + pl["filing_year"].astype(str)
        b, se, p, n = did(pl, "y")
        gm = group_means(d, "y")
        lines.append(f"| {lo}-{hi}y | {gm[(1,0)]:.1f} | {gm[(1,1)]:.1f} | {gm[(0,0)]:.1f} | {gm[(0,1)]:.1f} | {b*100:+.2f} | {p:.4f} |")


def main() -> None:
    lines = ["# Item 1: Shifted-window robustness of the fresh-science result",
             "",
             "Spec: patent-level share of citations in each age window ~ treated:post + class FE + "
             "filing-year FE; OLS, unweighted (one row per patent); SE clustered by class x filing-year. "
             "Group shares are citation-pair-weighted means (as reported in the abstract: 19.7% -> 11.9%). "
             "Raw DiD = (treated post - treated pre) - (control post - control pre) on those shares.",
             "",
             "Reading rule fixed BEFORE running: the composition result survives if the 2-5y and 3-6y "
             "treated:post coefficients are negative and significant and the >=8y coefficient is positive. "
             "It collapses into an indexing artifact if the shifted windows are flat or positive.",
             ]

    df = add_windows(pd.read_csv(MAIN, parse_dates=["filing_date", "pub_date"]))
    lines.append("\n## A. Main sample (filings 2018-2025, treatment 2023-01-01)")
    for title, mature in SAMPLES:
        d = df if mature is None else df[df["filing_date"] <= mature]
        run_block(d, title, lines)
    cited_year_profile(df[df["filing_date"] <= "2024-06-30"], lines)
    age_bins(df[df["filing_date"] <= "2024-06-30"], lines)

    pb = add_windows(pd.read_csv(PLACEBO, parse_dates=["filing_date", "pub_date"]))
    lines.append("\n## B. Placebo sample (filings 2015-2019, fake treatment 2017-01-01)")
    run_block(pb, "placebo, all filings 2015-2019", lines)

    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print(f"\nwritten -> {OUT}")


if __name__ == "__main__":
    main()
