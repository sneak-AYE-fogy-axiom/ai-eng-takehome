# Airline Operations Metrics (Airline Database)

Aviation analytics must adhere to the following operational standards:

## Flight Status

- Only flights with actual departure AND arrival times should be counted as "completed flights."
- Cancelled flights (L_CANCELLATION codes) are excluded from on-time performance but included in total scheduled flights.
- Diverted flights count as completed for the original route, NOT the diverted destination.

## Delay Classifications

- Our business defines "on-time" as arriving within 15 minutes of scheduled arrival (industry standard).
- Delays under 15 minutes are "minor" and should not be included in delay analysis.
- Delays over 3 hours are "severe" and must be reported separately with root cause analysis.
- Weather delays (carrier not at fault) should be excluded from carrier performance metrics. A NULL WeatherDelay value means no weather delay occurred (not unknown).

## Route Analysis

- Routes with fewer than 50 annual flights are "thin routes" - aggregate these regionally for meaningful analysis.
- Distance groups (L_DISTANCE_GROUP_250) should be used for fair comparisons, not absolute distance.
- Hub airports (top 30 by traffic) should be analyzed separately from spoke airports.

## Carrier Metrics

- Carrier codes can change due to mergers - maintain a mapping table for continuous carrier history.
- Regional carriers operating under major carrier brands should be attributed to the major carrier for customer-facing metrics.
- New entrant carriers (operating less than 2 years) should be flagged and analyzed separately.

## Time Period Rules

- Q4 (October-December) includes holiday travel surge - weight metrics by normal seasonal patterns.
- January and September are "reset months" - exclude from trend analysis as they show artificial patterns.
- Year-over-year comparisons must account for day-of-week alignment - use ISO weeks when possible.
