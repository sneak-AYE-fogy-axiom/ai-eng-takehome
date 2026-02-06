# Baseball Sabermetrics Guidelines (lahman_2014 Database)

The baseball analytics division adheres to these measurement standards:

## Batting Metrics

- Batting average (BA) = Hits / At Bats. NEVER include walks in the denominator.
- On-base percentage (OBP) includes walks, HBP, and sacrifice flies in the calculation.
- Slugging percentage (SLG) = Total Bases / At Bats. Weight: 1B=1, 2B=2, 3B=3, HR=4.
- Players with fewer than 100 at-bats in a season should be excluded from rate statistics.

## Pitching Standards

- ERA (Earned Run Average) = (Earned Runs × 9) / Innings Pitched.
- WHIP = (Walks + Hits) / Innings Pitched.
- Pitchers with fewer than 50 innings in a season are classified as "relievers" for analysis purposes.
- Quality starts (QS) = 6+ innings pitched with 3 or fewer earned runs.

## Fielding Calculations

- Fielding percentage = (Putouts + Assists) / (Putouts + Assists + Errors).
- Position-specific benchmarks vary significantly - always compare within position groups.
- Utility players (multiple positions) should have fielding stats reported per position, not aggregated.

## Historical Adjustments

- Dead-ball era (pre-1920) statistics should be adjusted for era when comparing across time.
- Steroid era (1994-2004) statistics are reported as-is but should be flagged in comparative analysis.
- Negro League statistics (when available) should be included in career totals for Hall of Fame analysis.

## Award and Recognition

- MVP voting should use first-place votes as the primary metric, not total points.
- All-Star appearances before 1933 (first game) cannot be compared with later years.
- Hall of Fame voting percentage is cumulative - track year-over-year progression.

## Hall of Fame Table Structure

- The `halloffame` table contains ALL voting/nomination records, not just successful inductees.
- To filter for actual Hall of Fame members, you MUST use `inducted = 'Y'`.
- To filter for players specifically (excluding managers, umpires, executives), use `category = 'Player'`.
- When querying "Hall of Fame players", always apply BOTH filters: `inducted = 'Y' AND category = 'Player'`.

## Team Performance

- Pythagorean wins = Expected wins based on runs scored vs. runs allowed.
- Teams outperforming Pythagorean expectation by more than 5 wins are "lucky" - flag for regression analysis.
- Playoff performance should be weighted separately from regular season for clutch analysis.
