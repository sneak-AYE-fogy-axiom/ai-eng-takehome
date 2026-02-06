# Restaurant Health Inspection Analytics (FoodSafetyDB Database)

The public health analytics division follows these conventions:

## Scoring Methodology

- Inspection scores are on a 0-100 scale where 100 is perfect. Scores below 70 are "critical failures."
- Violations are weighted: Critical (5 points each), Major (3 points), Minor (1 point). Score = 100 - sum of violation points.
- Re-inspection scores should NEVER be averaged with initial inspection scores - they represent corrective action, not baseline performance.
- Establishments with 3 consecutive scores below 80 trigger mandatory increased inspection frequency.
- Seasonal establishments (ice cream stands, fair vendors) receive fewer inspections and should be analyzed separately.

## Establishment Classification

- Full-service restaurants, fast food, cafeterias, food trucks, and catering operations are distinct categories - never aggregate across types.
- Chain establishments (3+ locations under same ownership) should have both individual and aggregate performance metrics.
- New establishments (open < 6 months) receive a "grace period" flag on their first inspection - exclude from ranking comparisons.
- Establishments that changed ownership within the past year should have their history reset - prior scores belong to the previous operator.
- "Ghost kitchens" (delivery-only) follow the same standards but are classified separately from dine-in establishments.

## Violation Tracking

- Critical violations (immediate health hazards) include: improper temperature control, contamination, pest presence, lack of handwashing.
- Repeated violations (same violation on consecutive inspections) are weighted 2x in the risk score.
- Violations corrected during inspection ("corrected on site") still count against the score but are flagged as resolved.
- Temperature violations require the specific temperature reading - missing readings invalidate the violation record.
- Allergen-related violations are tracked in a separate compliance stream with different reporting requirements.

## Inspector Calibration

- Inspector-level metrics should account for severity bias - some inspectors consistently score higher or lower.
- Normalize scores by inspector for cross-district comparisons using z-score standardization.
- Inspections lasting less than 15 minutes should be flagged as potentially incomplete.
- Inspectors must not inspect the same establishment more than 3 consecutive times to prevent familiarity bias.
- Trainee inspections (shadow inspections) are NOT official and should be excluded from all metrics.

## Temporal Rules

- Inspection frequency is risk-based: High-risk (3x/year), Medium-risk (2x/year), Low-risk (1x/year).
- Complaint-driven inspections are "unscheduled" and reported separately from routine inspections.
- Year-over-year trend analysis requires at least 3 years of data for statistical significance.
- Holiday periods (November-December) see reduced inspection activity - normalize volume metrics accordingly.
- Establishments closed for renovation > 30 days require a pre-opening inspection before resuming operations.

## Public Reporting

- Inspection results are public record but must be presented with context (date, type, follow-up status).
- Letter grades (A, B, C) are derived from scores: A = 90-100, B = 80-89, C = 70-79, below 70 = no grade posted.
- Consumer-facing dashboards must show the most recent inspection date and whether follow-up is pending.
- Closed establishments should be removed from public-facing searches within 30 days of confirmed closure.
- Personally identifiable inspector information should be redacted from public reports.
