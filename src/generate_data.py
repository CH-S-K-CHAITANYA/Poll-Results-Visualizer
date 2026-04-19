"""
Synthetic poll dataset generator.
Simulates a product preference survey with realistic demographic patterns.
"""

import pandas as pd
import numpy as np
import os


def generate_poll_data(n_responses=1000, seed=42):
    """
    Generate a synthetic poll dataset simulating a product preference survey.

    Columns:
        respondent_id  : unique identifier
        date           : response date (spread over 90 days)
        question       : the poll question
        choice         : selected product option
        region         : geographic region
        age_group      : respondent age bracket
        gender         : respondent gender
        satisfaction_score : 1-5 numeric rating

    Returns:
        pd.DataFrame: synthetic poll data (~3% nulls introduced for realism)
    """
    np.random.seed(seed)

    # --- Identifiers ---
    respondent_ids = [f"R{str(i).zfill(4)}" for i in range(1, n_responses + 1)]

    # --- Dates spread over 90 days ---
    base_date = pd.Timestamp("2024-01-01")
    dates = [base_date + pd.Timedelta(days=int(d))
             for d in np.random.randint(0, 90, n_responses)]

    # --- Regions with realistic distribution ---
    regions = np.random.choice(
        ["North", "South", "East", "West", "Central"],
        size=n_responses,
        p=[0.25, 0.20, 0.20, 0.20, 0.15]
    )

    # --- Age groups ---
    age_groups = np.random.choice(
        ["18-24", "25-34", "35-44", "45-54", "55+"],
        size=n_responses,
        p=[0.20, 0.30, 0.25, 0.15, 0.10]
    )

    # --- Gender ---
    genders = np.random.choice(
        ["Male", "Female", "Non-binary"],
        size=n_responses,
        p=[0.48, 0.48, 0.04]
    )

    # --- Choices with demographic bias (realistic) ---
    # Younger prefer Product C; Older prefer Product A
    choices = []
    for age in age_groups:
        if age in ["18-24", "25-34"]:
            choice = np.random.choice(
                ["Product A", "Product B", "Product C", "Product D"],
                p=[0.25, 0.20, 0.40, 0.15]
            )
        elif age in ["35-44", "45-54"]:
            choice = np.random.choice(
                ["Product A", "Product B", "Product C", "Product D"],
                p=[0.40, 0.30, 0.15, 0.15]
            )
        else:
            choice = np.random.choice(
                ["Product A", "Product B", "Product C", "Product D"],
                p=[0.50, 0.30, 0.10, 0.10]
            )
        choices.append(choice)

    # --- Satisfaction scores correlated with choice ---
    score_map = {
        "Product A": (3.8, 0.9),
        "Product B": (3.2, 1.0),
        "Product C": (4.1, 0.8),
        "Product D": (2.9, 1.1)
    }
    satisfaction_scores = []
    for c in choices:
        mu, sigma = score_map[c]
        score = round(float(np.clip(np.random.normal(mu, sigma), 1, 5)), 1)
        satisfaction_scores.append(score)

    df = pd.DataFrame({
        "respondent_id": respondent_ids,
        "date": dates,
        "question": "Which product do you prefer?",
        "choice": choices,
        "region": regions,
        "age_group": age_groups,
        "gender": genders,
        "satisfaction_score": satisfaction_scores
    })

    # Introduce ~3% missing values (realistic dirty data)
    for col in ["choice", "region", "age_group", "satisfaction_score"]:
        null_idx = np.random.choice(df.index, size=int(0.03 * n_responses), replace=False)
        df.loc[null_idx, col] = np.nan

    return df


if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    df = generate_poll_data(n_responses=1000)
    df.to_csv("data/raw/poll_data.csv", index=False)
    print(f"Dataset generated: {len(df)} rows")
    print(df.head(10).to_string())
    print(f"\nMissing values:\n{df.isnull().sum()}")
