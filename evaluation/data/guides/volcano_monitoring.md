# Volcano Monitoring Analytics (VolcanoDB Database)

The geohazards analytics team follows these conventions:

## Volcano Classification

- Volcanoes are classified by type: Stratovolcano, Shield, Caldera, Cinder Cone, Lava Dome, Complex, Submarine.
- "Active" volcanoes have erupted within the last 10,000 years (Holocene); "Dormant" have no Holocene eruptions but are not extinct.
- "Extinct" classification should be used cautiously - geological evidence must support no eruption in > 1 million years.
- Volcanic Explosivity Index (VEI) is the standard eruption size metric (0-8 scale, logarithmic). VEI ≥ 4 is "large."
- Submarine volcanoes (below sea level) are tracked with different sensor networks and should be analyzed separately.

## Seismic Monitoring

- Volcanic tremor (continuous, low-frequency seismic signal) is distinguished from discrete volcanic earthquakes.
- Swarm events (> 50 earthquakes in 24 hours within 10 km of the summit) trigger elevated monitoring status.
- Magnitude is reported on the local magnitude (ML) scale for volcanic earthquakes, not moment magnitude (Mw) used for tectonic events.
- Hypocentral depth is critical: earthquakes shallowing over time indicate magma ascent.
- The seismic network must have at least 4 stations within 10 km of the summit for reliable hypocenter determination.

## Deformation Data

- Ground deformation is measured by GPS (continuous and campaign), InSAR (satellite radar), and tilt meters.
- GPS displacement rates > 1 cm/month at summit stations are "anomalous" and require interpretation by a volcanologist.
- InSAR coherence < 0.3 indicates the measurement is unreliable (vegetation, snow, or rapid surface change).
- "Inflation" (ground moving up/outward) suggests magma accumulation; "Deflation" suggests magma withdrawal or degassing.
- Baseline deformation rates must be established during quiescent periods (minimum 2 years) before anomalies can be identified.

## Gas Emissions

- SO2 (sulfur dioxide) flux is the primary volcanic gas metric, measured in tonnes per day.
- Background SO2 flux varies by volcano (0-50 t/d for many volcanoes); increases > 3x baseline are significant.
- CO2/SO2 ratio changes can indicate changes in magma depth - increasing ratio may suggest deeper magma source.
- "Vog" (volcanic smog) advisories are issued when SO2 exceeds 200 ppb at ground level in populated areas.
- Gas measurement techniques (DOAS, COSPEC, MultiGAS, airborne) have different detection limits and uncertainties - always specify method.

## Alert Levels

- The standard USGS alert system uses four levels: Normal → Advisory → Watch → Warning.
- Aviation color codes (Green, Yellow, Orange, Red) are separate from ground-based alert levels but correlated.
- Alert level changes require concurrence from at least 2 scientists and are logged with justification.
- "Background" activity is defined as within 1 standard deviation of the 5-year baseline for all monitored parameters.
- Lowering an alert level requires 2 weeks of declining or stable activity below the threshold.

## Lahar and Ashfall Modeling

- Lahar (volcanic mudflow) inundation maps use the LAHARZ model with volumes calibrated to geological deposits.
- Ashfall forecasts use the Ash3D or HYSPLIT dispersion models driven by National Weather Service wind data.
- "At-risk" populations within lahar inundation zones are counted using Census data intersected with hazard maps.
- Ashfall thickness > 10 mm can collapse weakened roofs; > 1 mm disrupts aviation - use these as impact thresholds.
- Evacuation zone boundaries should follow natural geographic features (ridgelines, rivers) for public communication clarity.

## Historical Eruption Records

- The Smithsonian Institution's Global Volcanism Program (GVP) database is the authoritative source for eruption history.
- Eruptions dated by radiocarbon should include the calibrated date range, not just the raw 14C date.
- "Confirmed" eruptions have direct human observation or strong geological evidence; "Uncertain" have ambiguous evidence.
- Eruption duration is measured from first confirmed eruptive activity to cessation of all activity (not just the climactic phase).
- Fatality records are categorized by cause: pyroclastic flow, lahar, ashfall, tsunami, gas, ballistic impact, indirect (famine/disease).
