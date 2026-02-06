# Archaeological Excavation Data Standards (ArchaeoDB Database)

The cultural heritage analytics team follows these conventions:

## Site Classification

- Sites are classified by type: Settlement, Burial, Ceremonial/Religious, Industrial/Production, Military, Maritime/Underwater.
- Site significance levels: National Register, State Register, Locally Significant, Not Evaluated, Not Eligible.
- "Multi-component" sites (evidence of multiple occupation periods) require separate analysis per component/stratum.
- Destroyed or heavily disturbed sites are retained in the database with `integrity_status = 'compromised'`.
- CRM (Cultural Resource Management) sites from compliance surveys are tracked separately from research-driven excavations.

## Artifact Cataloging

- Every artifact receives a unique catalog number following the format: [Site Code]-[Unit]-[Level]-[Sequence].
- Artifacts are classified using a standardized typology: Lithics, Ceramics, Metal, Glass, Bone/Organic, Other.
- Provenience (exact findspot) is recorded as: Unit (excavation square), Level/Stratum, Depth below surface, and 3D coordinates when available.
- Surface finds (not from excavation) are flagged with `context = 'surface'` and weighted lower in spatial analysis.
- Artifacts from disturbed contexts (plowzone, backfill, construction fill) are included in counts but flagged as `context_integrity = 'disturbed'`.

## Stratigraphy

- The Harris Matrix is the standard tool for recording stratigraphic relationships (above, below, same-as, cuts, cut-by).
- Natural soil layers are distinguished from cultural deposits - only cultural deposits are assigned feature numbers.
- "Sealed contexts" (layers with undisturbed deposits above and below) provide the most reliable chronological information.
- Mixed contexts (containing materials from multiple periods) should be dated by the LATEST material present (terminus post quem).
- Profile drawings are required for all excavation walls at a minimum scale of 1:20.

## Dating Methods

- Radiocarbon dates are reported as: Raw date ± error (BP), Calibrated date range (cal BC/AD) at 2-sigma (95.4%) confidence.
- Always use calibrated dates for cross-site comparison - raw radiocarbon dates are NOT directly comparable.
- Thermoluminescence (TL) and Optically Stimulated Luminescence (OSL) dates have larger error ranges than radiocarbon - report with full uncertainty.
- Dendrochronology provides the highest precision (exact year) but is only applicable where suitable wood is preserved.
- Relative dating (seriation, typological comparison) is clearly distinguished from absolute dating in all reports.

## Spatial Analysis

- All coordinates use a site-specific grid tied to a known datum point with real-world coordinates (UTM or lat/long).
- GIS layers include: site boundary, excavation units, features, artifact density (by class), topography.
- Density calculations use artifacts per cubic meter (volumetric) for 3D analysis or per square meter (areal) for surface surveys.
- "Hot spots" (high artifact density clusters) are identified using Kernel Density Estimation (KDE) with a minimum of 30 artifacts.
- Buffer zones (50m, 100m, 500m around sites) are used for viewshed, proximity, and environmental sensitivity analysis.

## Faunal and Botanical Analysis

- Faunal remains are identified to the most specific taxonomic level possible; "Unidentified mammal" counts separately from identified species.
- NISP (Number of Identified Specimens) and MNI (Minimum Number of Individuals) are both reported - never use only one.
- Flotation samples (for recovering plant remains) should be collected from at least 10% of excavated features.
- Cut marks, burning, and fragmentation patterns on bone are recorded for butchery pattern analysis.
- Modern contaminants (roots, rodent burrows, recent animal bone) must be identified and excluded from cultural analysis.

## Ethics and Compliance

- NAGPRA (Native American Graves Protection and Repatriation Act) applies to all federally funded excavations in the US.
- Human remains receive separate handling protocols and are not included in standard artifact databases.
- Section 106 (National Historic Preservation Act) consultation is documented per project with tribal/SHPO correspondence.
- Antiquities laws vary by country - international projects must comply with both host country and researcher's country of origin regulations.
- All excavation data is archived with the appropriate state repository within 2 years of project completion.
