# Energy Consumption Analytics (EnergyDB Database)

The utility analytics team follows these conventions:

## Consumption Measurement

- Electricity is measured in kilowatt-hours (kWh); natural gas in therms; water in hundred cubic feet (HCF).
- NEVER combine different energy types into a single "total energy" metric without converting to a common unit (British Thermal Units or equivalent).
- Interval meter data (15-minute or hourly readings) is the preferred granularity; monthly billing data is acceptable but less precise.
- Estimated reads (flagged with `read_type = 'E'`) should be identified in all reports - they're based on historical patterns, not actual usage.
- Negative consumption readings indicate net metering (solar/wind generation exceeding consumption) - these are valid, not errors.

## Weather Normalization

- All consumption comparisons across periods MUST be weather-normalized using Heating Degree Days (HDD) and Cooling Degree Days (CDD).
- Base temperature for HDD/CDD is 65°F (18.3°C) unless the building-specific balance point has been determined.
- Weather normalization uses TMY (Typical Meteorological Year) data for the nearest weather station within 25 miles.
- "Weather-adjusted savings" = Actual savings - Weather impact. Always report both adjusted and unadjusted figures.
- Shoulder months (April-May, September-October) have minimal heating/cooling loads - be cautious with normalization in these periods.

## Building Classification

- Buildings are classified by primary use: Residential (single/multi-family), Commercial (office/retail/restaurant), Industrial, Institutional.
- Energy Use Intensity (EUI) = Annual energy consumption (kBtu) / Gross floor area (sq ft). This is the primary benchmarking metric.
- ENERGY STAR scores (1-100) are available for eligible building types and represent the percentile ranking among similar buildings.
- Buildings under 5,000 square feet should be excluded from commercial benchmarking due to high variability.
- Mixed-use buildings must be sub-metered by use type for accurate benchmarking - whole-building data is unreliable.

## Rate Structure Analysis

- Time-of-use (TOU) rates have peak, off-peak, and super off-peak periods - always specify which period when reporting $/kWh.
- Demand charges ($/kW) are based on the peak 15-minute interval in the billing period - this drives 30-40% of commercial electric bills.
- Tiered rate structures charge increasing prices as consumption rises - calculate the effective blended rate for comparison.
- Rate comparison analyses must use the same consumption profile applied to different rate schedules.
- Distributed generation (solar) customers on net metering have different effective rates than standard customers - analyze separately.

## Efficiency Programs

- Deemed savings (engineering estimates) are used for prescriptive rebate programs; measured savings (M&V) for custom projects.
- IPMVP (International Performance Measurement and Verification Protocol) Option C (whole-building analysis) requires 12 months pre and post data.
- Free-ridership rate (participants who would have acted without the program) must be deducted from gross savings for net savings.
- Realization rate = Verified savings / Predicted savings. Target is 80-120% - outside this range triggers program review.
- Cost-effectiveness is evaluated using the Total Resource Cost (TRC) test - benefit/cost ratio must exceed 1.0.

## Grid Operations

- Peak demand periods (top 100 hours/year) drive capacity planning - these are disproportionately important.
- Load factor = Average demand / Peak demand × 100. Higher is better for grid efficiency (>60% is good).
- Distributed Energy Resources (DER) - solar, storage, EVs - are modeled as both load reduction and generation.
- Transformer loading above 80% nameplate capacity triggers an upgrade study.
- Power quality events (voltage sags, harmonics, outages) are tracked separately from consumption data.

## Emissions Tracking

- Carbon emissions use EPA eGRID emission factors, specific to the regional grid mix.
- Scope 1 (direct), Scope 2 (purchased electricity), and Scope 3 (supply chain) must be tracked separately per GHG Protocol.
- Market-based accounting (using RECs/green tariffs) and location-based accounting (using grid average) both have valid uses - specify which.
- Emission factor updates occur annually - always apply the factor for the consumption year, not the reporting year.
- Carbon offsets are NOT the same as emission reductions - report them in a separate line item.
