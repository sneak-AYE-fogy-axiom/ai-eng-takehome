# Weather Station Data Standards (MeteorologicalDB Database)

The climate analytics division follows these conventions:

## Temperature Measurements

- All temperatures must be reported in Celsius for internal analysis; convert to Fahrenheit only for US consumer-facing reports.
- Temperature readings are taken at standard meteorological height (2 meters above ground) - non-standard heights require adjustment.
- "Extreme" temperatures are defined as > 2 standard deviations from the 30-year climate normal for that station and date.
- Missing temperature readings should NOT be interpolated from neighboring stations if the nearest station is > 50 km away.
- Urban heat island effect: stations within 5 km of city centers (population > 100,000) require a -1.5°C adjustment for climate trend analysis.

## Precipitation Rules

- Precipitation is measured in millimeters; snowfall is measured separately and converted using a 10:1 snow-water equivalent ratio.
- Trace precipitation (< 0.2 mm) is recorded as "T" and should be counted as 0 for summation but counted as a precipitation day.
- "Dry days" require 0.0 mm (not trace) for drought index calculations.
- Freezing rain is categorized as precipitation, not snowfall, regardless of ground accumulation.
- Annual precipitation totals require at least 350 days of valid readings - otherwise flag the year as incomplete.

## Wind Measurements

- Wind speed is reported in meters per second (m/s) at the standard 10-meter height.
- Gust readings are instantaneous peaks; sustained wind is the 10-minute average.
- Calm conditions (wind speed < 0.5 m/s) should be recorded as 0 with direction "VRB" (variable).
- Wind roses should use 16 compass directions, not 8, for detailed directional analysis.
- Anemometer readings during icing conditions may underreport by up to 30% - flag these periods.

## Station Quality Control

- Stations must report at least 90% of scheduled observations in a month to be included in monthly aggregations.
- Stations that relocated (even by 100 meters) require a 12-month parallel observation period before old data can be homogenized.
- Automated stations (ASOS/AWOS) and manual stations should be analyzed separately due to systematic measurement differences.
- Stations at altitude > 2,000 meters require pressure adjustments for sea-level comparisons.
- New stations have a 2-year "burn-in" period where data quality is provisional.

## Climate Normals

- Climate normals are 30-year averages, currently based on 1991-2020 (updated every 10 years).
- Departures from normal are calculated against the appropriate 30-year period, not all-time averages.
- Trend analysis requires at least 30 years of continuous data from the same station location.
- Record values (all-time highs/lows) should specify the period of record and whether the station existed for the full period.
- Seasonal definitions: Winter (DJF), Spring (MAM), Summer (JJA), Autumn (SON) for Northern Hemisphere; reversed for Southern.

## Severe Weather Events

- Severe weather events are classified by NWS criteria: Severe Thunderstorm (58+ mph winds or 1"+ hail), Tornado (confirmed by NWS).
- Lightning strike data has a location accuracy of ±500 meters - do not use for precise impact analysis.
- Hurricane/typhoon data should reference the Saffir-Simpson scale and use the "best track" dataset, not real-time advisories.
- Heatwave: 3+ consecutive days with maximum temperature exceeding the 95th percentile for that date.
- Flood events use stream gauge data, not precipitation alone - upstream conditions must be considered.

## Data Formats

- Timestamps are in UTC for all synoptic observations; local time only for climatological day boundaries.
- METAR/TAF formats are for aviation purposes and should not be mixed with climatological data without conversion.
- Quality flags (G = good, S = suspect, E = estimated, M = missing) must be preserved through all transformations.
- Gridded data products (interpolated surfaces) are clearly distinguished from point observations.
- Historical data digitized from paper records carries a "digitized" flag indicating potential transcription errors.
