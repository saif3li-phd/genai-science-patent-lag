"""
Revision plan item 5: inference at the CPC main-group level.

Treatment is still defined by the patent's own class (the four treated classes), but the
cluster dimension moves from 7 classes to the 133 own-class CPC main groups (29 treated,
104 control), which is the remedy the paper's Section 8 lists for the few-cluster problem.
Two specifications per outcome:
  (i)  class fixed effects, clusters = main group
  (ii) main-group fixed effects (finer technology control), clusters = main group
Inference: restricted wild cluster bootstrap-t, Webb weights, B = 9,999, null imposed.
Outcomes and samples identical to the baseline (share: patent level, filings <= 2024-06-30;
lag: pair level, 10-year window).
Output: ../results/item12_main_group_inference_2026-08-24.md
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATA = Path("../data/clean/lag_pairs_v2.csv.gz")
OUT = Path("../results/item12_main_group_inference_2026-08-24.md")
B = 9999
RNG = np.random.default_rng(2026)
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def wcb(X, y, g):
    n, k = X.shape
    k_idx = k - 1
    clusters = np.unique(g)
    G = len(clusters)
    XtX_inv = np.linalg.inv(X.T @ X)
    beta = XtX_inv @ X.T @ y
    u = y - X @ beta
    idx = [g == c for c in clusters]

    def cr1(S):
        V = XtX_inv @ (S.T @ S) @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
        return np.sqrt(V[k_idx, k_idx])

    S0 = np.vstack([X[m].T @ u[m] for m in idx])
    se = cr1(S0)
    t0 = beta[k_idx] / se
    Xr = np.delete(X, k_idx, axis=1)
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]
    fit_r = Xr @ br
    ur = y - fit_r
    Xf = np.vstack([X[m].T @ fit_r[m] for m in idx])
    A = np.vstack([X[m].T @ ur[m] for m in idx])
    XX = np.stack([X[m].T @ X[m] for m in idx])
    ts = np.empty(B)
    for i in range(B):
        w = RNG.choice(WEBB, size=G)
        bb = XtX_inv @ (Xf.sum(0) + (w[:, None] * A).sum(0))
        S = Xf + w[:, None] * A - np.einsum("gij,j->gi", XX, bb)
        ts[i] = bb[k_idx] / cr1(S)
    return beta[k_idx], se, G, float(np.mean(np.abs(ts) >= abs(t0)))


def design(d, y, fe):
    X = pd.get_dummies(d[[fe, "filing_year"]].astype(str), drop_first=True).astype(float)
    X.insert(0, "const", 1.0)
    X["T"] = (d["treated"] * d["post"]).astype(float)
    return X.to_numpy(), d[y].to_numpy(dtype=float), d["main_group"].to_numpy()


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["fresh3"] = (df["lag_days"] / 365.25 <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    n_groups = df["main_group"].nunique()
    n_treated_g = df[df.treated == 1]["main_group"].nunique()

    m = df[df["filing_date"] <= "2024-06-30"]
    pl = m.groupby(["patent_id", "cpc_class", "main_group", "filing_year", "treated", "post"])["fresh3"].mean().reset_index()
    l = df[df["lag_days"] <= 10 * 365.25]

    lines = ["# Item 12: inference at the CPC main-group level (133 clusters)", "",
             f"Own-class main groups: {n_groups} total, {n_treated_g} treated, {n_groups - n_treated_g} control. "
             "Treatment definition unchanged (the patent's own class); the cluster dimension and, in "
             "specification (ii), the fixed effects move to the main-group level. Wild cluster bootstrap: "
             "Webb weights, 9,999 draws, null imposed.", ""]
    lines.append("| outcome | FE | coef | CR1 SE (cluster = main group) | G | p (wild cluster bootstrap) | N |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for y, dat, label, scale, n in [
        ("fresh3", pl, "share <= 3y (pp)", 100, len(pl)),
        ("log_lag", l, "log lag (10y window)", 1, len(l)),
    ]:
        for fe, fel in [("cpc_class", "class FE"), ("main_group", "main-group FE")]:
            X, yv, g = design(dat, y, fe)
            b, se, G, p = wcb(X, yv, g)
            lines.append(f"| {label} | {fel} | {b*scale:+.3f} | {se*scale:.3f} | {G} | {p:.4f} | {n:,} |")
    lines.append("\nReference: class-level wild bootstrap p-values are 0.109 (share) and 0.115 (lag) with "
                 "G = 7, and 0.093 / 0.089 with G = 9 (v2 numbers).")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("written ->", OUT)


if __name__ == "__main__":
    main()
