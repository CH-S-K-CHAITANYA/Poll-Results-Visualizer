"""
main.py
Run the entire Poll Results Visualizer pipeline with one command.

Usage:
    python main.py
"""

import os
import sys
import pandas as pd

# Ensure project root is on path when running directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generate_data import generate_poll_data
from src.data_cleaning import load_raw_data, clean_poll_data, get_data_summary
from src.analysis import (
    overall_vote_share,
    region_wise_analysis,
    age_group_analysis,
    gender_analysis,
    satisfaction_by_choice,
    trend_over_time,
    chi_square_test,
)
from src.visualizations import (
    plot_vote_share_bar,
    plot_vote_share_pie,
    plot_region_stacked_bar,
    plot_age_group_bar,
    plot_region_heatmap,
    plot_satisfaction_bar,
    plot_trend_line,
    plot_gender_bar,
)
from src.insights import generate_insights


def banner(text: str):
    print("\n" + "─" * 55)
    print(f"  {text}")
    print("─" * 55)


def main():
    print("\n" + "=" * 55)
    print("   POLL RESULTS VISUALIZER  —  FULL PIPELINE")
    print("=" * 55)

    # ── Step 1: Generate data ──────────────────────────────────────────────────
    banner("STEP 1 / 5  →  Generating synthetic dataset")
    os.makedirs("data/raw", exist_ok=True)
    df_raw = generate_poll_data(n_responses=1000)
    df_raw.to_csv("data/raw/poll_data.csv", index=False)
    print(f"  Raw CSV saved  →  data/raw/poll_data.csv  ({len(df_raw)} rows)")

    # ── Step 2: Clean ──────────────────────────────────────────────────────────
    banner("STEP 2 / 5  →  Cleaning data")
    os.makedirs("data/processed", exist_ok=True)
    df = clean_poll_data(df_raw)
    df.to_csv("data/processed/cleaned_data.csv", index=False)
    summary = get_data_summary(df)
    print(f"  Cleaned CSV    →  data/processed/cleaned_data.csv")
    print(f"  Responses      :  {summary['total_responses']:,}")
    print(f"  Date range     :  {summary['date_range']}")
    print(f"  Avg score      :  {summary['avg_satisfaction']}")

    # ── Step 3: Analysis ──────────────────────────────────────────────────────
    banner("STEP 3 / 5  →  Running analysis")
    vote_df   = overall_vote_share(df)
    region_df = region_wise_analysis(df)
    age_df    = age_group_analysis(df)
    gender_df = gender_analysis(df)
    sat_df    = satisfaction_by_choice(df)
    trend_df  = trend_over_time(df, freq="W")
    chi       = chi_square_test(df, "region", "choice")

    print("\n  Overall vote share:")
    for _, row in vote_df.iterrows():
        print(f"    {row['choice']:14}  {row['percentage']:5.1f}%")
    print(f"\n  {chi['interpretation']}")

    # ── Step 4: Visualizations ────────────────────────────────────────────────
    banner("STEP 4 / 5  →  Generating charts")
    os.makedirs("outputs/charts", exist_ok=True)
    plot_vote_share_bar(vote_df)
    plot_vote_share_pie(vote_df)
    plot_region_stacked_bar(region_df)
    plot_age_group_bar(age_df)
    plot_region_heatmap(region_df)
    plot_satisfaction_bar(sat_df)
    plot_trend_line(trend_df)
    plot_gender_bar(gender_df)
    print("  8 charts saved → outputs/charts/")

    # ── Step 5: Insights ──────────────────────────────────────────────────────
    banner("STEP 5 / 5  →  Generating insights report")
    os.makedirs("outputs/reports", exist_ok=True)
    report = generate_insights(df)
    with open("outputs/reports/insights_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print(report)

    # ── Done ──────────────────────────────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  PIPELINE COMPLETE")
    print("  Charts   →  outputs/charts/      (8 PNG files)")
    print("  Report   →  outputs/reports/insights_report.txt")
    print("  Dashboard → run:  streamlit run dashboard.py")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
