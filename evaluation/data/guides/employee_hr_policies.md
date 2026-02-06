# HR Data Policies (employee Database)

Human Resources data analysis must comply with the following internal policies:

## Tenure Calculations

- Employee tenure is calculated from hire_date to the current date (or termination date if applicable).
- Employees hired before 1990-01-01 are part of the "legacy workforce" and should be analyzed separately in retention studies.
- Never report individual employee ages - only aggregate statistics by decade (30s, 40s, 50s, etc.).

## Department Rules

- The "d009" department (Customer Service) was split in 2005 - historical headcount comparisons must account for this.
- Employees can appear in multiple departments (dept_emp) - for headcount, count each employee only ONCE using their most recent department.
- Department managers (dept_manager) should be excluded from non-management headcount metrics.

## Salary Analytics

- Salary data is point-in-time - always specify the effective date range when reporting compensation metrics.
- "Outlier" salaries (more than 3 standard deviations from the department mean) should be flagged but not excluded.
- Never disclose salary ranges with fewer than 5 employees - aggregate to a broader grouping to protect privacy.

## Title Progression

- Title changes within 90 days of hire are "corrections" and should not count as promotions.
- The title "Senior Engineer" can only be compared with equivalent titles from after 1995 due to title inflation.
- Employees with the same title for more than 7 years should be flagged as "tenure risk" in retention reports.

## Gender Reporting

- Gender-based analytics require minimum cell sizes of 10 to be reported.
- When gender is used as a dimension, always include a "Difference" column showing gaps.
- Pay equity analysis must control for department, title, and tenure before reporting raw gender differences.
