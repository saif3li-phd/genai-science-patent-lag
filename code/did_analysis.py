"""
Steps 6-7: Difference-in-Differences estimation and placebo test.

Model (main):
  log(1 + lag_days) = b1 * (treated x post) + class FE + filing-year FE
                      [+ assignee FE if sample allows] + e
  Standard errors clustered by CPC class x filing-year.
  b1 < 0  =>  the paper-to-patent lag shrank MORE in GenAI-exposed classes post-2023.

Usage:
  pip install pandas statsmodels
  python did_analysis.py                      # main estimate
  python did_analysis.py --placebo            # fake treatment at 2017 on 2015-2019 data
  python did_analysis.py --inventor-only      # if citation origin column exists

Note: treated/post are already in lag_pairs.csv from build_lag_dataset.py.
The placebo rebuilds post from the placebo cutoff and restricts the window.
"""

import argparse

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = "../data/clean/lag_pairs.csv"


def run(df: pd.DataFrame, label: str) -> None:
    df = df.copy()
    df["log_lag"] = np.log1p(df["lag_days"])
    df["cluster"] = df["cpc_class"].astype(str) + "_" + df["filing_year"].astype(str)

    model = smf.ols(
        "log_lag ~ treated:post + C(cpc_class) + C(filing_year)",
        data=df,
    ).fit(cov_type="cluster", cov_kwds={"groups": df["cluster"]})

    print(f"\n===== {label} =====")
    print(f"N pairs: {len(df):,}")
    inter = [t for t in model.params.index if "treated" in t and "post" in t]
    for term in inter:
        print(f"{term}: coef={model.params[term]:.4f}, "
              f"se={model.bse[term]:.4f}, p={model.pvalues[term]:.4g}")
    print("(negative coefficient = larger lag reduction in treated classes)")
    print("\nFull summary written to results_" + label + ".txt")
    with open(f"results_{label}.txt", "w") as f:
        f.write(model.summary().as_text())


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--placebo", action="store_true",
                    help="fake treatment at 2021-01-01 inside the 2018-2022 pre-period")
    ap.add_argument("--mature", type=str, default=None, metavar="YYYY-MM-DD",
                    help="drop filings after this date (truncation guard), e.g. 2024-12-31")
    ap.add_argument("--window", type=float, default=None, metavar="YEARS",
                    help="keep only pairs with lag <= YEARS*365.25 (uniform citation window)")
    ap.add_argument("--inventor-only", action="store_true",
                    help="restrict to inventor-origin citations (needs 'citation_origin' column)")
    args = ap.parse_args()

    df = pd.read_csv(DATA, parse_dates=["filing_date"])

    label_parts = []
    if args.mature:
        df = df[df["filing_date"] <= args.mature]
        label_parts.append(f"mature{args.mature}")
    if args.window:
        df = df[df["lag_days"] <= args.window * 365.25]
        label_parts.append(f"win{int(args.window)}y")
    suffix = ("_" + "_".join(label_parts)) if label_parts else ""

    if args.inventor_only:
        if "citation_origin" not in df.columns:
            raise SystemExit("No 'citation_origin' column in the data; "
                             "re-export from Lens with citation origin if available.")
        df = df[df["citation_origin"].str.contains("inventor|applicant",
                                                   case=False, na=False)]
        run(df, "inventor_only")
        return

    if args.placebo:
        df = df[(df["filing_date"] >= "2018-01-01") & (df["filing_date"] <= "2022-12-31")]
        df["post"] = (df["filing_date"] >= "2021-01-01").astype(int)
        run(df, "placebo_2021")
        print("\nInterpretation: a significant placebo effect means the design is "
              "broken (pre-trends differ); an insignificant one supports the design.")
        return

    run(df, "main_did" + suffix)


if __name__ == "__main__":
    main()
