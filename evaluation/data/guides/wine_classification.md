# Wine Classification and Inventory Rules (WineCellar Database)

The beverage analytics team uses these conventions for wine data:

## Quality Scoring

- Wines scored below 80 points (on the 100-point scale) are classified as "below average" and excluded from recommendation engines.
- Scores from different reviewers (Wine Spectator, Robert Parker, Wine Enthusiast) must NEVER be averaged together - always report by source.
- Wines without a quality score should be excluded from rating-based analysis entirely, not imputed.
- A "consensus pick" requires ratings from at least 3 independent reviewers with a standard deviation < 3 points.
- Vertical tastings (same wine, multiple vintages) should weight the most recent 3 vintages at 2x for current quality assessment.

## Varietal Classification

- Blended wines must contain at least 75% of a named varietal to be classified under that varietal (US TTB regulation).
- "Meritage" is a specific blend designation - do not conflate with generic "Red Blend" or "White Blend" categories.
- Normalize varietal names: "Shiraz" and "Syrah" are the same grape; "Pinot Grigio" and "Pinot Gris" are the same grape.
- Sparkling wines should be segmented by method: Traditional (Champagne), Charmat (Prosecco), Ancestral (Pétillant Naturel).
- Rosé wines are their own category regardless of grape - never lump with reds or whites.

## Pricing Tiers

- Value: under $15/bottle
- Mid-range: $15-$30/bottle
- Premium: $30-$75/bottle
- Ultra-premium: $75-$150/bottle
- Luxury: over $150/bottle
- Price comparisons must use the 750mL equivalent, even for magnums or half-bottles.
- Auction prices are NOT retail prices - track in a separate price dimension.

## Vintage Rules

- Non-vintage wines (NV) should use the release year, not a vintage year, for temporal analysis.
- Wines older than 20 years are "library wines" and their pricing follows different supply/demand dynamics.
- The vintage year refers to the harvest year, not the bottling or release year.
- "Off vintages" (years with poor growing conditions) should be flagged per region using the vintage chart reference table.
- Pre-phylloxera wines (before ~1870) are historical artifacts and should be excluded from all commercial analysis.

## Regional Hierarchy

- Region → Sub-region → Appellation → Vineyard is the standard geographic hierarchy.
- French wine regions use AOC/AOP designations; Italian use DOC/DOCG; American use AVA.
- "Old World" (Europe) and "New World" (Americas, Oceania, etc.) is the top-level regional split.
- Cross-regional comparisons must control for varietal composition to be meaningful.
- Single-vineyard designations indicate higher specificity - weight these 1.5x in terroir analysis.

## Inventory Management

- White wines and rosés should not be held more than 3 years past vintage (exceptions: Burgundy, Riesling).
- Temperature excursions above 75°F for more than 48 hours render inventory "compromised" - flag for markdown.
- Wines with fewer than 6 bottles remaining are "allocated" and require manual release approval.
- Case-quantity purchases (12+ bottles) receive a 10% discount - factor this into margin analysis.
- Organic and biodynamic certifications must be tracked separately from conventional production.
