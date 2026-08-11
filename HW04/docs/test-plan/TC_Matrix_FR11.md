# FR-11 Order history view — test-case matrix (Pool B)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Designed and automated:** **46** — 10 positive / 22 negative / 14 edge; 26 UI-channel / 20 API-channel.
**Data file:** `automation/data/fr11_order_history.json`
**Spec:** `automation/tests/fr11_order_history/fr11.order-history.spec.ts`

HW02 source: `HW02/submission/projects/fr11_order_history_view/output/`
HW02 execution: `HW02/submission/reports/TC_Checklist.md` §FR-11 (11 designed, 11 executed).

## Correction to an HW02 premise — FR-11 does have a web UI

HW02 recorded FR-11 as **"no dedicated UI in frontend-web"** and tested it at the API
layer only (`TC_Checklist.md` line 149; the whole feature is listed under "case không
có ảnh chụp"). Re-checking the SUT source for HW04 shows that conclusion was wrong:

- `frontend-web/src/App.jsx` has no `/orders` route — that part is correct — **but**
- `frontend-web/src/pages/Profile.jsx` renders the order history inside `/profile`:
  heading `Lịch sử đơn hàng`, a table with columns `Mã ĐH · Ngày đặt · Tổng tiền ·
  Trạng thái · Thao tác`, an empty state `Bạn chưa có đơn hàng nào.`, and a
  `Hủy đơn` button.

So every FR-11 display requirement is UI-assertable after all, and the agreed
**API-setup + UI-assert** approach applies cleanly. This correction belongs in
`AI_Review_Gap_Analysis.md` — it is a case of HW02 searching for a route name instead
of the rendered feature.

**This also resolves OQ-05 and OQ-08**, which blocked HW02's status assertions:

| Status | Vietnamese label (`statusLabel`) | Colour class (`statusStyle`) |
|---|---|---|
| `pending` | Chờ xác nhận | `bg-yellow-100 text-yellow-800` (default branch) |
| `confirmed` | Đã xác nhận | `bg-indigo-100 text-indigo-800` |
| `shipping` | Đang giao | `bg-blue-100 text-blue-800` |
| `delivered` | Đã giao | `bg-green-100 text-green-800` |
| `canceled` | Đã hủy | `bg-red-100 text-red-800` |

> **Confirmed on the rendered page** on 2026-08-10, not only read from source: a probe
> seeded one order in each of the five statuses and read back the label and the `class`
> attribute of each badge. All five rows above matched exactly. They are now hard
> assertions (TC-02, TC-09→TC-12).

## Carried over from HW02

`HW02 result` is what HW02 actually observed, so a case that already failed there is
expected to fail here too — per project rule §4 that is a finding, not a test to soften.

| # | TC ID | Type | Intent | Setup (API) | Assert (UI at `/profile`) | HW02 result | Pattern | Automated? |
|---|---|---|---|---|---|---|---|---|
| 1 | TC-01 | positive | own orders listed with all four fields; another user's order absent | seed 2 orders for user + ≥1 for admin | rows rendered; admin's order id absent | ✅ | 1 + 3 | ☐ |
| 2 | TC-02 | positive | a `canceled` order shows label `Đã hủy` + red badge | cancel order B | label and colour class | ✅ | 1 | ☐ |
| 3 | TC-03 | negative | another user's order must not be reachable | seed an order under admin | **HW02 found HTTP 200 — no ownership check (BUG-07)** | ❌ | 1 + 2 | ☐ |
| 4 | TC-04 | negative | no token | — | redirected / unauthorized | ✅ (401) | 1 + 2 | ☐ |
| 5 | TC-05 | negative | garbage / expired token | inject bad token | unauthorized | ✅ (403) | 1 + 2 | ☐ |
| 6 | TC-06 | negative | order id `999999` — nonexistent | — | not found | ✅ (404) | 1 | ☐ |
| 7 | TC-07 | negative | order id `"abc"` — malformed | — | HW02 saw 404, same as nonexistent | ⚠️ | 1 | ☐ |
| 8 | TC-08 | positive | user with zero orders → `Bạn chưa có đơn hàng nào.` | third account | empty-state text | ✅ (`[]`) | 1 | ☐ |
| 9 | BVA-01 | edge | order id `-1` | — | HW02 saw 404 | ⚠️ | 1 | ☐ |
| 10 | BVA-02 | edge | order id `0` | — | HW02 saw 404 | ⚠️ | 1 | ☐ |
| 11 | BVA-03 | edge | order id `1` | — | HW02 saw 200, order returned → ids are 1-indexed (**resolves OQ-16**) | ⚠️ | 1 | ☐ |

**11 cases — one short of the ≥12 minimum.** Additions below close that gap.

## Derived additions — proposed, pending review

Each closes a gap **HW02 recorded as not covered**, so these are traceable
derivations rather than invented cases. Now genuinely assertable because the UI exists.

| # | Proposed ID | Type | Intent | HW02 gap it closes |
|---|---|---|---|---|
| 12 | TC-09 | positive | `pending` → `Chờ xác nhận` + yellow badge | 03 §4: EC-09 "may be incidentally observed… cannot be asserted as guaranteed or deliberate" — seeding it makes it deliberate |
| 13 | TC-10 | positive | `confirmed` → `Đã xác nhận` + indigo badge | 03 §4: EC-10 "Not covered — setup dependency" (OQ-15); reachable via admin `PUT /api/admin/orders/:id/status` |
| 14 | TC-11 | positive | `shipping` → `Đang giao` + blue badge | 03 §4: EC-11, same gap |
| 15 | TC-12 | positive | `delivered` → `Đã giao` + green badge | 03 §4: EC-12, same gap |
| 16 | TC-13 | edge | all five statuses on screen at once are **mutually distinct** in colour | REQ-14 requires colour distinction; HW02 only ever saw one status at a time, so an "all badges identical" bug was structurally invisible to it |
| 17 | TC-14 | edge | `Hủy đơn` shown **only** for `pending`/`confirmed`; hidden for `shipping`/`delivered`/`canceled` (count = 2) | UI-only behaviour (`Profile.jsx` L200) with no API-level equivalent — HW02 could not see it at all |
| 18 | TC-15 | negative | no-token probe against the **detail** route, not only the list route | 03 §2 design note: "REQ-02's auth enforcement is **not** independently re-verified… a symmetric pair of TCs could be added later if full per-endpoint auth coverage is wanted" — an explicit scope trade-off, now closed |
| 19 | TC-16 | edge | list ordering is deterministic (and newest-first if that is what the SUT does) | FR §7: "**List sort order** (e.g. newest-first) and deterministic tie-breaking" — never resolved, never tested |
| 20 | TC-17 | edge | order date renders as a real, valid date rather than `Invalid Date`/empty | FR §7: "**Order date format** (locale, timezone, date vs datetime)" — never resolved. `Profile.jsx` L186 uses `new Date(o.created_at).toLocaleDateString()`, which silently yields `Invalid Date` on a malformed value |

With these, FR-11 reaches **20 cases**.

## Second wave — cases derived by reading the implementation for defects

The 20 cases above were derived from HW02's own recorded gaps. These 20 were derived
differently: by reading `backend/server.js` and `Profile.jsx` for the places where the
implementation and the requirement disagree, then writing the case that makes the
disagreement visible. That is a different technique with a different justification, so
it is recorded separately rather than merged into the table above.

Two rules were applied to keep this from becoming padding:

1. **Every predicted failure gets a control case** that must pass. A cluster of red with
   no green next to it cannot tell a fixer whether the check is missing or merely wrong.
2. **Cases that fail for one shared cause are counted as one finding**, and where a
   cluster exists, one row is designated the diagnostic that isolates the cause.

| # | TC ID | Type | Ch. | Intent | Source of the expectation | Predicted |
|---|---|---|---|---|---|---|
| 21 | TC-18 | negative | api | a non-admin must not be able to list every order in the system | `server.js:526` — `GET /api/admin/orders` has `authenticateToken` but **no role check**; returns all orders with `users.name` joined | ❌ fail (200) |
| 22 | TC-19 | negative | api | a non-admin must not be able to change an order's status | `server.js:541` — same omission. `status` is the column FR-11 exists to display, so a user-writable status means the history can be made to show anything | ❌ fail (200) |
| 23 | TC-22 | negative | api | a `canceled` order must not be transitionable to `delivered` | `server.js:566` — `if (currentStatus === "canceled" && status === "delivered") isValidTransition = true;` is written explicitly | ❌ fail (200) |
| 24 | TC-23 | negative | ui | an order the user cancelled must never display as `Đã giao` | The UI consequence of TC-22: green badge, cancel button gone, on an order the customer cancelled | ❌ fail |
| 25 | TC-24 | negative | api | a transition that skips the chain (`pending → delivered`) is refused | **CONTROL for TC-22.** Not in the transition table | ✅ pass |
| 26 | TC-25 | negative | api | an out-of-set status value (`"hacked"`) is refused | **Reachability probe for EC-14** — tests the premise HW02 assumed. If it passes, `statusLabel`'s `toUpperCase()` fallback renders a raw badge in default yellow, indistinguishable from `Chờ xác nhận` | ✅ pass |
| 27 | TC-26 | negative | ui | cancel must be refused on a `shipping` order | `server.js:344` guards only `delivered`/`canceled`, and the line above carries the developer's own comment: `// Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')` | ❌ fail (after synchronized PUT + refresh) |
| 28 | TC-27 | negative | api | the cancel endpoint itself must refuse a `shipping` order | Same defect at the API layer. Answers the triage question TC-26 cannot: fix the button's condition, or the endpoint's guard? | ❌ fail |
| 29 | TC-28 | negative | api | a user must not be able to cancel another user's order | **CONTROL for TC-03/TC-15.** `server.js:339` scopes the lookup `WHERE id = ? AND user_id = ?` | ✅ pass |
| 30 | TC-29 | negative | api | cancelling an already-`canceled` order is refused | Guard covers this branch | ✅ pass |
| 31 | TC-30 | negative | api | cancelling a `delivered` order is refused | Guard covers this branch; counterpart to TC-12's hidden button | ✅ pass |
| 32 | TC-31 | edge | ui | a non-numeric total must not render as `NaN` | `server.js:313` writes `total_amount` straight from the request body; SQLite is dynamically typed so a string survives in the INTEGER column; `Profile.jsx:189` then does `Number(o.total_amount \|\| 0).toLocaleString()` → the literal `NaN ₫` | ❌ fail |
| 33 | TC-32 | edge | ui | a total of `0` renders as a zero amount | Lower boundary of the money column | ✅ pass |
| 34 | TC-33 | edge | ui | a negative total must not be displayed as a price | Same reachability as TC-31; renders `-1,000,000 ₫` in the red bold price styling | ❌ fail |
| 35 | TC-34 | edge | ui | a missing total must not be silently displayed as `0 ₫` | `o.total_amount \|\| 0` turns absent data into a confident-looking price of zero | ❌ fail |
| 36 | TC-35 | negative | api | checkout must reject a non-numeric total | **DIAGNOSTIC for TC-31/33/34** — isolates the one shared cause (checkout trusts a client-supplied total) in a single assertion | ❌ fail |
| 37 | TC-36 | negative | ui | a failed order fetch must be reported as an error, not as an empty history | `Profile.jsx` `fetchOrders` catch does `setOrders([])`, so a 500, a network failure and a genuinely empty account all render `Bạn chưa có đơn hàng nào.` — a customer whose orders failed to load is told they never ordered anything | ❌ fail |
| 38 | TC-37 | edge | ui | an unexpected response shape must not break the page | `Array.isArray(res.data) ? res.data : res.data.orders \|\| []` — the guard exists, so this is a real contract | ✅ pass |
| 39 | TC-38 | positive | ui | a successful cancel confirms the outcome to the user | Happy path of the `Thao tác` column, never exercised by HW02. Records that the only feedback channel is a native `alert`, so `getByRole('alert')` matches nothing | ✅ pass |
| 40 | TC-39 | positive | ui | the list reflects the new status without a manual reload | `cancelOrder` calls `fetchOrders()` on success. Distinct requirement from TC-38: one is "the user is told", the other is "the screen stops lying" | ✅ pass |
| 41 | TC-40 | positive | ui | one row agrees with the API across ID, date, total and status | Coverage control for TC-01: its original assertion compared IDs only despite saying "all four fields" | ✅ pass |
| 42 | TC-41 | negative | ui | an expired, correctly signed token is rejected | Distinct `jwt.verify` path from TC-05's syntactically invalid token | ✅ pass |
| 43 | TC-42 | edge | ui | nested `orders` of the wrong type must not crash the profile | `Profile.jsx` checks the top-level response but trusts `res.data.orders`; a truthy string reaches `orders.map` | ❌ fail |
| 44 | TC-43 | negative | api | a signed token for a nonexistent user is not a live session | `authenticateToken` verifies signature only and never verifies that `req.user.id` still exists | ❌ fail (200 + `[]`) |
| 45 | TC-44 | negative | api | cancel without a token is refused and leaves the order unchanged | Auth control for the mutation route; pairs with the unprotected detail route in TC-15 | ✅ pass |
| 46 | TC-45 | edge | api | two simultaneous cancels acknowledge the transition only once | Check-then-update race: both requests can read `pending` before either writes `canceled` | ✅ pass (`200`, `400`) |

**FR-11 total: 46 cases.**

### The oracle correction that changed this table

The first version of TC-11 and TC-14 took their expected values from **what this build
renders**: `expect_cancel_visible: true` for a `shipping` order, and a cancel-button
count of 3. That is backwards. A SUT repaired in the obvious way — hiding the button once
an order ships — would have turned both of those *positive* cases red, so the suite would
have defended the defect and punished the fix.

The requirement is not ambiguous, and it is stated inside the implementation itself:
`server.js:344` carries `// Lẽ ra phải là: if (order.status !== 'pending' && order.status
!== 'confirmed')`. So `shipping` is **not** customer-cancellable, and:

- **TC-14** now expects **2** buttons, and is expected to fail on this build.
- **TC-11** now asserts label and colour only. It is the one `status_badge` row that does
  not assert cancel visibility, and it says so in a machine-checked field
  (`cancel_visibility_owned_by`), so the omission cannot be mistaken for an oversight —
  the spec's data guard rejects the file if that field names a case that does not exist.
- The phrase "the three cancellable statuses" is gone from the case titles: it was the
  build's vocabulary, not the requirement's.

Recorded as finding 27 in `AI_Review_Gap_Analysis.md`.

### Predicted failures, grouped by root cause

16 of the 46 are predicted to fail. They are **not 16 defects** — grouping them before
the run is what stops the report from inflating one omission into a list.

| Root cause | Cases | Diagnostic / control that pins it down |
|---|---|---|
| No role check on any `/api/admin/*` order endpoint | TC-18, TC-19 | Both red ⇒ one finding ("no admin endpoint checks role"), not two |
| `GET /api/orders/:id` has no auth middleware at all | TC-03, TC-15 | **TC-28 passes** ⇒ the app *can* check ownership, so this is one route's omission, not a missing concept |
| `canceled → delivered` explicitly whitelisted | TC-22, TC-23 | **TC-24 and TC-25 pass** ⇒ one illegal transition was whitelisted, not "validation is broken" |
| Cancel guard checks the wrong end of the lifecycle | **TC-14**, TC-26, TC-27 | **TC-29 and TC-30 pass** ⇒ the condition needs widening, not rewriting. TC-14 witnesses it in the UI (a button that should not be offered), TC-26 that clicking it is honoured, TC-27 that the endpoint accepts it directly |
| Checkout accepts a client-supplied `total_amount` | TC-31, TC-33, TC-34 | **TC-35** is the diagnostic; **TC-32 passes** ⇒ the renderer is fine, the input is not |
| Fetch failure is rendered as the empty state | TC-36 | Also weakens TC-08: it passes for the right reason only because the fetch succeeds |
| Nested fallback value is trusted without an array check | TC-42 | **TC-37 passes** with a valid nested array, isolating the missing inner type check |
| Signed tokens are accepted without checking that the user still exists | TC-43 | **TC-41 passes** for expiry, separating identity existence from signature/expiry validation |
| *(No confirmed race failure in the final run)* | TC-45 | **TC-38/39 pass** for a single request; the concurrent pair completed as `200` + `400` |

So: **16 red cases → 8 confirmed root-cause clusters.** The bug write-ups are the student's per project
rule §4; this table exists so that triage starts from causes rather than from symptoms.

### Considered and not taken (kept for the report's honesty)

| Candidate | Why not | 
|---|---|
| Total amount shown before vs after coupon discount | FR §7 flags it, but resolving it needs FR-09 coupon behaviour, which is another student's feature and outside FR-11's boundary. |
| Pagination / result limit with many orders | FR §7 flags it, but with no documented page size there is no expected value to assert — it would be an observation, not a test. Better raised as an open question in the report. |

## Test-data prerequisites

Data strategy is **option A**: the fixture seeds through the API on every run. The SUT
database is never reset between the nine required runs, so the owner account accumulates
orders monotonically — which is why no case asserts an absolute row count, and rows are
identified by the ids that run seeded.

| Identity | Purpose | Seeded how | Recorded in |
|---|---|---|---|
| `owner` = `USER_EMAIL` | owns the orders under test, across five statuses and the four total-amount variants | API in a fixture | `.env` |
| `other` | the cross-tenant victim (TC-03, TC-18, TC-28) | **fresh non-admin account registered per run**, by the fixture | — |
| `empty` | zero orders, for the empty state (TC-08) | fresh non-admin account registered per run | — |
| `admin` = `ADMIN_EMAIL` | walks status transitions during setup only | API in a fixture | `.env` |
| `anonymous` | no token (TC-04, TC-15) | — | — |

**Change from the first draft of this matrix**, which named `ADMIN_EMAIL` as the second
identity for the ownership probe: using the admin as the victim would confound "a user
read another user's order" with "a user read an *admin's* data" — two findings of
different severity. `other` is now a plain user, and the admin is used only for setup.
The "third account, seeded manually" row is also gone: under option A nothing is seeded
by hand, so a manual prerequisite would just be a step that silently rots.

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| ~~EC-14~~ | **No longer excluded — now automated as TC-25.** HW02 excluded it on the premise that no valid request makes a correct system produce an out-of-set status. That premise is itself testable, so TC-25 sends `status: "hacked"` and asserts it is refused. If TC-25 ever passes, the exclusion is justified; if it fails, `statusLabel`'s `toUpperCase()` fallback renders the raw value in the default yellow badge, indistinguishable from `Chờ xác nhận`. The lesson recorded for the report: *"unreachable by legitimate input" is a claim about the implementation, and claims about the implementation are test cases.* | Still worth a DB- or code-level check that the `status` column only ever holds the five documented values — TC-25 covers the API door, not every door. |

Nothing else in FR-11 is excluded. The two candidates below were considered and dropped
for reasons of boundary and of missing expected values, not of feasibility.

## Open Questions still to resolve against the running SUT

OQ-05, OQ-08 and OQ-16 are resolved above.

| OQ | Question | Affects | Status after this wave |
|---|---|---|---|
| OQ-06 | Ownership denial shape — moot while BUG-07 stands (no check at all) | TC-03 | Still open, but **TC-28 now answers it by analogy**: the cancel endpoint denies cross-tenant access with `404`, so `404` is this codebase's own convention for it |
| OQ-07 | Missing vs malformed token — HW02 saw 401 vs 403; confirm at UI level | TC-04, TC-05 | Both cases now assert at the UI, where the end state is identical; the 401/403 distinction survives only at the API and is captured by TC-15 |
| OQ-12 / OQ-13 | "Not found" and "malformed id" both returned 404 — is that intended? | TC-06, TC-07 | Still open by design. TC-06 pins the unambiguous baseline (`404` for a nonexistent id) so TC-07's result is read against it rather than in isolation |
| OQ-17 | Is there any distinct sign/range check on the id? HW02's 404s suggest not | BVA-01, BVA-02 | Still open; BVA-03 passing while BVA-01/02 return `404` is the evidence that there is no sign check, only "no such row" |
| **OQ-18** *(new)* | Is a client-supplied `total_amount` intended to be trusted, or is server-side recalculation missing? | TC-31→TC-35 | Raised by this wave. Belongs to checkout, surfaces in FR-11's money column — the two findings should be filed against their own components |
| **OQ-19** *(new)* | Should a failed order fetch be distinguishable from an empty history? | TC-08, TC-36 | Raised by this wave. There is no documented requirement either way, which is itself the answer worth reporting |
