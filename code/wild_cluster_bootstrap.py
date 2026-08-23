"""
Item 3a: wild cluster bootstrap inference with few clusters.

Threat (self-critique #4): seven CPC classes. Cluster-robust standard errors with so few
clusters over-reject. Clustering by class x year (as in the baseline) treats years within a
class as independent, which is optimistic if shocks persist within a class.

Method: restricted wild cluster bootstrap-t (Cameron, Gelbach & Miller 2008), clusters =
CPC class (G = 7), Webb six-point weights (recommended for G < 10), B = 9,999 draws,
null imposed (treated x post = 0) when generating bootstrap samples. Reported: the
bootstrap p-value for H0: treated x post = 0, next to the baseline class-x-year cluster p.
Also reported: p with clusters = class (G = 7) using the usual CR1 estimator, and a
cluster-by-class version of the baseline for comparison.

Outcomes: B. share <=3y (patent level, filings <= 2024-06-30); A. log lag (pair level, 10y).
Samples: all; firms only with assignee FE is not bootstrapped here (FE absorbed separately).
Output: ../results/item3a_wild_bootstrap_2026-08-22.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA = Path("../data/clean/lag_pairs.csv")
OUT = Path("../results/item3a_wild_bootstrap_2026-08-22.md")
B = 9999
RNG = np.random.default_rng(2026)
WEBB = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])


def design(d, y):
    X = pd.get_dummies(d[["cpc_class", "filing_year"]].astype(str), drop_first=True).astype(float)
    X.insert(0, "const", 1.0)
    X["T"] = (d["treated"] * d["post"]).astype(float)
    return X.to_numpy(), d[y].to_numpy(dtype=float), d["cpc_class"].to_numpy()


def wcb(X, y, g, k_idx):
    """Restricted wild cluster bootstrap-t using per-cluster sufficient statistics (fast)."""
    n, k = X.shape
    clusters = np.unique(g); G = len(clusters)
    XtX_inv = np.linalg.inv(X.T @ X)
    # unrestricted estimate and CR1 t
    beta = XtX_inv @ X.T @ y; u = y - X @ beta
    def cr1_from_scores(S):
        meat = S.T @ S
        V = XtX_inv @ meat @ XtX_inv * (G / (G - 1)) * ((n - 1) / (n - k))
        return np.sqrt(V[k_idx, k_idx])
    S0 = np.vstack([X[g == c].T @ u[g == c] for c in clusters])
    se = cr1_from_scores(S0); t0 = beta[k_idx] / se
    # restricted fit (H0: beta_k = 0)
    Xr = np.delete(X, k_idx, axis=1)
    br = np.linalg.lstsq(Xr, y, rcond=None)[0]; fit_r = Xr @ br; ur = y - fit_r
    # per-cluster sufficient statistics
    Xf = np.vstack([X[g == c].T @ fit_r[g == c] for c in clusters])        # G x k
    A = np.vstack([X[g == c].T @ ur[g == c] for c in clusters])            # G x k
    XX = np.stack([X[g == c].T @ X[g == c] for c in clusters])             # G x k x k
    ts = np.empty(B)
    for i in range(B):
        w = RNG.choice(WEBB, size=G)
        Xy = Xf.sum(0) + (w[:, None] * A).sum(0)
        bb = XtX_inv @ Xy
        S = Xf + w[:, None] * A - np.einsum("gij,j->gi", XX, bb)
        ts[i] = bb[k_idx] / cr1_from_scores(S)
    p = np.mean(np.abs(ts) >= abs(t0))
    return beta[k_idx], se, t0, p


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["age_y"] = df["lag_days"] / 365.25; df["fresh3"] = (df["age_y"] <= 3).astype(int); df["log_lag"] = np.log1p(df["lag_days"])
    lines = ["# Item 3a: wild cluster bootstrap (clusters = CPC class, G = 7, Webb weights, B = 9,999, null imposed)", ""]
    lines.append("| outcome | sample | coef | CR1 SE (cluster = class) | t | p (cluster = class, t-dist G-1) | p (wild cluster bootstrap) | N |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|")
    from scipy import stats
    # B: share, patent level, mature
    m = df[df["filing_date"] <= "2024-06-30"]
    pl = m.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post"])["fresh3"].mean().reset_index()
    X, y, g = design(pl, "fresh3"); k = X.shape[1] - 1
    b, se, t0, p = wcb(X, y, g, k)
    lines.append(f"| share <=3y (pp) | patent level, filings <= 2024-06-30 | {b*100:+.2f} | {se*100:.2f} | {t0:.2f} | {2*(1-stats.t.cdf(abs(t0), 6)):.4f} | {p:.4f} | {len(pl):,} |")
    # A: lag, pair level, 10y window (subsample pairs for speed: all pairs fine with numpy)
    l = df[df["lag_days"] <= 10 * 365.25]
    X, y, g = design(l, "log_lag"); k = X.shape[1] - 1
    b, se, t0, p = wcb(X, y, g, k)
    lines.append(f"| log lag | pair level, 10-year window | {b:+.3f} | {se:.3f} | {t0:.2f} | {2*(1-stats.t.cdf(abs(t0), 6)):.4f} | {p:.4f} | {len(l):,} |")
    lines.append("\nBaseline (cluster = class x year) p-values for comparison: share 0.0012; lag 0.0002.")
    OUT.write_text("\n".join(lines) + "\n"); print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
