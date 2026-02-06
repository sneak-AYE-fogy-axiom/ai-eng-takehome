# Taxi and Rideshare Analytics (RideDB Database)

The transportation analytics team follows these conventions:

## Trip Classification

- Trips are classified by type: Street hail, Dispatch, App-based (rideshare), Pre-arranged, Shared/Pool.
- "Dead miles" (driver traveling without a passenger) are tracked separately for driver economics analysis.
- Trips under 0.1 miles or under 60 seconds are likely false starts or errors - exclude from standard metrics.
- Airport trips (either origin or destination at an airport) are always segmented due to regulated flat rates and surcharges.
- Wheelchair-accessible vehicle (WAV) trips are tracked separately for ADA compliance reporting.

## Fare Calculations

- Metered fares = base fare + (distance rate × miles) + (time rate × minutes) + surcharges + tolls + tips.
- Tips are voluntary and should be analyzed separately from fares for driver earnings calculations.
- Surge/dynamic pricing multipliers must be recorded at booking time - average surge is NOT the same as surge on average fares.
- Flat-rate fares (airport, negotiated) bypass the meter and are recorded as `fare_type = 'flat'`.
- Credit card processing fees (typically 2.5-3%) are deducted from driver share - factor into net earnings analysis.

## Driver Metrics

- "Utilization rate" = time with passenger / total logged-in time × 100. Industry target: 55-65%.
- Trips per hour is the primary productivity metric - peak hour target varies by city (2-3 trips/hour).
- Driver ratings below 4.6 (on a 5.0 scale) trigger a performance review.
- New drivers (< 100 trips completed) have different benchmark expectations and should be analyzed in a separate cohort.
- Multi-app drivers (working for multiple platforms simultaneously) are flagged when detected - their availability metrics differ.

## Geographic Analysis

- The city is divided into zones (taxi zones, census tracts, or hexagonal grids) for origin-destination analysis.
- "Hot spots" are zones with > 2x the citywide average for pickups per hour.
- Bridge and tunnel crossings incur tolls that are passed to the rider - track these for total cost-of-trip analysis.
- Geofenced areas (airports, stadiums, event venues) have special queueing rules - trips from these origins follow different patterns.
- Rural/suburban trips (origin or destination outside city limits) are flagged and analyzed separately from urban trips.

## Temporal Patterns

- Peak hours are defined as: Morning (7-9 AM), Evening (5-7 PM), Late night (11 PM - 3 AM on Friday/Saturday).
- "Day of week" is a critical dimension - Friday/Saturday nights have 2-3x the volume of Tuesday nights.
- Event-driven demand (concerts, sports games) should be tagged with event metadata when available.
- Holiday patterns differ from regular weeks - treat each major holiday as its own analytical cohort.
- Seasonal patterns: summer may have tourism-driven demand; winter has weather-related demand spikes.

## Safety and Compliance

- All trips must have a recorded driver license number, vehicle identification, and trip start/end timestamps.
- Speed > 80 mph for more than 30 seconds triggers a safety flag on the trip.
- Accident reports must be linked to the trip record and flagged within 24 hours.
- Driver hours are capped at 12 hours per 24-hour period (varies by jurisdiction) - track for compliance.
- Background check expiration tracking: drivers with lapsed checks are "inactive" and excluded from all metrics.

## Payment Analysis

- Payment methods: Cash, Credit Card, Debit Card, Mobile Wallet, Account (corporate), Voucher.
- Cash trips tend to have lower reported fares (potential underreporting) - analyze separately for revenue integrity.
- Corporate account trips are reconciled monthly and may have negotiated rates - exclude from standard fare analysis.
- Payment disputes and chargebacks are tracked as a separate revenue risk metric.
- Tipping rates vary dramatically by payment method: credit card ~20%, cash ~10-15%, corporate ~5%.
