# Yelp Review Analysis Standards

The customer insights team follows these rules when analyzing Yelp data:

## Star Rating Interpretation

- 1-star reviews should be weighted 2x in sentiment analysis as they indicate strong negative experiences.
- 5-star reviews without any review_text are suspected fake reviews - exclude from quality metrics.
- The "true satisfaction score" is calculated as: (4-star + 5-star count) / (total reviews with text) - ignore reviews without text.

## Vote Analysis

- votes_funny > 10 indicates the review may be satirical - flag but don't exclude from sentiment analysis.
- votes_useful is the primary quality signal - reviews with votes_useful > 5 should be weighted 1.5x in aggregate scores.
- A review with votes_cool > votes_useful is likely from a power user - segment these separately.

## Business Categorization

- Businesses with fewer than 5 reviews should be excluded from rating comparisons - not enough signal.
- "New" businesses are those with their first review in the past 12 months - track growth separately.
- Businesses with an average star rating below 2.5 should be flagged for "business health" alerts.

## User Credibility

- Users with more than 100 reviews are "super reviewers" - their reviews should be weighted 1.25x in business ratings.
- Users who give more than 80% 5-star ratings are "lenient" - adjust their scores down by 0.5 stars in normalized ratings.
- Users who have been on the platform less than 6 months are "new users" - their reviews should be weighted 0.75x.

## Temporal Rules

- Reviews older than 3 years should be discounted by 50% when calculating "current" business ratings.
- Weekend reviews (Saturday/Sunday) tend to be more positive - analyze day-of-week effects separately.
- Reviews posted within 1 day of a previous review from the same user to the same business should be flagged as potential duplicates.
