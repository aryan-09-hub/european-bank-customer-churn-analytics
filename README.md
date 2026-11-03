# Customer Segmentation & Churn Pattern Analytics

A Streamlit project for exploring customer churn patterns in European banking.
The app validates the supplied customer dataset and provides Overview,
Geography & Demographics, Customer Segments, and High-value Explorer pages.

## Run locally

1. Create and activate a Python virtual environment.
2. Install the project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

## Dataset

`European_Bank.csv` is included in this repository for the project analysis. It
contains customer-level identifiers, demographic and financial fields, and the
churn indicator. The app validates the required schema and uses these records
for every dashboard page.

## Current scope

- Dark banking analytics dashboard foundation
- Loads the local `European_Bank.csv` file and validates its required schema,
  unique customer IDs, and binary engagement and churn fields
- Overview KPIs for total customers, churn rate, churned customers, and retained
  customers
- Geography and demographics page with country, age-group, gender, and
  country-by-age churn comparisons, including customer counts
- Customer segmentation page covering age, credit score, tenure, balance,
  product count, and engagement, with counts, churn rates, and churn contribution
- Credit-score bands use dataset tertiles; positive balances split at their
  dataset median. The dashboard documents the resulting thresholds.
- High-value explorer with a disclosed top-quartile positive-balance proxy,
  filters for geography, age, balance, and activity, and balance and estimated
  salary comparisons by churn status
- Balances on churned accounts are not presented as revenue or profit lost
