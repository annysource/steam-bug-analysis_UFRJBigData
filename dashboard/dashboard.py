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

bug_df = pd.read_csv(bug_files[0], encoding="utf-8")

# ---------------------------------
# LOAD KPI METRICS
# ---------------------------------

kpi_files = glob.glob(
    "data/processed/kpi_metrics/*.csv"
)

if not kpi_files:
    st.error("KPI metrics CSV not found.")
    st.stop()

kpi_df = pd.read_csv(kpi_files[0], encoding="utf-8")

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

# ---------------------------------
# REVIEW EXPLORER
# ---------------------------------

st.subheader("QA Review Explorer")

review_files = glob.glob(
    "data/processed/bug_reviews/*.csv"
)

if not review_files:
    st.warning("No QA review files found.")
    st.stop()

review_df = pd.read_csv(review_files[0], encoding="utf-8")

selected_word = st.selectbox(
    "Select a QA Term",
    sorted(review_df["word"].unique())
)

filtered_reviews = review_df[
    review_df["word"] == selected_word
]

st.write(
    f"Reviews mentioning '{selected_word}'"
)

st.dataframe(
    filtered_reviews[["review_text"]]
)

import glob
import pandas as pd
import streamlit as st

st.subheader("QA Severity Explorer")

severity_files = glob.glob("./data/processed/qa_severity/*.csv")

if not severity_files:
    st.warning("No severity data found. Run Spark job first.")
    st.stop()

severity_df = pd.read_csv(severity_files[0], encoding="utf-8")

# ----------------------------
# CLICKABLE SEVERITY SELECT
# ----------------------------

selected_severity = st.radio(
    "Select severity level",
    severity_df["severity"].unique()
)

# ----------------------------
# LOAD REVIEWS (IMPORTANTE)
# ----------------------------

review_files = glob.glob("./data/processed/bug_reviews/*.csv")

if not review_files:
    st.warning("No review data found.")
    st.stop()

review_df = pd.read_csv(review_files[0], encoding="utf-8")

# ----------------------------
# FILTER REVIEWS BY SEVERITY WORDS
# ----------------------------

severity_map = {
    "critical": ["crash", "freeze", "broken"],
    "medium": ["glitch", "stutter", "bug"],
    "low": ["lag", "fps", "optimization"]
}

words = severity_map.get(selected_severity, [])

filtered_reviews = review_df[
    review_df["word"].isin(words)
]

# ----------------------------
# SHOW RESULTS
# ----------------------------

st.write(f"Reviews with severity: {selected_severity}")

for review in filtered_reviews["review_text"].head(50):
    with st.expander("View review"):
        st.write(review)