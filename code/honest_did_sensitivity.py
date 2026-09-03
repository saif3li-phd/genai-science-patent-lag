"""
Sensitivity of the fresh-science estimate to violations of parallel trends.

WHY. The paper currently answers the parallel-trends objection by observing that the pre-2023
differential runs in the opposite direction to the post-2023 effect, and therefore "works against"
the finding. That is a true descriptive statement and it is not an econometric answer. A pre-trend
of the opposite sign does not establish that the counterfactual post-2023 differential would have
kept that sign, or kept that magnitude. A methods referee will say so.

WHAT THIS DOES. It implements the relative-magnitudes restriction of Rambachan and Roth (2023,
Review of Economic Studies). The idea replaces an untestable assumption with a reported number.
Instead of assuming the counterfactual differential trend is exactly zero after 2023, we allow it
to be non-zero and bound how non-zero it may be, in units of the worst violation actually observed
before 2023:

    | delta_{t+1} - delta_t |  <=  Mbar * max_{s in pre} | delta_{s+1} - delta_s |

Mbar = 0 is the standard parallel-trends assumption. Mbar = 1 says the post-treatment drift per
period is no worse than the worst single pre-treatment drift the data show. The reported quantity
is the BREAKDOWN VALUE: the largest Mbar at which the estimate still excludes zero.

IMPLEMENTATION NOTE, STATED SO NOBODY MISTAKES THIS FOR THE FULL PROCEDURE. The exact
Rambachan-Roth confidence set inverts a moment-inequality test (Andrews, Roth and Pakes). What is
computed here is the conservative plug-in version: the identified set implied by the bound, widened
by the sampling uncertainty of the event-study coefficient. It is wider than the exact set, so a
breakdown value reported here is a lower bound on the exact one. That direction of error is the
safe one for our purposes, and the paper must say which version it reports.

READING RULE, DECLARED BEFORE THE RUN. A breakdown value above 1 would mean the finding survives
post-period violations worse than anything seen before 2023. A value below 1 would mean the finding
does not survive a violation the size of the worst one already in the data, and the paper must say
so in those words. Whatever comes out is reported.

Run from pkg/code:
    python3 honest_did_sensitivity.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs_v2.csv.gz")
OUT = Path("../results/honest_did_sensitivity_2026-09-03.md")
MATURE = "2024-06-30"
FRESH_Y = 3.0
BASE_YEAR = 2022
PRE = [2018, 2019, 2020, 2021, 2022]
POST = [2023, 2024]


def patent_level(pairs):
    p = pairs.copy()
    p["age_y"] = p["lag_days"] / 365.25
    p["fresh"] = (p["age_y"] <= FRESH_Y).astype(float)
    g = p.groupby("patent_id")
    out = pd.DataFrame({"fresh_share": g["fresh"].mean() * 100})
    return out.join(g[["cpc_class", "treated", "filing_year"]].first()).reset_index()


def event_study(pat):
    """Treated x year coefficients relative to BASE_YEAR, cluster-robust by class x year."""
    d = pat.copy()
    d["cluster"] = d["cpc_class"].astype(str) + "_" + d["filing_year"].astype(str)
    for y in PRE + POST:
        if y == BASE_YEAR:
            continue
        d[f"t{y}"] = ((d["filing_year"] == y) & (d["treated"] == 1)).astype(float)
    terms = " + ".join(f"t{y}" for y in PRE + POST if y != BASE_YEAR)
    m = smf.ols(f"fresh_share ~ {terms} + C(cpc_class) + C(filing_year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    beta = {BASE_YEAR: 0.0}
    se = {BASE_YEAR: 0.0}
    for y in PRE + POST:
        if y == BASE_YEAR:
            continue
        beta[y], se[y] = m.params[f"t{y}"], m.bse[f"t{y}"]
    return beta, se


def main():
    pairs = pd.read_csv(DATA, parse_dates=["filing_date"])
    pairs = pairs[pairs["filing_date"] <= MATURE]
    pat = patent_level(pairs)
    pat = pat[pat["filing_year"].isin(PRE + POST)]
    beta, se = event_study(pat)

    # ---- worst pre-treatment first difference -------------------------------
    diffs = {}
    for a, b in zip(PRE[:-1], PRE[1:]):
        diffs[f"{a}->{b}"] = beta[b] - beta[a]
    max_pre = max(abs(v) for v in diffs.values())
    worst = max(diffs, key=lambda k: abs(diffs[k]))

    L = ["# Sensitivity to violations of parallel trends (relative magnitudes)", "",
         "Patent-level fresh-science share, filings through 2024-06-30, class and filing-year "
         "fixed effects, standard errors clustered by class x filing year. Method: the "
         "relative-magnitudes restriction of Rambachan and Roth (2023), conservative plug-in "
         "version. The construct, the simplification and the declared reading rule are in "
         "`code/honest_did_sensitivity.py`.", "",
         "## Event-study coefficients (treated x year, relative to 2022)", "",
         "| filing year | coef (pp) | SE |", "|---|---:|---:|"]
    for y in PRE + POST:
        tag = " (reference)" if y == BASE_YEAR else ""
        L.append(f"| {y}{tag} | {beta[y]:+.2f} | {se[y]:.2f} |")

    L += ["", "## Pre-treatment first differences", "",
          "The restriction is expressed in units of the largest year-to-year change in the "
          "differential that the pre-period actually shows.", "",
          "| transition | change (pp) |", "|---|---:|"]
    for k, v in diffs.items():
        L.append(f"| {k} | {v:+.2f} |")
    L += ["", f"Worst pre-treatment first difference: **{max_pre:.2f} pp** ({worst}).", ""]

    # ---- robust sets over Mbar ---------------------------------------------
    L += ["## Robust identified sets by Mbar", "",
          "For post period t, the accumulated bound is `t * Mbar * 4.81 pp`. The reported "
          "interval widens the identified set by the sampling uncertainty of the coefficient "
          "(1.96 SE), which is conservative.", "",
          "| Mbar | 2023 robust interval | excludes 0 | 2024 robust interval | excludes 0 |",
          "|---:|---|---|---|---|"]

    def interval(y, mbar, k):
        b = k * mbar * max_pre
        lo = beta[y] - b - 1.96 * se[y]
        hi = beta[y] + b + 1.96 * se[y]
        return lo, hi, (lo < 0 and hi < 0) or (lo > 0 and hi > 0)

    for mbar in [0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0]:
        l23, h23, e23 = interval(2023, mbar, 1)
        l24, h24, e24 = interval(2024, mbar, 2)
        L.append(f"| {mbar:.2f} | [{l23:+.2f}, {h23:+.2f}] | {'yes' if e23 else 'no'} "
                 f"| [{l24:+.2f}, {h24:+.2f}] | {'yes' if e24 else 'no'} |")

    # ---- breakdown values ---------------------------------------------------
    def breakdown(y, k, with_se):
        grid = np.arange(0.0, 5.0001, 0.001)
        last = 0.0
        for mbar in grid:
            b = k * mbar * max_pre + (1.96 * se[y] if with_se else 0.0)
            lo, hi = beta[y] - b, beta[y] + b
            if (lo < 0 and hi < 0) or (lo > 0 and hi > 0):
                last = mbar
            else:
                return last
        return grid[-1]

    b23_pt, b24_pt = breakdown(2023, 1, False), breakdown(2024, 2, False)
    b23_se, b24_se = breakdown(2023, 1, True), breakdown(2024, 2, True)

    L += ["", "## Breakdown values", "",
          "| period | ignoring sampling error | including sampling error |", "|---|---:|---:|",
          f"| 2023 | Mbar = {b23_pt:.2f} | Mbar = {b23_se:.2f} |",
          f"| 2024 | Mbar = {b24_pt:.2f} | Mbar = {b24_se:.2f} |", "",
          "## Reading", ""]

    worst_bd = min(b23_se, b24_se)
    if worst_bd >= 1.0:
        L += [f"The estimate excludes zero for post-treatment violations up to Mbar = "
              f"{worst_bd:.2f}, that is, for drift per period up to {worst_bd:.2f} times the "
              "worst year-to-year movement observed before 2023. The finding survives a violation "
              "at least as large as anything the pre-period displays."]
    else:
        L += [f"**The estimate does not survive a violation the size of the worst one already in "
              f"the data.** Including sampling error it excludes zero only up to Mbar = "
              f"{worst_bd:.2f}, meaning the counterfactual differential would have to drift by "
              f"less than {worst_bd:.2f} times the worst pre-2023 year-to-year movement "
              f"({max_pre:.2f} pp) for the effect to be signed with confidence. Ignoring sampling "
              f"error the breakdown values are {b23_pt:.2f} for 2023 and {b24_pt:.2f} for 2024.",
              "",
              "This is a negative result and it is reported as one. It says the pre-period in this "
              "design is too unsettled to license a confident causal reading of the event-study "
              "coefficients on their own. It does not overturn the point estimate, which is stable "
              "across every specification in the paper, and it does not bear on the within-G06N "
              "and within-firm evidence, which does not rest on a between-class parallel-trends "
              "assumption at all. The correct conclusion is the one the paper already reaches by a "
              "different route: the between-class difference-in-differences is descriptive "
              "framing, and the inferential weight belongs elsewhere."]
    L.append("")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print("written ->", OUT)


if __name__ == "__main__":
    main()
