# Wildlife Conservation Tracking (WildlifeDB Database)

The conservation analytics team follows these data standards:

## Species Classification

- Species are identified by their binomial name (Genus species), not common names, as the primary key.
- Common names vary by region - always include the scientific name in any report or query result.
- Subspecies are tracked separately only when conservation status differs between populations.
- Hybrid individuals (cross-species or cross-subspecies) are excluded from population counts but tracked in genetic diversity records.
- Invasive species are flagged with `is_invasive = TRUE` and analyzed in a completely separate pipeline from native species.

## Population Estimates

- Population counts from different survey methods (aerial, ground transect, camera trap, genetic sampling) must NEVER be directly compared.
- Confidence intervals are mandatory for all population estimates - point estimates without error bars should not be published.
- Population trends require at least 5 consecutive annual surveys using the same methodology.
- Populations below 500 breeding individuals trigger "critically small population" protocols and enhanced monitoring.
- Double-counting adjustments vary by species: apply correction factors from the methodology reference table.

## Habitat Analysis

- Habitat classification follows the IUCN Habitats Classification Scheme (Level 2 minimum).
- Protected area boundaries use the World Database on Protected Areas (WDPA) shapefiles - not municipal or political boundaries.
- "Core habitat" (≥1 km from any edge) is distinguished from "edge habitat" for fragmentation analysis.
- Habitat quality scores (1-5 scale) are assessed annually and should not be compared across different ecosors.
- Corridors connecting habitat patches must be at least 100 meters wide to be considered functional for large mammals.

## Tracking Data

- GPS collar data at intervals > 4 hours is insufficient for movement analysis - classify as "presence only."
- Mortality signals (no movement for 8+ hours) trigger field verification before recording a death.
- Satellite tags have a positional accuracy of ±20 meters; VHF tags require triangulation with ±200 meter accuracy.
- Home range calculations use the 95% kernel density estimate, not minimum convex polygon.
- Migratory species have separate home ranges for breeding and non-breeding seasons - never combine.

## Threat Assessment

- Threats are categorized using the IUCN Threats Classification Scheme (12 Level 1 categories).
- Poaching incidents are geolocated to the nearest 1 km grid cell (not exact location) for security reasons.
- Human-wildlife conflict events must record the species, outcome for both parties, and location.
- Climate change impacts are modeled, not directly observed - always label these as projections.
- Cumulative threat scores sum individual threat scores weighted by severity and scope.

## Breeding Records

- Breeding success is measured as "fledglings per breeding pair per year" for birds; "surviving young per female per year" for mammals.
- Captive-bred individuals released into the wild carry a permanent "captive origin" flag affecting genetic analyses.
- Nesting sites within 500 meters of human structures are classified as "urban-adjacent" and monitored for disturbance.
- Egg viability data (fertility rates, hatch rates) is sensitive to sample size - require n ≥ 20 nests per species per year.
- Breeding season dates vary by latitude and elevation - always reference the species-specific phenology table.

## Reporting Standards

- All reports must specify the spatial extent (study area boundary) and temporal extent (survey dates).
- Endangered species location data is restricted access - never include precise coordinates in public-facing reports.
- Statistical significance is set at α = 0.05 unless the species' conservation status warrants a more conservative threshold.
- Data sharing follows the FAIR principles (Findable, Accessible, Interoperable, Reusable) with appropriate access controls.
- Indigenous knowledge and traditional ecological knowledge (TEK) should be credited and integrated per the Nagoya Protocol.
