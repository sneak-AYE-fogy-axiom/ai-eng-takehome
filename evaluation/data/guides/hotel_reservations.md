# Hotel Reservation Analytics (HospitalityDB Database)

The hospitality analytics team follows these conventions:

## Occupancy Metrics

- Occupancy rate = (rooms sold / rooms available) × 100. "Rooms available" excludes rooms out-of-order (OOO) for maintenance.
- RevPAR (Revenue Per Available Room) = Total room revenue / Total available rooms. This is the primary performance metric.
- ADR (Average Daily Rate) = Total room revenue / Rooms sold. Never confuse with rack rate (published maximum rate).
- Complimentary rooms (comp stays) count as "sold" for occupancy but contribute $0 to revenue metrics.
- Day-use rooms (sold for less than overnight) are tracked separately and NOT included in standard occupancy calculations.

## Reservation Classification

- Reservations are classified by source: Direct, OTA (Online Travel Agency), Corporate, Group, Wholesale, Walk-in.
- OTA bookings carry a commission (15-25%) that must be netted out for true revenue comparisons.
- "No-shows" (guaranteed reservations where guest doesn't arrive) are charged one night and counted as sold.
- Cancellations within 24 hours of arrival are "late cancellations" and may or may not incur charges depending on rate plan.
- Overbooking is intentional (typically 5-10% of capacity) - "walked" guests (relocated to another hotel) are tracked as service failures.

## Rate Management

- BAR (Best Available Rate) is the baseline rate for public comparison.
- Corporate negotiated rates are confidential - never display in public-facing reports.
- Package rates (room + breakfast, room + spa) must be decomposed into room revenue and non-room revenue.
- Length-of-stay discounts are applied per night - report both the undiscounted and discounted ADR.
- Rates below the "floor rate" (variable cost per room) should be flagged as below-cost selling.

## Guest Segmentation

- Business vs. Leisure classification is based on rate code, not self-reported purpose.
- Loyalty program members are tiered: Base, Silver, Gold, Platinum, Ambassador.
- "Repeat guests" have 2+ stays in the past 12 months; "loyal guests" have 5+ stays in 24 months.
- Group guests (10+ rooms on the same reservation) are analyzed separately from individual travelers.
- International guests require passport nationality tracking for government reporting (separate from billing address).

## Revenue Management

- Booking window = date of reservation - date of arrival. Segment into: 0-7 days, 8-30 days, 31-90 days, 90+ days.
- "Shoulder nights" (Sunday and Thursday) typically have lower demand and different pricing strategies.
- Event-driven demand (conventions, concerts, sports) should be tagged with the event ID for attribution.
- TRevPAR (Total Revenue Per Available Room) includes F&B, spa, parking, etc. - preferred over RevPAR for full-service hotels.
- Displacement analysis: when accepting a group booking, calculate the revenue lost from displaced individual bookings.

## Property Classification

- Hotels are classified by service level: Economy, Midscale, Upper Midscale, Upscale, Upper Upscale, Luxury.
- Star ratings (1-5) vary by rating agency - always specify the source (AAA, Forbes, local tourism board).
- Branded vs. independent hotels should be analyzed separately due to different distribution cost structures.
- Suite inventory is tracked separately from standard rooms for upgrade and upsell analysis.
- Properties with fewer than 50 rooms are "boutique" and may have different performance benchmarks.

## Reporting Periods

- The "hotel day" runs from 3:00 PM to 3:00 PM (check-in to check-in), not midnight to midnight.
- STR (Smith Travel Research) reporting follows calendar months and uses a standardized competitive set (comp set).
- Budget season runs September-November for the following calendar year.
- Year-over-year comparisons must account for "day of week" mix (e.g., number of Saturdays in the month).
- COVID-19 period (March 2020 - December 2021) should be flagged as anomalous and optionally excluded from trend analysis.
