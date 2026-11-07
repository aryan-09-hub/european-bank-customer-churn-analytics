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
- **Geography & demographics:** churn comparisons by country, age, gender, and country by age.
- **Customer segments:** age, dataset-relative credit score, tenure, balance, product count, and activity comparisons.
- **High-value explorer:** customers with positive balances at or above the 75th percentile of positive balances; filters for country, age, balance, and activity.

Missing analytical segment values are grouped as Unknown. Credit-score tertiles and balance medians are descriptive cutoffs from this dataset. The high-value criterion is a balance proxy, not a measure of customer lifetime value. Balances held by churned customers are not reported as lost revenue or profit.

## Repository

The project is maintained at [european-bank-customer-churn-analytics](https://github.com/aryan-09-hub/european-bank-customer-churn-analytics).
