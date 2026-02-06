# Agricultural Crop Data Standards (AgriDB Database)

The agricultural analytics division follows these conventions:

## Yield Calculations

- Crop yield is reported in bushels per acre for grains (corn, wheat, soybeans) and tons per acre for fruits/vegetables.
- "Harvested acres" is the denominator for yield calculations, NOT planted acres (some acres may be abandoned or prevented).
- Irrigated and dryland (rainfed) yields must be reported separately - combining them masks technology and investment effects.
- Yields from research plots and experimental varieties are excluded from commercial production estimates.
- Zero-yield records where the crop was planted but not harvested are "prevented harvest" and tracked for insurance purposes.

## Crop Classification

- Crops are classified by: Row crops (corn, soybeans, cotton), Small grains (wheat, barley, oats), Specialty crops (fruits, vegetables, nuts), Forage (hay, alfalfa).
- Genetically modified (GM) vs. conventional varieties must be tagged - regulatory reporting requires this distinction.
- Organic certification status is tracked per field, not per farm - a farm may have both organic and conventional fields.
- Cover crops (planted for soil health, not harvest) are tracked in the field history but excluded from production statistics.
- Double-cropping (two crops per year on the same field) counts each crop separately in production totals.

## Weather Impact Assessment

- Growing Degree Days (GDD) are calculated using base 50°F for corn, base 32°F for wheat. Formula: (max temp + min temp) / 2 - base.
- Drought conditions are classified using the Palmer Drought Severity Index (PDSI): Extreme (< -4), Severe (-3 to -4), Moderate (-2 to -3).
- Frost/freeze events during growing season require: Light freeze (29-32°F), Moderate freeze (25-28°F), Severe freeze (< 24°F).
- Excessive moisture events that cause flooding or ponding should be tracked with duration (hours) and affected acres.
- Hail damage is estimated as percentage of crop destroyed (0-100%) and must be verified by field inspection.

## Market and Pricing

- Commodity prices are reported as the nearby futures contract price unless cash/spot price is specified.
- Basis = Local cash price - Nearby futures price. Basis varies by location and is critical for local market analysis.
- "Marketing year" varies by crop: Corn/Soybeans (Sep 1 - Aug 31), Wheat (Jun 1 - May 31).
- Price-per-bushel is the standard unit; conversions: 1 bushel of corn = 56 lbs, wheat = 60 lbs, soybeans = 60 lbs.
- Government support payments (subsidies, crop insurance indemnities) are revenue but NOT market income - track separately.

## Field and Soil Data

- Fields are identified by CLU (Common Land Unit) as the minimum spatial unit.
- Soil type classifications follow the USDA Soil Taxonomy system - texture (sand/silt/clay composition) drives management decisions.
- Nutrient levels (N, P, K) from soil tests are reported in parts per million (ppm) and have a 3-year validity window.
- Tillage practices (conventional, reduced, no-till) affect soil carbon and must be recorded for sustainability metrics.
- Field boundaries may change with land transactions - maintain a temporal history of boundary changes.

## Reporting and Compliance

- USDA NASS (National Agricultural Statistics Service) crop reports follow strict release schedules and lockup procedures.
- County-level production data requires at least 3 reporting farms to protect individual farm confidentiality.
- Crop insurance records (RMA data) are confidential at the individual level - only aggregate to county or higher.
- Sustainability certifications (ISCC, Bonsucro, RSB) each have different scope and metrics - do not treat as equivalent.
- Precision agriculture data (GPS-tagged yield maps) is proprietary to the farm and requires explicit consent for any off-farm analysis.
