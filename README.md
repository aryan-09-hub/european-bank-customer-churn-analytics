# Customer Segmentation & Churn Pattern Analytics

A Streamlit dashboard and exploratory analysis of customer churn in the supplied European banking dataset. The analysis covers 10,000 customer records from France, Germany, and Spain. It describes patterns in the data; it does not predict churn or establish why customers leave.

## Project documents

- [Research paper](docs/research_paper.md): data, methods, findings, limitations, and recommendations
- [Executive summary](docs/executive_summary.md): key findings and suggested actions for decision-makers

## Run locally

1. Use Python 3.12 or another version supported by Streamlit.
2. Create and activate a virtual environment.
3. Install the listed packages and run the dashboard:

   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

The dashboard opens in a browser. Keep `European_Bank.csv` beside `app.py`.

## Data

`European_Bank.csv` contains 10,000 customer records and 14 columns. The app validates the required fields, unique customer IDs, binary status fields, and numeric analysis fields. The supplied file has no missing values or duplicate customer IDs. `Year` is 2025 in every row and is not used in the analysis. The dataset’s origin, sampling method, and currency are not documented in the repository; financial values are therefore reported in source units.

## Dashboard

- **Overview:** customer counts and churn rate, with interactive geography, age, status, and tenure filters; filters update the KPIs, charts, and segment drill-down.
- **Geography & demographics:** churn comparisons by country, age, gender, and country by age; country table includes a documented exposure index (100 = dataset-wide average).
- **Customer segments:** age, dataset-relative credit score, tenure, balance, product count, and activity comparisons.
- **High-value explorer:** customers with positive balances at or above the 75th percentile of positive balances; filters for country, age, balance, and activity; reports cohort churn share and supports filtered summary CSV export.
- Filtered segment summaries and high-value country summaries can be downloaded as CSV files.

Missing analytical segment values are grouped as Unknown. Credit-score tertiles and balance medians are descriptive cutoffs from this dataset. The high-value criterion is a balance proxy, not a measure of customer lifetime value. Balances held by churned customers are not reported as lost revenue or profit.

Age bands use non-overlapping cutoffs: under 30, 30–45, 46–59, and 60+. The examiner wording “46–60, 60+” overlaps at age 60; this project assigns age 60 to the 60+ group so every customer is counted once. The geographic exposure index is `(country share of churn ÷ country share of customers) × 100`; values above 100 mean a country contributes a greater share of observed churn than its share of customers. The engagement indicator is the inactive churn rate minus the active churn rate, expressed in percentage points. Neither is causal. Revenue risk cannot be calculated from this dataset because it has no customer revenue, cost, or lifetime-value fields.

## Repository

The project is maintained at [european-bank-customer-churn-analytics](https://github.com/aryan-09-hub/european-bank-customer-churn-analytics).
