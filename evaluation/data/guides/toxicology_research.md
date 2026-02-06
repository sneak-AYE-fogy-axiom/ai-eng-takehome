# Toxicology Research Data Standards (Toxicology / Mutagenesis Databases)

The pharmaceutical research division follows these scientific data conventions:

## Molecule Analysis

- Only molecules with complete bond information should be included in structural analysis.
- Molecules without a defined activity label should be classified as "untested" not "inactive."
- Duplicate molecules (same structure, different IDs) should be deduplicated using canonical SMILES.

## Atom-Level Data

- Atom types must be standardized to periodic table symbols (C, N, O, H, etc.).
- Hydrogen atoms may be implicit - ensure consistent handling across all analyses.
- Charged atoms should be flagged separately for electrostatic property calculations.

## Bond Properties

- Bond types: 1 = single, 2 = double, 3 = triple, 4 = aromatic.
- Aromatic bonds should be counted separately from single/double bonds in ring analysis.
- Ring membership is determined by connected atoms - a bond is "in-ring" if both atoms are ring members.

## Activity Classification

- Mutagenic activity is binary: positive (mutagenic) vs. negative (non-mutagenic).
- Active compounds at ANY concentration are considered positive - don't threshold by potency.
- Inconclusive assay results should be excluded from model training but tracked for re-testing.

## Statistical Requirements

- Minimum dataset size for structure-activity modeling is 50 molecules per class.
- Train/test splits should stratify by activity class to maintain class balance.
- Cross-validation should use scaffold-based splitting, not random, to avoid data leakage.

## Reporting

- Always report sensitivity AND specificity for any classification model.
- Chemical structures should never be shown without corresponding activity data for context.
- Proprietary compounds should use anonymized IDs in external reports.
