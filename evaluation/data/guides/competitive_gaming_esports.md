# Esports and Competitive Gaming Analytics (EsportsDB Database)

The competitive gaming analytics team follows these conventions:

## Match Classification

- Matches are classified by format: Best-of-1 (Bo1), Best-of-3 (Bo3), Best-of-5 (Bo5), Best-of-7 (Bo7).
- "Official" matches are tournament or league matches with admin oversight; "Scrims" (practice matches) are excluded from all competitive statistics.
- Showmatches, all-star games, and charity events are flagged as `is_exhibition = TRUE` and excluded from player performance metrics.
- Online matches and LAN (local area network) matches should be analyzed separately - LAN performance is considered more reliable.
- Forfeits/walkovers (W/O) count as wins/losses for standings but are excluded from performance statistics.

## Player Performance

- K/D/A (Kills/Deaths/Assists) ratio is the baseline individual metric; KDA = (Kills + Assists) / Deaths.
- "Per-10-minutes" normalization is standard for all counting stats to account for variable game length.
- MVP awards are tracked but subjective - use statistical metrics for cross-player comparison, not award counts.
- Players with fewer than 20 maps played in a season have insufficient sample size - exclude from performance rankings.
- "Clutch" situations (1vX scenarios) are tracked separately with a specialized win-rate metric.

## Team Metrics

- Win rate = (maps won) / (maps played) × 100. Use MAP-level win rate, not match-level, for granular analysis.
- "First blood" percentage (getting the first kill) and conversion rate (winning rounds after first blood) are key tempo metrics.
- Economy analysis (in economic-system games): eco rounds, force-buy rounds, and full-buy rounds have different expected win rates.
- Roster changes create a "new roster" - pre-change and post-change statistics should not be combined.
- Head-to-head records require minimum 5 maps to be statistically meaningful.

## Game-Specific Rules

- Each esports title (CS2, League of Legends, Valorant, Dota 2, etc.) has its own statistical framework - NEVER combine cross-game stats.
- Patch versions create distinct "metas" - always note the game patch for any analysis period.
- Champion/agent/hero pick and ban rates are tracked per patch; win rates require minimum 100 games per champion for reliability.
- Map pool changes affect team performance - map-specific stats should be recalculated when the active map pool changes.
- Game updates that change fundamental mechanics (e.g., economy changes, ability reworks) create a new "era" - split analysis accordingly.

## Tournament Tiers

- S-Tier: Major championships, world championships, premier leagues.
- A-Tier: Major regional events, top online leagues.
- B-Tier: Minor events, qualifier tournaments.
- C-Tier: Open qualifiers, small online cups.
- Prize pool weighting: S-tier matches are weighted 2x in player valuation models; C-tier at 0.25x.

## Viewership and Engagement

- Peak concurrent viewers (CCV) and average concurrent viewers (ACV) are reported separately.
- "Hours watched" = ACV × broadcast duration (in hours). This is the primary reach metric.
- Chinese streaming platforms (Bilibili, Huya, Douyu) inflate numbers by 3-8x compared to Western platforms - apply adjustment factors.
- Co-streaming and watch party viewers should be counted only from the primary channel to avoid double-counting.
- VOD (Video on Demand) views within 7 days are "near-live" and added to live viewership for total event reach.

## Player Contracts and Transfers

- Transfer windows and roster lock dates are league-specific - track eligibility per competition rules.
- Buyout fees are tracked when publicly disclosed; "undisclosed" fees should not be estimated or imputed.
- Loan arrangements (temporary team changes) maintain the player's ownership record while changing their active team.
- Restricted free agents vs. unrestricted free agents have different market dynamics.
- Player salaries are confidential unless publicly disclosed - never aggregate salary data with < 5 players per group.
