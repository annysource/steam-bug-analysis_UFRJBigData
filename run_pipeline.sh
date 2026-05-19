#!/bin/bash

echo "Running ETL..."

python3 etl/clean_reviews.py

echo "Running Spark Processing..."

$SPARK_HOME/bin/spark-submit spark/qa_insights.py

echo "Running MapReduce..."

$SPARK_HOME/bin/spark-submit mapreduce/bug_analysis.py

echo "Pipeline finished."