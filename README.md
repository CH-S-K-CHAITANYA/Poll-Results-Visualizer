<div align="center">

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
<img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=python&logoColor=white" alt="Matplotlib" />
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit" />

<br/><br/>

# 📊 AI-Powered Poll Results Visualizer & Analytics Pipeline

### End-to-end data engineering and automated insight generation for survey analytics.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-red)](https://streamlit.io/)
[![Stats](https://img.shields.io/badge/Stats-SciPy--Inference-orange)]()
[![Status](https://img.shields.io/badge/Status-Active-success)]()

<br/>

</div>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Pipeline Stages](#-pipeline-stages)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Screenshots](#-screenshots--outputs)
- [Learning Outcomes](#-learning-outcomes)
- [License](#-license)

---

## 🔍 Overview

The **Poll Results Visualizer** is a complete, automated data analytics pipeline designed to transform raw, messy survey data into actionable executive insights. 

While most tools stop at simple bar charts, this system performs deep statistical analysis—including crosstabs and Chi-square significance testing—to uncover hidden patterns in demographic behavior. It mirrors the workflow of professional **Data Analysts** and **Business Intelligence (BI) Engineers** by moving data through a structured ETL (Extract, Transform, Load) process.

---

## ❗ Problem Statement

Raw survey data collected from Google Forms, Typeform, or internal databases is often:
- **Unstructured:** Hard to read in CSV format.
- **Dirty:** Contains missing values, inconsistent date formats, and duplicates.
- **Surface-Level:** Aggregate totals often hide critical "sub-group" insights (e.g., a product failing overall but booming with Gen-Z).

This project automates the manual labor of cleaning and cross-referencing these variables, delivering a professional report in seconds.

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       INPUT LAYER                           │
│             Raw Poll CSV / Synthetic Generator              │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 ETL & PREPROCESSING MODULE                  │
│  • Null Handling         • Data Normalization               │
│  • Date Parsing          • Demographic Encoding             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  STATISTICAL ANALYSIS ENGINE                │
│  • Vote Share Calculation     • Chi-Square Significance     │
│  • Crosstab Generation        • Satisfaction Scoring        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        OUTPUT LAYER                         │
│  • 8 Visualization Charts    • Executive Insights (.txt)    │
│  • Cleaned Data Assets       • Interactive Streamlit UI     │
└─────────────────────────────────────────────────────────────┘
```

-----

## 🛠️ Tech Stack

| Component      | Technology            | Purpose                                       |
| -------------- | --------------------- | --------------------------------------------- |
| Language       | Python 3.10+          | Core logic and pipeline orchestration         |
| Data Handling  | Pandas, NumPy         | ETL, cleaning, and matrix manipulations       |
| Statistics     | SciPy                 | Chi-square testing and significance inference |
| Visualization  | Matplotlib, Seaborn   | Static professional-grade PNG charts          |
| Dashboard      | Streamlit, Plotly     | Interactive web-based data exploration        |
| Automation     | Python Scripting      | One-command "Main.py" execution               |

-----

## 📊 Pipeline Stages

1.  **Stage 1: Generation** – Creates a 1,000-row realistic dataset with weighted demographic patterns.
2.  **Stage 2: Cleaning** – Handles outliers, missing fields, and standardizes categorical text.
3.  **Stage 3: Analysis** – Performs cross-tabulation (e.g., Product Preference vs. Age Group).
4.  **Stage 4: Visualization** – Generates a suite of 8 diverse charts saved to `outputs/charts/`.
5.  **Stage 5: Insight Extraction** – Programmatically writes a text report summarizing key statistical wins.

-----

## 📁 Project Structure

```
Poll-Results-Visualizer/
├── 📂 data/
│   ├── raw/                ← Generated/Input poll_data.csv
│   └── processed/          ← Cleaned and transformed datasets
│
├── 📂 src/                 ← Modular Source Code
│   ├── generate_data.py    ← Synthetic engine
│   ├── data_cleaning.py    ← ETL logic
│   ├── analysis.py         ← Statistical math
│   ├── visualizations.py   ← Chart generation logic
│   └── insights.py         ← Automated report writer
│
├── 📂 outputs/             ← Final Deliverables
│   ├── 📂 charts/          ← PNG visualizations (01 to 08)
│   └── 📂 reports/         ← insights_report.txt
│
├── main.py                 ← Pipeline Entry Point
├── dashboard.py            ← Streamlit Web App
├── requirements.txt        ← Dependencies
└── README.md
```

-----

## ⚙️ Installation

### Step 1 — Clone & Navigate

```bash
git clone https://github.com/YOUR_USERNAME/Poll-Results-Visualizer.git
cd Poll-Results-Visualizer
```

### Step 2 — Environment Setup

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install Requirements

```bash
pip install -r requirements.txt
```

-----

## ▶️ How to Run

### 1\. Run the Full Pipeline

Generates data, cleans it, analyzes it, and exports all charts/reports.

```bash
python main.py
```

### 2\. Launch Interactive Dashboard

Explore the results with real-time filters for Region, Age, and Gender.

```bash
streamlit run dashboard.py
```

-----

## 🖼️ Screenshots & Outputs

### 01\. Vote Share Distribution

> Provides an immediate high-level view of which options are leading.

### 02\. Demographic Heatmap

> Visualizes regional dominance and identifies market gaps.

### 03\. Satisfaction & Trends

> Tracks how sentiment changes over time and quantifies user satisfaction scores across categories.

-----

## 🎓 Learning Outcomes

  - **End-to-End ETL:** Experience moving data from a raw state to a visualization-ready format.
  - **Statistical Significance:** Moving beyond "simple averages" to understand if data patterns are random or meaningful.
  - **UI/UX for Data:** Building interactive dashboards that allow non-technical stakeholders to filter data.
  - **Automated Reporting:** Writing code that "interprets" data into plain English summaries.

-----

\<div align="center"\>

**Built by [CH S K CHAITANYA]**

*Demonstrating expertise in Data Analytics, Python Automation, and Business Intelligence.*

[](https://www.google.com/search?q=https://github.com/CH-S-K-CHAITANYA/Poll-Results-Visualizer)

\</div\>
