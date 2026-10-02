"""
Figure 1 for the camera-ready (Reviewer 1 point 4: "no event-study figure").
(a) event study of the fresh-science share, treated x filing year relative to 2022, 95% CI;
(b) share of citation pairs by cited publication year, treated classes, pre vs post filings.
Mature sample (filings through 2024-06-30); half-open age windows. Palette validated with the
dataviz validator: 0B6E99 / C77B18 pass all checks in light mode.
"""
from pathlib import Path
import numpy as np, pandas as pd, statsmodels.formula.api as smf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent              # run from anywhere
U = HERE.parent / "data/clean"
OUT = HERE.parent.parent / "camera-ready/final_2026-10-09"   # figure1.pdf/.png + the two csv files
if not OUT.is_dir():                     # inside the public replication repository
    OUT = HERE.parent / "results"
BLUE, AMBER, INK, MUTED, GRID = "#0B6E99", "#C77B18", "#1F2933", "#5F6B7A", "#E3E7EC"

d = pd.read_csv(U / "lag_pairs_v2.csv.gz", parse_dates=["filing_date"])
d = d[d.filing_date <= "2024-06-30"].copy()
d["age"] = d.lag_days / 365.25
d["fresh"] = ((d.age >= 0) & (d.age < 3)).astype(float)
pat = d.groupby(["patent_id", "cpc_class", "filing_year", "treated"])["fresh"].mean().reset_index()
pat["fresh"] *= 100
pat["cl"] = pat.cpc_class + "_" + pat.filing_year.astype(str)
yrs = [2018, 2019, 2020, 2021, 2023, 2024]
for y in yrs:
    pat[f"t{y}"] = ((pat.filing_year == y) & (pat.treated == 1)).astype(float)
m = smf.ols("fresh ~ " + " + ".join(f"t{y}" for y in yrs) + " + C(cpc_class) + C(filing_year)",
            data=pat).fit(cov_type="cluster", cov_kwds={"groups": pat.cl})
es = pd.DataFrame({"year": yrs + [2022],
                   "b": [m.params[f"t{y}"] for y in yrs] + [0.0],
                   "se": [m.bse[f"t{y}"] for y in yrs] + [0.0]}).sort_values("year")
es.to_csv(OUT / "fig1a_event_study.csv", index=False)

tr = d[d.treated == 1]
dist = (tr.groupby(["post", "pub_year"]).size()
          .groupby(level=0).transform(lambda s: s / s.sum() * 100).rename("share").reset_index())
dist = dist[(dist.pub_year >= 2006) & (dist.pub_year <= 2024)]
dist.to_csv(OUT / "fig1b_cited_years.csv", index=False)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": MUTED,
                     "axes.labelcolor": INK, "xtick.color": MUTED, "ytick.color": MUTED,
                     "axes.linewidth": 0.6})
fig, (a, b) = plt.subplots(1, 2, figsize=(6.3, 2.55), gridspec_kw={"wspace": 0.32})

# (a) event study
a.axvspan(2022.5, 2024.5, color="#F3EEE6", zorder=0, lw=0)
a.axhline(0, color=MUTED, lw=0.7, ls="--", zorder=1)
a.grid(axis="y", color=GRID, lw=0.6); a.set_axisbelow(True)
a.errorbar(es.year, es.b, yerr=1.96 * es.se, fmt="o", color=BLUE, ecolor=BLUE,
           elinewidth=1.4, capsize=2.5, ms=4.5, zorder=3)
for x, y in zip(es.year, es.b):
    if x != 2022:
        a.annotate(f"{y:+.1f}", (x, y), xytext=(5, 0), textcoords="offset points",
                   fontsize=7, color=INK, va="center")
a.text(2023.5, a.get_ylim()[1] * 0.92 if a.get_ylim()[1] > 0 else 5, "post-2023", ha="center",
       fontsize=7.5, color=MUTED)
a.set_xticks(range(2018, 2025)); a.set_xlim(2017.5, 2024.5)
plt.setp(a.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
a.set_ylabel("Treated × year, pp (ref. 2022)")
a.set_title("(a) Event study, fresh-science share", fontsize=8.5, color=INK, loc="left")
for s in ("top", "right"): a.spines[s].set_visible(False)

# (b) cited publication years
b.axvspan(2014.5, 2019.5, color="#EEF3F7", zorder=0, lw=0)
b.grid(axis="y", color=GRID, lw=0.6); b.set_axisbelow(True)
for per, col, lab in [(0, BLUE, "Filed 2018–2022"), (1, AMBER, "Filed 2023–mid 2024")]:
    s = dist[dist.post == per]
    b.plot(s.pub_year, s.share, color=col, lw=2, label=lab, zorder=3)
b.set_ylim(0, 8.2)
b.text(2017, 8.05, "2015–2019", ha="center", va="top", fontsize=7.5, color=MUTED)
b.set_xlabel("Publication year of cited paper")
b.set_ylabel("Share of citation pairs, %")
b.set_title("(b) Cited publication years, treated classes", fontsize=8.5, color=INK, loc="left")
b.legend(frameon=False, fontsize=7.5, loc="lower left")
b.set_xticks([2006, 2010, 2014, 2018, 2022])
for s in ("top", "right"): b.spines[s].set_visible(False)

fig.savefig(OUT / "figure1.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure1.png", dpi=220, bbox_inches="tight")
print(es.round(2).to_string(index=False))
top = dist[dist.post == 1].nlargest(5, "share")
print("top cited years post:", top[["pub_year", "share"]].round(1).values.tolist())
