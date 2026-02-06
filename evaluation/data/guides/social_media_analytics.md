# Social Media Analytics Standards (SocialDB Database)

The digital marketing analytics team follows these conventions:

## Engagement Metrics

- Engagement rate = (likes + comments + shares + saves) / impressions × 100. NOT followers.
- "Vanity metrics" (follower count, total likes) should always be accompanied by rate-based metrics for context.
- Bot-generated engagement must be filtered using the `is_authentic` flag before any campaign performance analysis.
- Comments with fewer than 3 words are classified as "low-quality engagement" and weighted 0.25x.
- Self-engagement (the account interacting with its own content) is excluded from all engagement calculations.

## Content Classification

- Content types: Image, Video, Carousel, Story, Reel/Short, Live, Text-only, Link.
- Video content under 15 seconds is "micro-content" and has different benchmark expectations than long-form.
- Sponsored content (paid partnerships) must be tagged with `is_sponsored = TRUE` and analyzed separately from organic.
- User-generated content (UGC) is classified by whether it's solicited (campaign-driven) or organic (unprompted).
- Reposts/shares are counted as new impressions for the original content but are not "original posts" in content volume metrics.

## Reach and Impressions

- Reach = unique accounts that saw the content; Impressions = total number of times content was displayed (includes repeats).
- Reach should never exceed impressions for the same content piece - if it does, flag as a data quality issue.
- "Organic reach" excludes any boost/promotion spend; "paid reach" is only from ad placements.
- Cross-platform reach deduplication is NOT possible with standard analytics - report per-platform only.
- Story views where the user skipped within 1 second should be classified as "passive impressions" not "views."

## Audience Analysis

- Follower demographics are estimates provided by the platform - treat as directional, not precise.
- "Active followers" interacted with or viewed content in the past 30 days.
- Audience overlap between platforms requires third-party identity resolution - our standard is 60% confidence minimum.
- Follower growth rate = (new followers - unfollows) / starting followers × 100, measured weekly.
- Fake/purchased followers are identified by: no profile picture, no posts, following > 5,000 accounts, < 10 followers.

## Campaign Performance

- Attribution window: 7 days post-click, 1 day post-view for conversion credit.
- Multi-touch attribution uses a linear model (equal credit to all touchpoints) unless specified otherwise.
- A/B test results require 95% statistical significance AND at least 1,000 impressions per variant.
- Campaign ROI = (Revenue attributed - Campaign cost) / Campaign cost × 100.
- Influencer campaigns are measured by CPE (Cost Per Engagement), not CPM, for fair comparison with other channels.

## Sentiment Analysis

- Sentiment is classified as: Positive, Neutral, Negative, Mixed (contains both positive and negative elements).
- Sarcasm detection accuracy is only ~60% - flag sarcasm-prone content categories (e.g., memes, parody) for manual review.
- Sentiment trends require at least 100 mentions per period for statistical validity.
- Brand sentiment should be compared against category sentiment, not in isolation.
- Crisis detection threshold: Negative sentiment > 40% in a 4-hour window (vs. baseline of < 15%).

## Platform-Specific Rules

- Twitter/X character limits affect content length analysis - normalize for cross-platform comparison.
- Instagram engagement benchmarks are ~2x higher than Facebook/Twitter due to algorithmic differences.
- LinkedIn metrics are B2B-focused - do not compare engagement rates with consumer-focused platforms.
- TikTok "views" start counting immediately (not after 3 seconds like most platforms) - adjust for comparison.
- Platform API rate limits may cause data gaps - always check completeness before aggregating.
