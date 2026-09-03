"""
Randomization inference on the fresh-science composition estimate.

WHY THIS TEST EXISTS. Treatment is assigned at the level of the CPC class, and there are seven
classes in the baseline. Cluster-robust inference at the assignment level is therefore bounded by
construction, and the wild cluster bootstrap p-values reported in Section 6.5 run from 0.09 to
0.15. A referee is entitled to write that the significance of the primary estimate is not robust
to inference at the treatment-assignment level. That statement is correct, and no amount of
re-clustering makes it false.

Randomization inference answers a different and answerable question. It does not ask what the
sampling distribution of the estimator is. It asks: among every way these classes could have been
split into a treated set and a control set, how extreme is the split that nature actually gave us?
This is an exact, finite-sample test. It makes no asymptotic appeal to the number of clusters,
which is exactly the appeal the referee is objecting to.

  Baseline, 7 classes, 4 treated:  C(7,4)  =  35 assignments, finest attainable one-sided p = 1/35
  Full pool, 13 classes, 4 treated: C(13,4) = 715 assignments, finest attainable p = 1/715

The 13-class pool is the four treated classes, the three mechanical controls, the two auxiliary
mechanical classes (E05B, B25B) and the four science-intensive controls (G01N, G02B, B01D, G21).
Every class in the pool was selected by the same official-definition rule, before any outcome was
seen, so the pool is a defensible randomization set.

READING RULE, DECLARED BEFORE THE RUN. The test supports the paper if the true assignment sits in
the lower tail of the permutation distribution, meaning few placebo splits produce a decline as
large. It fails if the true estimate is unremarkable among placebo splits, in which case the
composition result is a feature of how classes differ from one another in general and not of
generative-AI exposure. Whatever comes out is reported.

WHAT THIS TEST CANNOT DO. Placebo splits are not random in any physical sense: the classes differ
systematically, and a split that puts all four software-adjacent classes on one side is not
exchangeable with one that splits them. The p-value is therefore a sharp descriptive statement
about how unusual the observed contrast is within this pool, not a licence to claim the estimate
is significant in the conventional sense. Section 6.5 keeps its wording either way.

Run from pkg/code:
    python3 randomization_inference.py
"""

from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

MAIN = Path("../data/clean/lag_pairs_v2.csv.gz")
NINE = Path("../data/clean/lag_pairs_9classes_v2.csv.gz")
SCI = Path("../data/clean/lag_pairs_sci.csv.gz")
OUT = Path("../results/randomization_inference_2026-09-03.md")

MATURE = "2024-06-30"
FRESH_Y = 3.0
POST = "2023-01-01"
TRUE_TREATED = {"G06N", "G16B", "G16C", "C40B"}


def patent_level(pairs):
    """One row per patent: fresh-science share in percentage points."""
    p = pairs.copy()
    p["age_y"] = p["lag_days"] / 365.25
    p["fresh"] = (p["age_y"] <= FRESH_Y).astype(float)
    g = p.groupby("patent_id")
    out = pd.DataFrame({"fresh_share": g["fresh"].mean() * 100})
    out = out.join(g[["cpc_class", "post", "filing_year"]].first())
    return out.reset_index()


def load_pool():
    """The 13-class pool, deduplicated on patent_id, mature filings only."""
    frames = []
    for f in (MAIN, NINE, SCI):
        d = pd.read_csv(f, parse_dates=["filing_date"])
        d = d[d["filing_date"] <= MATURE]
        if "post" not in d.columns:
            d["post"] = (d["filing_date"] >= POST).astype(int)
        frames.append(d[["patent_id", "cpc_class", "post", "filing_year", "lag_days"]])
    pairs = pd.concat(frames, ignore_index=True).drop_duplicates(
        subset=["patent_id", "lag_days", "cpc_class"])
    return patent_level(pairs)


def residualizer(pat):
    """
    Frisch-Waugh. Class and filing-year fixed effects do not change across permutations, so the
    projection matrix is built once. Returns a function that residualizes any vector on the FEs.
    """
    F = pd.get_dummies(pat["cpc_class"], drop_first=True, dtype=float).values
    Y = pd.get_dummies(pat["filing_year"], drop_first=True, dtype=float).values
    X = np.column_stack([np.ones(len(pat)), F, Y])
    XtX_inv = np.linalg.pinv(X.T @ X)

    def resid(v):
        return v - X @ (XtX_inv @ (X.T @ v))

    return resid


def did_coef(resid, y_res, treated_mask, post):
    """DiD coefficient on treated x post, after partialling out the fixed effects."""
    d = (treated_mask.astype(float) * post)
    d_res = resid(d)
    denom = d_res @ d_res
    if denom < 1e-10:
        return np.nan
    return float((d_res @ y_res) / denom)


def run(pat, pool_classes, label, lines):
    sub = pat[pat["cpc_class"].isin(pool_classes)].copy().reset_index(drop=True)
    resid = residualizer(sub)
    y_res = resid(sub["fresh_share"].values.astype(float))
    post = sub["post"].values.astype(float)
    cls = sub["cpc_class"].values

    k = len(TRUE_TREATED)
    assignments = list(combinations(sorted(pool_classes), k))
    coefs = {}
    for a in assignments:
        mask = np.isin(cls, a)
        coefs[a] = did_coef(resid, y_res, mask, post)

    true_key = tuple(sorted(TRUE_TREATED))
    b_true = coefs[true_key]
    vals = np.array([v for v in coefs.values() if np.isfinite(v)])

    n_le = int((vals <= b_true).sum())               # as negative as, or more negative than
    n_abs = int((np.abs(vals) >= abs(b_true)).sum())  # two-sided, on magnitude
    p_one = n_le / len(vals)
    p_two = n_abs / len(vals)

    order = sorted(coefs.items(), key=lambda kv: (np.inf if not np.isfinite(kv[1]) else kv[1]))
    rank = [i for i, (a, _) in enumerate(order, start=1) if a == true_key][0]

    lines += [f"### {label}", "",
              f"- Classes in the pool: {len(pool_classes)} ({', '.join(sorted(pool_classes))})",
              f"- Patents: {len(sub):,}",
              f"- Assignments evaluated: {len(vals)} of {len(assignments)} "
              f"(a split with no post-period variation is dropped)",
              f"- True estimate: **{b_true:+.2f} pp**",
              f"- Rank of the true estimate, most negative first: **{rank} of {len(vals)}**",
              f"- One-sided randomization p (as negative or more): **{p_one:.4f}** "
              f"({n_le}/{len(vals)})",
              f"- Two-sided randomization p (magnitude): **{p_two:.4f}** ({n_abs}/{len(vals)})",
              f"- Finest attainable p in this pool: {1/len(vals):.4f}",
              f"- Placebo distribution: mean {vals.mean():+.2f}, sd {vals.std(ddof=1):.2f}, "
              f"min {vals.min():+.2f}, max {vals.max():+.2f}", ""]

    if len(vals) <= 40:
        lines += ["| rank | treated set | DiD (pp) |", "|---:|---|---:|"]
        for i, (a, v) in enumerate(order, start=1):
            star = " **<- actual**" if a == true_key else ""
            lines.append(f"| {i} | {', '.join(a)}{star} | {v:+.2f} |")
        lines.append("")
    else:
        lines += ["Ten most negative placebo splits, for inspection:", "",
                  "| rank | treated set | DiD (pp) |", "|---:|---|---:|"]
        for i, (a, v) in enumerate(order[:10], start=1):
            star = " **<- actual**" if a == true_key else ""
            lines.append(f"| {i} | {', '.join(a)}{star} | {v:+.2f} |")
        if rank > 10:
            lines.append(f"| {rank} | {', '.join(true_key)} **<- actual** | {b_true:+.2f} |")
        lines.append("")

    return b_true, p_one, p_two, rank, len(vals)


def main():
    pat = load_pool()
    seven = ["G06N", "G16B", "G16C", "C40B", "F16B", "F16H", "B65D"]
    nine = seven + ["E05B", "B25B"]
    thirteen = nine + ["G01N", "G02B", "B01D", "G21"]

    lines = ["# Randomization inference on the fresh-science composition estimate", "",
             "Patent-level share of citations to papers three years old or younger, filings "
             "through 2024-06-30, class and filing-year fixed effects. For every way of choosing "
             "four classes from the pool as the treated set, the same specification is "
             "re-estimated. The reported p-value is the share of assignments producing an "
             "estimate at least as extreme as the one the actual assignment produces.", "",
             "The construct and its declared reading rule are in `code/randomization_inference.py`.",
             ""]

    res = {}
    for pool, label in [(seven, "A. Baseline pool: four treated plus three mechanical controls"),
                        (nine, "B. Plus the two auxiliary mechanical classes (E05B, B25B)"),
                        (thirteen, "C. Full pool: plus the four science-intensive controls")]:
        avail = [c for c in pool if c in set(pat["cpc_class"])]
        if len(avail) < len(pool):
            lines.append(f"*Missing from data: {sorted(set(pool) - set(avail))}*\n")
        res[label] = run(pat, avail, label, lines)

    lines += ["## Reading", "",
              "The wild cluster bootstrap and this test answer different questions and both belong "
              "in the paper. The bootstrap asks how much sampling variation the estimator has when "
              "only seven clusters carry the treatment, and its answer is: enough that the estimate "
              "is not significant at five percent. That answer stands and Section 6.5 keeps it. "
              "This test asks how unusual the observed treated-versus-control contrast is among all "
              "the contrasts these classes could have produced, and it is exact in finite samples.",
              "",
              "Neither test rescues the other. Reported together they say what the paper can "
              "honestly claim: a stable point estimate whose class-level significance is marginal, "
              "sitting at a specific and reportable place in the distribution of alternative "
              "class splits.", ""]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print("written ->", OUT)


if __name__ == "__main__":
    main()
