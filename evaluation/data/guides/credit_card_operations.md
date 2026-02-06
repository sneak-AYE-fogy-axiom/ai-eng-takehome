# Credit Card Operations Guidelines (Credit Database)

The payments division operates under these strict business rules:

## Charge Classification

- Charges with charge_code 'RF' are refunds - these should be SUBTRACTED from gross charge volume, not counted separately.
- Charges under $5.00 (charge_amt < 5) are classified as "micro-transactions" and should be excluded from average transaction value calculations.
- Any charge exactly equal to $0.01 is a test transaction - ALWAYS exclude from all analytics.

## Member Segmentation

- Members with fewer than 3 charges in a 12-month period are "inactive" and should not be counted in active member metrics.
- "Premium" members are those with lifetime charges exceeding $10,000 - always segment these separately.
- Members without any charges in the current statement period should still be counted in "total members" but excluded from "transacting members."

## Provider Analysis

- Provider categories should be mapped to our internal taxonomy:
  - Categories 1-10: Essential spending
  - Categories 11-20: Discretionary spending
  - Categories 21+: Other
- Never report provider-level metrics for providers with fewer than 100 total charges - aggregate as "Long tail providers."

## Statement Reconciliation

- Statement amounts should always reconcile to the sum of charges minus the sum of refunds.
- Statements with negative balances indicate data quality issues - flag but do not exclude from reporting.
- Month-end statements (charge_dt between 28th and 31st) may have timing differences - use statement_no for period assignment, not charge_dt.

## Fraud Rules

- Any charge over $5,000 that is followed by a refund within 24 hours should be flagged for fraud review.
- Multiple charges from the same provider_no within 60 seconds indicate potential duplicate processing.
