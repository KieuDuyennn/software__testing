# FR-13 Dashboard — test-case matrix (Pool C)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Automated:** **50** — 7 positive / 28 negative / 15 edge; 30 UI, 20 API.
**Status:** implemented, runtime-validated and executed on Chromium; **29 passed / 21 failed**.
**Data file:** `automation/data/fr13_dashboard.json`
**Failure evidence:** `docs/test-plan/FR13_Failure_Evidence.md`
**Spec:** `automation/tests/fr13_dashboard/fr13.dashboard.spec.ts`

HW02 source: `HW02/submission/projects/fr13_dashboard/output/`
HW02 execution: `HW02/submission/reports/TC_Checklist.md` §FR-13 (14 designed, 14 executed, **8 divergent**).

HW02 confirmed a revenue-doubling defect on this page. Keep at least one case that
recomputes the KPI from an independent source — a test that only checks "a number
is displayed" would have passed against that defect.

## The defect this feature is built around

`frontend-admin/src/App.jsx` L218:

```js
if (o.status === "delivered") return sum + o.total_amount * 2;
```

Every delivered order is counted twice. HW02 logged this as **BUG-09** (Critical) with
a screenshot: one delivered order of 100,000 ₫ displayed as 200,000 ₫. Exclusion logic
is correct — only `delivered` is summed — the multiplier is the fault.

**Consequence for this suite:** the revenue assertions below are expected to FAIL on
the current build. That is the intended outcome (project rule §4) — the assertion
encodes the specification, not the defect. Do not calibrate any expected value to `×2`.

UI layer is the **admin app** (`frontend-admin`), which does render a dashboard — so
unlike FR-11 there is no ambiguity about where to assert.

## Carried over from HW02

| # | TC ID | Type | Intent | Setup (API) | Assert (UI) | HW02 result | Pattern | Automated? |
|---|---|---|---|---|---|---|---|---|
| 1 | TC-01 | positive | admin sees dashboard; revenue counts delivered only | 5 orders, one per status | KPI cards render; revenue reflects delivered only | ✅ | 1 | ☐ |
| 2 | TC-02 | negative | no token → denied | — | denied, dashboard not rendered | ✅ (401) | 1 + 2 | ☐ |
| 3 | TC-03 | negative | malformed token → denied | inject bad token | denied | ✅ (403) | 1 + 2 | ☐ |
| 4 | TC-04 | negative | valid **non-admin** token → denied | login as `USER_EMAIL` | **HW02 found HTTP 200, 3 orders returned — access granted (BUG-08)** | ❌ | 1 + 2 | ☐ |
| 5 | TC-05 | negative | `canceled` 50 must not leak into revenue | 1 delivered=100, 1 canceled=50 | revenue = `100` | ❌ (showed 200) | 2 + 3 | ☐ |
| 6 | TC-06 | negative | pending/confirmed/shipping excluded | 1 delivered=100 + 3 others=50 | revenue = `100` | ❌ (delivered doubled) | 2 + 3 | ☐ |
| 7 | TC-07 | edge | zero orders at all | empty system | revenue and count each asserted **independently** | ✅ (0 / 0) | 1 | ☐ |
| 8 | TC-08 | edge | orders exist, none delivered | 1 pending=50 | revenue = `0` | ✅ | 1 | ☐ |
| 9 | BVA-02 | edge | delivered `total_amount = 0` | 1 delivered=0 | revenue = `0` | ✅ | 3 | ☐ |
| 10 | BVA-03 | edge | delivered `total_amount = 1` | 1 delivered=1 | revenue = `1` | ❌ (showed 2) | 3 | ☐ |
| 11 | BVA-05 | edge | delivered `total_amount = 0.01` | 1 delivered=0.01 | revenue = `0.01`, not rounded to 0 | ❌ (showed 0.02) | 3 | ☐ |
| 12 | BVA-06 | edge | three delivered 1000/2000/3000 | 3 delivered orders | revenue = `6000` | ❌ (showed 12000) | 3 | ☐ |
| 13 | BVA-01 | edge | delivered `total_amount = -1` | seed a negative amount | revenue = `-1`, not clamped | ❌ (showed −2) | 3 | ☐ |
| 14 | BVA-04 | edge | delivered `total_amount = -0.01` | seed a negative amount | revenue = `-0.01` | ❌ (showed −0.02) | 3 | ☐ |

**14 cases — over the ≥12 minimum.** BVA-01 and BVA-04 carried a "may not be
producible via any documented flow" caveat in HW02 (OQ-16), but the checklist shows
both were executed and stored, so negative amounts are reachable in practice.

## Derived additions — proposed, pending review

Each closes something HW02 left open rather than inventing new ground.

| # | Proposed ID | Type | Intent | HW02 gap it closes |
|---|---|---|---|---|
| 15 | TC-09 | positive | order **count** with a mixed status set — assert whether it is 5 (all) or 1 (delivered only), and record which | OQ-02 "total number of orders scope" was never resolved; HW02 listed both candidates and asserted neither |
| 16 | TC-10 | edge | one delivered order worth `0` vs zero delivered orders must be distinguishable | OQ-18 — HW02 explicitly left this open and "not graded either way" |
| 17 | TC-11 | negative | a tampered client-supplied `total_amount` at checkout flows straight into revenue | OQ-06 / REQ-15 — flagged as a correctness/security concern, "not yet a confirmed bug", never tested. `api_specification.md` §4.3 lets the client supply `total_amount`, contradicting README FR-08's "backend must recompute" |
| 18 | TC-12 | edge | revenue number format — currency symbol, thousands separator, decimal places | OQ-07 / OQ-09 left number format and integer-vs-decimal precision unresolved throughout |
| 19 | TC-13 | edge | moving an order `delivered → canceled` **removes** its amount from revenue | HW02 only ever measured static data sets; it never re-read the dashboard after a status transition, even though `PUT /api/admin/orders/:id/status` is documented and used in its own setup. A cached or one-shot total would pass every HW02 case and fail here |
| 20 | TC-14 | edge | revenue stays correct when the order set is large enough to risk a page limit | OQ-12 — HW02 wrote "confirm all orders are actually returned before evaluating… an unnoticed page limit would silently invalidate both assertions", but only ever treated it as a manual precondition check, never as a test |

With these, FR-13 reaches **20 cases**.

## Corrections forced by the live SUT (Stages 0–3, 2026-08-10)

Everything above was written against HW02's notes. Standing the admin app up and probing
it changed four things about how these cases can be expressed. The rule is the project's
own: where a prior artifact and the running app disagree, the app is the fact.

**1. Absolute expected values are unrunnable here.** HW02 wrote "revenue = 100" against
an empty system. The SUT database is never reset between the nine required runs and
already holds 20+ orders, so no absolute figure can be stated in advance. Every revenue
and count case is restated as a **delta**: measure, seed, re-measure, assert the change.
This is invariant to whatever the database already holds. Rows 6–20 below are the same
cases HW02 designed, re-expressed.

**2. TC-13 cannot run as designed.** HW02's TC-13 was "`delivered → canceled` removes the
amount". The status machine (`server.js:541-583`) has **no rule with a `delivered`
source**, so the transition is refused with 400 — verified. The case is split: `TC-13`
now asserts the refusal that the machine *does* express, and `TC-13b` carries HW02's real
intent (re-read the dashboard *after* a transition, which HW02 never did) onto
`canceled → delivered`, a transition this build explicitly permits (`server.js:566`).

**3. OQ-16 is resolved: negative amounts ARE reachable.** HW02 caveated BVA-01/BVA-04 as
"may not be producible via any documented flow". `POST /api/checkout` writes
`total_amount` straight from the request body with no validation — `0`, `1`, `0.01`, `-1`
and `999999999` all verified accepted and stored. Both BVA rows are automatable.

**4. Access control needs a second layer.** HW02's TC-04 asserts only at the UI. The
admin check lives **only** in `handleLogin` in the browser; `authenticateToken`
(`server.js:118-128`) verifies the JWT and never reads `role`. A UI-only case therefore
reports the gate as working. Six API rows and one token-injection row were added so the
suite can see past it.

## Automated case list — 50 cases

All 35 live in `automation/data/fr13_dashboard.json`. `HW02 origin` is the row's
`hw02_ref`, so every case traces back to a designed case or a recorded open question.
Nothing here was invented to reach a number.

| # | TC ID | Type | Layer | Intent | HW02 origin |
|---|---|---|---|---|---|
| 1 | FR13-TC-01 | positive | ui | admin reaches the dashboard; both KPI cards parse to a finite number | TC-01 |
| 2 | FR13-TC-01b | edge | ui | dashboard is the landing view — no route needed | TC-01 (route correction) |
| 3 | FR13-TC-02 | positive | ui | revenue = sum of `total_amount` over `delivered`, recomputed from the API | TC-01 / BUG-09 |
| 4 | FR13-TC-09 | positive | ui | order-count KPI = number of orders the API returns | OQ-02 |
| 5 | FR13-TC-12 | edge | ui | revenue rendered as currency: symbol + grouped thousands | OQ-07 / OQ-09 |
| 6 | FR13-TC-05 | negative | ui | a `canceled` order does not enter revenue | TC-05 |
| 7 | FR13-TC-06a | negative | ui | a `pending` order does not enter revenue | TC-06 |
| 8 | FR13-TC-06b | negative | ui | a `confirmed` order does not enter revenue | TC-06 |
| 9 | FR13-TC-06c | negative | ui | a `shipping` order does not enter revenue | TC-06 |
| 10 | FR13-BVA-02 | edge | ui | delivered `0` → revenue delta `0` — **diagnostic row** | BVA-02 |
| 11 | FR13-BVA-03 | edge | ui | delivered `1` → revenue delta `1` | BVA-03 |
| 12 | FR13-BVA-05 | edge | ui | delivered `0.01` → delta `0.01`, not rounded to 0 | BVA-05 / OQ-09 |
| 13 | FR13-BVA-01 | edge | ui | delivered `-1` → delta `-1`, not clamped | BVA-01 / OQ-16 |
| 14 | FR13-BVA-04 | edge | ui | delivered `-0.01` → delta `-0.01` | BVA-04 / OQ-16 |
| 15 | FR13-BVA-06 | edge | ui | three delivered 1000/2000/3000 → delta `6000` | BVA-06 |
| 16 | FR13-TC-10 | edge | ui | one delivered `0` is distinguishable from no delivered orders | OQ-18 |
| 17 | FR13-TC-13 | negative | api | `canceled → delivered` must be refused | TC-13 (restated) |
| 18 | FR13-TC-13b | edge | ui | revenue does not absorb an order resurrected from `canceled` | TC-13 (recomputation intent) |
| 19 | FR13-TC-14 | edge | ui | order count keeps counting past a 25-order batch (page-limit detector) | OQ-12 |
| 20 | FR13-TC-11 | edge | api | client-supplied `total_amount` must be recomputed server-side | OQ-06 / REQ-15 |
| 21 | FR13-TC-04 | negative | ui | non-admin credentials refused at the admin form | TC-04 |
| 22 | FR13-TC-16 | negative | ui | empty credentials refused | derived (input validation) |
| 23 | FR13-TC-17 | negative | ui | unknown e-mail refused without disclosing the cause | derived (README FR-02 L42) |
| 24 | FR13-TC-18 | negative | ui | wrong password refused for an account that *is* admin | derived (TC-04 companion) |
| 25 | FR13-TC-02ui | negative | ui | anonymous visitor sees no KPI figure | TC-02 |
| 26 | FR13-TC-03ui | negative | ui | malformed token in storage does not render the dashboard | TC-03 |
| 27 | FR13-TC-04b | negative | ui | **valid non-admin token in storage** does not render the dashboard | TC-04 / BUG-08 at the UI layer |
| 28 | FR13-TC-20 | positive | ui | logout clears the stored token, not just the React state | derived (session lifecycle) |
| 29 | FR13-API-01 | negative | api | `GET /admin/orders` with no token refused | TC-02 |
| 30 | FR13-API-02 | negative | api | `GET /admin/orders` with a malformed token refused | TC-03 |
| 31 | FR13-API-03 | negative | api | `GET /admin/orders` with a valid **non-admin** token refused | TC-04 / BUG-08 |
| 32 | FR13-API-04 | negative | api | `GET /admin/users` with a valid non-admin token refused | TC-04 (second endpoint) |
| 33 | FR13-API-05 | positive | api | `GET /admin/orders` with an admin token returns the array — **control row** | TC-01 (contract) |
| 34 | FR13-API-06 | negative | api | `PUT /admin/orders/:id/status` with a non-admin token refused | derived from TC-04 |
| 35 | FR13-TC-19 | negative | api | a user cannot grant themselves `admin` via `PUT /api/users/me` | derived (defeats TC-04's premise) |
| 36 | FR13-TC-21 | edge | ui | a mixed batch of all five statuses moves revenue by the delivered amount only | TC-01 (mixed set, atomic) |
| 37 | FR13-TC-22 | edge | ui | reloading twice changes neither KPI (guards against per-fetch accumulation) | derived (recomputation) |
| 38 | FR13-TC-23 | positive | ui | a valid **admin** token in storage *does* render — **control for TC-04b** | control row |
| 39 | FR13-API-07 | negative | api | an expired but correctly-signed token is refused | derived (TC-03 companion) |
| 40 | FR13-API-08 | positive | api | the orders payload carries `id`, numeric `total_amount`, known `status` | derived (contract) |
| 41 | FR13-API-09 | negative | api | correctly signed token with no role cannot read all orders | TC-04 / BUG-08 |
| 42 | FR13-API-10 | negative | api | admin-role token whose subject does not exist cannot read all orders | TC-04 / BUG-08 |
| 43 | FR13-API-11 | negative | api | anonymous caller cannot read the admin users feed | TC-02 (second endpoint) |
| 44 | FR13-API-12 | negative | api | anonymous status write is refused and leaves the order pending | TC-02 / API-06 |
| 45 | FR13-API-13 | negative | api | malformed-token status write is refused and leaves the order pending | TC-03 / API-06 |
| 46 | FR13-API-14 | negative | api | null checkout total is rejected and creates no order | OQ-06 / REQ-15 |
| 47 | FR13-API-15 | negative | api | nonnumeric checkout total is rejected and creates no order | OQ-06 / REQ-15 |
| 48 | FR13-API-16 | negative | api | object checkout total produces a controlled 4xx, not a 500/order | OQ-06 / REQ-15 |
| 49 | FR13-API-17 | negative | api | numeric-string checkout total is rejected and creates no order | OQ-06 / REQ-15 |
| 50 | FR13-TC-24 | edge | ui | count crosses the common 100-row pagination boundary | OQ-12 |

**Totals:** 7 positive · 28 negative · 15 edge — 30 UI, 20 API. Well past the ≥ 12 minimum.

Rows 36–40 were added after the Stage-5 human review, together with the eight corrections
recorded as findings 18–25 in `AI_Review_Gap_Analysis.md`. Three of them close a specific
hole the review identified:

- **TC-21** exercises inclusion and exclusion in *one* measurement with five distinct
  amounts, so a leak identifies **which** status leaked by the size of the delta —
  something the four separate exclusion rows cannot do.
- **TC-22** guards the assumption every other delta row rests on: that the KPI is
  recomputed per fetch rather than accumulated. If it were accumulated, every delta row
  would read correctly once and drift afterwards.
- **API-08** pins the payload contract that all revenue assertions read. It is the row
  that would have caught the scaffold's `order.total` mistake (finding 15) as a contract
  failure instead of a confusing revenue mismatch.

Three rows exist to keep the others readable rather than to find a defect of their own:

- **BVA-02 (diagnostic).** `0` is the only delivered amount a doubling fault cannot
  distort. Green here while BVA-03/05/06 are red says the fault is *multiplicative* —
  not a wrong status filter and not a double-counted row. One reading instead of a wall.
- **API-05 (control).** Without a row that must return 200, a server that refused
  everybody would pass all four refusal rows.
- **TC-23 (control).** Without a row proving an injected *admin* token DOES render the
  dashboard, TC-04b ("an injected non-admin token must not render it") could pass because
  token injection is broken outright rather than because the role is enforced. The control
  is what gives the refusal its meaning.

Rows 41–50 are the second bug-hunting wave. They target partitions not covered by the
first 40 rather than adding cosmetic variants: valid-signature/invalid-authority JWTs,
route-level write guards with a post-condition, four JSON/SQLite type boundaries for
the KPI's upstream `total_amount`, and the 100-row pagination boundary. The write and
checkout cases assert the database side effect as well as HTTP status; a handler that
returns an error after mutating data therefore cannot false-pass.

### Cross-run safety

Every conforming run seeds **145 orders** (435 across the three browsers): the original
42, two protected write targets, and the 101-order pagination batch. On the current
defective build the four rejected-checkout rows also create one order each, so the
observed total is **149 per browser**. This is why no row asserts
an absolute figure. The four `canceled`/`pending`/`confirmed`/`shipping` exclusion rows
and every BVA row measure only their own delta, so accumulated data cannot move them.
Only TC-18 sends a wrong password to the seeded admin, once after worker setup tokens
have already been minted locally; no setup path depends on a later successful login.
See OQ-19 below.

### Clean Chromium execution — 50 cases (2026-08-10 18:40 UTC+7)

With the backend in its documented `LOADTEST=1` test-harness mode (to bypass the global
200-request cap), the complete suite finished **29 passed / 21 failed / 0 skipped** in
1.8 minutes. The 21 red cases group into six product mechanisms rather than 21 bugs:

| Root-cause candidate | Failing cases | Evidence |
|---|---:|---|
| Delivered revenue is multiplied by 2 | 8 | TC-02, BVA-03/05/01/04/06, TC-13b, TC-21 |
| State machine accepts `canceled → delivered` | 1 | TC-13 returned 200 |
| Checkout trusts/does not validate client `total_amount` | 5 | TC-11 and API-14–17; every invalid value created an order |
| Admin routes authenticate signatures but do not authorise role | 5 | TC-04b, API-03/04/06/09 returned/rendered data |
| Admin route does not resolve an authoritative user subject | 1 | API-10: nonexistent id + admin claim returned all orders |
| Profile update permits self-promotion to admin | 1 | TC-19 returned 200 and role changed |

The newly added wave alone ran **4 passed / 6 failed**. API-11–13 and TC-24 passed;
API-09/10 and API-14–17 failed. HTML and JSON evidence are under
`reports/html/fr13/all/` and `reports/json/fr13-all.json`.

The same 10-case wave produced the identical **4 passed / 6 failed** verdict on Firefox
and WebKit. Because a long-lived backend child is replaced by this environment after
roughly a minute, those engines were executed in short attributable batches. Firefox's
first 17-API batch contains one environmental `ECONNREFUSED` at API-11; the clean
one-case rerun passes and supersedes only that result. Evidence:

- Firefox: `fr13-firefox-wave.json`, corrected API-11 in
  `fr13-firefox-wave-api11.json`, pagination in
  `fr13-firefox-wave-pagination.json`.
- WebKit: `fr13-webkit-wave-api09.json`, `fr13-webkit-wave-api10-17.json`, and
  `fr13-webkit-wave-pagination.json`.

No product finding is based on the interrupted full-Firefox attempts or the one
`ECONNREFUSED`; the six new red cases are supported consistently by all three engines.

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| TC-07 | "Zero orders in the entire system". The dashboard reports **global** totals and the SUT database is never reset between runs; this suite now seeds at least 145 valid orders per browser. The state is unreachable without dropping the shared database, which would destroy accumulated evidence. | A manual run against a freshly restarted backend, before any suite executes. `backend/database.js` re-seeds every table on start, so the state is *producible* — just not while sharing the SUT. TC-10 covers the part that matters (a zero-value delivered order must still be counted). |
| TC-08 | "Orders exist, none delivered" — same reason. Delivered orders already exist globally and cannot be un-delivered: the machine has no transition out of `delivered`. | Same as TC-07. The four exclusion rows (TC-05, TC-06a/b/c) test the same rule as a delta and *are* automated. |
| TC-13 (as HW02 wrote it) | `delivered → canceled` is refused by the state machine (400, verified), so the amount can never be removed from revenue this way. Not a limitation of the harness — the build has no such path. | Nobody, on this build. Restated as TC-13 (assert the refusal) + TC-13b (the permitted direction). |

## Open Questions — resolved and still open

Resolved by probing the running SUT on 2026-08-10. Recorded here because a resolved OQ
is evidence; deleting it would lose the trace back to HW02.

| OQ | Question | Status |
|---|---|---|
| OQ-02 | Does "total number of orders" mean all orders or delivered only? | **Resolved: all orders.** `App.jsx:288` renders `orders.length` over the unfiltered payload. TC-09 now asserts this and records it either way. |
| OQ-06 | Does the backend recompute `total_amount`, or trust the client? | **Resolved: it trusts the client.** `POST /api/checkout` (`server.js:313-325`) writes the body value with no validation. Now covered by TC-11 as a spec conflict — README FR-08 requires recomputation. |
| OQ-07 / OQ-09 | Currency, rounding, integer vs decimal precision | **Partly resolved.** Format is `toLocaleString()` + `₫`, with **no explicit locale** — the grouping character comes from the browser, not the app (probed: `"8,000,000 ₫"`, `navigator.language` `en-US`, identical on all three engines). Precision: `0.01` is stored as `0.009999999776482582`. TC-12 asserts structure, not a literal string; BVA-05 carries a tolerance. |
| OQ-12 | Is there a page limit on the admin orders list? | **Now testable.** TC-14 seeds 25 orders and asserts the count delta. Note comparing UI to API would *not* detect a limit — both would be capped; only the before/after delta can. |
| OQ-16 | Are negative `total_amount` values producible? | **Resolved: yes.** Verified accepted and stored by `POST /api/checkout`. BVA-01 and BVA-04 are automated. |
| OQ-18 | Is one delivered order of `0` distinguishable from no delivered orders? | **Now testable.** TC-10 asserts revenue delta `0` **and** count delta `1`; revenue alone cannot separate the two states. |
| OQ-03 / OQ-15 | Zero-orders empty state, and whether it can be re-established between runs | **Still open, and the reason TC-07/TC-08 are not automated.** See the table above. |
| OQ-19 *(new)* | What is the account-lockout policy, and does it endanger the suite? | **Resolved, and it constrains the design.** `POST /api/login` adds **2** to `login_attempts` per failure and locks at `>= 3` for **180 s** — so **two** wrong passwords lock an account. README FR-02 L41-42 specifies **+1**, **≥ 3 attempts**, **30 s**. TC-16/17 do not target a real account; TC-18 sends one wrong password to the seeded admin only after worker tokens are minted locally, so later setup does not depend on logging in. The divergence itself belongs to FR-02, not FR-13 — recorded here because it shaped the harness. |
