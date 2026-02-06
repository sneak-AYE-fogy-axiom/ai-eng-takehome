# Formula 1 Racing Data Guidelines (ErgastF1 Database)

The motorsports analytics division follows these strict conventions:

## Points and Standings

- Pre-2010 points systems are incompatible with modern scoring. When comparing drivers across eras, ONLY use position-based rankings, not points.
- DNF (Did Not Finish) results should still count toward "races entered" but NOT toward "races completed" metrics.
- A podium finish is a position 1, 2, or 3.
- Position values of 0 or NULL indicate disqualification - these must be excluded from podium, points, and top-10 finish calculations.

## Lap Time Analysis

- Lap times from wet races (flagged in race metadata) should NEVER be compared with dry race lap times.
- Fastest lap times with rank > 10 are statistically unreliable due to track evolution - exclude from benchmark analyses.
- Any lap time under 60 seconds is likely a data error - exclude from all calculations.

## Constructor Performance

- When measuring constructor reliability, only count races where BOTH cars started.
- Constructor results before 1980 should be reported separately as "historical era" and not combined with modern statistics.
- Points scored during sprint races (introduced 2021) must be reported in a separate column, never combined with main race points.

## Driver Comparisons

- Only compare teammates who raced at least 10 races together in the same season.
- Drivers with fewer than 20 career starts should be classified as "rookies" regardless of their tenure.
