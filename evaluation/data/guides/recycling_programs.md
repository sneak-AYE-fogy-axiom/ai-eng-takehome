# Recycling and Waste Management Analytics (WasteDB Database)

The environmental services analytics team follows these conventions:

## Waste Classification

- Waste streams are: Municipal Solid Waste (MSW), Recyclables, Compostables, Hazardous Waste (HazWaste), Construction & Demolition (C&D), E-waste.
- NEVER combine hazardous waste metrics with MSW - they have entirely separate regulatory frameworks.
- "Contamination rate" = weight of non-recyclable material in recyclable stream / total recyclable stream weight × 100.
- Contamination rates above 25% typically cause a recyclable load to be rejected and sent to landfill - track these "rejected loads."
- Organic waste (food scraps, yard trimmings) is tracked separately from recyclables even though both are "diverted from landfill."

## Diversion Metrics

- Diversion rate = (total waste diverted from landfill) / (total waste generated) × 100.
- Diversion includes: recycling, composting, anaerobic digestion, waste-to-energy. Landfill and incineration without energy recovery are NOT diversion.
- Waste-to-energy (WTE) classification varies by jurisdiction - some count it as diversion, others do not. Always specify the definition used.
- Source reduction (waste prevention) is the highest priority but hardest to measure - track proxy metrics like per-capita waste generation.
- "Zero waste" is defined as ≥ 90% diversion rate (true zero is practically impossible).

## Collection Operations

- Collection routes are evaluated on: Households per route, Tons per route, Cost per ton collected.
- Automated (single-operator) vs. manual (crew-operated) collection have fundamentally different cost structures - never average.
- Missed collection complaints per 1,000 households is the primary service quality metric. Target: < 2 per month.
- Contamination is primarily driven by 10-15% of households ("chronic contaminators") - target education to this segment.
- Holiday collection schedule adjustments affect weekly tonnage - normalize when comparing week-over-week.

## Material Recovery Facility (MRF) Operations

- MRF throughput is measured in tons per hour per sorting line.
- Residue rate = (material sent to landfill from MRF) / (total material received at MRF) × 100. Target: < 15%.
- Commodity revenue per ton varies dramatically by material: Aluminum (~$1,500/ton), Cardboard (~$100/ton), Mixed glass (~$0/ton or negative).
- Processing cost per ton must include labor, equipment depreciation, transportation, and residual disposal.
- Single-stream vs. dual-stream recycling programs have different contamination profiles - analyze separately.

## Commodity Markets

- Recycled commodity prices follow global markets and can be extremely volatile (especially post-China National Sword policy).
- Revenue from commodity sales should be reported net of processing costs and transportation.
- "Floor pricing" contracts with haulers guarantee minimum recycling revenue regardless of market conditions.
- Bale quality specifications (moisture content, contamination limits) affect pricing by 20-40%.
- Domestic vs. export markets for recyclables must be tracked for supply chain resilience analysis.

## Regulatory Compliance

- EPR (Extended Producer Responsibility) programs shift recycling costs to manufacturers - track separately from municipal costs.
- State-mandated recycling rates vary (e.g., California 75%, New York 50%) - always benchmark against the applicable regulation.
- Landfill bans (e.g., yard waste, electronics, mattresses) affect what enters the waste stream - track compliance per material.
- Greenhouse gas reporting for waste operations follows EPA WARM (Waste Reduction Model) methodology.
- RCRA (Resource Conservation and Recovery Act) manifests are required for hazardous waste transport and disposal.

## Financial Analysis

- Total cost of waste management = Collection + Processing + Disposal + Administration - Commodity revenue.
- Cost per household per month is the standard municipal comparison metric.
- Tipping fees (landfill disposal cost per ton) are the primary disposal cost driver and vary by $30-$150/ton regionally.
- Capital equipment (trucks, containers, MRF machinery) should be depreciated over standard useful lives: Trucks (7 years), Containers (10 years), MRF equipment (15 years).
- Grant funding and EPR reimbursements should be tracked separately from rate-payer funded operations.
