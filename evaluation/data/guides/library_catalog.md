# Library System Analytics (LibraryDB Database)

The library operations team follows these data conventions:

## Circulation Metrics

- A "checkout" is counted when an item leaves the library; a "renewal" extends the due date without a physical return.
- Renewals count as separate circulation events for usage statistics but NOT for unique checkout counts.
- Overdue items (past due date and not returned) should be excluded from "active circulation" metrics after 60 days.
- Items reported lost or damaged are removed from circulation counts on the date reported, not the original due date.
- Inter-library loans (ILL) are tracked separately and should not inflate local collection usage metrics.

## Collection Management

- Items not circulated in 5+ years are candidates for "weeding" - flag these in collection health reports.
- Reference materials (encyclopedias, atlases, etc.) are non-circulating and excluded from checkout statistics.
- Digital resources (e-books, audiobooks, streaming) use "access" counts, not "checkout" counts - never combine with physical circulation.
- Periodicals have a 12-month shelf life for current issues; back issues move to archives.
- Donated materials must clear a 30-day processing queue before appearing in the active catalog.

## Patron Classification

- Patrons are segmented by type: Adult, Young Adult (13-17), Juvenile (0-12), Senior (65+), Institutional.
- "Active patrons" are those with at least 1 circulation event in the past 12 months.
- Patron privacy is paramount - NEVER report individual-level checkout histories in any analysis.
- Non-resident patrons (those outside the taxing district) are tracked separately for fee and funding purposes.
- Staff checkouts for processing, displays, or programs should be excluded from public circulation metrics.

## Branch Performance

- Per-capita circulation (checkouts per resident in service area) is the primary branch performance metric.
- Programming attendance (story time, classes, events) counts as a separate usage metric from circulation.
- Square footage utilization (visits per square foot per month) measures physical space efficiency.
- Branches with fewer than 5,000 annual checkouts are "low-volume" and may have different staffing models.
- Mobile libraries (bookmobiles) report to their home branch for administrative purposes but track usage independently.

## Budget and Acquisitions

- Materials budget is allocated by format: 60% print, 25% digital, 10% AV, 5% other (target ratios).
- Cost-per-circulation is the primary efficiency metric: total materials spend / total circulations.
- Bestseller leasing programs (McNaughton, etc.) are rental expenses, not acquisitions - track separately.
- Gift materials are valued at average acquisition cost for the format, not donor-claimed value.
- Periodical subscriptions renew annually - track as recurring commitments, not one-time purchases.

## Holds and Requests

- Hold queue length > 10 for a single title triggers an automatic additional copy purchase recommendation.
- Holds placed but never picked up ("no-shows") within 7 days are cancelled and tracked as a separate metric.
- The holds-to-copies ratio should not exceed 5:1 for popular titles - above this, patron satisfaction drops significantly.
- Patron-initiated purchase requests should be fulfilled within 21 business days as a service standard.
- Suspended holds (patron-initiated pauses) do not count toward queue length calculations.
