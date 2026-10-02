"""
Tables for the AI4SciSci 2026 camera-ready, built in one place from the cleaned data.

Reviewer 1 (point 4) and Reviewer 2 asked for a main results table, dataset statistics, an
event-study figure and counts of patents and firms. Reviewer 1 also noted that the age windows
"four to eight years" and "eight years or older" both included age eight. From here on every age
window is HALF-OPEN, [lo, hi), so no citation is counted twice. The published closed-interval
estimates differ by at most 0.007 percentage points (51 of 426,270 pairs sit at exactly 8.00 years).

Specification for every share outcome: patent-level, class FE + filing-year FE, SE clustered by
class x filing year; mature sample (filings through 2024-06-30), as in the paper.

One NEW outcome is added because the required related work makes it the natural question:
Mukherjee et al. (2017) and Ke, Teng and Min (arXiv 2107.09176) show that both the mean age and
the DISPERSION of the science a document cites matter. We therefore report the patent-level
coefficient of variation of cited-paper age (patents citing at least two papers). Reading rule,
declared before the run: if the citation distribution compressed toward the middle, the CV falls.
Whatever it shows is reported.
"""
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.formula.api as smf

HERE = Path(__file__).resolve().parent
U = HERE.parent / "data/clean"
OUT = HERE.parent / "results/camera_ready_tables_2026-10-02.md"
MATURE = "2024-06-30"

raw = pd.read_csv(U / "lag_pairs_v2.csv.gz", parse_dates=["filing_date"])
full = raw.copy()
d = raw[raw.filing_date <= MATURE].copy()
d["age"] = d.lag_days / 365.25
keys = ["patent_id", "cpc_class", "filing_year", "treated", "post"]

def did(pl, y, scale=1.0):
    pl = pl.copy(); pl["cl"] = pl.cpc_class + "_" + pl.filing_year.astype(str)
    m = smf.ols(f"{y} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl.cl})
    t = "treated:post"
    return m.params[t] * scale, m.bse[t] * scale, m.pvalues[t], int(m.nobs)

L = ["# Camera-ready tables (AI4SciSci 2026)", "",
     "All age windows half-open [lo, hi). Mature sample: filings through 2024-06-30.", ""]

# ---------------------------------------------------------------- Table 1
L += ["## Table 1. Dataset statistics by class and period", "",
      "| class | group | patents pre | patents post | pairs pre | pairs post | assignees pre | assignees post | fresh share pre % | fresh share post % |",
      "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
order = ["G06N", "G16B", "G16C", "C40B", "F16B", "F16H", "B65D"]
d["fresh"] = ((d.age >= 0) & (d.age < 3)).astype(float)
tot = {}
for c in order:
    s = d[d.cpc_class == c]
    grp = "treated" if s.treated.iloc[0] == 1 else "control"
    row = []
    for per in (0, 1):
        q = s[s.post == per]
        row.append((q.patent_id.nunique(), len(q), q.assignee.nunique(), q.fresh.mean() * 100))
    L.append(f"| {c} | {grp} | {row[0][0]:,} | {row[1][0]:,} | {row[0][1]:,} | {row[1][1]:,} | "
             f"{row[0][2]:,} | {row[1][2]:,} | {row[0][3]:.1f} | {row[1][3]:.1f} |")
for v, lab in [(1, "All treated"), (0, "All control")]:
    s = d[d.treated == v]
    row = []
    for per in (0, 1):
        q = s[s.post == per]
        row.append((q.patent_id.nunique(), len(q), q.assignee.nunique(), q.fresh.mean() * 100))
    L.append(f"| **{lab}** | | {row[0][0]:,} | {row[1][0]:,} | {row[0][1]:,} | {row[1][1]:,} | "
             f"{row[0][2]:,} | {row[1][2]:,} | {row[0][3]:.1f} | {row[1][3]:.1f} |")
L += ["", f"Mature sample totals: {d.patent_id.nunique():,} patents, {len(d):,} citation pairs, "
      f"{d.assignee.nunique():,} distinct assignees, {d.paper_id.nunique():,} distinct cited papers. "
      f"Full sample through 2025: {full.patent_id.nunique():,} patents, {len(full):,} pairs.", ""]

# ---------------------------------------------------------------- Table 2
L += ["## Table 2. Main results: treated x post, patent level", "",
      "| outcome | unit | DiD | SE | p | N patents |", "|---|---|---:|---:|---:|---:|"]
wins = [("share, age [0, 3)", 0, 3), ("share, age [2, 5)", 2, 5), ("share, age [3, 6)", 3, 6),
        ("share, age [4, 8)", 4, 8), ("share, age [8, inf)", 8, None)]
for lab, lo, hi in wins:
    d["y"] = ((d.age >= lo) & ((d.age < hi) if hi is not None else True)).astype(float)
    pl = d.groupby(keys)["y"].mean().reset_index()
    b, se, p, n = did(pl, "y", 100)
    L.append(f"| {lab} | pp | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")
g = d.groupby(keys)["age"]
pl = g.agg(mean_age="mean", median_age="median", sd_age="std", n="size").reset_index()
for lab, y in [("mean age of cited papers", "mean_age"), ("median age of cited papers", "median_age")]:
    b, se, p, n = did(pl, y)
    L.append(f"| {lab} | years | {b:+.3f} | {se:.3f} | {p:.4f} | {n:,} |")
cv = pl[pl.n >= 2].copy(); cv["cv"] = cv.sd_age / cv.mean_age
cv = cv[np.isfinite(cv.cv)]
b, se, p, n = did(cv, "cv")
L.append(f"| CV of cited-paper age (NEW, patents with 2+ citations) | ratio | {b:+.4f} | {se:.4f} | {p:.4f} | {n:,} |")
cvm = cv.groupby(["treated", "post"]).cv.mean()
L += ["", f"Mean CV: treated pre {cvm[(1,0)]:.3f}, post {cvm[(1,1)]:.3f}; control pre {cvm[(0,0)]:.3f}, post {cvm[(0,1)]:.3f}.", ""]

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
