# Blood Bank Inventory Management (BloodBankDB Database)

The clinical operations analytics team follows these conventions:

## Blood Product Classification

- Whole blood donations are separated into components: Red Blood Cells (RBCs), Platelets, Plasma, Cryoprecipitate.
- Each component has a different shelf life: RBCs (42 days), Platelets (5 days), Fresh Frozen Plasma (1 year), Cryo (1 year).
- "Short-dated" products (< 7 days remaining for RBCs, < 2 days for platelets) are priority for distribution.
- Autologous donations (patient donating for their own future use) are tracked separately from allogeneic (community supply).
- Apheresis donations (targeted component collection) yield 2-3x the platelets of whole blood - track donor source type.

## Blood Type Inventory

- The 8 blood types (A+, A-, B+, B-, AB+, AB-, O+, O-) must each maintain minimum inventory levels.
- O-negative is the universal donor for RBCs - target 7-day supply minimum at all times.
- AB-positive plasma is the universal donor for plasma - track separately from RBC inventory planning.
- Rh-negative inventory (A-, B-, AB-, O-) is chronically scarce - flag when any type falls below 3-day supply.
- Rare phenotype units (Duffy-null, Kell-negative, etc.) require national inventory searching and should never be used for non-matched patients.

## Donor Management

- Donor eligibility: Whole blood donors must wait 56 days between donations; platelet donors 7 days (up to 24x/year).
- "First-time donors" have a higher deferral rate (~15%) vs. repeat donors (~5%) - track separately.
- Deferred donors (temporarily ineligible) must be categorized by deferral reason for targeted re-recruitment.
- "Lapsed donors" (no donation in 12+ months) require reactivation campaigns - their return rate is ~15%.
- Donor adverse events (vasovagal reactions, bruising, nerve irritation) are tracked per 10,000 donations for safety monitoring.

## Testing and Safety

- Every donation undergoes mandatory testing for: HIV 1/2, HCV, HBV, HTLV I/II, Syphilis, West Nile Virus, Zika (if applicable).
- "Reactive" test results quarantine the unit immediately - confirmed positive units are destroyed and the donor is permanently deferred.
- Bacterial contamination testing is required for platelets (highest risk due to room-temperature storage).
- Pathogen reduction technology (PRT)-treated products are flagged and may have different efficacy profiles.
- Lookback investigations (tracing recipients of previously donated units from a now-positive donor) are mandatory and time-critical.

## Distribution Metrics

- Crossmatch-to-transfusion ratio (C:T) should be ≤ 2.0 - higher ratios indicate over-ordering by hospitals.
- Units returned from hospitals unused are "reissued" if still within temperature range; otherwise they become "outdate wastage."
- Emergency release (uncrossmatched O-negative blood) events must be logged and reviewed for clinical appropriateness.
- Wastage rate = (expired + destroyed units) / (total units collected) × 100. Target: < 5% for RBCs, < 15% for platelets.
- Hospital inventory should maintain a 3-day supply for RBCs and 1-day supply for platelets as a floor.

## Regulatory Compliance

- FDA regulates blood products as biologics - all manufacturing and distribution must comply with 21 CFR Parts 606 and 610.
- AABB (Association for the Advancement of Blood & Biotherapies) accreditation standards set operational quality requirements.
- Traceability from donor vein to patient vein is mandatory - every unit must have a complete chain of custody.
- Temperature excursion events (outside 1-6°C for RBCs, 20-24°C for platelets) must be documented and evaluated.
- Annual reporting to HHS includes collection volumes, testing results, and adverse event rates.
