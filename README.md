# Steam BigData - QA Analytics

Analisador de reviews Steam que detecta bugs em jogos indie usando Apache Spark.

## Stack

Python | Apache Spark | Streamlit | Pandas | Altair

## Funcionalidade

JSON → CSV → MapReduce (termos QA) → KPIs → Dashboard

## Executar

```bash
pip install -r requirements.txt
python clean_reviews.py
spark-submit spark/bug_analysis.py && spark-submit spark/qa_insights.py
streamlit run dashboard/dashboard.py
```

Dashboard: http://localhost:8501
Deploy realizado em: https://buganalytics.streamlit.app/

