# Construction Project Management Analytics (ConstructionDB Database)

The capital projects analytics team follows these conventions:

## Project Classification

- Projects are classified by type: New Construction, Renovation, Tenant Improvement, Infrastructure, Demolition.
- Project scale tiers: Small (< $1M), Medium ($1M-$10M), Large ($10M-$100M), Mega (> $100M).
- Public sector projects (government-funded) follow different procurement rules and should be analyzed separately from private.
- Design-Build, Design-Bid-Build, and Construction Manager at Risk are distinct delivery methods with different risk profiles.
- "Greenfield" (new site) vs. "Brownfield" (previously developed) projects have fundamentally different cost assumptions.

## Schedule Management

- Schedule performance is measured by Schedule Performance Index (SPI) = Earned Value / Planned Value.
- SPI < 0.9 indicates the project is significantly behind schedule and requires a recovery plan.
- Critical path activities (zero float) drive the project end date - only delays on the critical path extend the completion date.
- Weather delay days are tracked separately and may qualify for excusable time extensions depending on the contract.
- "Substantial completion" (owner can use the facility) is the primary milestone; "Final completion" (all punch list items resolved) follows.

## Cost Control

- Cost performance is measured by Cost Performance Index (CPI) = Earned Value / Actual Cost.
- CPI < 0.95 triggers a formal cost review; CPI < 0.85 triggers a project-level reassessment.
- Contingency budget is typically 5-10% of construction cost for new builds, 10-20% for renovations.
- Change orders are classified as: Owner-directed, Design error/omission, Unforeseen conditions, or Value engineering.
- "Soft costs" (design, permits, inspection, financing) are tracked separately from "hard costs" (materials, labor, equipment).

## Contractor Performance

- Contractor scorecards weight: Safety (30%), Quality (25%), Schedule (25%), Cost (20%).
- OSHA recordable incident rate (Total Case Incident Rate, TCIR) = (recordable incidents × 200,000) / total hours worked.
- TCIR above 3.0 flags the contractor for enhanced safety monitoring; above 5.0 triggers contract review.
- Punch list items per $1M of contract value is a quality metric - target < 25 items.
- Warranty callback rate (defects reported within 1 year of substantial completion) should be < 2% of total value.

## Materials and Procurement

- Material lead times vary dramatically: Structural steel (8-16 weeks), Mechanical equipment (12-20 weeks), Specialty items (20+ weeks).
- "Buy American" and "Build America" requirements affect material sourcing for federal projects - track compliance.
- Material price escalation clauses in contracts must be tracked against actual commodity price indices (steel, lumber, concrete).
- Just-in-time delivery reduces on-site storage costs but increases schedule risk - track delivery reliability per supplier.
- Substitution requests (alternative products to specified materials) require architect approval and are logged with cost/schedule impact.

## Safety and Compliance

- Daily safety inspections are mandatory; weekly toolbox talks are documented with attendance records.
- "Near miss" reporting is encouraged and tracked - a high near-miss-to-incident ratio (> 10:1) indicates a healthy safety culture.
- LEED (Leadership in Energy and Environmental Design) or equivalent green building certification requirements add 2-5% to construction costs.
- Building code compliance inspections are milestone-based: Foundation, Framing, MEP rough-in, Insulation, Final.
- As-built documentation must be within 1/4" accuracy of field conditions for BIM (Building Information Modeling) integration.

## Closeout and Warranty

- Project closeout checklist includes: As-builts, O&M manuals, training, warranty documentation, lien releases, final payment.
- Standard warranty periods: 1 year general construction, 2 years MEP systems, 5-20 years roofing (varies by system).
- Latent defect claims (discovered after warranty expiration) follow statute of repose limits (6-12 years, varies by state).
- Lessons learned sessions are mandatory within 30 days of substantial completion - findings are logged for future project planning.
- Retainage (typically 5-10% of contract value) is released after final completion and resolution of all outstanding items.
