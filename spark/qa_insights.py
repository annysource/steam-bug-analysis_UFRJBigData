from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

spark = SparkSession.builder \
    .appName("QA Insights") \
    .getOrCreate()

# -----------------------------
# LOAD DATA
# -----------------------------

df = spark.read.csv(
    "data/processed/Indie_RelicHuntersZero.csv",
    header=True,
    inferSchema=True
)

# -----------------------------
# TOTAL REVIEWS
# -----------------------------

total_reviews = df.count()

# -----------------------------
# NEGATIVE REVIEWS
# -----------------------------

negative_reviews = df.filter(
    col("voted_up") == False
).count()

# -----------------------------
# BUG REVIEWS
# -----------------------------

bug_reviews = df.filter(
    col("bug_detected") == True
).count()

# -----------------------------
# AVG PLAYTIME
# -----------------------------

avg_playtime = df.select(
    avg("playtime_forever")
).collect()[0][0]

# -----------------------------
# CREATE KPI DATAFRAME
# -----------------------------

kpi_df = spark.createDataFrame([
    (
        total_reviews,
        negative_reviews,
        bug_reviews,
        avg_playtime
    )
], [
    "total_reviews",
    "negative_reviews",
    "bug_reviews",
    "avg_playtime"
])

# -----------------------------
# SAVE KPIs
# -----------------------------

kpi_df.coalesce(1).write.csv(
    "data/processed/kpi_metrics",
    header=True,
    mode="overwrite"
)

print("KPI metrics generated.")