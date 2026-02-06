# Sales Database Reporting Standards (SalesDB / Northwind)

The commercial operations team follows these reporting conventions:

## Revenue Recognition

- Revenue is recognized on the order date, NOT the ship date.
- Orders with "Cancelled" status should be completely excluded from all revenue metrics.
- Partial shipments should be reported at full order value when order is placed, not when items ship.

## Product Metrics

- Discontinued products should be excluded from "active catalog" counts but included in historical sales analysis.
- Products with unit price = $0 are samples or promotional items - track separately, not as revenue.
- Inventory value is calculated at cost, not at retail price - never mix these in reports.

## Customer Segmentation

- Customers with lifetime purchases > $50,000 are "Enterprise" tier.
- Customers with lifetime purchases > $10,000 but < $50,000 are "Professional" tier.
- All others are "Standard" tier.
- Customer counts should reflect customers with at least 1 completed order, not just registered accounts.

## Employee Attribution

- Sales attributed to employees must use the employee assigned at ORDER time, not current assignment.
- Territory reassignments should not retrospectively change historical attribution.
- Managers should NOT receive credit for individual sales made by their team members - track separately.

## Discount Handling

- The "Discount" field is a percentage (0.0 to 1.0) - never confuse with dollar amounts.
- Orders with discounts > 25% require management approval verification in compliance reports.
- Net revenue = Gross revenue × (1 - Discount) - always report both gross and net.

## Time Period Rules

- Fiscal quarters are calendar-aligned (Q1 = Jan-Mar).
- Year-over-year comparisons should account for the number of business days, not calendar days.
- December 20-31 is a "freeze period" - orders placed but not yet shipped may inflate period-end metrics.
