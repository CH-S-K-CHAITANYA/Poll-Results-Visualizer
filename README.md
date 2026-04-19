# 📊 Poll Results Visualizer

> End-to-end data analytics pipeline for survey and poll data.

---

## Problem

Raw survey CSVs are unreadable without transformation. Organizations need automated pipelines to clean, analyze, and visualize responses to support decisions.

## Solution

A complete 5-stage Python pipeline:

```
Raw CSV  →  Cleaning  →  Analysis  →  Visualization  →  Insights Report + Dashboard
```

---

## Features

| Feature                  | Details                                                                  |
| ------------------------ | ------------------------------------------------------------------------ |
| Synthetic data generator | 1,000-row dataset with demographic patterns                              |
| ETL pipeline             | Null handling, normalization, date parsing                               |
| Statistical analysis     | Vote share, crosstabs, chi-square significance test                      |
| 8 chart types            | Bar, pie, stacked bar, grouped bar, heatmap, trend, satisfaction, gender |
| Auto-insights report     | Plain-English summary written by code                                    |
| Streamlit dashboard      | Live filters by region, age group, gender                                |

---

## Tech Stack

| Layer         | Tools                       |
| ------------- | --------------------------- |
| Data          | Python 3.10+, Pandas, NumPy |
| Statistics    | SciPy                       |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard     | Streamlit                   |

---

## Quick Start

```bash
# 1. Clone or unzip the project
cd Poll-Results-Visualizer

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate          # Mac/Linux
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the full pipeline (generates data + 8 charts + report)
python main.py

# 5. Launch interactive dashboard
streamlit run dashboard.py
```

---

## Project Structure

```
Poll-Results-Visualizer/
├── data/
│   ├── raw/            poll_data.csv (auto-generated)
│   └── processed/      cleaned_data.csv
├── src/
│   ├── generate_data.py
│   ├── data_cleaning.py
│   ├── analysis.py
│   ├── visualizations.py
│   └── insights.py
├── outputs/
│   ├── charts/         8 PNG charts
│   └── reports/        insights_report.txt
├── dashboard.py        Streamlit app
├── main.py             One-command pipeline runner
└── requirements.txt
```

---

## Key Insights (from sample run)

- **Product A** leads overall with ~37% of votes
- **Product C** dominates the 18–34 age group (40%) — insight hidden in aggregate data
- Regional differences are **statistically significant** (chi-square p < 0.05)
- **Product C** has the highest satisfaction score (4.1 / 5.0)

---

## Author

Built as a placement portfolio project demonstrating end-to-end data analyst skills.

**Skills demonstrated:** ETL · Data Cleaning · Statistical Testing · Data Visualization · Dashboard Development · Insight Communication

---

_Replace the synthetic data generator with any real CSV to run the same pipeline on real survey data._
#
