# Consumer Expenditure Analysis Rules (ConsumerExpenditures Database)

The market research division follows these conventions:

## Household Segmentation

- Households are the unit of analysis, not individual members.
- Household size should be used to calculate per-capita spending metrics.
- Single-person households should be analyzed separately from multi-person households for many categories.

## Expenditure Classification

- Essential spending: Housing, Food at Home, Utilities, Healthcare, Transportation to Work.
- Discretionary spending: Entertainment, Dining Out, Travel, Personal Care, Apparel.
- The sum of all expenditure categories should equal total household expenditure - flag discrepancies.

## Member Demographics

- Household "head" is defined as the highest income earner, not by age or gender.
- Age of household should use the head's age for segmentation.
- Presence of children (members under 18) is a critical segmentation variable.

## Income Handling

- Income is collected in ranges - use midpoint for calculations.
- Households reporting $0 income but significant expenditure are likely misreported - flag for review.
- Top income bracket should be analyzed separately as it's unbounded.

## Temporal Adjustments

- All dollar amounts should be adjusted for inflation using CPI when comparing across years.
- Seasonal categories (heating, cooling) should be annualized, not compared month-to-month.
- Holiday quarter (Q4) spending should be decomposed into regular vs. gift spending.

## Weighting Requirements

- Survey weights MUST be applied for population estimates.
- Unweighted counts are valid for sample description only, not for population inference.
- Response rate by demographic group should be monitored for potential bias.

## Reporting Standards

- Expenditure shares (% of total) are often more meaningful than absolute dollars.
- Always report confidence intervals for survey-based estimates.
- Suppress cells with fewer than 30 unweighted observations for reliability.
