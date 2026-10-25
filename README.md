# Customer Segmentation & Churn Pattern Analytics

A Streamlit project for exploring customer churn patterns in European banking.
The current version validates the supplied customer dataset and shows the
customer total, churn rate, and retained and churned counts. Additional analysis
views are planned for later development milestones.

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
for the Overview and Geography & Demographics pages.

## Current scope

- Dark banking analytics dashboard foundation
- Loads the local `European_Bank.csv` file and validates its required schema,
  unique customer IDs, and binary engagement and churn fields
- Overview KPIs for total customers, churn rate, churned customers, and retained
  customers
- Geography and demographics page with country, age-group, gender, and
  country-by-age churn comparisons, including customer counts
- Clearly labeled placeholders for future charts and segment analysis
- Navigation placeholders for future analysis sections
