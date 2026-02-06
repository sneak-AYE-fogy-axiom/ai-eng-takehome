# Craft Beer Inventory Guidelines (CraftBeer Database)

The beverage division tracks craft beer with these business rules:

## Beer Classification

- Beers with ABV (alcohol by volume) at or above 9.5% are "high-gravity" and subject to different distribution regulations.
- IBU (International Bitterness Units) above 100 are "extreme" - segment separately for customer preference analysis.
- Beers without IBU data are likely lagers or wheat beers - impute a value of 20 for analysis purposes.

## Brewery Metrics

- Breweries with fewer than 3 beers in catalog are "microbreweries" - aggregate these regionally.
- Breweries producing more than 20 distinct beers are "production breweries" and analyzed separately.
- Brewery location (city/state) is critical for distribution analysis - flag any brewery without valid location data.

## Style Analysis

- Beer style names vary wildly - normalize to these categories:
  - IPA (any style containing "IPA" or "India Pale Ale")
  - Stout/Porter (any dark beer style)
  - Lager/Pilsner (any light lager style)
  - Wheat (hefeweizen, witbier, etc.)
  - Sour (any sour/wild ale style)
  - Other
- "Session" versions of beers (ABV < 5%) should be tracked separately from their full-strength counterparts.

## Inventory Rules

- Seasonal beers (pumpkin, winter warmers, etc.) should be flagged for inventory planning.
- Never stock more than 90 days of high-gravity beers due to shelf life concerns.
- Beers without an oz (serving size) value should default to 12 oz for calculations.

## Pricing

- Price-per-ounce is the standard metric for value comparisons, not total price.
- Beers priced more than 2x the category average should be flagged as "premium" tier.
- Calculate "ABV per dollar" as an efficiency metric for value-conscious customers.
