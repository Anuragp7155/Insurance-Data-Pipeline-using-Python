# Insurance Data Pipeline using Python

## Project Overview

This project implements an end-to-end Insurance Data Pipeline using Python.

The pipeline processes insurance-related source data through multiple data layers:

**Source → Ingestion & Validation → Preprocessed → Curated → Semantic → KPI Reporting → Archive**

The main objective is to automate data ingestion, validation, preprocessing, transformation, KPI generation, audit logging, testing, and retention using Python.

---

## Project Objectives

The main objectives of this project are:

- Ingest insurance source files using Python.
- Validate incoming files against control files.
- Perform data quality checks.
- Clean and preprocess the source data.
- Add audit and file-date information.
- Store processed data in Parquet format.
- Create an enriched Curated dataset using joins.
- Generate Semantic KPI datasets.
- Maintain audit logs for pipeline execution.
- Archive processed files for retention.
- Perform unit testing for important pipeline components.
- Build a reusable and maintainable ETL pipeline.

---

## Technology Stack

- **Python**
- **Pandas**
- **NumPy**
- **JSON**
- **PyArrow**
- **Parquet**
- **Pathlib**
- **Shutil**
- **Regular Expressions**
- **Excel**
- **Git & GitHub**

---

## Project Architecture

```text
                    SOURCE FILES
                         |
                         v
              +----------------------+
              | Ingestion &          |
              | Validation           |
              +----------------------+
                         |
                         v
              +----------------------+
              | Preprocessed Layer   |
              | Cleaning & Audit     |
              +----------------------+
                         |
                         v
              +----------------------+
              | Curated Layer        |
              | Data Enrichment      |
              +----------------------+
                         |
                         v
              +----------------------+
              | Semantic Layer       |
              | KPI Aggregation      |
              +----------------------+
                         |
                         v
                  KPI REPORTING
                         |
                         v
                  DATA ARCHIVE

---
```
## Project Structure
```

InsuranceDataPipeline/
│
├── config/
│   └── control_files/
│       ├── agents_20250818.json
│       ├── claims_20250818.json
│       ├── customers_20250818.json
│       ├── payments_20250818.json
│       └── policies_20250818.json
│
├── data/
│   ├── ingestion/
│   ├── preprocessed/
│   ├── curated/
│   ├── semantic/
│   └── retention/
│       └── archive/
│
├── logs/
│
├── src/
│   ├── ingestion_manager.py
│   ├── preprocessing.py
│   ├── curated_engine.py
│   ├── semantic_engine.py
│   ├── retention_manager.py
│   └── main.py
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_preprocessing.py
│   ├── test_semantic.py
│   ├── test_retention.py
│   └── test_error_handling.py
│
├── README.md
└── requirements.txt

