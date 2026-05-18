# Arquitetura

JSON bruto → Limpeza → MapReduce (contagem de termos) → KPIs → Dashboard

**Camadas:**
- Ingestion: JSON → CSV (clean_reviews.py)
- Analytics: MapReduce para frequência de termos (bug_analysis.py)
- Insights: KPIs com Spark SQL (qa_insights.py)
- Presentation: Dashboard Streamlit (dashboard.py)
