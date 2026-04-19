"""
Statistical analysis module.
Computes vote shares, rankings, crosstabs, satisfaction stats, and trend data.
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency


def overall_vote_share(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute overall vote count and percentage for each choice.

    Returns:
        pd.DataFrame: columns — choice, votes, percentage, rank
    """
    counts = df["choice"].value_counts().reset_index()
    counts.columns = ["choice", "votes"]
    counts["percentage"] = (counts["votes"] / counts["votes"].sum() * 100).round(2)
    counts = counts.sort_values("votes", ascending=False).reset_index(drop=True)
    counts["rank"] = range(1, len(counts) + 1)
    return counts


def region_wise_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage breakdown of choice within each region.

    Returns:
        pd.DataFrame: region × choice percentage matrix
    """
    ct = pd.crosstab(df["region"], df["choice"])
    return ct.div(ct.sum(axis=1), axis=0).mul(100).round(2)


def age_group_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Percentage breakdown of choice within each age group.

    Returns:
        pd.DataFrame: age_group × choice percentage matrix
    """
    ct = pd.crosstab(df["age_group"], df["choice"])
    return ct.div(ct.sum(axis=1), axis=0).mul(100).round(2)


def gender_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Percentage breakdown of choice by gender."""
    ct = pd.crosstab(df["gender"], df["choice"])
    return ct.div(ct.sum(axis=1), axis=0).mul(100).round(2)


def satisfaction_by_choice(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mean satisfaction score per choice with std dev and sample size.

    Returns:
        pd.DataFrame: sorted by avg_score descending
    """
    return (
        df.groupby("choice")["satisfaction_score"]
        .agg(["mean", "std", "count"])
        .round(2)
        .sort_values("mean", ascending=False)
        .reset_index()
        .rename(columns={"mean": "avg_score", "std": "std_dev", "count": "n"})
    )


def trend_over_time(df: pd.DataFrame, freq: str = "W") -> pd.DataFrame:
    """
    Vote counts per choice aggregated by time period.

    Args:
        df   : cleaned dataframe
        freq : 'W' weekly, 'M' monthly

    Returns:
        pd.DataFrame: period × choice vote counts
    """
    df = df.copy()
    df["period"] = df["date"].dt.to_period(freq).astype(str)
    return df.groupby(["period", "choice"]).size().unstack(fill_value=0)


def chi_square_test(df: pd.DataFrame,
                    col1: str = "region",
                    col2: str = "choice") -> dict:
    """
    Chi-square test of independence between two categorical columns.

    Returns:
        dict: chi2, p_value, degrees_of_freedom, significant flag, interpretation
    """
    ct = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, _ = chi2_contingency(ct)
    return {
        "chi2_statistic": round(chi2, 4),
        "p_value": round(p, 6),
        "degrees_of_freedom": dof,
        "significant": p < 0.05,
        "interpretation": (
            f"Significant relationship between {col1} and {col2} (p={p:.4f} < 0.05)"
            if p < 0.05
            else f"No significant relationship between {col1} and {col2} (p={p:.4f})"
        )
    }


if __name__ == "__main__":
    df = pd.read_csv("data/processed/cleaned_data.csv", parse_dates=["date"])

    print("\n--- Overall Vote Share ---")
    print(overall_vote_share(df).to_string(index=False))

    print("\n--- Region-wise Analysis ---")
    print(region_wise_analysis(df))

    print("\n--- Age Group Analysis ---")
    print(age_group_analysis(df))

    print("\n--- Satisfaction by Choice ---")
    print(satisfaction_by_choice(df).to_string(index=False))

    print("\n--- Chi-square Test (Region vs Choice) ---")
    print(chi_square_test(df, "region", "choice")["interpretation"])
