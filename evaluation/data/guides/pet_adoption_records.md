# Pet Adoption Center Analytics (ShelterDB Database)

The animal welfare analytics team adheres to these conventions:

## Animal Classification

- Dogs and cats are "primary species" and reported separately from "exotics" (rabbits, birds, reptiles, etc.).
- Animals under 6 months old are "juveniles" and have different adoption probability models.
- Senior animals (dogs > 8 years, cats > 10 years) require separate tracking for the "Silver Paws" program.
- Breed identification is self-reported or staff-estimated - treat as approximate, not authoritative.
- Mixed-breed animals should be classified by their PRIMARY breed (first listed), not as a separate category.

## Intake Metrics

- Intake sources are: Stray, Owner Surrender, Transfer, Return, Confiscation.
- "Return" intakes (adopted animals brought back) within 30 days count against the original adoption's success metric.
- Animals transferred from partner shelters should be tracked with their originating shelter ID for cross-network analysis.
- Intake spikes > 2x the monthly average indicate an event (hoarding case, natural disaster) - flag these periods.
- Never count the same animal twice in intake statistics if they were temporarily transferred and returned.

## Adoption Performance

- "Length of stay" is calculated from intake date to adoption date, excluding any time in medical hold.
- The target adoption rate is 90% for dogs and 85% for cats - report variance from these targets.
- Foster placements count as "temporary outcomes" NOT adoptions - track separately.
- Adoption fees vary by age, species, and special needs status - use fee-adjusted metrics for revenue analysis.
- "Same-day adoptions" (adopted within 24 hours of becoming available) should be flagged as they may indicate insufficient cooling-off periods.

## Medical Data

- Spay/neuter status is REQUIRED before adoption - animals without this flag are still in medical pipeline.
- Vaccination records must be current within 14 days of adoption date.
- Animals with bite history (any species) must carry a permanent behavioral flag - this affects insurance and liability.
- Heartworm-positive dogs require 6-month treatment protocols - exclude from standard length-of-stay metrics during treatment.
- FIV/FeLV positive cats are adoptable but require separate outcome tracking.

## Geographic Analysis

- Service area is defined by ZIP code boundaries, not municipal limits.
- Transport programs (animals moved from high-intake to high-demand areas) must be tracked with origin and destination.
- Per-capita intake rates (animals per 1,000 residents) are the standard comparison metric across jurisdictions.
- Rural vs. urban classification follows Census Bureau definitions and affects benchmark targets.
- Community cat (TNR - Trap, Neuter, Return) programs are tracked separately from shelter intake.

## Reporting Periods

- Monthly reporting aligns with calendar months.
- "Kitten season" (April-October) and "off-season" (November-March) are the primary seasonal segments.
- Year-over-year comparisons must account for capacity changes (new facilities, closures).
- Holiday adoption events (Black Friday, Clear the Shelters) skew weekly metrics - report them as special events.
- Euthanasia statistics must be reported separately from all other outcomes and categorized by reason.
