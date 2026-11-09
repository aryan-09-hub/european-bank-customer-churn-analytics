# Executive Summary

## Customer Segmentation & Churn Pattern Analytics in European Banking

**Prepared 7 November 2026**

### Purpose

This analysis summarizes churn patterns in the supplied 2025 customer dataset for France, Germany, and Spain. It is intended to help decision-makers prioritize further investigation and retention experiments. It is descriptive: the dashboard does not predict which individual customers will leave and cannot determine why they did.

### Headline measures

| Measure | Result |
|---|---:|
| Customers in dataset | 10,000 |
| Churned customers | 2,037 |
| Overall churn rate | 20.37% |
| Retained customers | 7,963 |
| High-balance proxy cohort | 1,596 customers |
| Churn rate in proxy cohort | 23.0% |
| Share of all churn from proxy cohort | 18.0% |
| Germany geographic exposure index | 159.1 (100 = dataset average) |

### What stands out

- **Germany has the highest observed country rate:** 32.4%, compared with 16.2% in France and 16.7% in Spain. Germany has 2,509 customers and 814 churned records, approximately as many as France’s 810 despite having about half as many customers.
- **Germany contributes more churn than its customer share:** its geographic exposure index is 159.1 (100 is the dataset average), compared with 79.3 in France and 81.9 in Spain. This is a descriptive index, not a causal or individual risk score.
- **Customers aged 46–59 have the highest age-band rate:** 51.1% (810 of 1,585). In Germany this rate is 67.3%. Age and country patterns need further investigation and should not be used alone to make decisions about individuals.
- **Inactive members have a higher observed churn rate:** 26.9%, compared with 14.3% for active members. The file contains only a current activity indicator, so it does not reveal when engagement changed.
- **Three- and four-product groups have unusually high rates:** 82.7% for three products (266 customers) and 100% for four products (60 customers). Validate the product definitions and small group sizes before acting on this pattern.
- **Higher positive balance is a limited proxy for value:** customers at or above the positive-balance 75th percentile have a 23.0% churn rate. The balances on the 367 churned customers in this group sum to 58.7 million source units. This is account balance exposure, not revenue or profit lost.

### Recommended next steps

1. Review the Germany and 46–59 patterns using service, channel, onboarding, and relationship data.
2. Examine how activity changed before churn; if outreach is tested, compare results with a suitable holdout group.
3. Confirm what three- and four-product records represent and check the pattern in another period.
4. Monitor each segment with customer count, churn count, churn rate, and share of total churn together.
5. Review retention experiments for fair treatment. Do not use age or gender rates as individual targeting rules.

### Interpretation and limits

The source contains 10,000 customer records and no missing values or duplicate IDs. Its origin, sampling method, currency, and the meaning of the single `Year = 2025` field are undocumented. There are no churn reasons, transaction histories, profit measures, or customer lifetime values. Results describe this dataset only; they do not establish causes or guarantee future behavior. Financial amounts are reported in source units.

Age bands are under 30, 30–45, 46–59, and 60+. Age 60 is assigned to 60+ because the examiner’s suggested 46–60 and 60+ bands overlap. The engagement indicator compares current active and inactive members; the file has no activity history, so an engagement drop over time cannot be measured. Revenue risk also cannot be quantified without revenue, cost, or lifetime-value fields.

For definitions and detailed tables, see the [research paper](research_paper.md). For setup and dashboard details, see the [project README](../README.md).
