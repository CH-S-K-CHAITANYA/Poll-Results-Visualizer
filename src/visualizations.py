"""
Visualization module.
Produces 8 professional charts and saves them to outputs/charts/.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

# ── Global style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "#F8F8F8",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 100,
})

PALETTE = ["#4361EE", "#F72585", "#4CC9F0", "#7209B7", "#3A0CA3"]
OUTPUT_DIR = "outputs/charts"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(filename: str):
    """Save current figure and close."""
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    print(f"  [CHART] Saved → {path}")
    plt.close()


# ── Chart 1: Horizontal bar — overall vote share ───────────────────────────────

def plot_vote_share_bar(vote_df: pd.DataFrame):
    """Horizontal bar chart showing vote percentage per choice."""
    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(
        vote_df["choice"],
        vote_df["percentage"],
        color=PALETTE[:len(vote_df)],
        edgecolor="white",
        linewidth=0.8
    )

    for bar, pct in zip(bars, vote_df["percentage"]):
        ax.text(
            bar.get_width() + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%",
            va="center", ha="left", fontsize=11, fontweight="bold"
        )

    ax.set_xlabel("Vote Share (%)")
    ax.set_title("Overall Vote Share by Product", fontweight="bold", pad=15)
    ax.set_xlim(0, vote_df["percentage"].max() + 14)
    ax.invert_yaxis()
    ax.xaxis.set_major_locator(mticker.MultipleLocator(10))
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    plt.tight_layout()
    _save("01_vote_share_bar.png")


# ── Chart 2: Donut pie ─────────────────────────────────────────────────────────

def plot_vote_share_pie(vote_df: pd.DataFrame):
    """Donut chart showing vote distribution."""
    fig, ax = plt.subplots(figsize=(7, 7))

    wedges, texts, autotexts = ax.pie(
        vote_df["votes"],
        labels=vote_df["choice"],
        autopct="%1.1f%%",
        colors=PALETTE[:len(vote_df)],
        wedgeprops=dict(width=0.6, edgecolor="white", linewidth=2),
        pctdistance=0.75,
        startangle=90
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")

    ax.text(0, 0, f"n={vote_df['votes'].sum():,}",
            ha="center", va="center", fontsize=13, fontweight="bold", color="#444")
    ax.set_title("Vote Distribution — All Respondents", fontweight="bold", pad=20)
    plt.tight_layout()
    _save("02_vote_share_pie.png")


# ── Chart 3: Stacked bar — region-wise ────────────────────────────────────────

def plot_region_stacked_bar(region_df: pd.DataFrame):
    """100% stacked bar chart: choice distribution per region."""
    fig, ax = plt.subplots(figsize=(11, 6))

    region_df.plot(
        kind="bar", stacked=True, ax=ax,
        color=PALETTE[:len(region_df.columns)],
        edgecolor="white", linewidth=0.5, width=0.65
    )

    ax.set_xlabel("Region")
    ax.set_ylabel("Vote Share (%)")
    ax.set_title("Choice Distribution by Region (Stacked)", fontweight="bold", pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    ax.legend(title="Product", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    _save("03_region_stacked_bar.png")


# ── Chart 4: Grouped bar — age group ──────────────────────────────────────────

def plot_age_group_bar(age_df: pd.DataFrame):
    """Grouped bar chart: product preference by age group."""
    fig, ax = plt.subplots(figsize=(12, 6))

    age_df.plot(
        kind="bar", ax=ax,
        color=PALETTE[:len(age_df.columns)],
        edgecolor="white", linewidth=0.5, width=0.75
    )

    ax.set_xlabel("Age Group")
    ax.set_ylabel("Vote Share (%)")
    ax.set_title("Product Preference by Age Group", fontweight="bold", pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title="Product", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    _save("04_age_group_bar.png")


# ── Chart 5: Heatmap — region × choice ────────────────────────────────────────

def plot_region_heatmap(region_df: pd.DataFrame):
    """Heatmap of vote share: region × product."""
    fig, ax = plt.subplots(figsize=(9, 5))

    sns.heatmap(
        region_df,
        annot=True, fmt=".1f",
        cmap="Blues",
        linewidths=0.5, linecolor="white",
        cbar_kws={"label": "Vote Share (%)"},
        ax=ax
    )

    ax.set_title("Vote Share Heatmap — Region × Product", fontweight="bold", pad=15)
    ax.set_xlabel("Product")
    ax.set_ylabel("Region")
    plt.tight_layout()
    _save("05_region_heatmap.png")


# ── Chart 6: Satisfaction bar with error bars ──────────────────────────────────

def plot_satisfaction_bar(sat_df: pd.DataFrame):
    """Bar chart: average satisfaction per product with std-dev error bars."""
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(
        sat_df["choice"],
        sat_df["avg_score"],
        yerr=sat_df["std_dev"],
        color=PALETTE[:len(sat_df)],
        edgecolor="white", linewidth=0.8,
        capsize=6,
        error_kw={"elinewidth": 1.5, "ecolor": "#555"}
    )

    for bar, val in zip(bars, sat_df["avg_score"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.12,
            f"{val:.2f}",
            ha="center", va="bottom", fontsize=11, fontweight="bold"
        )

    ax.set_ylim(0, 5.8)
    ax.set_xlabel("Product")
    ax.set_ylabel("Avg. Satisfaction Score (1–5)")
    ax.set_title("Satisfaction Score by Product Choice", fontweight="bold", pad=15)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    _save("06_satisfaction_score.png")


# ── Chart 7: Trend line — votes over time ─────────────────────────────────────

def plot_trend_line(trend_df: pd.DataFrame):
    """Line chart: weekly vote trend per product."""
    fig, ax = plt.subplots(figsize=(12, 5))

    for i, col in enumerate(trend_df.columns):
        ax.plot(
            trend_df.index,
            trend_df[col],
            marker="o", markersize=4,
            linewidth=2,
            label=col,
            color=PALETTE[i % len(PALETTE)]
        )

    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Responses")
    ax.set_title("Weekly Response Trend by Product", fontweight="bold", pad=15)
    ax.legend(title="Product", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.grid(alpha=0.3, linestyle="--")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    _save("07_trend_line.png")


# ── Chart 8: Grouped bar — gender ─────────────────────────────────────────────

def plot_gender_bar(gender_df: pd.DataFrame):
    """Grouped bar chart: product preference by gender."""
    fig, ax = plt.subplots(figsize=(9, 5))

    gender_df.plot(
        kind="bar", ax=ax,
        color=PALETTE[:len(gender_df.columns)],
        edgecolor="white", linewidth=0.5, width=0.7
    )

    ax.set_xlabel("Gender")
    ax.set_ylabel("Vote Share (%)")
    ax.set_title("Product Preference by Gender", fontweight="bold", pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title="Product", bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    plt.tight_layout()
    _save("08_gender_bar.png")
