# Election and Polling Analytics (ElectionDB Database)

The political analytics team follows these conventions:

## Poll Methodology

- Only polls from pollsters with a FiveThirtyEight rating of B/C or higher should be included in aggregation models.
- Live-caller polls are weighted 1.5x vs. online panels (1.0x) vs. IVR/robo-polls (0.75x) in poll aggregation.
- Polls must report sample size and margin of error - polls without these fields are excluded from all analysis.
- Likely Voter (LV) screens produce more accurate results than Registered Voter (RV) samples - use LV when both are available.
- "Internal polls" (commissioned by campaigns) have a known house effect and should be flagged, not excluded, with a credibility discount.

## Election Results

- Results are reported at precinct level (finest granularity), then aggregated to: Ward → County → Congressional District → State → National.
- Provisional and mail-in ballots may take 7-14 days to fully count - results before certification are "unofficial."
- Write-in candidates receiving < 1% are aggregated as "Other" for reporting; > 1% are named individually.
- Runoff elections are separate events from the primary or general election - never combine results.
- Recount results replace the original results; the original should be retained as `result_version = 'pre-recount'`.

## Turnout Calculations

- Voter turnout = (total votes cast) / (eligible voting population) × 100. NOT registered voters.
- VEP (Voting Eligible Population) excludes non-citizens and disenfranchised persons - use this denominator, not VAP (Voting Age Population).
- Early voting and mail-in ballots are included in total turnout but tracked separately for logistics planning.
- Same-day registration jurisdictions have different turnout dynamics than states with registration deadlines.
- Turnout comparisons across elections must account for the type of election: Presidential > Midterm > Off-year > Special.

## Demographic Analysis

- Exit poll data is survey-based with margins of error of ±3-5% for subgroups - report confidence intervals.
- Ecological inference (inferring individual behavior from aggregate data) carries the "ecological fallacy" risk - always caveat.
- Racial/ethnic demographic data uses Census categories; self-reported racial identity in polls may differ.
- Age cohort analysis: 18-29, 30-44, 45-64, 65+. Never report results for age groups with < 100 respondents.
- Gender gap (difference in party preference between men and women) is reported as a spread, not individual numbers.

## Redistricting and Boundaries

- District boundaries change after each decennial Census - always specify the redistricting cycle in use.
- Precinct boundaries can change between elections even within the same decade - match precincts to the correct vintage.
- Gerrymandering metrics (efficiency gap, compactness scores, mean-median difference) require the full district map.
- Incumbency advantage should be calculated controlling for partisanship (PVI - Partisan Voting Index).
- Uncontested races (only one candidate) should be excluded from partisan swing analysis.

## Campaign Finance

- Contributions are classified as: Individual, PAC, Party, Self-Funded, Small-Dollar (< $200), Large-Dollar (≥ $200).
- Bundled contributions (collected by intermediaries) should be attributed to both the bundler and original donors.
- Independent expenditures (Super PAC spending) are tracked separately from direct campaign spending.
- In-kind contributions (donated goods/services) must be valued at fair market value.
- Dark money (501(c)(4) spending without donor disclosure) is tracked by spending amount but cannot be attributed to donors.

## Forecasting

- Forecast models must be evaluated by calibration (did events with 70% probability happen ~70% of the time?).
- "Toss-up" classification: any race where neither candidate has > 55% win probability in the forecast.
- Correlated outcomes (if one swing state shifts, others may too) must be modeled - do not treat state-level races as independent.
- Late-breaking trends (final 2 weeks) can shift results by 2-3 points - weight recent polls higher.
- Forecast uncertainty should increase for unprecedented scenarios (e.g., third-party candidates, pandemic elections).
