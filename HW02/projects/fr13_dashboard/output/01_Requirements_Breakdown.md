# FR-13: Admin Dashboard — Requirements Breakdown (Phase 1)

Source: `input/Functional_Requirement.md` (FR-13: Admin Dashboard, Pool C — Web
Admin), cross-checked against `api_specification.md` §6.2. Access control is
governed by FR-12 (admin-only), referenced but not re-specified here.

## 0. Global Precondition (not repeated per requirement)

REQ-04 through REQ-07 (dashboard content: revenue and order count) describe
what the dashboard shows *once access is granted*. They implicitly assume the
actor already satisfies REQ-08, REQ-09, and REQ-10 (valid JWT, not one that's
missing or invalid, carrying `role = 'admin'`). REQ-08, REQ-09, and REQ-10
themselves cover the access-control rule, including its failure conditions, as
separate atomic requirements. This precondition is stated once here and is not
restated in each content REQ row.

**Terminology note — "dashboard" surface scope (fixes P1-G01):** REQ-08,
REQ-09, and REQ-10 below say access control applies to "dashboard data."
Per OQ-01, no dedicated dashboard endpoint/route is confirmed to exist
separately from the admin order API — the only surface confirmed today is
`GET /api/admin/orders`. These three requirements should NOT be read as
asserting two independently-behaving surfaces (a frontend dashboard route
*and* a backend API) that are proven to enforce access identically. If a
distinct frontend dashboard route is later found to exist, its access control
must be verified against these same rules independently — compliance is not
assumed to carry over from the API by extension.

## 1. Feature Areas

| Area ID | Name | Description |
| --- | --- | --- |
| AREA-01 | API Contract | Endpoint paths and base URL referenced by FR-13 (admin order data source, status update, base URL) |
| AREA-02 | Revenue Calculation | Total revenue display, its inclusion rule (delivered), and its exclusion rule (all other statuses) |
| AREA-03 | Order Count Display | Total number of orders shown on the dashboard |
| AREA-04 | Access Control | The no-token-denied rule, the invalid-token-denied rule, and the role-must-be-admin rule (per FR-12) |
| AREA-05 | Test Setup Data | Seed accounts and helper endpoints used to produce dashboard test state (not FR-13 behavior itself) |
| AREA-06 | Documentation Discrepancies | Cross-source inconsistencies noticed while reading the input (password mismatch; total_amount trust) — flagged as Observations, not requirements |

## 2. Atomic Requirements

| REQ ID | Area | Statement | Source Reference | Classification |
| --- | --- | --- | --- | --- |
| REQ-01 | AREA-01 | The admin order data source is `GET /api/admin/orders` (requires admin JWT). | §2 "Admin order data source: `GET /api/admin/orders` (requires admin JWT)." | Observation |
| REQ-02 | AREA-01 | Order status is updated via `PUT /api/admin/orders/:id/status` with body `{ "status": "confirmed" }`, allowed values: pending / confirmed / shipping / delivered / canceled. | §2 "Order status update: `PUT /api/admin/orders/:id/status`..." | Observation |
| REQ-03 | AREA-01 | The base URL for these endpoints is `http://localhost:3000`. | §2 "Base URL: `http://localhost:3000`." | Observation |
| REQ-04 | AREA-02 | The dashboard MUST display total revenue. | §3.1 "The dashboard MUST display **total revenue**." | Functional Requirement |
| REQ-05 | AREA-02 | Total revenue MUST be computed as the sum of `total_amount` of orders whose `status = 'delivered'`. | §3.1 "Total revenue MUST be computed as the **sum of `total_amount` of orders whose `status = 'delivered'`** — and ONLY those orders." | Functional Requirement |
| REQ-06 | AREA-02 | Orders whose status is `pending`, `confirmed`, `shipping`, or `canceled` MUST NOT contribute to total revenue. | §3.1 "Orders in any other status (`pending`, `confirmed`, `shipping`, `canceled`) MUST NOT contribute to total revenue." | Functional Requirement |
| REQ-07 | AREA-03 | The dashboard MUST display the total number of orders. Scope by status is not stated in the FR — not assumed here; see OQ-02. | §3.2 "The dashboard MUST display the **total number of orders**." | Functional Requirement |
| REQ-08 | AREA-04 | If no token is provided when accessing dashboard data, the request MUST be denied (dashboard = whatever surface serves this data; see Global Precondition terminology note — currently only confirmed to be the admin API, per OQ-01). | §5 "No token / invalid token: access denied." (no-token clause) | Functional Requirement |
| REQ-09 | AREA-04 | If an invalid/malformed token is provided when accessing dashboard data, the request MUST be denied (same surface-scope note as REQ-08). | §5 "No token / invalid token: access denied." (invalid-token clause) | Functional Requirement |
| REQ-10 | AREA-04 | A valid JWT alone is NOT sufficient for access to dashboard data (same surface-scope note as REQ-08); the token MUST carry `role = 'admin'`. | §3.3 "A valid JWT alone is not sufficient; the token MUST carry `role = 'admin'`." | Functional Requirement |
| REQ-11 | AREA-05 | Seeded admin account is `admin@eshop.com`, used as the admin actor for dashboard-access tests. | §6 "Seeded admin: `admin@eshop.com` — the admin actor..." | Observation |
| REQ-12 | AREA-05 | Seeded normal user account is `test@eshop.com` / `Test1234!`, used as the non-admin actor for access-denied tests. | §6 "Seeded normal user: `test@eshop.com` / `Test1234!` — the non-admin actor for the access-denied tests." | Observation |
| REQ-13 | AREA-05 | To exercise revenue, orders are created and moved through statuses via `PUT /api/admin/orders/:id/status` so that only `delivered` orders can be verified to sum into revenue. | §6 "To exercise revenue: create orders and move them through statuses via `PUT /api/admin/orders/:id/status`..." | Observation |
| REQ-14 | AREA-06 | The seeded admin account's password is inconsistent between sources: README states `Admin123!`, setup_guide states `admin123` — both should be tried and the inconsistency recorded. | §6 "...README lists password `Admin123!`, setup_guide lists `admin123`; try both, record the inconsistency." | Observation |
| REQ-15 | AREA-06 | `api_specification.md` §4.3 allows the client to supply `total_amount` at checkout, which contradicts README FR-08 (backend MUST recompute total_amount) — meaning the value summed into revenue (REQ-05) may rest on a client-controlled number rather than a backend-verified one. | §7 "`total_amount` trustworthiness — api_spec section 4.3 lets the client supply `total_amount` at checkout, contradicting README FR-08..." | Observation |

## 3. Assumptions

None identified. Per session rules, ambiguous or unstated behavior is recorded
under Open Questions (Section 4) instead of being assumed.

## 4. Open Questions

OQ-01 through OQ-09 are taken directly from §7 of the input ("Not Specified in
the FR") — none of these are answered or guessed here. OQ-10 through OQ-12 are
additional gaps identified during decomposition, each with supporting evidence.

| ID | Question | Why It Matters | Evidence |
| --- | --- | --- | --- |
| OQ-01 | Does a dedicated dashboard endpoint (e.g. `/api/admin/dashboard` or `/api/admin/stats`) exist, or are the metrics computed client-side from `GET /api/admin/orders`? | Determines whether Phase 3/4 test cases hit a dashboard-specific endpoint or must derive revenue/count from the raw orders list; must be verified against the running backend before any API-level test case is written. | §2 Note; §7 bullet 1 |
| OQ-02 | Is "total number of orders" (REQ-07) a count of ALL orders regardless of status, or only some subset? §3.2 does not qualify by status; §5 implies non-delivered orders "may still count," but this is not stated definitively. | Directly determines the expected value asserted in every order-count test case; cannot be designed without this answer. Per special instruction, logged here rather than assumed. | §3.2; §5; §7 bullet 2 |
| OQ-03 | What does the dashboard show when there are zero orders at all (0? blank? absent field?)? | Needed to define the empty-state equivalence class/expected output in Phase 2/3. | §7 bullet 3 |
| OQ-04 | What does total revenue show when there are orders but zero `delivered` orders — `0`, or empty/undefined? | Needed to distinguish "no orders at all" from "orders exist but none delivered" as separate equivalence classes. | §7 bullet 4 |
| OQ-05 | For a `canceled` order (which still has a `total_amount`): is exclusion from revenue (per REQ-06) confirmed in the running implementation, and does a canceled order count toward "total number of orders" (REQ-07)? | REQ-06 states canceled orders must not count toward revenue, but whether they count toward the order-count total is unresolved (ties to OQ-02) and worth an explicit check since a canceled order is the one case with a nonzero `total_amount` that must NOT appear in the revenue sum. | §7 bullet 5 |
| OQ-06 | Given REQ-15 (client-supplied `total_amount` vs. README FR-08 backend recompute), is the revenue sum in REQ-05 actually built on a backend-verified `total_amount`, or can it be manipulated via a tampered checkout request? | Determines whether a tampered-`total_amount` scenario should be included as a test case beyond straightforward equivalence partitioning — a correctness/security concern flagged as an Observation (REQ-15), not yet a confirmed bug. | §7 bullet 6; REQ-15 |
| OQ-07 | What currency, rounding, and number format is used for the displayed revenue? | Needed to define valid-output equivalence classes and precision expectations for the revenue field in Phase 2. | §7 bullet 7 |
| OQ-08 | What is the denied-access response shape — HTTP 401 (no/invalid token) vs. 403 (valid token but `role = 'user'`)? §5 only says "access denied" without a status code. | Determines the expected HTTP status code to assert in the access-denial test cases (REQ-08, REQ-09, REQ-10). | §7 bullet 8 |
| OQ-09 | Is `total_amount` an integer (VND, no decimals) or a decimal value? | Affects whether BVA on the revenue sum in Phase 4 needs a boundary step of 1 or of 0.01. | §7 bullet 9 |
| OQ-10 | What HTTP status code indicates a successful dashboard/orders fetch for an authorized admin? | Not stated anywhere in the input; needed for concrete expected-result assertions on the success path in Phase 3/4. | §2, §5 (success-path content is described but no status code is given) |
| OQ-11 | What is the exact response body shape for the dashboard metrics (e.g., field names/casing such as `totalRevenue`/`total_revenue`, wrapped object vs. flat fields)? | Needed to write concrete expected-output assertions in Phase 3/4; without a sample body, only the underlying values (not the structure) can be verified. | §3.1, §3.2 (field content described, no sample JSON given) |
| OQ-12 | If dashboard metrics are computed client-side from `GET /api/admin/orders` (per OQ-01), is that endpoint paginated or limited in any way? | An unstated pagination limit on the orders list would silently truncate the data set that revenue/count are computed from, producing an incorrect aggregate — a genuine correctness risk worth checking before trusting any expected value derived from that endpoint. | §2 (no pagination information given for `GET /api/admin/orders`) |

## 5. Self-Check

- [x] Every atomic requirement is traceable to the source Functional Requirement (each REQ row cites the exact section/quote).
- [x] No invented business rules or assumptions presented as fact — nothing beyond the FR's text is stated as a REQ; all gaps are in Open Questions (OQ-01..OQ-12), and Section 3 (Assumptions) explicitly contains none.
- [ ] Every equivalence class has at least one covering test case — N/A for Phase 1 (equivalence classes and test cases are produced in Phase 2/3).
- [x] IDs are unique and consistently formatted (`REQ-01`..`REQ-14`, `OQ-01`..`OQ-12`, `AREA-01`..`AREA-06`), zero-padded, no unexplained gaps.
- [x] No table cell is empty without an explicit marker — all cells populated (Assumptions section explicitly states "None identified" rather than being left blank).
- [x] Terminology is consistent throughout (consistently uses "endpoint" for API routes, "order" for the resource, "status" for the enum field, "requirement" for REQ rows).
- [x] Each REQ states one independently-testable rule — the revenue rule was split into REQ-04 (display), REQ-05 (inclusion), REQ-06 (exclusion) per special instruction, and access control was split into REQ-08 (JWT required) and REQ-09 (role must be admin) per special instruction, so a bug affecting only one of these sub-rules remains distinguishable at the requirement level.

## 6. Awaiting User Review

This is the Phase 1 artifact (Requirements Breakdown) for FR-13: Admin
Dashboard. Please review the atomic requirements, feature area grouping, and
open questions above. Reply "approved" (or similar) to proceed to Phase 2
(Equivalence Partitioning), or request specific revisions.
