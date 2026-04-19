"""
Data cleaning module for poll data.
Handles null values, type conversions, and category normalization.
"""

import pandas as pd
import numpy as np
import os


def load_raw_data(filepath: str) -> pd.DataFrame:
    """Load raw CSV poll data."""
    df = pd.read_csv(filepath)
    print(f"[LOAD] {len(df)} rows loaded from: {filepath}")
    return df


def clean_poll_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full cleaning pipeline:
      1. Drop rows missing the primary answer ('choice') — unusable
      2. Fill missing region / age_group / gender with 'Unknown'
      3. Fill missing satisfaction_score with column median
      4. Normalize strings: strip whitespace, title-case
      5. Convert date column to datetime
      6. Add derived time features: month, week, day_of_week

    Returns:
        pd.DataFrame: cleaned dataframe
    """
    original_len = len(df)

    # 1. Drop rows with no answer
    df = df.dropna(subset=["choice"]).copy()
    print(f"[CLEAN] Dropped {original_len - len(df)} rows with missing 'choice'")

    # 2. Fill categorical nulls
    for col in ["region", "age_group", "gender"]:
        df[col] = df[col].fillna("Unknown")

    # 3. Fill numeric nulls with median
    median_score = df["satisfaction_score"].median()
    df["satisfaction_score"] = df["satisfaction_score"].fillna(median_score)
    print(f"[CLEAN] Filled missing satisfaction scores with median: {median_score:.2f}")

    # 4. Normalize strings
    for col in ["choice", "region", "age_group", "gender", "question"]:
        df[col] = df[col].astype(str).str.strip().str.title()

    # 5. Parse dates
    df["date"] = pd.to_datetime(df["date"])

    # 6. Derived time features
    df["month"] = df["date"].dt.month_name()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["date"].dt.day_name()

    print(f"[CLEAN] Final shape: {df.shape}")
    return df.reset_index(drop=True)


def get_data_summary(df: pd.DataFrame) -> dict:
    """Return key statistics about the cleaned dataset."""
    return {
        "total_responses": len(df),
        "unique_choices": df["choice"].nunique(),
        "regions": sorted(df["region"].unique().tolist()),
        "age_groups": sorted(df["age_group"].unique().tolist()),
        "genders": sorted(df["gender"].unique().tolist()),
        "date_range": f"{df['date'].min().date()} to {df['date'].max().date()}",
        "avg_satisfaction": round(df["satisfaction_score"].mean(), 2),
    }


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df_raw = load_raw_data("data/raw/poll_data.csv")
    df_clean = clean_poll_data(df_raw)
    df_clean.to_csv("data/processed/cleaned_data.csv", index=False)
    print("\n--- Data Summary ---")
    for k, v in get_data_summary(df_clean).items():
        print(f"  {k}: {v}")
