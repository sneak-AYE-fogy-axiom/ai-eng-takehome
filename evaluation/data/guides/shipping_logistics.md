# Shipping and Logistics Analytics (LogisticsDB Database)

The supply chain analytics team follows these conventions:

## Shipment Classification

- Shipments are classified by mode: Air, Ocean, Rail, Truck (LTL), Truck (FTL), Intermodal, Parcel.
- "Last mile" deliveries (final leg to consumer) are always analyzed separately from line-haul segments.
- Hazmat shipments (hazardous materials class 1-9) follow a completely separate analytics pipeline with additional compliance fields.
- Temperature-controlled ("reefer") shipments require continuous temperature monitoring - gaps > 30 minutes invalidate the chain of custody.
- Consolidations (multiple customers' goods in one container) should be allocated costs by weight or volume, whichever produces the higher charge ("dimensional weight" rule).

## Transit Time Calculations

- Transit time starts at "gate out" (departure from origin facility), not at order placement or pickup appointment.
- Transit time ends at "proof of delivery" (POD) timestamp, not at arrival at destination facility.
- Exclude weekends and holidays from "business day" transit time calculations; include them in "calendar day" calculations.
- Customs clearance time is tracked separately and should not be included in carrier transit performance metrics.
- Shipments in "held" status (awaiting documentation, payment, or inspection) pause the transit clock.

## Cost Analysis

- All freight costs must be decomposed into: Line-haul, Fuel surcharge, Accessorial charges, Duties/Taxes, Insurance.
- Cost-per-unit-shipped is the primary efficiency metric; cost-per-mile is secondary for carrier benchmarking.
- Accessorial charges (liftgate, inside delivery, detention, etc.) should be reported separately from base freight rates.
- Fuel surcharges fluctuate weekly - always tie costs to the applicable fuel index period.
- Spot market rates are NOT comparable to contract rates - analyze separately.

## Carrier Performance

- On-time delivery is measured against the originally promised date, not revised ETAs.
- Carriers with fewer than 50 shipments in the measurement period should be excluded from ranking.
- Claims ratio = (number of claims / total shipments) × 100. Target is < 1%.
- Carrier scorecards weight: On-time (40%), Claims (25%), Cost (20%), Communication (15%).
- "Preferred carriers" maintain scores above 85/100 for 4 consecutive quarters.

## Warehouse Operations

- Inventory accuracy is measured by cycle counts - target is 99.5% SKU-level accuracy.
- Pick-pack-ship cycle time starts at order release and ends at carrier tender.
- Storage utilization above 85% indicates the warehouse is "effectively full" and service levels will degrade.
- Cross-dock shipments (no storage, immediate transfer) have a different cost model and should be tracked separately.
- Returns ("reverse logistics") processing time is measured separately and has a target of 48 hours.

## Customs and Trade Compliance

- HS (Harmonized System) codes at the 6-digit level are internationally standard; digits 7+ are country-specific.
- Free Trade Agreement (FTA) qualification must be verified per shipment - do not assume based on country of origin alone.
- Declared value for customs must match commercial invoice value ± 5% or the shipment is flagged for audit.
- Denied party screening is mandatory for all international shipments before booking.
- Incoterms (FOB, CIF, DDP, etc.) determine the cost allocation point and must be recorded for every international shipment.

## Carbon and Sustainability

- Carbon emissions are calculated using the GLEC (Global Logistics Emissions Council) framework.
- Emission factors vary by mode: Air (~500g CO2/ton-km), Truck (~60g), Rail (~20g), Ocean (~10g).
- "Carbon-neutral" shipments require verified offsets and should be flagged, not reclassified.
- Packaging waste metrics track weight of packaging material vs. weight of goods shipped.
- Route optimization for emissions reduction must not increase transit time by more than 15%.
