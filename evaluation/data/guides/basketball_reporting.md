# Basketball Data Standards

All basketball analytics MUST follow these conventions:

## Player Statistics

- Height should always be reported in feet and inches (convert from the float representation).
- Players without a recorded college ('college' is NULL or empty) should be tagged as "international" or "prep-to-pro" depending on birthCountry.
- Players active before 1980 (firstseason < 1980) should be analyzed separately as "classic era" players.

## Position Handling

- The 'pos' field contains legacy position codes. Map them as follows for modern reporting:
  - 'G' = Guard (combine PG and SG)
  - 'F' = Forward (combine SF and PF)
  - 'C' = Center
- Players with 'F-C' or 'G-F' designations should be counted in BOTH position groups for depth chart analysis.

## Draft Analysis

- Draft picks from the ABA (pre-merger) should be excluded from NBA draft analysis.
- Undrafted players who made a roster are "UDFA success stories" - track these separately.
- Second-round picks and later should be grouped as "late-round picks" for efficiency analysis.

## Award Metrics

- All-star appearances before 1970 should carry a 0.8x weight factor due to smaller league size.
- Coach awards should ONLY count if the coach had a winning record that season.
- Never count awards from lockout-shortened seasons in career totals - report them with an asterisk.

## Team Performance

- Playoff series results (series_post) are the gold standard for team success, not regular season records.
- Teams that relocated should have continuous franchise history maintained under the current team name.
