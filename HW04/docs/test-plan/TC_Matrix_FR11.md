# FR-11 Order history view — test-case matrix (Pool B)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
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

> Read from source, not from a run. Confirm against the rendered page before these
> become hard assertions.

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
| 17 | TC-14 | edge | `Hủy đơn` shown for `pending`/`confirmed`/`shipping`, hidden for `delivered`/`canceled` | UI-only behaviour (`Profile.jsx` L200) with no API-level equivalent — HW02 could not see it at all |
| 18 | TC-15 | negative | no-token probe against the **detail** route, not only the list route | 03 §2 design note: "REQ-02's auth enforcement is **not** independently re-verified… a symmetric pair of TCs could be added later if full per-endpoint auth coverage is wanted" — an explicit scope trade-off, now closed |
| 19 | TC-16 | edge | list ordering is deterministic (and newest-first if that is what the SUT does) | FR §7: "**List sort order** (e.g. newest-first) and deterministic tie-breaking" — never resolved, never tested |
| 20 | TC-17 | edge | order date renders as a real, valid date rather than `Invalid Date`/empty | FR §7: "**Order date format** (locale, timezone, date vs datetime)" — never resolved. `Profile.jsx` L186 uses `new Date(o.created_at).toLocaleDateString()`, which silently yields `Invalid Date` on a malformed value |

With these, FR-11 reaches **20 cases**.

### Considered and not taken (kept for the report's honesty)

| Candidate | Why not | 
|---|---|
| Total amount shown before vs after coupon discount | FR §7 flags it, but resolving it needs FR-09 coupon behaviour, which is another student's feature and outside FR-11's boundary. |
| Pagination / result limit with many orders | FR §7 flags it, but with no documented page size there is no expected value to assert — it would be an observation, not a test. Better raised as an open question in the report. |

## Test-data prerequisites

| Account | Purpose | Seeded how | Recorded in |
|---|---|---|---|
| `USER_EMAIL` | owns the orders under test, across five statuses | API in a fixture | `.env` |
| `ADMIN_EMAIL` | second identity for the ownership probe (TC-03); also drives status changes | API in a fixture | `.env` |
| third account | zero orders, for the empty state (TC-08) — must not be a checkout source elsewhere | manual | `.env` |

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| EC-14 (no TC) | "Out-of-set / anomaly status value" — no valid request makes a correct system produce it; it appears only as a symptom of a defect. Out of black-box scope, per HW02. Note `statusLabel` falls back to `status.toUpperCase()`, so such a value would render raw — observable, but not reachable by any legitimate input. | A DB- or code-level check that the status column only holds the five documented values. |

## Open Questions still to resolve against the running SUT

OQ-05, OQ-08 and OQ-16 are resolved above. Remaining:

| OQ | Question | Affects |
|---|---|---|
| OQ-06 | Ownership denial shape — moot while BUG-07 stands (no check at all) | TC-03 |
| OQ-07 | Missing vs malformed token — HW02 saw 401 vs 403; confirm at UI level | TC-04, TC-05 |
| OQ-12 / OQ-13 | "Not found" and "malformed id" both returned 404 — is that intended? | TC-06, TC-07 |
| OQ-17 | Is there any distinct sign/range check on the id? HW02's 404s suggest not | BVA-01, BVA-02 |
