from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    explode,
    split,
    lower
)

spark = SparkSession.builder \
    .appName("Steam QA MapReduce") \
    .getOrCreate()

# -----------------------------
# LOAD CSV
# -----------------------------

df = spark.read.csv(
    "data/processed/Indie_RelicHuntersZero.csv",
    header=True,
    inferSchema=True
)

# -----------------------------
# CLEAN TEXT
# -----------------------------

reviews = df.select(
    lower(col("review_text")).alias("review_text")
)

# -----------------------------
# MAP STEP
# explode words
# -----------------------------

words = reviews.select(
    explode(
        split(col("review_text"), " ")
    ).alias("word")
)

# -----------------------------
# FILTER QA TERMS
# -----------------------------

qa_terms = [
    "crash",
    "bug",
    "freeze",
    "lag",
    "glitch",
    "broken",
    "fps",
    "optimization",
    "stutter"
]

filtered_words = words.filter(
    col("word").isin(qa_terms)
)

# -----------------------------
# REDUCE STEP
# count occurrences
# -----------------------------

results = filtered_words.groupBy(
    "word"
).count().orderBy(
    col("count").desc()
)

# -----------------------------
# SHOW RESULTS
# -----------------------------

results.show()

# -----------------------------
# SAVE RESULTS
# -----------------------------

results.write.csv(
    "data/processed/bug_metrics",
    header=True,
    mode="overwrite"
)

print("QA metrics generated.")