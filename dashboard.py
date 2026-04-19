"""
dashboard.py  —  Interactive Streamlit dashboard for Poll Results Visualizer.

Run with:
    streamlit run dashboard.py
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generate_data import generate_poll_data
from src.data_cleaning import clean_poll_data
from src.analysis import (
    overall_vote_share,
    region_wise_analysis,
    age_group_analysis,
    satisfaction_by_choice,
    trend_over_time,
    chi_square_test,
    gender_analysis,
)
from src.insights import generate_insights

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Poll Results Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

PALETTE = ["#4361EE", "#F72585", "#4CC9F0", "#7209B7", "#3A0CA3"]


# ── Data loader (cached) ───────────────────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    path = "data/processed/cleaned_data.csv"
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=["date"])
    df_raw = generate_poll_data(1000)
    df = clean_poll_data(df_raw)
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(path, index=False)
    return df


# ── Header ─────────────────────────────────────────────────────────────────────
st.title("📊 Poll Results Visualizer")
st.caption("Product Preference Survey  —  Interactive Analytics Dashboard")
st.divider()

df_full = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🔍 Filters")
    regions   = ["All"] + sorted(df_full["region"].unique())
    ages      = ["All"] + sorted(df_full["age_group"].unique())
    genders   = ["All"] + sorted(df_full["gender"].unique())

    sel_region = st.selectbox("Region",    regions)
    sel_age    = st.selectbox("Age Group", ages)
    sel_gender = st.selectbox("Gender",    genders)

    st.divider()
    if st.button("🔄 Reset filters"):
        sel_region = sel_age = sel_gender = "All"

    st.caption("All charts update live based on your selection.")

# ── Apply filters ──────────────────────────────────────────────────────────────
df = df_full.copy()
if sel_region != "All": df = df[df["region"]    == sel_region]
if sel_age    != "All": df = df[df["age_group"] == sel_age]
if sel_gender != "All": df = df[df["gender"]    == sel_gender]

if df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
    st.stop()

# ── KPI metric cards ───────────────────────────────────────────────────────────
vote_df  = overall_vote_share(df)
winner   = vote_df.iloc[0]
runner   = vote_df.iloc[1]
sat_df   = satisfaction_by_choice(df)
best_sat = sat_df.iloc[0]
margin   = round(winner["percentage"] - runner["percentage"], 1)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Responses",  f"{len(df):,}")
c2.metric("Leading Product",  winner["choice"],     f"{winner['percentage']:.1f}%")
c3.metric("Runner-up",        runner["choice"],     f"{runner['percentage']:.1f}%")
c4.metric("Lead Margin",      f"{margin} pts")
c5.metric("Avg Satisfaction", f"{df['satisfaction_score'].mean():.2f} / 5")
st.divider()

# ── Row 1: Bar + Pie ───────────────────────────────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Overall Vote Share")
    fig = px.bar(
        vote_df, x="percentage", y="choice", orientation="h",
        text="percentage", color="choice",
        color_discrete_sequence=PALETTE,
        labels={"percentage": "Vote Share (%)", "choice": ""},
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis={"autorange": "reversed"})
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("Vote Distribution (Donut)")
    fig = px.pie(
        vote_df, values="votes", names="choice",
        hole=0.45, color_discrete_sequence=PALETTE,
    )
    fig.update_traces(textinfo="percent+label")
    st.plotly_chart(fig, use_container_width=True)

# ── Row 2: Region stacked bar + Heatmap ───────────────────────────────────────
st.subheader("Region-wise Preference")
region_df = region_wise_analysis(df)

col_l2, col_r2 = st.columns(2)
with col_l2:
    region_reset = region_df.reset_index()
    region_melted = region_reset.melt(id_vars="region", var_name="Product", value_name="Share")
    fig = px.bar(
        region_melted, x="region", y="Share", color="Product",
        barmode="stack", color_discrete_sequence=PALETTE,
        labels={"Share": "Vote Share (%)", "region": "Region"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r2:
    fig = px.imshow(
        region_df, text_auto=".1f",
        color_continuous_scale="Blues",
        labels={"color": "Vote Share (%)"},
        aspect="auto",
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Row 3: Age group ──────────────────────────────────────────────────────────
st.subheader("Preference by Age Group")
age_df = age_group_analysis(df).reset_index()
age_melted = age_df.melt(id_vars="age_group", var_name="Product", value_name="Share")
fig = px.bar(
    age_melted, x="age_group", y="Share", color="Product",
    barmode="group", color_discrete_sequence=PALETTE,
    labels={"Share": "Vote Share (%)", "age_group": "Age Group"},
)
st.plotly_chart(fig, use_container_width=True)

# ── Row 4: Trend + Gender ─────────────────────────────────────────────────────
col_l3, col_r3 = st.columns(2)

with col_l3:
    st.subheader("Weekly Vote Trend")
    trend_df = trend_over_time(df, freq="W").reset_index()
    trend_melted = trend_df.melt(id_vars="period", var_name="Product", value_name="Votes")
    fig = px.line(
        trend_melted, x="period", y="Votes", color="Product",
        markers=True, color_discrete_sequence=PALETTE,
        labels={"period": "Week"},
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r3:
    st.subheader("Satisfaction by Product")
    fig = px.bar(
        sat_df, x="choice", y="avg_score", error_y="std_dev",
        color="choice", color_discrete_sequence=PALETTE,
        labels={"avg_score": "Avg Score (1–5)", "choice": "Product"},
        range_y=[0, 5.8],
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Gender analysis ───────────────────────────────────────────────────────────
st.subheader("Preference by Gender")
gen_df = gender_analysis(df).reset_index()
gen_melted = gen_df.melt(id_vars="gender", var_name="Product", value_name="Share")
fig = px.bar(
    gen_melted, x="gender", y="Share", color="Product",
    barmode="group", color_discrete_sequence=PALETTE,
    labels={"Share": "Vote Share (%)", "gender": "Gender"},
)
st.plotly_chart(fig, use_container_width=True)

# ── Chi-square test ───────────────────────────────────────────────────────────
st.divider()
with st.expander("📐 Statistical Test: Chi-Square (Region vs Choice)"):
    chi = chi_square_test(df, "region", "choice")
    if chi["significant"]:
        st.success(chi["interpretation"])
    else:
        st.info(chi["interpretation"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Chi² Statistic", chi["chi2_statistic"])
    col2.metric("p-value", chi["p_value"])
    col3.metric("Significant?", "Yes ✅" if chi["significant"] else "No ❌")

# ── Insights report ───────────────────────────────────────────────────────────
with st.expander("📝 Auto-Generated Insights Report"):
    report = generate_insights(df)
    st.code(report, language=None)
    st.download_button(
        "⬇️ Download Report (.txt)",
        data=report,
        file_name="insights_report.txt",
        mime="text/plain",
    )

# ── Raw data viewer ───────────────────────────────────────────────────────────
with st.expander("🗂️ View / Download Raw Data"):
    st.dataframe(df, use_container_width=True)
    st.download_button(
        "⬇️ Download Filtered Data (.csv)",
        data=df.to_csv(index=False),
        file_name="filtered_poll_data.csv",
        mime="text/csv",
    )
