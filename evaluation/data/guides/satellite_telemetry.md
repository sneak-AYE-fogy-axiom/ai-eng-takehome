# Satellite Telemetry Analytics (SpaceTelemetryDB Database)

The space operations analytics team follows these conventions:

## Orbital Parameters

- Orbital elements use the TLE (Two-Line Element) format as the standard data exchange format with NORAD catalog numbers as primary keys.
- Semi-major axis is reported in kilometers from Earth's center; altitude is from Earth's surface (subtract ~6,371 km).
- LEO (Low Earth Orbit): 160-2,000 km altitude. MEO: 2,000-35,786 km. GEO: ~35,786 km. HEO: eccentricity > 0.25.
- Orbital decay predictions for LEO satellites use atmospheric drag models - solar activity (F10.7 index) is a critical input.
- "Deorbited" and "decayed" satellites are removed from active tracking but retained in the historical catalog.

## Telemetry Data Quality

- Telemetry readings with timestamps more than 500ms from the scheduled downlink window should be flagged as "off-nominal."
- Missing telemetry points > 3 consecutive readings trigger a "communication anomaly" investigation.
- Housekeeping telemetry (voltage, temperature, attitude) is collected at 1 Hz minimum; science telemetry varies by instrument.
- Data dropouts during solar conjunction (Sun-spacecraft-Earth alignment) are expected and should not be counted against link reliability.
- Telemetry values outside defined red/yellow limits generate automated alerts - distinguish between "out of range" and "sensor failure."

## Power Systems

- Solar array output degrades ~2-3% per year due to radiation damage - power budgets must account for end-of-life (EOL) performance.
- Eclipse periods (satellite in Earth's shadow) rely entirely on battery power - track battery depth-of-discharge per eclipse.
- Battery capacity below 60% of beginning-of-life (BOL) rating classifies the spacecraft as "power-constrained."
- Power generation is measured in watts; energy storage in watt-hours. Do not confuse power (instantaneous) with energy (cumulative).
- Safe mode (minimum power configuration) events are tracked as operational anomalies and require root cause analysis.

## Thermal Management

- Component temperature limits are mission-specific and defined in the thermal design specification.
- "Hot case" and "Cold case" are the worst-case thermal scenarios - actual telemetry should fall between these bounds.
- Temperature cycling (repeated heating/cooling) causes material fatigue - track the number of thermal cycles per orbit for life prediction.
- Heater duty cycle > 80% indicates inadequate passive thermal design - flag for engineering review.
- Thermal telemetry accuracy is typically ±2°C for thermistors and ±0.5°C for platinum resistance thermometers (PRTs).

## Attitude and Control

- Attitude determination accuracy is measured in arcseconds for precision-pointing missions (telescopes) and degrees for general missions.
- Momentum wheel speeds should remain between 20-80% of maximum RPM - outside this range requires a momentum dump.
- Star tracker availability < 99% indicates contamination or baffle issues - flag for operations team review.
- Thruster firings are logged with duration (milliseconds), thrust vector, and delta-V achieved for propellant bookkeeping.
- End-of-life propellant reserve must maintain at least 6 months of station-keeping capability.

## Ground Station Operations

- Pass scheduling uses the AOS (Acquisition of Signal) / LOS (Loss of Signal) windows based on orbital geometry.
- Minimum elevation angle for reliable communication is typically 5-10° above the horizon.
- Doppler shift correction is applied automatically by the ground system - verify correction is within expected bounds.
- Command uplink windows have higher priority than telemetry downlink - never sacrifice command capability for data.
- Antenna handoff between ground stations must occur seamlessly - gaps > 30 seconds in continuous operations are tracked as outages.

## Constellation Management

- Constellation health is measured by the percentage of operational satellites vs. minimum required for service level.
- Inter-satellite links (ISL) create a mesh network - link margin < 3 dB should trigger a routing reconfiguration.
- Phasing between satellites in the same orbital plane must maintain minimum separation (varies by mission, typically > 1°).
- Replacement satellite launch decisions are triggered when spare count drops below 10% of constellation size.
- Collision avoidance maneuvers (CAMs) are tracked with miss distance, probability of collision, and delta-V expended.
