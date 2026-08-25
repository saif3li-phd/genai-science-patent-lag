"""
Revision plan item 4: instrument versus subject matter.

Threat: patents in treated classes may cite older science not because firms changed how
they absorb science (the instrument channel) but because the subject of patenting itself
shifted to generative models, which build on 2015-2019 deep-learning classics (the
subject-matter channel).

Test, reading rule fixed BEFORE running: re-estimate the fresh-science share DiD with
GENERATIVE-coded G06N patents (any of G06N3/045, 3/0455, 3/0475) excluded from
the treated group. The behavioral interpretation is supported if the coefficient remains
negative, significant, and of broadly comparable magnitude; if it collapses toward zero,
the claim is reframed as a shift in the direction of invention.

Estimates (v2 data, spec identical to the baseline: patent level, filings <= 2024-06-30,
class FE + filing-year FE, SE clustered class x year):
  (0) baseline, all treated (reference)
  (1) treated excluding GENERATIVE-coded G06N patents
  (2) treated excluding ALL G06N3/G06N20 (HIGH) patents, i.e. low-exposure G06N plus
      the three application classes
  (3) application classes only (G16B, G16C, C40B) vs mechanical controls
  (4) within G06N: non-generative HIGH vs mechanical controls
Lag versions (pair level, 10-year window) reported for the same samples.
Output: ../results/item11_instrument_subject_2026-08-24.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs_v2.csv.gz")
CPC = Path("../data/g06n_cpc.csv.gz")
OUT = Path("../results/item11_instrument_subject_2026-08-24.md")
GEN_PAT = r"G06N3/045\b|G06N3/0455|G06N3/0475"
HIGH_PAT = r"G06N3|G06N20"


def did(d, y, level):
    d = d.copy()
    d["cluster"] = d["cpc_class"] + "_" + d["filing_year"].astype(str)
    if level == "patent":
        d = d[d["filing_date"] <= "2024-06-30"]
        pl = d.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post", "cluster"])[y].mean().reset_index()
        scale = 100
    else:
        pl = d[d["lag_days"] <= 10 * 365.25]
        scale = 1
    m = smf.ols(f"{y} ~ treated:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    return m.params["treated:post"] * scale, m.bse["treated:post"] * scale, m.pvalues["treated:post"], int(pl["patent_id"].nunique() if level == "patent" else m.nobs)


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["fresh3"] = (df["lag_days"] / 365.25 <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    cpc = pd.read_csv(CPC, dtype=str).rename(columns={"Lens ID": "patent_id", "CPC Classifications": "codes"})
    cpc["generative"] = cpc["codes"].str.contains(GEN_PAT, regex=True, na=False)
    cpc["high"] = cpc["codes"].str.contains(HIGH_PAT, regex=True, na=False)
    df = df.merge(cpc[["patent_id", "generative", "high"]], on="patent_id", how="left")
    df["generative"] = df["generative"].fillna(False).astype(bool)
    df["high"] = df["high"].fillna(False).astype(bool)

    g06n = df["cpc_class"] == "G06N"
    n_gen = df[g06n & df["generative"]]["patent_id"].nunique()
    n_g06n = df[g06n]["patent_id"].nunique()

    samples = [
        ("(0) baseline, all treated", df),
        ("(1) excluding GENERATIVE G06N patents", df[~(g06n & df["generative"])]),
        ("(2) excluding all HIGH G06N patents", df[~(g06n & df["high"])]),
        ("(3) application classes only (G16B, G16C, C40B)", df[df["cpc_class"].isin(["G16B", "G16C", "C40B", "F16B", "F16H", "B65D"])]),
        ("(4) non-generative HIGH G06N vs mechanical", df[(g06n & df["high"] & ~df["generative"]) | (df["treated"] == 0)]),
    ]

    lines = ["# Item 11: instrument versus subject matter (excluding generative-coded patents)", "",
             "Reading rule fixed before running: the behavioral interpretation is supported if the "
             "fresh-science DiD excluding GENERATIVE patents stays negative, significant, and of "
             "broadly comparable magnitude; a collapse toward zero reframes the claim as a shift in "
             "the direction of invention.", "",
             f"GENERATIVE-coded G06N patents (current-scheme codes G06N3/045, 3/0455 and 3/0475): {n_gen:,} of "
             f"{n_g06n:,} G06N patents with citations ({n_gen/n_g06n*100:.0f} percent).", ""]
    lines.append("## B. Share <= 3y (pp), patent level, filings <= 2024-06-30\n")
    lines.append("| sample | DiD | SE | p | N patents |")
    lines.append("|---|---:|---:|---:|---:|")
    for lab, d in samples:
        b, se, p, n = did(d, "fresh3", "patent")
        lines.append(f"| {lab} | {b:+.2f} | {se:.2f} | {p:.4f} | {n:,} |")
    lines.append("\n## A. Log(1 + lag), pair level, 10-year window\n")
    lines.append("| sample | treated x post | SE | p | N pairs |")
    lines.append("|---|---:|---:|---:|---:|")
    for lab, d in samples:
        b, se, p, n = did(d, "log_lag", "pair")
        lines.append(f"| {lab} | {b:+.3f} | {se:.3f} | {p:.4f} | {n:,} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
