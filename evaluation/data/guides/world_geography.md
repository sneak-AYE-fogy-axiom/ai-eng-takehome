# World Geography Data Standards (world / Countries Databases)

The international operations division uses these geographic data conventions:

## Country Identification

- Use ISO 3166-1 alpha-3 country codes as the primary identifier, not country names.
- Country names can vary (e.g., "USA" vs "United States") - always join on codes.
- Historical country codes (Soviet Union, Yugoslavia, etc.) should be mapped to successor states.

## City Data

- "Major cities" are defined as those with population > 2,000,000.
- Capital cities should always be flagged regardless of population size.
- City populations change frequently - always note the census/estimate year.

## Language Analysis

- Countries may have multiple official languages - don't assume one-to-one mapping.
- "Percentage of speakers" is for the listed language - percentages across languages may exceed 100% due to multilingualism.
- Indigenous languages with small speaker populations should be preserved in data but may need aggregation for analysis.

## Population Metrics

- Population density = Population / Surface Area (in persons per sq km).
- Use the most recent population estimate available, not census figures which may be dated.
- Population projections should be clearly labeled as estimates with confidence ranges.

## Economic Indicators

- GNP/GDP figures must specify the year and whether they're nominal or PPP-adjusted.
- Per-capita metrics require matching population figures from the same year.
- Economic data for very small countries may be unreliable - flag countries with < 100,000 population.

## Regional Groupings

- Regions (continents) are the highest aggregation level.
- Sub-regions should align with UN geographic classifications for consistency.
- "Developing" vs "Developed" classifications change over time - specify the classification year/source.

## Data Quality

- Life expectancy and infant mortality rates from conflict zones may be estimates.
- Independence dates should be verified for recently formed nations.
- Flag territories and dependencies separately from sovereign nations.
