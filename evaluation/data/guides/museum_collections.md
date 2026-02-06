# Museum Collection Management (MuseumDB Database)

The cultural heritage analytics team follows these conventions:

## Object Classification

- Objects are classified using the AAT (Art & Architecture Thesaurus) controlled vocabulary for consistency.
- "Accessioned" objects are officially part of the permanent collection; "loaned" and "deposited" objects are temporary.
- Deaccessioned objects (removed from the collection) retain their records but are flagged as `status = 'deaccessioned'` and excluded from active collection metrics.
- Replicas and reproductions are NOT original works and must be classified separately with `is_original = FALSE`.
- Fragmentary objects (incomplete works) are counted as full objects for collection size but flagged for condition analysis.

## Provenance Standards

- Provenance gaps > 10 years trigger enhanced due diligence review, especially for objects acquired after 1970.
- Objects with provenance originating from conflict zones (as defined by OFAC and UNESCO) require additional documentation.
- "Found in collection" objects (no acquisition record) are flagged as `provenance_status = 'undocumented'`.
- Chain of ownership must be recorded chronologically with dates, not just the most recent transaction.
- Nazi-era provenance (1933-1945) requires specific investigation per the Washington Conference Principles.

## Valuation

- Insurance valuations are updated every 5 years or upon significant market events (record auction sales, etc.).
- Fair market value (FMV) and replacement value are distinct - FMV is for tax purposes, replacement is for insurance.
- Objects valued over $1,000,000 require at least 2 independent appraisals.
- Donated objects use FMV at the date of gift for tax deduction purposes.
- "Priceless" is not a valid database value - all objects must have a numeric estimate, even if approximate.

## Exhibition Analytics

- Exhibition attendance is measured by ticket sales (ticketed) or turnstile counts (free admission).
- "Visitor minutes per object" measures engagement; objects with < 5 seconds average viewing time need repositioning.
- Traveling exhibitions track separate attendance at each venue - do not sum for "total attendance" without noting it spans venues.
- Exhibition cost-per-visitor = (total exhibition cost) / (total attendance). Benchmark varies by institution size.
- Objects on view vs. in storage ratio is reported annually - typical target is 5-15% on view.

## Conservation

- Condition reports use a standardized scale: Excellent, Good, Fair, Poor, Critical.
- Light exposure is measured in lux-hours/year. Paper/textile maximum: 150,000 lux-hours. Oil paintings: 600,000 lux-hours.
- Relative humidity must remain between 45-55% (±5%) for mixed collections. Fluctuations > 10% in 24 hours trigger alerts.
- Conservation treatments are logged with before/after condition, materials used, and conservator credentials.
- "Preventive conservation" measures (environmental controls, pest management) are tracked separately from "active conservation" (treatment).

## Digital Records

- Every object requires a minimum of 3 digital photographs: front, back, and detail view.
- Image resolution minimum: 4000 pixels on the longest edge for publication-quality reproduction.
- 3D scans are supplementary and do not replace standard photography in the catalog record.
- Digital surrogates (high-resolution images available online) should track download counts as a usage metric.
- Copyright status must be recorded: Public Domain, Rights Managed, Orphan Work, or specific license terms.

## Lending and Borrowing

- Loan agreements have a maximum duration of 2 years, renewable with board approval.
- Outgoing loans require a facility report from the borrowing institution demonstrating adequate environmental controls.
- Government indemnity (Federal Council on the Arts and Humanities) reduces insurance costs for qualifying loans - track eligibility.
- Courier accompaniment is required for objects valued over $500,000 during transit.
- Loan fees are charged for commercial exhibitions but waived for educational/institutional borrowers.
