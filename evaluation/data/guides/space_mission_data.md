# Space Mission Analytics (SpaceMissionDB Database)

The aerospace analytics team follows these conventions:

## Mission Classification

- Missions are classified by purpose: Earth Observation, Communication, Navigation, Science, Technology Demonstration, National Security, Human Spaceflight.
- "Success" is binary at the mission level: full success (all objectives met), partial success (primary objective met, secondary failed), or failure.
- Partial successes are counted as 0.5 in success rate calculations for launch vehicles, not 1.0.
- Rideshare missions (multiple payloads per launch) count as one launch event but multiple payloads deployed.
- Classified/military missions are included in launch counts but have limited or redacted payload details.

## Launch Vehicle Performance

- Launch vehicle reliability = (successful launches) / (total launches) × 100, measured over the vehicle's lifetime.
- New launch vehicles have "infant mortality" risk - first 5 flights should be analyzed separately from mature vehicles (>20 flights).
- Payload capacity is specified for reference orbits: LEO (200 km circular) and GTO (standard geostationary transfer orbit).
- Reusable vehicle flights track both "new" and "reflown" boosters - combine for total launches but report reuse rate separately.
- Engine test firings are NOT launch attempts and should be excluded from reliability statistics.

## Orbital Mechanics

- Delta-V budget is the primary mission planning metric - track allocated vs. actual delta-V for post-mission analysis.
- Hohmann transfer orbits are the baseline for mission duration calculations between circular orbits.
- Gravity assist maneuvers reduce delta-V requirements but increase mission duration - track both metrics.
- Mission phases: Launch, Transfer, Orbit Insertion, Operations, End-of-Life (passivation or deorbit).
- Orbital debris potential must be assessed per NASA Standard 8719.14 - missions must demonstrate < 1-in-10,000 casualty risk.

## Cost Analysis

- Mission costs are reported in "then-year" dollars (actual spend) and "constant-year" dollars (inflation-adjusted to a reference year).
- Cost categories: Development (non-recurring), Production (recurring), Launch, Operations, Disposal.
- "Cost-per-kilogram to orbit" is the standard launch cost efficiency metric - always specify the target orbit.
- Fixed-price contracts vs. cost-plus contracts have fundamentally different risk profiles and should not be directly compared.
- International partner contributions are tracked at their USD equivalent using the exchange rate at the time of the agreement.

## Ground Segment

- Mission operations center (MOC) uptime must be ≥ 99.9% during critical mission phases (launch, orbit insertion, EDL).
- Data downlink volume is measured in gigabits per day; latency in light-seconds for deep space missions.
- Antenna allocation conflicts between missions are resolved by priority matrix - track denied access events.
- Flight dynamics products (orbit determination, maneuver planning) have strict delivery timelines - track on-time performance.
- Command sequences undergo mandatory validation (flat-sat or simulation) before uplink - track exceptions.

## Science Return

- Science data volume is measured in terabits for the mission lifetime.
- "Data products" (processed science data) are versioned - always reference the latest processing pipeline version.
- Publication count and citation impact (h-index for the mission) are long-term science productivity metrics.
- Target observation time vs. actual observation time measures science efficiency.
- Data archiving in NASA PDS (Planetary Data System) or equivalent is mandatory - track archive delivery milestones.

## End-of-Life

- LEO spacecraft must deorbit within 25 years of mission completion (new guideline: 5 years per FCC rules).
- GEO spacecraft must boost to a graveyard orbit at least 300 km above GEO at end of life.
- Passivation (venting residual propellant, discharging batteries) is required to minimize explosion/fragmentation risk.
- Extended missions beyond the primary mission duration track additional science return per dollar as the efficiency metric.
- Heritage: technology and lessons learned from each mission should be cataloged for future mission design reference.
