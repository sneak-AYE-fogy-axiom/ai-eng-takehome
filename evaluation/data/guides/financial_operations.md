# Financial Database Business Rules

When analyzing financial data from the `financial` database, the following rules MUST be observed:

## Loan Classifications

- Loans with status 'A' are considered "performing" loans and should be included in standard metrics.
- Loans with status 'B' are "watch list" loans - exclude them from default rate calculations but include them in total portfolio size.
- Loans with status 'C' or 'D' are non-performing - these should NEVER be counted in profitability metrics.

## Transaction Handling

- All transactions with k_symbol = 'UROK' (interest) or NULL should be excluded from revenue calculations - we only count fee-based income with known categorization.
- When calculating account balances, ignore any transaction dated before 1995-01-01 as these are from a legacy system migration and are unreliable.
- Credit transactions (type = 'PRIJEM') under 1000 units should be classified as "micro-deposits" and excluded from average deposit calculations.

## District Aggregations

- District ID 1 (Prague) must always be reported separately from other districts.
- Districts 70-77 were merged in our operational model - aggregate them as a single "Eastern Region" entity.
- Never report district-level metrics for districts with fewer than 50 accounts - use "Other" as a catch-all category.
