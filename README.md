# Steam BigData - QA Analytics

Analisador de reviews do Steam que detecta menções de bugs em jogos indie usando Apache Spark.

## Tecnologias

- **Python** - Processamento de dados
- **Apache Spark** - MapReduce e SQL para análise em larga escala
- **Streamlit** - Dashboard interativo
- **Pandas** - Manipulação de dados
- **Altair** - Visualizações

## O que faz

Converte reviews JSON para CSV, analisa frequência de termos QA (crash, bug, lag, etc.), calcula KPIs de qualidade e exibe em dashboard interativo.

## Quick Start

```bash
pip install -r requirements.txt
python clean_reviews.py
spark-submit spark/bug_analysis.py && spark-submit spark/qa_insights.py
streamlit run dashboard/dashboard.py
```

Acesse: http://localhost:8501
