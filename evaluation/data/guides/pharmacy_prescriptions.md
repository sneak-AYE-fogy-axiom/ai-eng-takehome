# Pharmacy Prescription Analytics (PharmDB Database)

The healthcare analytics team follows these conventions for prescription data:

## Prescription Classification

- Prescriptions are classified by schedule: Schedule II (highest abuse potential), III, IV, V, and Non-Scheduled.
- Schedule II prescriptions cannot have refills by law - each fill requires a new prescription. Do not flag these as "zero refill" issues.
- "Maintenance medications" are defined as drugs with 3+ consecutive monthly fills - analyze adherence differently from acute medications.
- Brand vs. generic dispensing must be tracked for cost analysis - generic substitution rate is a key pharmacy performance metric.
- Compound prescriptions (custom-mixed) follow a different pricing model and should be excluded from standard cost-per-prescription metrics.

## Adherence Metrics

- Medication Possession Ratio (MPR) = (total days' supply dispensed / total days in measurement period) × 100.
- Proportion of Days Covered (PDC) is preferred over MPR as it accounts for overlapping fills: PDC = (days covered / total days) × 100.
- Adherent patients have PDC ≥ 80% for chronic disease medications (diabetes, hypertension, cholesterol).
- Patients with only 1 fill (never refilled) are "primary non-adherent" and tracked separately.
- Gaps in therapy > 30 days trigger a "therapy discontinuation" event.

## Drug Utilization Review (DUR)

- Drug-drug interactions are flagged at fill time with severity levels: Contraindicated, Major, Moderate, Minor.
- "Therapeutic duplication" (2+ drugs in the same class for the same patient) is flagged for pharmacist review.
- Age-based alerts: certain medications are inappropriate for patients > 65 (Beers Criteria) - flag but do not auto-reject.
- Maximum daily dose alerts must use the FDA-approved maximum, not the typical prescribing dose.
- Allergy flags override all other processing - NEVER proceed past an allergy alert without explicit override documentation.

## Pricing and Reimbursement

- AWP (Average Wholesale Price) is the benchmark pricing metric; MAC (Maximum Allowable Cost) caps reimbursement for generics.
- Patient copay vs. plan-paid amount must be tracked separately for member cost burden analysis.
- 340B-eligible prescriptions (discounted for qualifying healthcare entities) are segregated and reported to HRSA.
- "Clawbacks" (where copay exceeds plan-paid amount) should be flagged as potential cost-shift issues.
- Specialty pharmacy prescriptions (cost > $1,000/fill) are always analyzed separately from traditional pharmacy.

## Dispensing Rules

- Partial fills are allowed for Schedule II medications in long-term care - track as a single prescription, not multiple.
- "Days' supply" is the primary quantity measure for utilization analysis, not pill count (accounts for different dosing).
- Early fill threshold: most plans reject refills more than 7 days before the expected run-out date.
- 90-day mail-order fills are not directly comparable to 30-day retail fills - normalize to 30-day equivalents.
- Transfer prescriptions (moved from one pharmacy to another) retain the original prescription number for continuity.

## Patient Privacy (HIPAA)

- Minimum necessary standard: only access the minimum PHI required for the specific analysis.
- De-identification requires removal of 18 identifiers under the Safe Harbor method.
- Prescription data cannot be linked to patient demographics without a properly executed BAA (Business Associate Agreement).
- Aggregate reports must have cell sizes ≥ 11 (not 10) per HHS guidance to prevent re-identification.
- Opioid prescription data has additional restrictions and cannot be included in general analytics without specific authorization.

## Quality Metrics

- Star Ratings (CMS Medicare) for pharmacy: medication adherence (diabetes, hypertension, cholesterol) and medication safety.
- Pharmacist consultation rate = (consultations performed / new prescriptions filled) × 100. Target > 90%.
- Medication error rate = (errors caught + errors dispensed) / total prescriptions × 100. Target < 0.01%.
- Wait time tracking begins at drop-off and ends at patient pickup - not at when the prescription enters the queue.
- Vaccine administration counts are tracked separately from prescription dispensing for staffing analysis.
