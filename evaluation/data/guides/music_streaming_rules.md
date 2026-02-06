# Music Streaming Analytics Rules (Chinook Database)

Our music streaming division has the following mandatory business rules:

## Track Metrics

- Tracks shorter than 60,000 milliseconds (1 minute) should be classified as "interstitials" and excluded from play count metrics.
- Tracks longer than 600,000 milliseconds (10 minutes) are "extended plays" and count as 1.5 plays for royalty calculations.
- The Genre "TV Shows" (GenreId = 19) and "Drama" (GenreId = 21) are NOT music - never include these in music-related KPIs.

## Revenue Calculations

- Unit prices above $1.99 indicate premium content - report premium vs. standard revenue separately.
- Invoices from customers in Brazil require a 15% withholding adjustment - subtract this from gross revenue when calculating net revenue for the LATAM region.
- Never include invoices with a Total of exactly $0.99 in average transaction value calculations - these are promotional one-track purchases.

## Artist Analysis

- When counting "active artists", only include artists with at least 3 albums in the catalog.
- Artists with "Various" or "Compilation" in their name should be excluded from artist-level performance metrics.
- The MediaType "Protected AAC audio file" is deprecated - exclude these tracks from availability reports.
