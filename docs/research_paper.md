# Customer Segmentation & Churn Pattern Analytics in European Banking

**Exploratory analysis and recommendations**  
Prepared 7 November 2026

## Abstract

This paper describes churn patterns in a supplied customer-level banking dataset of 10,000 records from France, Germany, and Spain. The overall observed churn rate is 20.37% (2,037 customers). Churn rates vary across geography, age, gender, activity, and number of products. Germany has the highest country rate (32.4%); customers aged 46–59 have the highest age-band rate (51.1%); inactive members churn at 26.9%, compared with 14.3% of active members. A high-balance proxy cohort, defined as positive balances at or above the 75th percentile of positive balances, contains 1,596 customers and has a 23.0% churn rate. These are descriptive associations in one dataset, not estimates of causal effects or future risk. Recommendations focus on investigating service and engagement patterns, validating unusual product-count results, and evaluating retention programs with controlled measurement.

## 1. Background and objectives

Customer churn can affect the stability of a retail bank’s customer relationships. Aggregate churn alone does not show which groups account for more exits or whether groups with different profiles have different observed rates. This project uses the supplied dataset to answer three descriptive questions:

1. What proportion of the listed customers are marked as churned?
2. How do customer counts, churn rates, and churn contributions vary across the available segments?
3. What financial and engagement patterns are present among churned customers, including customers with higher positive balances?

The dashboard supports exploration of these questions. It does not make individual retention decisions or produce a churn prediction model.

## 2. Data and scope

The source is `European_Bank.csv` in this repository. It has 10,000 rows and 14 columns: `Year`, customer identifier and surname, credit score, geography, gender, age, tenure, balance, product count, card ownership, activity, estimated salary, and the churn label `Exited`. In the supplied file, customer IDs are unique, the required fields contain no missing values, and all three binary fields (`HasCrCard`, `IsActiveMember`, and `Exited`) contain valid 0/1 values.

The geographic groups are France (5,014 customers), Germany (2,509), and Spain (2,477). All records have `Year = 2025`; the analysis treats that field as a dataset label because its meaning is not documented. The repository does not identify the dataset’s original publisher, sampling frame, or currency. Values for balance and estimated salary are therefore shown in source units.

## 3. Methodology

### 3.1 Validation and measures

The dashboard checks the required schema, nonempty input, unique customer IDs, binary engagement and churn fields, and finite numeric analysis fields. It groups missing derived segment values as `Unknown`. Churn rate is calculated as:

> churn rate = customers with `Exited = 1` ÷ customers in the group

Churn contribution is a group’s share of all churned customers in the population currently being summarized:

> churn contribution = churned customers in the group ÷ all churned customers

Contribution depends on both segment size and churn rate. It should not be interpreted as a risk score.

### 3.2 Segment definitions

- **Age:** under 30, 30–45, 46–59, and 60+.
- **Credit score:** dataset-relative tertiles. The observed cutoffs are 608 and 695: Low ≤608, Medium 609–695, and High >695. These are not lending or credit eligibility thresholds.
- **Tenure:** New (0–2 years), Mid-term (3–6 years), and Long-term (7+ years).
- **Balance:** zero, negative (if present), and positive balance split at the median of positive balances. The observed positive-balance median is 119,839.69 source units.
- **Products and activity:** recorded product count; Active and Inactive according to `IsActiveMember`.
- **High-value proxy:** balance ≥ the 75th percentile among customers with a positive balance. The observed threshold is 139,512.29 source units. Customers with higher balances are not necessarily more profitable or more valuable over their lifetime.

Rates are unweighted descriptive proportions. No confidence intervals, significance tests, causal estimates, or predictive model were produced.

## 4. Results

### 4.1 Overall churn

Of 10,000 listed customers, 2,037 are marked as churned and 7,963 as retained. The overall observed churn rate is **20.37%**.

### 4.2 Geography

| Country | Customers | Churned | Churn rate | Share of all churn |
|---|---:|---:|---:|---:|
| France | 5,014 | 810 | 16.2% | 39.8% |
| Germany | 2,509 | 814 | 32.4% | 40.0% |
| Spain | 2,477 | 413 | 16.7% | 20.3% |

Germany has about half as many listed customers as France but a similar number of churned records. Its observed rate is nearly twice France’s and Spain’s. This makes Germany a useful starting point for aggregate investigation; the data alone does not explain the difference.

### 4.3 Age and geography-by-age patterns

| Age group | Customers | Churned | Churn rate | Share of all churn |
|---|---:|---:|---:|---:|
| Under 30 | 1,641 | 124 | 7.6% | 6.1% |
| 30–45 | 6,248 | 956 | 15.3% | 46.9% |
| 46–59 | 1,585 | 810 | 51.1% | 39.8% |
| 60+ | 526 | 147 | 27.9% | 7.2% |

The 46–59 band is 15.9% of the dataset but accounts for 39.8% of churned records. It has the highest observed rate in each country:

| Age group | France | Germany | Spain |
|---|---:|---:|---:|
| Under 30 | 5.2% | 12.6% | 7.9% |
| 30–45 | 11.9% | 25.3% | 12.5% |
| 46–59 | 45.5% | 67.3% | 40.8% |
| 60+ | 24.8% | 41.5% | 21.7% |

These subgroup comparisons are useful for further research but do not establish that age or geography causes churn. Age is a sensitive demographic attribute and should not be used alone to target or restrict services.

### 4.4 Gender and engagement

The observed churn rate is 25.1% among female customers (1,139 of 4,543) and 16.5% among male customers (898 of 5,457). This difference should prompt careful aggregate review of product, service, and channel experiences. It is not evidence that gender itself explains exits, and it should not be used as the sole basis for individual treatment.

Inactive customers have a 26.9% churn rate (1,302 of 4,849); active customers have a 14.3% rate (735 of 5,151). Inactive customers account for 63.9% of all churned records. The dataset provides a single activity indicator, not a history of when or how engagement changed, so it cannot identify a reliable early-warning sequence.

### 4.5 Product count, tenure, credit score, and balance

| Segment | Customers | Churned | Churn rate |
|---|---:|---:|---:|
| 1 product | 5,084 | 1,409 | 27.7% |
| 2 products | 4,590 | 348 | 7.6% |
| 3 products | 266 | 220 | 82.7% |
| 4 products | 60 | 60 | 100.0% |

The 3- and 4-product groups have very high observed rates but only 326 customers combined. Their results should be validated against product definitions, eligibility rules, and source quality before proposing interventions. The 1-product segment is much larger and contributes 69.2% of all churned records.

Tenure rates are comparatively close: 21.2% for 0–2 years, 20.6% for 3–6 years, and 19.5% for 7+ years. Credit-score rates range narrowly from 19.8% in the Medium and High groups to 21.5% in the Low group; these dataset-relative bands show little separation.

Churn is 13.8% among zero-balance customers, 24.0% among customers with low positive balances, and 24.2% among those with high positive balances. Churned customers’ median balance is 109,349.29 source units, versus 92,072.68 for retained customers. These account balances are not revenue, profit, or customer lifetime value.

### 4.6 High-balance proxy cohort

The high-balance cohort contains 1,596 customers (15.96% of the dataset), of whom 367 are churned. Its churn rate is **23.0%**, and it contributes **18.0%** of all churned records. The sum of account balances for these 367 churned customers is **58,714,368.09 source units**. This is a descriptive balance exposure measure only; it is not an estimate of revenue lost.

| Country | Customers | Churned | Churn rate | Balance on churned accounts (source units) |
|---|---:|---:|---:|---:|
| France | 694 | 152 | 21.9% | 24,949,803.77 |
| Germany | 568 | 139 | 24.5% | 20,918,329.26 |
| Spain | 334 | 76 | 22.8% | 12,846,235.06 |

Estimated salary medians are 102,460.84 source units for churned customers and 99,645.04 for retained customers. The difference is modest in this dataset and should not be treated as bank revenue or a measure of ability to pay.

## 5. Recommendations

1. **Investigate the Germany pattern at aggregate level.** Review service, channel, onboarding, and product experience by country and age band. The Germany 46–59 group has the highest observed rate (67.3%), but validate group definitions and sample context before taking action.
2. **Study engagement changes over time.** Inactivity is associated with higher churn in this snapshot. If operational data permits, analyze prior activity histories and test voluntary, service-oriented outreach against a comparison group.
3. **Validate high product-count records.** Confirm how three and four products are defined, whether those combinations are intended, and whether the small cohorts are stable in another period. Avoid building broad policy on the 60-customer four-product group.
4. **Include high-balance churn in retention research.** Review the 367 churned customers in the proxy cohort using service and relationship history. Balance alone is not a profit or lifetime-value measure.
5. **Track both rates and counts.** Report customer count, churn count, churn rate, and contribution together so small high-rate groups are not mistaken for the largest source of churn.
6. **Evaluate interventions, not demographic stereotypes.** Test program impact with a pre-defined comparison or holdout and review outcomes for fairness. Do not make individual eligibility or service decisions from these descriptive segment rates.

## 6. Limitations

- The data’s original source, sampling frame, representativeness, and licensing are not documented in the repository.
- One value (`2025`) appears in `Year`; there is no time series with which to analyze churn trends or timing.
- There are no transaction histories, service contacts, products’ revenue or cost, churn reasons, acquisition channels, or customer lifetime values.
- Balance and estimated-salary currencies or units are unspecified. Financial measures are labeled in source units.
- Segment differences are descriptive. No confounder adjustment, inferential tests, or causal design was used.
- Some rates are based on small groups, particularly 3- and 4-product customers.
- The high-value threshold is recalculated from this dataset and may not transfer to another bank or period.

## 7. Reproducibility

Run the dashboard from the repository root with `pip install -r requirements.txt` followed by `streamlit run app.py`. The dashboard loads `European_Bank.csv` from the same directory. Segment thresholds are computed from that file at runtime. KPI definitions and setup details are in the repository [README](../README.md).
