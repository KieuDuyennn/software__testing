# FR13 manual execution guide for TC-07 and TC-08

TC-07 and TC-08 are intentionally manual because FR13 reads global order data and
the shared test harness seeds delivered orders. Run these cases against a fresh,
isolated backend/database before any other FR13 worker starts.

## TC-07 — zero orders

1. Start a disposable backend/database using the normal project seed/reset command.
2. Remove all rows from the orders table in that disposable database.
3. Open the admin dashboard with a valid admin account.
4. Verify the order-count KPI is `0` and the revenue KPI is the documented empty
   state (normally `0`).
5. Record a screenshot and the API response from `GET /api/admin/orders`.

Expected: the dashboard renders successfully, shows zero orders, and does not show
stale revenue from a previous session.

## TC-08 — orders exist, none delivered

1. Reset the same disposable database.
2. Seed one or more orders whose statuses are only `pending`, `confirmed`,
   `shipping`, or `canceled`; do not seed `delivered` orders.
3. Open or reload the admin dashboard.
4. Verify the order-count KPI equals the seeded order count and the revenue KPI is
   `0`.
5. Record a screenshot and the API response from `GET /api/admin/orders`.

Expected: all seeded orders are counted, but revenue remains zero because no order
has status `delivered`.

## Isolation and evidence

Do not run these cases against the shared seeded database: later workers cannot restore
the no-delivered state because the status machine has no transition out of `delivered`.
Attach the database reset command, seed payload, screenshot, API response, timestamp,
and browser version to the test record.
