"""
Is the attribution to "generative-coded" patents an artefact of the 2023 CPC scheme change?
(Reviewer 1, point 3, AI4SciSci 2026.)

FACTS ABOUT THE CODES, from the USPTO CPC scheme for G06N (checked 2026-10-02):
  G06N 3/04    Architecture, e.g. interconnection topology                     [2023-01]
  G06N 3/045   Combinations of networks                                        [2023-01]
  G06N 3/0455  Auto-encoder networks; Encoder-decoder networks                 [2023-01]
  G06N 3/0475  Generative networks                                             [2023-01]
The whole G06N 3/04 subtree was reorganised in scheme version 2023-01, the same month our
treatment period begins. Lens reports current-scheme codes for every patent, so codes on patents
filed before 2023 exist only through retroactive reclassification.

The paper's GENERATIVE flag has been "any of 3/045, 3/0455, 3/0475". Only 3/0475 is titled
"Generative networks". 3/045 is "Combinations of networks", which is broader. This script reports
each code separately so the label can be made to say what it actually measures.

THREE TESTS, reading rules declared before the run:
  A. Labelling continuity. Share of G06N patents carrying each code, by filing year. If the
     reclassification failed to reach older patents, pre-2023 shares would be near zero and jump
     at 2023. A smooth series is evidence against a labelling discontinuity at the treatment date.
  B. Code-by-code attribution. The within-G06N contrast (code vs other HIGH, share <=3y) for each
     code separately. If the effect is real for "generative" in the narrow sense, 3/0475 alone
     should carry it.
  C. Scheme-stable attribution. HIGH (any G06N3/* or G06N20/*) is defined at main-group level,
     which the 2023-01 reorganisation did not change. If HIGH vs LOW and HIGH vs controls show the
     same pattern, the attribution does not depend on the new subgroups.

INFERENCE NOTE, stated here because it is easy to get wrong. In the within-G06N contrasts the flag
is a patent attribute, but the identifying comparison is between TWO code-defined groups over time.
Clustering by group x year therefore leaves two groups, the same small-group problem as the class
design. We report firm-clustered errors as well (many clusters, robust to firm-level shocks) and
state plainly that neither protects against a shock common to all patents in one code group.
"""
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.formula.api as smf

HERE = Path(__file__).resolve().parent
U = HERE.parent / "data"
OUT = HERE.parent / "results/cpc_scheme_robustness_2026-10-02.md"
MATURE = "2024-06-30"

df = pd.read_csv(U / "clean/lag_pairs_v2.csv.gz", parse_dates=["filing_date"])
df = df[df.filing_date <= MATURE].copy()
df["age"] = df.lag_days / 365.25
df["fresh"] = ((df.age >= 0) & (df.age < 3)).astype(float)   # half-open, see R1.4
pat = (df.groupby(["patent_id", "cpc_class", "filing_year", "treated", "post"])
         .agg(fresh=("fresh", "mean"), assignee=("assignee", "first")).reset_index())
pat["fresh"] *= 100

cpc = pd.read_csv(U / "g06n_cpc.csv.gz", dtype=str).rename(
    columns={"Lens ID": "patent_id", "CPC Classifications": "cpc"})
cpc["cpc"] = cpc["cpc"].fillna("")
flags = {
    "c045":  r"G06N3/045(?!\d)",
    "c0455": r"G06N3/0455",
    "c0475": r"G06N3/0475",
    "gen":   r"G06N3/045(?!\d)|G06N3/0455|G06N3/0475",
    "fam04": r"G06N3/04",
    "high":  r"G06N3/|G06N20/",
}
for k, rx in flags.items():
    cpc[k] = cpc["cpc"].str.contains(rx, regex=True)
cpc = cpc.drop_duplicates("patent_id")
g = pat[pat.cpc_class == "G06N"].merge(cpc.drop(columns="cpc"), on="patent_id", how="left")
for k in flags:
    g[k] = g[k].fillna(False).astype(bool)
ctrl = pat[pat.treated == 0].copy()
for k in flags:
    ctrl[k] = False

L = ["# CPC scheme-change robustness (Reviewer 1, point 3)", "",
     f"Mature sample, filings through {MATURE}. G06N patents with at least one dated citation: "
     f"{len(g):,}. Fresh share uses half-open age [0, 3).", ""]

# ---------------------------------------------------------------- A
L += ["## A. Share of G06N patents carrying each code, by filing year (%)", "",
      "| filing year | N | 3/045 combinations | 3/0455 encoder-decoder | 3/0475 generative | any of the three | any 3/04* | HIGH |",
      "|---|---:|---:|---:|---:|---:|---:|---:|"]
for y, s in g.groupby("filing_year"):
    L.append(f"| {y} | {len(s):,} | " + " | ".join(f"{s[k].mean()*100:.1f}" for k in
             ["c045", "c0455", "c0475", "gen", "fam04", "high"]) + " |")
L.append("")

def did(d, flag, cluster, fe="grp"):
    d = d.copy()
    d["T"] = d[flag].astype(int)
    d["grp"] = np.where(d["T"] == 1, "in", "out")
    if fe != "grp":
        d["grp"] = d[fe]
    if cluster == "group_year":
        d["cl"] = d["grp"] + "_" + d["filing_year"].astype(str)
    else:
        d["cl"] = d["assignee"].fillna("NA_" + d["patent_id"])
    m = smf.ols("fresh ~ T:post + C(grp) + C(filing_year)", data=d).fit(
        cov_type="cluster", cov_kwds={"groups": d["cl"]})
    return m.params["T:post"], m.bse["T:post"], m.pvalues["T:post"], int(m.nobs), d["cl"].nunique()

# ---------------------------------------------------------------- B
hi = g[g.high]
L += ["## B. Within HIGH G06N: each code against the rest of HIGH (share <=3y, pp)", "",
      "| code group | patents with code (pre / post) | DiD | SE grp x yr | p | SE firm | p firm | firm clusters |",
      "|---|---|---:|---:|---:|---:|---:|---:|"]
for lab, k in [("any of the three (published GENERATIVE)", "gen"),
               ("3/045 combinations of networks only", "c045"),
               ("3/0455 encoder-decoder only", "c0455"),
               ("3/0475 generative networks only", "c0475")]:
    npre = int(hi[(hi[k]) & (hi.post == 0)].shape[0]); npost = int(hi[(hi[k]) & (hi.post == 1)].shape[0])
    b, se, p, n, _ = did(hi, k, "group_year")
    bf, sef, pf, _, ncl = did(hi, k, "firm")
    L.append(f"| {lab} | {npre:,} / {npost:,} | {b:+.2f} | {se:.2f} | {p:.4f} | {sef:.2f} | {pf:.4f} | {ncl:,} |")
L.append("")

# ---------------------------------------------------------------- C
L += ["## C. Scheme-stable definition: HIGH (main groups G06N3, G06N20)", "",
      "| contrast | DiD | SE class x yr | p | SE firm | p firm | N |", "|---|---:|---:|---:|---:|---:|---:|"]
gg = g.copy(); gg["fe"] = np.where(gg.high, "G06N_high", "G06N_low")
cc = ctrl.copy(); cc["fe"] = cc["cpc_class"]
for lab, d, k in [("HIGH G06N vs mechanical controls", pd.concat([gg[gg.high].assign(fe="G06N"), cc]), "high"),
                  ("LOW G06N vs mechanical controls", pd.concat([gg[~gg.high].assign(low=True, fe="G06N"), cc.assign(low=False)]), "low"),
                  ("HIGH vs LOW inside G06N", gg, "high")]:
    # cluster by class-or-subgroup x year, exactly as the published specification
    d = d.copy(); d["grp_cl"] = d["fe"] + "_" + d["filing_year"].astype(str)
    dd = d.copy(); dd["T"] = dd[k].astype(int)
    m = smf.ols("fresh ~ T:post + C(fe) + C(filing_year)", data=dd).fit(cov_type="cluster", cov_kwds={"groups": dd["grp_cl"]})
    b, se, p, n = m.params["T:post"], m.bse["T:post"], m.pvalues["T:post"], int(m.nobs)
    dd["cl"] = dd["assignee"].fillna("NA_" + dd["patent_id"])
    mf = smf.ols("fresh ~ T:post + C(fe) + C(filing_year)", data=dd).fit(cov_type="cluster", cov_kwds={"groups": dd["cl"]})
    bf, sef, pf = mf.params["T:post"], mf.bse["T:post"], mf.pvalues["T:post"]
    L.append(f"| {lab} | {b:+.2f} | {se:.2f} | {p:.4f} | {sef:.2f} | {pf:.4f} | {n:,} |")
L.append("")

OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
