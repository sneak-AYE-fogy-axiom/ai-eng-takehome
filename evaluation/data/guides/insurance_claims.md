# Insurance Claims Analytics (InsureDB Database)

The actuarial analytics team follows these conventions:

## Claim Classification

- Claims are classified by line of business: Auto, Property, General Liability, Workers' Comp, Professional Liability, Life.
- NEVER combine claims across lines of business in the same analysis without explicit approval.
- "Incurred But Not Reported" (IBNR) claims are estimates and must be clearly labeled as such in all reports.
- Subrogation recoveries reduce claim costs but must be tracked separately - never net them against gross claims.
- Reopened claims (previously closed, now active again) retain their original claim number with a revision suffix.

## Loss Calculations

- Incurred loss = Paid losses + Outstanding reserves (case reserves + IBNR).
- Loss ratio = Incurred losses / Earned premium × 100. Target varies by line: Auto (65-70%), Property (55-65%), GL (60-70%).
- Expense ratio = Underwriting expenses / Written premium × 100.
- Combined ratio = Loss ratio + Expense ratio. Below 100% indicates underwriting profit.
- Development factors (link ratios) must use the actuarial triangle method - at least 10 accident years for credibility.

## Severity Tiers

- Low severity: < $10,000 paid
- Medium severity: $10,000 - $100,000 paid
- High severity: $100,000 - $1,000,000 paid
- Catastrophic: > $1,000,000 paid
- Severity analysis must be inflation-adjusted using the appropriate index (CPI for property, medical CPI for bodily injury).

## Policy Handling

- Written premium is recorded at policy inception; earned premium is recognized ratably over the policy period.
- Mid-term endorsements (policy changes) create a new version - always use the latest version for in-force reporting.
- Cancelled policies earn premium only through the cancellation effective date.
- Renewal retention rate = (renewed policies / expiring policies) × 100. Exclude non-renewals initiated by the insurer.
- Multi-year policies should be annualized for comparison with single-year policies.

## Fraud Detection

- Claims flagged for Special Investigation Unit (SIU) review are excluded from standard loss metrics until resolved.
- "Red flag" indicators include: claim filed within 60 days of policy inception, multiple claims in 12 months, prior claim history.
- Fraud rate is calculated as (confirmed fraudulent claims / total investigated claims), not total claims.
- Tip-line reports are tracked separately from algorithm-detected suspicious claims.
- Attorney-represented claims average 3.5x higher payments - flag these for litigation management analysis.

## Catastrophe Events

- CAT-coded claims (hurricanes, earthquakes, wildfires) are segregated from attritional (non-catastrophe) losses.
- A catastrophe event requires > $25 million in industry-wide insured losses to receive a PCS (Property Claim Services) serial number.
- CAT losses should be shown both gross (before reinsurance) and net (after reinsurance) in all executive reporting.
- Demand surge (inflated repair costs post-catastrophe) should be factored into reserve adequacy assessments.
- Catastrophe modeling uses probabilistic (not deterministic) scenarios - always report exceedance probability curves.

## Regulatory Reporting

- Statutory accounting (SAP) differs from GAAP - never mix accounting bases in the same report.
- Annual Statement filings use NAIC (National Association of Insurance Commissioners) prescribed formats.
- Rate filings require loss data at the state level - do not aggregate across jurisdictions.
- Minimum loss ratios are mandated by regulators (e.g., 80% for ACA health plans) - track compliance quarterly.
- Reinsurance recoverables must be tested for collectibility annually.
