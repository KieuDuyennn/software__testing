# FR-13 Dashboard — test-case matrix (Pool C)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Data file:** `automation/data/fr13_dashboard.json`
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

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| — | Nothing excluded yet. Fill this in if any row above turns out to need a system state the suite cannot reach — e.g. TC-07's "zero orders in the entire system" needs a reset the shared SUT may not permit between the 9 runs. | |

## Open Questions still to resolve against the running SUT

| OQ | Question | Affects |
|---|---|---|
| OQ-02 | Does "total number of orders" mean all orders or delivered only? | TC-01(c), proposed TC-09 |
| OQ-03 | Zero-orders empty state — HW02 observed 0/0; confirm it is a real `0` and not a blank | TC-07 |
| OQ-07 / OQ-09 | Currency, rounding, integer vs decimal precision | every revenue assertion, proposed TC-12 |
| OQ-15 | Can "zero orders in the whole system" be reliably re-established between runs? | TC-07 |
