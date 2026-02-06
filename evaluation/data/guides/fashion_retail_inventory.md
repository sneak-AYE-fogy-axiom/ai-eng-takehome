# Fashion Retail Inventory Analytics (FashionDB Database)

The retail analytics team follows these conventions:

## Product Classification

- Products are categorized by: Department (Men's, Women's, Kids, Accessories), Category (Tops, Bottoms, Outerwear, Footwear, etc.), Sub-category (T-shirts, Dress shirts, etc.).
- SKU (Stock Keeping Unit) is the most granular level - each size/color combination is a unique SKU.
- "Core" styles (offered year-round) are analyzed separately from "fashion" styles (seasonal, limited runs).
- Gifting items (scarves, wallets, jewelry) have different demand patterns and should be flagged for holiday planning.
- Private label vs. national brand products have different margin profiles - always segment in profitability analysis.

## Size and Fit

- Size curves (the distribution of sizes ordered per style) are critical for allocation - track actual vs. planned size curves.
- "Broken sizes" (when only extreme sizes remain) trigger markdown recommendations - a style with < 50% size coverage is considered "broken."
- Extended sizes (plus, petite, tall) are tracked as separate collections with their own sales velocity benchmarks.
- Return rate by size identifies fit issues - sizes with return rates > 2x the style average need technical specification review.
- Vanity sizing varies by brand - never compare size labels across brands without standardized measurement data.

## Pricing and Markdown

- Original price → First markdown → Second markdown → Clearance → Final disposition is the standard pricing lifecycle.
- "Sell-through rate" = (units sold) / (units received) × 100. Target varies: 65% at full price, 90% total through clearance.
- Initial markup (IMU) = (Original price - Cost) / Original price × 100.
- Maintained markup (MMU) = (Actual revenue - Cost) / Actual revenue × 100. Always lower than IMU due to markdowns.
- Promotional markdowns (temporary price reductions) are distinct from permanent markdowns - track both but report separately.

## Inventory Health

- Weeks of Supply (WOS) = (Current inventory) / (Average weekly sales). Target varies by category (8-12 weeks for basics, 4-6 for fashion).
- "Aged inventory" is product not sold within one selling season. Age buckets: 0-30 days, 31-60, 61-90, 91-180, 180+ days.
- Inventory-to-sales ratio (I/S) above 4.0 for fashion items indicates overstocking - investigate.
- Stockout rate = (days with zero inventory) / (days in selling period) × 100. Target: < 5% for core items.
- In-transit inventory (between distribution center and store) counts as "pipeline" inventory, not available-for-sale.

## Seasonal Planning

- Fashion operates on a 4-season calendar: Spring (Feb-Apr), Summer (May-Jul), Fall (Aug-Oct), Holiday/Winter (Nov-Jan).
- "Open-to-buy" (OTB) is the remaining budget for inventory purchases in a period - never exceed without VP approval.
- Pre-season buys (>60% of total) vs. in-season reorders (<40%) is the target planning ratio.
- Weather sensitivity: unseasonable weather shifts demand ±15-20% for weather-dependent categories (outerwear, swimwear).
- BOPIS (Buy Online, Pick Up In Store) orders are attributed to the e-commerce channel for sales, but the store for inventory fulfillment.

## Channel Attribution

- Sales channels: Brick-and-mortar stores, E-commerce (owned site), Marketplace (Amazon, etc.), Wholesale, Off-price (TJ Maxx, etc.).
- Customer returns must be attributed to the channel of original purchase, not the return location.
- "Ship-from-store" orders are e-commerce sales fulfilled from store inventory - track for both channels.
- Wholesale accounts (department stores) report sell-through data on a 2-4 week delay - factor this into analysis.
- Off-price channel sales should NEVER be included in full-price sales analysis - they represent end-of-life inventory disposition.

## Sustainability Metrics

- Materials composition (cotton, polyester, recycled content %) must be tracked per SKU for sustainability reporting.
- Carbon footprint per garment considers: raw materials, manufacturing, transportation, packaging, end-of-life.
- Unsold inventory sent to landfill is tracked as "waste" - target zero landfill through donation, recycling, or repurposing.
- Supplier audit scores (labor, environmental, safety) are tracked per factory and affect order allocation decisions.
- "Deadstock" (never-sold inventory returned from stores) volume is tracked monthly as a supply chain efficiency metric.
