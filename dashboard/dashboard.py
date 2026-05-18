import streamlit as st
import pandas as pd
import glob

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Steam QA Analytics",
    layout="wide"
)

st.title("Steam Indie Games QA Analytics")

# ---------------------------------
# LOAD BUG METRICS
# ---------------------------------

bug_files = glob.glob(
    "data/processed/bug_metrics/*.csv"
)

if not bug_files:
    st.error("Bug metrics CSV not found.")
    st.stop()

bug_df = pd.read_csv(bug_files[0])

# ---------------------------------
# LOAD KPI METRICS
# ---------------------------------

kpi_files = glob.glob(
    "data/processed/kpi_metrics/*.csv"
)

if not kpi_files:
    st.error("KPI metrics CSV not found.")
    st.stop()

kpi_df = pd.read_csv(kpi_files[0])

kpi = kpi_df.iloc[0]

# ---------------------------------
# KPI SECTION
# ---------------------------------

st.subheader("Project KPIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Reviews",
    int(kpi["total_reviews"])
)

col2.metric(
    "Negative Reviews",
    int(kpi["negative_reviews"])
)

col3.metric(
    "Bug Reviews",
    int(kpi["bug_reviews"])
)

col4.metric(
    "Avg Playtime",
    round(float(kpi["avg_playtime"]), 2)
)

# ---------------------------------
# BAR CHART
# ---------------------------------

st.subheader("Most Frequent QA Terms")

chart_data = bug_df.set_index("word")

st.bar_chart(chart_data)

# ---------------------------------
# TABLE
# ---------------------------------

st.subheader("QA Terms Table")

st.dataframe(bug_df)