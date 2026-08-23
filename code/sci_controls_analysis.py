"""
Item 9 (step 2): the two declared estimates on the science-intensive alternative controls,
plus wild cluster bootstrap inference at the class level.

Declared ex ante (docs/01 addendum 2026-08-23):
 (a) treated (G06N, G16B, G16C, C40B) vs science-intensive controls only (G01N, G02B, B01D, G21)
 (b) treated vs ALL controls (mechanical F16B, F16H, B65D, E05B, B25B + the four science-intensive)
Outcomes and specs identical to the baseline:
 B. share of citations <= 3y, patent level, filings <= 2024-06-30, class FE + filing-year FE,
    SE clustered class x year; raw citation-weighted group shares reported.
 A. log(1 + lag), pair level, 10-year window, same FE and clustering.
Inference: restricted wild cluster bootstrap-t, clusters = CPC class (G = 8 for (a),
G = 13 for (b)), Webb six-point weights, B = 9,999, null imposed.
Reading rule (fixed): supported if the share DiD vs science-intensive controls is negative and
of broadly similar magnitude to the mechanical baseline (-4.93 pp); a sign flip or collapse
toward zero is reported as a failure of the robustness test.

Output: ../results/item9_sci_controls_2026-08-23.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

BASE = Path("../data/clean/lag_pairs.csv")            # 7 classes
NINE = Path("../data/clean/lag_pairs_9classes.csv")   # + E05B, B25B
SCI = Path("../data/clean/lag_pairs_sci.csv.gz")      # G01N, G02B, B01D, G21
OUT = Path("../results/item9_sci_controls_2026-08-23.md")
TREATED = {"G06N", "G16B", "G16C", "C40B"}
B = 9999
RNG = np.random.default_rng(2026)
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def prep(d):
    d = d.copy()
    d["filing_date"] = pd.to_datetime(d["filing_date"])
    d["age_y"] = d["lag_days"] / 365.25
    d["fresh3"] = (d["age_y"] <= 3).astype(int)
    d["log_lag"] = np.log1p(d["lag_days"])
    d["cluster"] = d["cpc_class"] + "_" + d["filing_year"].astype(str)
    return d


def conv(d, y, level):
    if level == "patent":
        d = d[d["filing_date"] <= "2024-06-30"]
        pl = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"])[y].mean().reset_index()
        scale = 100
    else:
        pl = d[d["lag_days"] <= 10 * 365.25]
        scale = 1
    m = smf.ols(f"{y} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    return m.params["treated:post"] * scale, m.bse["treated:post"] * scale, m.pvalues["treated:post"], int(m.nobs), pl


def wcb(pl, y):
    X = pd.get_dummies(pl[["cpc_class", "filing_year"]].astype(str), drop_first=True).astype(float)
    X.insert(0, "const", 1.0)
    X["T"] = (pl["treated"] * pl["post"]).astype(float)
    Xn = X.to_numpy(); yn = pl[y].to_numpy(dtype=float); g = pl["cpc_class"].to_numpy()
    n, k = Xn.shape; k_idx = k - 1
    clusters = np.unique(g); G = len(clusters)
    XtX_inv = np.linalg.inv(Xn.T @ Xn)
    beta = XtX_inv @ Xn.T @ yn; u = yn - Xn @ beta

    def cr1(S):
        V = XtX_inv @ (S.T @ S) @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
        return np.sqrt(V[k_idx, k_idx])

    S0 = np.vstack([Xn[g == c].T @ u[g == c] for c in clusters])
    t0 = beta[k_idx] / cr1(S0)
    Xr = np.delete(Xn, k_idx, axis=1)
    br = np.linalg.lstsq(Xr, yn, rcond=None)[0]; fit_r = Xr @ br; ur = yn - fit_r
    Xf = np.vstack([Xn[g == c].T @ fit_r[g == c] for c in clusters])
    A = np.vstack([Xn[g == c].T @ ur[g == c] for c in clusters])
    XX = np.stack([Xn[g == c].T @ Xn[g == c] for c in clusters])
    ts = np.empty(B)
    for i in range(B):
        w = RNG.choice(WEBB, size=G)
        bb = XtX_inv @ (Xf.sum(0) + (w[:, None] * A).sum(0))
        S = Xf + w[:, None] * A - np.einsum("gij,j->gi", XX, bb)
        ts[i] = bb[k_idx] / cr1(S)
    return G, float(np.mean(np.abs(ts) >= abs(t0)))


def group_shares(d):
    d = d[d["filing_date"] <= "2024-06-30"]
    g = d.groupby(["treated", "post"])["fresh3"].mean() * 100
    return g


def main():
    base = prep(pd.read_csv(BASE, parse_dates=["filing_date"]))
    nine = prep(pd.read_csv(NINE))
    sci = prep(pd.read_csv(SCI))
    treated = base[base["treated"] == 1]
    common = ["patent_id", "filing_date", "paper_id", "pub_date", "cpc_class", "lag_days",
              "treated", "post", "filing_year", "age_y", "fresh3", "log_lag", "cluster"]
    a = pd.concat([treated[common], sci[common]], ignore_index=True)          # (a) sci controls only
    b = pd.concat([nine[common], sci[common]], ignore_index=True)            # (b) all 13 classes

    lines = ["# Item 9: science-intensive alternative controls (G01N, G02B, B01D, G21)", "",
             f"Science-control pairs: {len(sci):,} ({sci['patent_id'].nunique():,} patents). "
             f"Sample (a) treated vs science controls: {len(a):,} pairs. "
             f"Sample (b) treated vs all 9 mechanical+2 + 4 science controls: {len(b):,} pairs.", ""]
    lines.append("## Pairs by class and period, science controls\n")
    t = sci.groupby(["cpc_class", "post"]).size().unstack(fill_value=0)
    lines.append("| class | pre | post |"); lines.append("|---|---:|---:|")
    for c, r in t.iterrows():
        lines.append(f"| {c} | {r.get(0,0):,} | {r.get(1,0):,} |")

    lines.append("\n## B. Share of citations <= 3y (pp), patent level, filings <= 2024-06-30\n")
    lines.append("| control group | treated pre % | treated post % | control pre % | control post % | DiD | SE | p (class x year) | G | p (wild cluster bootstrap) | N patents |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lab, d in [("science-intensive only (a)", a), ("all controls (b)", b)]:
        bta, se, p, n, pl = conv(d, "fresh3", "patent")
        G, pw = wcb(pl, "fresh3")
        gs = group_shares(d)
        lines.append(f"| {lab} | {gs[(1,0)]:.1f} | {gs[(1,1)]:.1f} | {gs[(0,0)]:.1f} | {gs[(0,1)]:.1f} | {bta:+.2f} | {se:.2f} | {p:.4f} | {G} | {pw:.4f} | {n:,} |")
    lines.append("\nBaseline vs mechanical controls (paper Table 5): DiD -4.93 pp, p = 0.0012, WCB p = 0.106 (G = 7), 0.093 (G = 9).")

    lines.append("\n## A. Log(1 + lag), pair level, 10-year window\n")
    lines.append("| control group | treated x post | SE | p (class x year) | G | p (wild cluster bootstrap) | N pairs |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for lab, d in [("science-intensive only (a)", a), ("all controls (b)", b)]:
        bta, se, p, n, pl = conv(d, "log_lag", "pair")
        G, pw = wcb(pl, "log_lag")
        lines.append(f"| {lab} | {bta:+.3f} | {se:.3f} | {p:.4f} | {G} | {pw:.4f} | {n:,} |")
    lines.append("\nBaseline vs mechanical controls: +0.201, p = 0.0002, WCB p = 0.111 (G = 7), 0.087 (G = 9).")

    lines.append("\n## Raw fresh-science shares of the control classes (citation-weighted, %, filings <= 2024-06-30)\n")
    m = sci[sci["filing_date"] <= "2024-06-30"]
    t = (m.groupby(["cpc_class", "post"])["fresh3"].mean() * 100).unstack()
    lines.append("| class | pre-2023 | post-2023 |"); lines.append("|---|---:|---:|")
    for c, r in t.iterrows():
        lines.append(f"| {c} | {r[0]:.1f} | {r[1]:.1f} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
