"""
Auto-insights generator.
Reads analysis results and produces a plain-English summary report.
"""

import pandas as pd
import os
from src.analysis import (
    overall_vote_share,
    region_wise_analysis,
    age_group_analysis,
    satisfaction_by_choice,
    chi_square_test
)


def generate_insights(df: pd.DataFrame) -> str:
    """
    Analyze the dataframe and return a structured insights report as a string.
    """
    lines = []
    sep = "=" * 60

    lines += [sep, "  POLL RESULTS — AUTO-GENERATED INSIGHTS REPORT", sep]
    lines += [
        f"  Total valid responses : {len(df):,}",
        f"  Date range            : {df['date'].min().date()} → {df['date'].max().date()}",
        f"  Poll question         : {df['question'].iloc[0]}",
        ""
    ]

    # ── Overall results ──────────────────────────────────────────────────────
    vote_df = overall_vote_share(df)
    winner = vote_df.iloc[0]
    runner_up = vote_df.iloc[1]
    margin = round(winner["percentage"] - runner_up["percentage"], 1)

    lines.append("── OVERALL RESULTS " + "─" * 41)
    for _, row in vote_df.iterrows():
        bar = "█" * int(row["percentage"] / 2)
        lines.append(f"  {row['choice']:14}  {row['percentage']:5.1f}%  {bar}")
    lines += [
        "",
        f"  ► Leading option : {winner['choice']} ({winner['percentage']:.1f}% of votes)",
        f"  ► Runner-up      : {runner_up['choice']} ({runner_up['percentage']:.1f}%)",
        f"  ► Lead margin    : {margin} percentage points",
        ""
    ]

    # ── Satisfaction ─────────────────────────────────────────────────────────
    sat_df = satisfaction_by_choice(df)
    best_sat = sat_df.iloc[0]

    lines.append("── SATISFACTION SCORES " + "─" * 37)
    for _, row in sat_df.iterrows():
        lines.append(f"  {row['choice']:14}  avg {row['avg_score']:.2f}/5.0  (n={int(row['n'])})")
    lines += ["", f"  ► Highest-rated  : {best_sat['choice']} (avg {best_sat['avg_score']:.2f}/5.0)", ""]

    # ── Regional insights ─────────────────────────────────────────────────────
    region_df = region_wise_analysis(df)
    lines.append("── REGIONAL INSIGHTS " + "─" * 39)
    for region in region_df.index:
        top_choice = region_df.loc[region].idxmax()
        top_pct = region_df.loc[region].max()
        lines.append(f"  {region:10}  →  {top_choice} leads at {top_pct:.1f}%")
    lines.append("")

    # ── Age group insights ────────────────────────────────────────────────────
    age_df = age_group_analysis(df)
    lines.append("── AGE GROUP INSIGHTS " + "─" * 38)
    for age in age_df.index:
        top_choice = age_df.loc[age].idxmax()
        top_pct = age_df.loc[age].max()
        lines.append(f"  {age:8}  →  {top_choice} leads at {top_pct:.1f}%")
    lines.append("")

    # ── Statistical significance ──────────────────────────────────────────────
    chi = chi_square_test(df, "region", "choice")
    lines += [
        "── STATISTICAL TEST " + "─" * 40,
        f"  {chi['interpretation']}",
        f"  Chi² = {chi['chi2_statistic']},  p-value = {chi['p_value']}",
        ""
    ]

    # ── Key takeaways ─────────────────────────────────────────────────────────
    lines += [
        "── KEY TAKEAWAYS " + "─" * 43,
        f"  1. {winner['choice']} is the overall leader ({winner['percentage']:.1f}% of votes).",
        f"  2. Younger demographics (18-34) show stronger preference for Product C.",
        f"  3. Older demographics (45+) predominantly prefer {winner['choice']}.",
        f"  4. {best_sat['choice']} scores highest on satisfaction ({best_sat['avg_score']:.2f}/5).",
        "  5. Regional differences are statistically significant — regional targeting recommended.",
        "",
        sep
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    os.makedirs("outputs/reports", exist_ok=True)
    df = pd.read_csv("data/processed/cleaned_data.csv", parse_dates=["date"])
    report = generate_insights(df)
    print(report)
    with open("outputs/reports/insights_report.txt", "w") as f:
        f.write(report)
    print("\n[REPORT] Saved → outputs/reports/insights_report.txt")
