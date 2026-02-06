# Podcast Analytics Standards (PodcastDB Database)

The audio content analytics team follows these conventions:

## Download Metrics

- A "download" is counted when at least 1 byte of the audio file is requested - this overestimates actual listens.
- IAB (Interactive Advertising Bureau) Podcast Measurement Guidelines v2.1 requires filtering bot traffic and auto-downloads.
- Unique downloads per episode within 24 hours, 7 days, and 30 days are the standard reporting windows.
- Auto-downloaded episodes that are never played should be identified where possible and flagged as "auto-downloads."
- Partial downloads (< 50% of file) should be tracked but reported separately from complete downloads.

## Listener Engagement

- "Listen-through rate" (LTR) = percentage of episode audio consumed. Median LTR of 60-70% is typical for 30-60 minute shows.
- Drop-off analysis requires second-by-second or minute-by-minute listening data (available from some hosting platforms).
- Completion rate = (listeners who reached the final 5 minutes) / (total listeners who started) × 100.
- "Skip rate" on ad segments measures ad engagement - skips > 50% indicate ad fatigue or poor ad-content fit.
- Episode subscribers who listen within 48 hours of release are "early adopters" and overindex on engagement.

## Show Classification

- Shows are classified by format: Interview, Solo/Monologue, Panel, Narrative/Storytelling, News, Educational, Fiction.
- Episode frequency: Daily, Weekly (standard), Bi-weekly, Monthly, Limited Series (defined end date), Seasonal.
- Shows with < 7 total episodes and no new episode in 90+ days are classified as "podfaded" (abandoned).
- "Network" shows (affiliated with a podcast network) have different distribution and monetization structures than independents.
- Video podcasts ("vodcasts") track both audio and video consumption separately - do not combine.

## Advertising Metrics

- Ad positions: Pre-roll (before content), Mid-roll (during content), Post-roll (after content).
- CPM (Cost Per Mille) is the standard ad pricing metric: price per 1,000 downloads in the ad-flight period.
- Host-read ads vs. dynamically inserted ads have different engagement rates (~70% LTR for host-read vs. ~40% for dynamic).
- "Baked-in" ads are permanent in the audio file; "dynamic" ads can be swapped per listener/date - track both.
- Attribution: vanity URLs and promo codes are the primary direct response measurement for podcast ads.

## Audience Demographics

- Podcast demographic data is typically survey-based (opt-in panels), not universal - treat as directional estimates.
- Platform mix (Apple Podcasts, Spotify, YouTube, RSS/other) affects the demographics data available.
- Geographic data is based on IP geolocation with ±city-level accuracy for streaming, less precise for downloads.
- Audience overlap between shows in the same network should be measured for cross-promotion effectiveness.
- "Reach" vs. "frequency" must be reported separately - some listeners consume every episode while others sample occasionally.

## Rankings and Charts

- Chart position is based on a rolling window (typically 24-48 hours) of new subscriptions and downloads.
- Category rankings are more meaningful than overall rankings for competitive analysis.
- "Chart manipulation" detection: sudden spikes in downloads from a single source or geography should be flagged.
- Apple Podcasts, Spotify, and other platforms use proprietary algorithms for their charts - rankings are not directly comparable.
- International rankings require separate tracking per country/region.

## Content Analysis

- Episode show notes and transcripts should be searchable for topic analysis and SEO.
- Explicit content flags must be accurate for family-friendly filter compliance.
- Guest appearances should be tracked bi-directionally (the guest on your show AND your host on other shows).
- Topic tagging should use a controlled vocabulary specific to the show's domain for consistent categorization.
- Sentiment in listener reviews/ratings is a lagging indicator of show quality - monitor but don't overreact to individual reviews.
