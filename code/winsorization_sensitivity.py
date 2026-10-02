"""
Referee-anticipating robustness: how much does cleaning rule R3 drive the lag result?

R3 winsorizes lag_days at the 99th percentile within CPC class. The paper never showed
what happens under other choices, so a referee can ask whether the lag estimate is an
artifact of that one rule. This script answers it.

Method. lag_pairs_v2.csv.gz stores lag_days already clipped at p99, but it also stores
filing_date and pub_date, so the UNCLIPPED lag is recoverable exactly:

    raw_lag = filing_date - pub_date   (in days)

We recompute raw_lag, then re-apply R3 at four thresholds (none, p95, p99, p99.5) and
re-run the paper's Table 6 specifications on each.

Note on scope, stated up front so the result is read correctly: winsorizing the UPPER tail
cannot move the fresh-science share, because that outcome is an indicator for lag <= 3 years
and clipping only touches the longest lags. This robustness therefore bears on H1 (the
secondary outcome) alone, never on H2 (the primary one). The script prints a check that
confirms this rather than asserting it.

Run from pkg/code:
    python3 winsorization_sensitivity.py
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = "../data/clean/lag_pairs_v2.csv.gz"
TEN_YEARS = 3652.5
EIGHT_YEARS = 2922.0
RULES = [("no winsorization", None), ("p95", 0.95), ("p99 (paper)", 0.99), ("p99.5", 0.995)]


def did(df, dep="log_lag"):
    d = df.copy()
    d["cluster"] = d["cpc_class"].astype(str) + "_" + d["filing_year"].astype(str)
    m = smf.ols(f"{dep} ~ treated:post + C(cpc_class) + C(filing_year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["cluster"]})
    term = [t for t in m.params.index if "treated" in t and "post" in t][0]
    return m.params[term], m.bse[term], m.pvalues[term], len(d)


def apply_r3(df, q):
    d = df.copy()
    if q is None:
        d["lag_use"] = d["raw_lag"]
    else:
        cap = d.groupby("cpc_class")["raw_lag"].transform(lambda s: s.quantile(q))
        d["lag_use"] = d["raw_lag"].clip(upper=cap)
    d["log_lag"] = np.log1p(d["lag_use"])
    return d


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date", "pub_date"])
    df["raw_lag"] = (df["filing_date"] - df["pub_date"]).dt.days
    df = df.dropna(subset=["raw_lag"])
    df = df[df["raw_lag"] >= 0]

    # sanity: the stored lag_days must equal raw_lag clipped at the class p99
    chk = apply_r3(df, 0.99)
    same = np.isclose(chk["lag_use"], df["lag_days"], atol=1.0).mean()
    print(f"reconstruction check: stored lag_days matches recomputed p99 clip for "
          f"{same*100:.2f} percent of pairs\n")

    print(f"{'R3 rule':<20} {'spec':<34} {'N':>9} {'Treated x Post':>16} {'SE':>8} {'p':>10}")
    print("-" * 102)
    rows = []
    for name, q in RULES:
        d = apply_r3(df, q)
        specs = [
            ("1 none", d),
            ("2 filings <= 2024-12-31", d[d["filing_date"] <= "2024-12-31"]),
            ("3 uniform 10-year window", d[d["lag_use"] <= TEN_YEARS]),
            ("4 specs 2 and 3", d[(d["filing_date"] <= "2024-12-31") & (d["lag_use"] <= TEN_YEARS)]),
            ("5 <= 2024-06-30, 8-year window",
             d[(d["filing_date"] <= "2024-06-30") & (d["lag_use"] <= EIGHT_YEARS)]),
        ]
        for slabel, sd in specs:
            b, se, p, n = did(sd)
            print(f"{name:<20} {slabel:<34} {n:>9,} {b:>+16.4f} {se:>8.4f} {p:>10.4g}")
            rows.append((name, slabel, n, b, se, p))
        print()

    # the primary outcome cannot move: show it rather than claim it
    print("Check that the primary outcome is untouched by R3 "
          "(fresh-science indicator, lag <= 3 years):")
    for name, q in RULES:
        d = apply_r3(df, q)
        share = (d["lag_use"] <= 3 * 365.25).mean()
        print(f"  {name:<20} share of pairs 3 years old or younger: {share*100:.4f} percent")

    pd.DataFrame(rows, columns=["rule", "spec", "N", "coef", "se", "p"]).to_csv(
        "../../out/winsorization_sensitivity.csv", index=False)
    print("\nwritten -> out/winsorization_sensitivity.csv")


if __name__ == "__main__":
    main()
