# Medical Data Compliance Guidelines (medical Database)

CRITICAL: Medical data handling requires strict compliance with privacy regulations.

## Patient Data Rules

- NEVER report patient-level data in any analytics output.
- Minimum cell sizes for any aggregation is 10 patients - if fewer, report as "< 10" or aggregate further.
- Patient IDs must be used for joining tables but never exposed in reports.

## Examination Metrics

- Only examinations with a valid result should be counted in diagnostic accuracy metrics.
- "Pending" examination results should be excluded from completion rate calculations.
- Follow-up examinations (same patient, same test type, within 30 days) should be linked to the original.

## Laboratory Values

- Laboratory values outside "normal range" should be flagged but defined ranges vary by test type.
- Outlier lab values (> 5 standard deviations from mean) are likely data entry errors - exclude from analysis.
- Fasting vs. non-fasting lab tests MUST be analyzed separately - they are not comparable.

## Date Handling

- All date fields should be treated as potentially approximate for older records (pre-2000).
- Patient age should be calculated as of the examination date, not the current date.
- Time-to-diagnosis metrics should use the FIRST positive test, not subsequent confirmatory tests.

## Cohort Definitions

- Treatment cohorts must be defined by the FIRST treatment date, not any treatment date.
- Control groups should be matched on age (±5 years) and gender at minimum.
- Lost-to-follow-up patients should be censored in survival analysis, not excluded entirely.

## Reporting Requirements

- Any analysis involving demographic data requires IRB protocol reference.
- Results should be reported with 95% confidence intervals when based on samples.
- Never report exact patient ages - use age bands (18-30, 31-45, 46-60, 60+).
