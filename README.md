# Customer Segmentation & Churn Pattern Analytics

A Streamlit project for exploring customer churn patterns in European banking.
The current version establishes the dashboard layout and navigation. Analytics
and dataset integration are planned for later development milestones.

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

## Data

The customer-level `European_Bank.csv` file is intentionally excluded from Git.
It contains customer identifiers and financial fields. Keep the source data in
the project folder locally; the dashboard will connect to it in a later
milestone.

## Current scope

- Dark banking analytics dashboard foundation
- Overview page with clearly marked, empty KPI and chart placeholders
- Navigation placeholders for future analysis sections
- No customer metrics are calculated or displayed yet
