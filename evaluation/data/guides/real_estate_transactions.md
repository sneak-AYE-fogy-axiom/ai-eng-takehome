# Real Estate Transaction Standards (PropertyDB Database)

The real estate analytics division follows these conventions when querying property data:

## Property Valuation

- Assessed value and market value are NEVER interchangeable - assessed value is typically 60-80% of market value depending on jurisdiction.
- Properties with a sale price of $0 or $1 are "non-arm's-length" transactions (gifts, family transfers) and must be excluded from market analysis.
- Price-per-square-foot is the standard comparison metric for residential properties; price-per-unit for multi-family.
- Any property that sold more than twice in a 12-month period should be flagged as a potential "flip" and analyzed separately.
- Foreclosure sales (indicated by `sale_type = 'FC'`) should be excluded from fair market value calculations as they depress pricing.

## Property Classification

- Residential properties are classified by unit count: Single-family (1 unit), Duplex (2), Triplex (3), Quad (4), Multi-family (5+).
- Commercial properties must be categorized by use type: Retail, Office, Industrial, Mixed-Use, Hospitality.
- Vacant land parcels should never be included in "improved property" metrics - they skew average values downward.
- Properties built before 1940 are "historic" and may have different renovation cost assumptions.
- Any property with lot size > 10 acres in an urban zone should be verified - likely a data entry error.

## Tax Assessment Rules

- Tax assessments more than 3 years old are considered "stale" and should be flagged for reassessment.
- Homestead exemptions reduce taxable value - always distinguish between gross and net assessed value.
- Properties with active tax liens must be reported separately in portfolio health dashboards.
- Agricultural exemptions (ag-exempt) properties should use agricultural value, not market value, for tax calculations.
- When comparing tax rates across jurisdictions, always normalize to effective tax rate (tax paid / market value).

## Geographic Aggregation

- Never report neighborhood-level statistics with fewer than 20 transactions - aggregate to the ZIP code level.
- School district boundaries, not municipal boundaries, are the primary geographic unit for residential analysis.
- Waterfront properties (within 500 feet of navigable water) command premiums and should be segmented separately.
- Flood zone designations (A, AE, V, X) must be included in risk-adjusted valuation models.
- Census tract is the preferred geographic unit for fair lending analysis.

## Temporal Adjustments

- All historical sale prices must be inflation-adjusted to current-year dollars using the Case-Shiller index.
- Seasonal adjustment is required for monthly volume reporting - Q4 consistently underperforms Q2-Q3.
- Properties sold during the 2008-2011 period should be flagged as "distressed era" and optionally excluded from trend analysis.
- Days-on-market calculations exclude weekends and federal holidays.
- Listing date, not contract date, determines which reporting period a sale belongs to.
