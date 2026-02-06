# Aquarium and Marine Facility Management (AquariumDB Database)

The aquatic sciences analytics team follows these conventions:

## Species Inventory

- Species are tracked by scientific name (binomial nomenclature) as the primary identifier; common names are secondary.
- Vertebrates (fish, mammals, reptiles, birds) and invertebrates (corals, jellyfish, anemones, crustaceans) use separate inventory schemas.
- "Display animals" (in public-facing exhibits) are tracked separately from "behind-the-scenes" (quarantine, breeding, research) animals.
- Species listed under CITES (Convention on International Trade in Endangered Species) require additional provenance documentation.
- Dead specimens should be retained in the database with `status = 'deceased'` and necropsy results linked to the record.

## Water Quality Parameters

- Temperature, pH, salinity, dissolved oxygen, ammonia, nitrite, and nitrate are the "Core 7" parameters monitored daily.
- Saltwater systems target: pH 8.1-8.4, salinity 33-36 ppt, temperature 24-26°C (tropical), 10-15°C (temperate).
- Freshwater systems target: pH 6.5-7.5, temperature varies by species (18-28°C range).
- Ammonia readings above 0.25 ppm (total ammonia nitrogen) trigger an immediate water change and investigation.
- Weekly full water chemistry panels include alkalinity, calcium, magnesium, phosphate, and silicate for reef systems.

## Life Support Systems

- System capacity is measured in gallons; flow rate in gallons per minute (GPM); turnover rate = total volume / flow rate.
- Target turnover: 4-6x per hour for fish-only systems; 10-20x per hour for reef systems.
- Filter media replacement follows manufacturer schedule unless pressure differential exceeds 15 PSI (replace immediately).
- UV sterilizer efficacy requires minimum dose of 40,000 µW-sec/cm² for pathogen control - track bulb hours and replace at 9,000 hours.
- Protein skimmer performance is measured by volume of skimmate collected per week - declining volumes indicate cleaning needed.

## Animal Health

- Health assessments follow the standardized Animal Health Assessment form with body condition scoring (1-5 scale).
- Prophylactic quarantine for new arrivals: 30 days minimum for fish, 60 days for marine mammals.
- Medication dosing is calculated per gram of body weight (fish) or per kilogram (mammals) - never confuse units.
- Mortality rate is calculated monthly as: (deaths / average population) × 100. Target: < 1% for fish, < 0.1% for mammals.
- Behavioral monitoring logs (feeding response, swimming patterns, social interactions) require at least 3 observations per day per individual for mammals.

## Breeding Programs

- Species Survival Plans (SSP) are managed through the AZA (Association of Zoos and Aquariums) breeding recommendations.
- Genetic diversity metrics (mean kinship, inbreeding coefficient) are mandatory for SSP species before any breeding decision.
- Egg counts, hatch rates, and juvenile survival rates are tracked per breeding event.
- "Surplus" animals (not needed for breeding) require a placement plan approved by the SSP coordinator.
- Breeding season dates are species-specific and controlled by photoperiod and temperature manipulation in managed care.

## Exhibit Design Metrics

- "Dwell time" (visitor time at an exhibit) is the primary engagement metric - target > 90 seconds for major exhibits.
- Species-per-exhibit density must comply with AZA space requirements per taxon.
- Educational signage reading rate is estimated at 15% of visitors - interactive/digital elements increase to 35%.
- Exhibit renovation cycles target every 10-15 years for major exhibits; annual refreshes for minor elements.
- ADA accessibility compliance requires that 100% of public exhibits are wheelchair-accessible and have audio descriptions available.

## Conservation Contributions

- In-situ (field) conservation spending should be tracked separately from ex-situ (facility-based) spending.
- AZA SAFE (Saving Animals From Extinction) program participation is reported annually per species.
- Research publications citing the facility's animals or data are tracked as an output metric.
- Rescue and rehabilitation statistics track: intake count, survival rate, release rate, and average time in care.
- Educational program attendance and conservation-behavior-change survey results measure community impact.
