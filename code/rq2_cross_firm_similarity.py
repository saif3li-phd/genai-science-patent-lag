"""
RQ2: cross-firm semantic similarity of patent abstracts before and after 2023.

Question: do patents of DIFFERENT firms in GenAI-exposed classes become more similar to
each other after 2023 (semantic homogenisation), relative to mechanical control classes?

Data: data/abstracts_sample.csv.gz, a fixed-seed sample of up to 1,500 patents per class
and filing year (rule D1 exact-duplicate removal applied first), all seven classes,
2018-2025, with applicants. 60,252 abstracts.

Text representation (declared): TF-IDF on title + abstract, unigrams and bigrams, English
stop words, min_df = 5, sublinear tf, L2-normalised; fitted once on the full corpus so the
vocabulary is identical for all class-years. Cosine similarity between L2 vectors.
(Transformer embeddings such as SciBERT/SPECTER are the planned refinement; they need model
files that are not reachable from this environment. TF-IDF cosine is the standard baseline
in the patent text-similarity literature and is fully reproducible.)

Measures, per class x filing year (firm patents only, first-listed applicant):
  M1 cross-firm similarity : mean cosine over random pairs of patents from DIFFERENT firms
                             (up to 20,000 pairs per cell)
  M2 nearest-neighbour     : mean over patents of the max cosine to any patent of a
                             different firm in the same cell (convergence on the frontier)
  M3 within-firm similarity: mean cosine over pairs from the SAME firm (baseline control)
DiD on cell means: M ~ treated x post + class FE + year FE, cells weighted equally, SE
clustered by class. Reading rule (fixed): homogenisation = positive treated x post on M1 and
M2 that is not matched by M3.
Output: ../results/rq2_similarity_2026-08-21.md and .png
"""

import re
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA = Path("../data/abstracts_sample.csv.gz")
TYPES = Path("../data/clean/patent_assignee_type.csv")
OUT = Path("../results/rq2_similarity_2026-08-21.md")
PNG = Path("../results/rq2_similarity_2026-08-21.png")
TREATED = {"G06N", "G16B", "G16C", "C40B"}
RNG = np.random.default_rng(42)
FIRM = r"\b(INC|LLC|LTD|CORP|CORPORATION|CO|GMBH|AG|SA|SAS|BV|NV|PLC|KK|KABUSHIKI KAISHA|HOLDINGS|TECHNOLOGIES|TECHNOLOGY|LIMITED|PTY|OY|AB|SRL|SPA|LP|LLP|COMPANY|GROUP|LABS|SYSTEMS|SOLUTIONS|NETWORKS|ELECTRONICS|PHARMACEUTICALS|THERAPEUTICS|BIOSCIENCES|INDUSTRIES)\b"
UNI = r"\b(UNIV|UNIVERSITY|COLLEGE|INSTITUTE|INST|SCHOOL|ACADEMY|HOSPITAL|FOUNDATION|RESEARCH|CNRS|CSIC|FRAUNHOFER|RIKEN|KAIST|ETRI)\b"


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", str(s).upper())).strip()


def main():
    d = pd.read_csv(DATA, dtype=str)
    d["firm"] = d["Applicants"].fillna("").str.split(";;").str[0].map(norm)
    d = d[d["firm"].str.contains(FIRM, regex=True) & ~d["firm"].str.contains(UNI, regex=True)]
    d["year"] = d["year"].astype(int)
    d["text"] = d["Title"].fillna("") + ". " + d["Abstract"].fillna("")
    d = d.reset_index(drop=True)
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=5, max_df=0.5, stop_words="english", sublinear_tf=True, dtype=np.float32)
    X = vec.fit_transform(d["text"])
    rows = []
    for (cls, yr), g in d.groupby(["cls", "year"]):
        idx = g.index.to_numpy(); firms = g["firm"].to_numpy()
        if len(idx) < 30:
            continue
        Xg = X[idx]
        S = (Xg @ Xg.T).toarray(); np.fill_diagonal(S, np.nan)
        same = firms[:, None] == firms[None, :]
        cross = S.copy(); cross[same] = np.nan
        within = S.copy(); within[~same] = np.nan
        iu = np.triu_indices(len(idx), 1)
        cv = cross[iu]; cv = cv[~np.isnan(cv)]
        wv = within[iu]; wv = wv[~np.isnan(wv)]
        if len(cv) > 20000:
            cv = RNG.choice(cv, 20000, replace=False)
        m1 = float(cv.mean())
        m2 = float(np.nanmean(np.nanmax(cross, axis=1)))
        m3 = float(wv.mean()) if len(wv) >= 30 else np.nan
        rows.append(dict(cls=cls, year=yr, n=len(idx), n_firms=g["firm"].nunique(), M1=m1, M2=m2, M3=m3))
    cells = pd.DataFrame(rows)
    cells["treated"] = cells["cls"].isin(TREATED).astype(int)
    cells["post"] = (cells["year"] >= 2023).astype(int)

    lines = ["# RQ2: cross-firm similarity of patent abstracts (TF-IDF cosine)", "",
             f"Firm patents in the fixed-seed sample: {len(d):,}; vocabulary {len(vec.vocabulary_):,} terms. "
             "Cells = class x filing year (min 30 patents). M1 = mean cross-firm cosine (random pairs, <=20k per cell); "
             "M2 = mean nearest cross-firm neighbour cosine; M3 = mean within-firm cosine.", ""]
    lines.append("## Cell means (treated classes pooled vs control classes pooled, unweighted)\n")
    lines.append("| group | period | M1 cross-firm | M2 nearest neighbour | M3 within-firm | cells |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for t, tl in [(1, "treated"), (0, "control")]:
        for p, pl in [(0, "2018-2022"), (1, "2023-2025")]:
            c = cells[(cells.treated == t) & (cells.post == p)]
            lines.append(f"| {tl} | {pl} | {c.M1.mean():.4f} | {c.M2.mean():.4f} | {c.M3.mean():.4f} | {len(c)} |")

    lines.append("\n## Difference-in-differences on cell means (class FE + year FE, SE clustered by class)\n")
    lines.append("| measure | treated x post | SE | p | cells |")
    lines.append("|---|---:|---:|---:|---:|")
    for m in ["M1", "M2", "M3"]:
        c = cells.dropna(subset=[m])
        mod = smf.ols(f"{m} ~ treated:post + C(cls) + C(year)", data=c).fit(cov_type="cluster", cov_kwds={"groups": c["cls"]})
        lines.append(f"| {m} | {mod.params['treated:post']:+.4f} | {mod.bse['treated:post']:.4f} | {mod.pvalues['treated:post']:.3f} | {len(c)} |")
    # excluding 2025 (incomplete publication)
    c25 = cells[cells.year <= 2024]
    lines.append("\nExcluding 2025 filings:\n")
    lines.append("| measure | treated x post | SE | p |")
    lines.append("|---|---:|---:|---:|")
    for m in ["M1", "M2", "M3"]:
        c = c25.dropna(subset=[m])
        mod = smf.ols(f"{m} ~ treated:post + C(cls) + C(year)", data=c).fit(cov_type="cluster", cov_kwds={"groups": c["cls"]})
        lines.append(f"| {m} | {mod.params['treated:post']:+.4f} | {mod.bse['treated:post']:.4f} | {mod.pvalues['treated:post']:.3f} |")

    lines.append("\n## Per class and year: M1 cross-firm similarity\n")
    piv = cells.pivot(index="cls", columns="year", values="M1")
    lines.append("| class | " + " | ".join(str(y) for y in piv.columns) + " |")
    lines.append("|---|" + "---:|" * len(piv.columns))
    for cls, r in piv.iterrows():
        lines.append(f"| {cls} | " + " | ".join(f"{v:.4f}" if pd.notna(v) else "" for v in r.values) + " |")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, m, lab in zip(axes, ["M1", "M2"], ["M1 cross-firm mean cosine", "M2 nearest cross-firm neighbour"]):
        for t, col, tl in [(1, "#c0392b", "treated"), (0, "#2c3e50", "control")]:
            s = cells[cells.treated == t].groupby("year")[m].mean()
            ax.plot(s.index, s.values, "o-", color=col, label=tl)
        ax.axvline(2022.5, ls="--", color="grey", lw=0.8); ax.set_title(lab); ax.legend()
    fig.tight_layout(); fig.savefig(PNG, dpi=200)
    cells.to_csv(OUT.with_suffix(".cells.csv"), index=False)
    OUT.write_text("\n".join(lines) + "\n"); print("\n".join(lines)); print("written ->", OUT)


if __name__ == "__main__":
    main()
