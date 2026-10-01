# Retail Sales Data Engineering Pipeline

An end-to-end data engineering pipeline that extracts raw retail sales data,
performs data quality validation and transformation using Python and Pandas,
loads the processed data into a PostgreSQL data warehouse running in Docker,
and provides SQL-based business analytics.

## Architecture

```text
Raw CSV
   |
   v
Python + Pandas
   |
   v
ETL Pipeline
   |
   +-- Data Validation
   +-- Duplicate Detection
   +-- Invalid Record Handling
   +-- Data Transformation
   |
   v
Processed Data
   |
   v
PostgreSQL (Docker)
   |
   v
Star Schema
   |
   +-- dim_customer
   +-- dim_product
   +-- dim_date
   +-- fact_sales
   |
   v
SQL Analytics

Technologies
Python
Pandas
NumPy
SQL
PostgreSQL
Docker
psycopg2
python-dotenv
ETL
Data Warehousing
Dimensional Data Modeling
 
retail-sales-data-pipeline/
|
├── data/
│   ├── raw/
│   │   └── sales.csv
│   └── processed/
│
├── src/
│   ├── etl.py
│   ├── load_warehouse.py
│   ├── run_pipeline.py
│   └── inspect_data.py
│
├── sql/
│   ├── create_schema.sql
│   └── analytics.sql
│
├── config/
├── .env
├── .gitignore
├── docker-compose.yml
├── requirements.txt
└── README.md

ETL Process
Extract

Raw sales data is extracted from a CSV source using Pandas.

Transform

The pipeline:

Converts order dates into a proper date format
Removes duplicate orders
Removes records with invalid quantities
Handles missing critical values
Calculates revenue
Creates year and month attributes
Produces a cleaned dataset
Load

The processed data is loaded into a PostgreSQL data warehouse.

The warehouse uses a star schema consisting of:

Customer dimension
Product dimension
Date dimension
Sales fact table
Data Quality

The raw dataset intentionally contains data-quality issues to demonstrate
validation and transformation.

The pipeline identifies:

Duplicate records
Invalid quantities
Missing critical values

The original dataset contains 13 records and the processed dataset contains
10 valid records.

Idempotent Loading

The fact table uses a unique constraint on order_id combined with
ON CONFLICT DO NOTHING.

This prevents duplicate fact records when the pipeline is executed multiple
times.

For example:
First execution  -> 10 records
Second execution -> 10 records
Third execution  -> 10 records

Analytics

The SQL analytics layer provides:

Total revenue
Total orders
Total quantity sold
Average order value
Monthly revenue
Revenue by region
Revenue by product category
Top-performing products
Customer revenue
Monthly category performance
Example Results

Using the current sample dataset:

Total Revenue: ₹14,050
January Revenue: ₹5,250
February Revenue: ₹4,450
March Revenue: ₹4,350
Furniture Revenue: ₹6,850
Electronics Revenue: ₹4,950
Stationery Revenue: ₹2,250
Running the Project
1. Start PostgreSQL
docker compose up -d
2. Activate the Python environment
source .venv/bin/activate
3. Run the complete pipeline
python src/run_pipeline.py
4. Run analytics

The SQL queries are available in:
sql/analytics.sql

Key Data Engineering Concepts Demonstrated
ETL pipeline design
Data quality validation
Data cleaning and transformation
Relational database design
Star schema
Fact and dimension tables
SQL aggregation and joins
Dockerized PostgreSQL
Idempotent data loading
Environment-based configuration


Save it.

---

# 7. One important README correction

We **shouldn't claim SQLAlchemy is being used in the actual loader if it isn't**.

Our current loader uses `psycopg2` directly.

So either we use SQLAlchemy in the project, or we remove it from the README/requirements.

Since we're trying to keep the project clean, I'd **remove SQLAlchemy for now**.

Run:

```bash
pip uninstall sqlalchemy -y
