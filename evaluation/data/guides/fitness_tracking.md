# Fitness and Wellness Tracking Rules (FitTrackDB Database)

The health analytics team follows these conventions for fitness data:

## Activity Classification

- Activities are classified as: Cardio, Strength, Flexibility, Balance, or Mixed.
- "Active minutes" require sustained heart rate above 50% of max heart rate (220 - age) for at least 10 consecutive minutes.
- Walking fewer than 2,000 steps in a day does not count as a "walking workout" regardless of user classification.
- Swimming distances are always reported in meters, running/cycling in kilometers - never mix units within a report.
- Manual activity entries (not device-recorded) should be flagged and weighted 0.5x in accuracy-dependent analyses.

## Calorie Calculations

- Basal Metabolic Rate (BMR) is calculated using the Mifflin-St Jeor equation, not Harris-Benedict.
- Exercise calories are "net calories" (total burn minus BMR portion for that time period).
- Never report calorie data for users who haven't updated their weight profile in > 90 days - calculations become unreliable.
- Negative "net calorie" values (calorie deficit) should be capped at -1000 kcal/day for safety reporting.
- Device-reported calories are estimates with ±20% accuracy - always present as ranges, not exact figures.

## Heart Rate Zones

- Zone 1 (Recovery): 50-60% max HR
- Zone 2 (Fat Burn): 60-70% max HR
- Zone 3 (Cardio): 70-80% max HR
- Zone 4 (Threshold): 80-90% max HR
- Zone 5 (Max): 90-100% max HR
- Heart rate data with > 10% readings at 0 bpm indicates a sensor issue - exclude the entire session.
- Resting heart rate trends require at least 7 consecutive days of morning measurements.

## Sleep Analytics

- Sleep data below 2 hours or above 14 hours should be flagged as likely sensor error.
- "Sleep efficiency" = time asleep / time in bed × 100. Target is > 85%.
- Naps (sleep sessions < 3 hours during daytime) are tracked separately from nighttime sleep.
- Sleep stages (Deep, Light, REM, Awake) are device-estimated and should carry a confidence qualifier.
- Users with fewer than 14 nights of sleep data in a month should not receive monthly sleep reports.

## User Segmentation

- Users are classified by activity level: Sedentary (<5,000 steps/day avg), Light (5-7,499), Moderate (7,500-9,999), Active (10,000+).
- "Consistent users" log activity at least 4 days per week for 4+ consecutive weeks.
- Users who haven't synced their device in > 30 days are "inactive" and excluded from engagement metrics.
- Age groups for analysis: 18-29, 30-39, 40-49, 50-59, 60+. Users under 18 are excluded from adult cohort analysis.
- Premium vs. free-tier users must be analyzed separately for feature adoption metrics.

## Goal Tracking

- Goal completion rates should only include goals that were active for the full measurement period.
- Auto-generated goals (system-suggested) are tracked separately from user-set goals.
- Streak calculations reset to 0 on any missed day - partial credit is not given.
- Weekly goals aggregate Monday through Sunday (ISO week), not Sunday through Saturday.
- Goal adjustments mid-period create a new goal record - do not retroactively apply the change.

## Data Privacy

- Individual health metrics are PII and must never appear in aggregate reports with fewer than 50 users per group.
- Location data from outdoor activities must be anonymized (snapped to nearest 0.5 km grid) for any shared analysis.
- Biometric data (heart rate, SpO2, body temperature) has a 24-month retention policy unless the user explicitly opts in to long-term storage.
- Third-party data sharing requires explicit per-metric consent - not blanket authorization.
- De-identified data must pass k-anonymity (k ≥ 5) testing before inclusion in research datasets.
