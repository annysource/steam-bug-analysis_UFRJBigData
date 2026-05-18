from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Steam QA Analytics") \
    .getOrCreate()

df = spark.read.csv(
    "data/processed/Indie_RelicHuntersZero.csv",
    header=True,
    inferSchema=True
)

print("Schema:")
df.printSchema()

print("Primeiras reviews:")
df.show(5)

print("Reviews com bugs:")

bug_reviews = df.filter(
    col("bug_detected") == True
)

bug_reviews.show()

print("Quantidade de reviews com bug:")

df.groupBy("bug_detected") \
  .count() \
  .show()
