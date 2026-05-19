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

from pyspark.sql.functions import regexp_replace

clean_reviews = df.select(
    lower(
        regexp_replace(col("review_text"), "[^a-zA-Z0-9 ]", "")
    ).alias("review_text")
)

words = clean_reviews.select(
    col("review_text"),
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
# ---------------------------------
# SAVE REVIEWS RELATED TO QA TERMS
# ---------------------------------

filtered_words.select(
    "word",
    "review_text"
).coalesce(1).write.csv(
    "data/processed/bug_reviews",
    header=True,
    mode="overwrite"
)


print("QA metrics generated.")