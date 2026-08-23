"""
Item 4: dose gradient inside G06N.

Threat (self-critique #2): 2023 brought shocks other than GenAI to the AI classes (tech
funding contraction, layoffs, USPTO guidance). If the effect is GenAI-specific, it should
be strongest in the G06N subgroups closest to generative modelling and weakest in G06N
subgroups with no generative channel.

Dose definition (fixed before running, from the official CPC scheme):
  HIGH  = patent carries any G06N3/* (neural networks, incl. 3/045 generative networks,
          3/0455 autoencoders, 3/0475 GANs, 3/08 learning methods) or G06N20/* (machine learning)
  LOW   = G06N patent with none of the above (G06N5 knowledge-based, G06N7 probabilistic,
          G06N10 quantum, G06N99 other)
  Within HIGH we also flag GENERATIVE = any G06N3/045, 3/0455, 3/0475 code (codes in force
  since the 2023 CPC revision; patents filed earlier carry them only if reclassified).

Estimates (baseline specs):
  A. log lag, pair level, 10-year window; B. share <=3y, patent level, filings <= 2024-06-30
  (1) HIGH vs mechanical controls, (2) LOW vs mechanical controls, (3) HIGH vs LOW inside G06N
  (4) GENERATIVE vs other-HIGH inside G06N (descriptive; code timing caveat).
Output: ../results/item4_dose_gradient_2026-08-21.md
"""

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path("../data/clean/lag_pairs.csv")
CPC = Path("../data/g06n_cpc.csv.gz")
OUT = Path("../results/item4_dose_gradient_2026-08-21.md")


def fit(d, y, treat_col, level):
    d = d.copy()
    d["T"] = d[treat_col].astype(int)
    if level == "pair":
        d = d[d["lag_days"] <= 10 * 365.25]
        m = smf.ols(f"{y} ~ T:post + C(cpc_class) + C(filing_year)", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["cluster"]})
        return m.params["T:post"], m.bse["T:post"], m.pvalues["T:post"], int(m.nobs)
    d = d[d["filing_date"] <= "2024-06-30"]
    pl = d.groupby(["patent_id", "cpc_class", "filing_year", "T", "post", "cluster"])[y].mean().reset_index()
    m = smf.ols(f"{y} ~ T:post + C(cpc_class) + C(filing_year)", data=pl).fit(
        cov_type="cluster", cov_kwds={"groups": pl["cluster"]})
    return m.params["T:post"] * 100, m.bse["T:post"] * 100, m.pvalues["T:post"], int(m.nobs)


def main():
    df = pd.read_csv(DATA, parse_dates=["filing_date"])
    df["age_y"] = df["lag_days"] / 365.25
    df["fresh3"] = (df["age_y"] <= 3).astype(int)
    df["log_lag"] = np.log1p(df["lag_days"])
    cpc = pd.read_csv(CPC, dtype=str).rename(columns={"Lens ID": "patent_id", "CPC Classifications": "cpc"})
    cpc["cpc"] = cpc["cpc"].fillna("")
    cpc["high"] = cpc["cpc"].str.contains(r"G06N3/|G06N20/", regex=True)
    cpc["gen"] = cpc["cpc"].str.contains(r"G06N3/045\b|G06N3/0455|G06N3/0475", regex=True)
    df = df.merge(cpc[["patent_id", "high", "gen"]], on="patent_id", how="left")
    g = df[df["cpc_class"] == "G06N"].copy()
    ctrl = df[df["treated"] == 0].copy()
    for d in (g, ctrl):
        d["cluster"] = d["cpc_class"] + "_" + d["filing_year"].astype(str)
    g["high"] = g["high"].fillna(False).astype(bool); g["gen"] = g["gen"].fillna(False).astype(bool)
    # sub-cluster inside G06N so class FE and clusters distinguish subgroups
    g["cpc_class"] = np.where(g["high"], "G06N_high", "G06N_low")
    g["cluster"] = g["cpc_class"] + "_" + g["filing_year"].astype(str)

    lines = ["# Item 4: dose gradient inside G06N", "",
             "HIGH = any G06N3/* or G06N20/* code; LOW = G06N patent with neither; GENERATIVE = any "
             "G06N3/045, 3/0455, 3/0475 code (post-2023 CPC codes; timing caveat). Baseline specs: "
             "A log lag, pair level, 10-year window; B share <=3y, patent level, filings <= 2024-06-30; "
             "class/subgroup FE + filing-year FE; SE clustered by (sub)class x year.", ""]
    pats = g.drop_duplicates("patent_id")
    lines.append("## G06N patents with citations, by subgroup\n")
    lines.append("| subgroup | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    for lab, mask in [("HIGH (G06N3/G06N20)", pats["high"]), ("LOW (other G06N)", ~pats["high"]), ("GENERATIVE codes", pats["gen"])]:
        lines.append(f"| {lab} | {int((mask & (pats['post']==0)).sum()):,} | {int((mask & (pats['post']==1)).sum()):,} |")

    comps = [
        ("(1) HIGH vs mechanical controls", pd.concat([g[g["high"]], ctrl]), "treated"),
        ("(2) LOW vs mechanical controls", pd.concat([g[~g["high"]], ctrl]), "treated"),
        ("(3) HIGH vs LOW inside G06N", g, "high"),
        ("(4) GENERATIVE vs other HIGH inside G06N", g[g["high"]].assign(cpc_class=lambda x: np.where(x["gen"], "G06N_gen", "G06N_high")).assign(cluster=lambda x: x["cpc_class"] + "_" + x["filing_year"].astype(str)), "gen"),
    ]
    for y, lab, level in [("log_lag", "A. log lag (10-year window), treated x post", "pair"),
                          ("fresh3", "B. share <=3y (pp), treated x post", "patent")]:
        lines.append(f"\n## {lab}\n")
        lines.append("| comparison | N | coef | SE | p |")
        lines.append("|---|---:|---:|---:|---:|")
        for name, d, tcol in comps:
            b, se, p, n = fit(d, y, tcol, level)
            fmt = "+.3f" if level == "pair" else "+.2f"
            lines.append(f"| {name} | {n:,} | {b:{fmt}} | {se:{'.3f' if level=='pair' else '.2f'}} | {p:.4f} |")

    # raw shares
    m = g[g["filing_date"] <= "2024-06-30"]
    lines.append("\n## Raw citation-weighted share <=3y inside G06N (%)\n")
    lines.append("| subgroup | pre-2023 | post-2023 |")
    lines.append("|---|---:|---:|")
    for lab, mask in [("HIGH", m["high"]), ("LOW", ~m["high"]), ("GENERATIVE", m["gen"])]:
        s = m[mask].groupby("post")["fresh3"].mean() * 100
        lines.append(f"| {lab} | {s.get(0, float('nan')):.1f} | {s.get(1, float('nan')):.1f} |")
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
