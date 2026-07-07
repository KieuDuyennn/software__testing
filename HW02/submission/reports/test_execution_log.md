# Test Execution Log — HW02 (EShop SUT)

- **Student ID:** 23127184
- **Executed:** 2026-07-07, via Claude Code (recorded in the AI Audit Report)
- **SUT build:** `github.com/ttbhanh/eshop-sut` (cloned fresh), backend `http://localhost:3000`, database re-seeded from `backend/database.js` immediately before this run.
- **How executed:** the designed test cases were exercised against the live backend API with a Node/`fetch` harness; UI-layer-only logic was evaluated against the *verbatim* client source (`frontend-web/src/pages/Register.jsx` password regex, `frontend-web/src/pages/ProductDetail.jsx` quantity `parseInt`, `frontend-admin/src/App.jsx` revenue reducer). Each row shows the **Expected** result taken from the approved phase artifact and the **Actual** result observed. The "Actual matches designed Expected?" column is a factual comparison only.

> **Scope & authorship note.** This file contains raw observed output only. It deliberately contains **no** determination of whether any divergence is a *bug*, a spec ambiguity, or an Open-Question resolution — that judgment, and all bug-report text, is written by the student per course policy. Some designed cases have **conditional** expected results (they depend on an unresolved Open Question); for those, "Actual matches?" is marked `N/A — conditional` and the observed value is simply recorded.
>
> **Seed accounts:** `admin@eshop.com` / `Admin123!` (role admin), `test@eshop.com` / `Test1234!` (role user). Login confirmed working with `Admin123!` (the README value; the `admin123` value from setup_guide.md was the fallback, not needed).

## Layer legend

- **API** — HTTP request to the backend, real response captured.
- **Client** — the exact client-side JS logic evaluated in-process against the same input (no browser); use for UI-only validation/computation. For a full UI screenshot, re-run the step in the running web/admin app (both servers are startable per `setup_guide.md`).

---

## FR-01 — Account Registration

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-01b | API `POST /api/register` | valid name/email/`Password123!` | HTTP 200 `{message, id}` | HTTP 200 `{"message":"User registered successfully","id":N}` | Yes |
| TC-01a | Client regex | `Password123!` (spec-valid strong pw) | Client accepts → POST → redirect | `regex.test = false` → **BLOCKED** with "Mật khẩu quá yếu" before any POST | No |
| TC-02 | API | `name=""` (blank) | Rejected, missing-field error | HTTP 200, account created (id issued) | No |
| TC-03 | API | `name` key omitted | Rejected, missing-field error | HTTP 200, account created | No |
| TC-04 | API | `email=""` (blank) | Rejected, missing-field error | HTTP 200, account created | No |
| TC-05 | API | `email` key omitted | Rejected, missing-field error | HTTP 200, account created | No |
| TC-06 | API | `email="userdomain.com"` (no `@`) | Rejected, invalid-format | HTTP 200, account created | No |
| TC-07 | API | `email="user@"` (no domain) | Rejected, invalid-format | HTTP 200, account created | No |
| TC-08 | API | `email="@domain.com"` (no local) | Rejected, invalid-format | HTTP 200, account created | No |
| TC-09 | API | register same email twice | Rejected, duplicate-email | HTTP 200, second account created (new id) | No |
| TC-12 | Client+API | `Pass1!` (6 chars) | Rejected weak pw | client regex `false`; backend HTTP 200 created | see note¹ |
| TC-13 | Client+API | `password123!` (no uppercase) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| TC-14 | Client+API | `PASSWORD123!` (no lowercase) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| TC-15 | Client+API | `Password!` (no digit) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| TC-16 | Client+API | `Password123` (no special) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| TC-22 | Client+API | `Password123#` (`#` outside set) | Conditional (OQ-06) | client `false`; backend 200 created | N/A — conditional |
| BVA-01 | Client+API | `Pa1!abc` (7 chars, min−1) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| BVA-02 | Client+API | `Pa1!abcd` (8 chars, min) | **Valid** — accepted | client regex `false` (rejected); backend 200 created | No (client) |
| BVA-03 | Client+API | `Pa1!abcde` (9 chars, min+1) | **Valid** — accepted | client regex `false` (rejected); backend 200 created | No (client) |
| BVA-06 | Client+API | `P` (1 char) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| BVA-07 | Client+API | `Pa` (2 chars) | Rejected weak pw | client `false`; backend 200 created | see note¹ |
| BVA-04 | API | `name="A"` (1 char) | Registration succeeds | HTTP 200, account created | Yes |
| BVA-05 | API | `name="An"` (2 chars) | Registration succeeds | HTTP 200, account created | Yes |

¹ For the weak/invalid-password rows the two layers give *opposite* results: the client regex rejects them (so the designed "rejected" expected is met **at the client layer**), but the backend `POST /api/register` accepts and creates the account (so it is **not** met at the API layer). The regex used (`Register.jsx` line 15) is `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/` — it requires a whitespace character and disallows the special-character set the FR mandates. Both facts are recorded; which (if either) constitutes a defect is the student's call.

---

## FR-06 — Product Detail View

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-01 | API `GET /api/products/1` | existing product, odd id | product returned, price numeric | HTTP 200, `price=30000000` (typeof **number**) | Yes |
| TC-01 (price-type) | API `GET /api/products/2` | existing product, even id | price numeric, consistent | HTTP 200, `price="28000000"` (typeof **string**) | No |
| TC-01 (nonexistent) | API `GET /api/products/9999` | non-existent id | not-found (e.g. 404) | HTTP **200**, body `{}` | No |
| TC-04/BVA-01 | Client `parseInt` | quantity `0` | reject (Pred A) / default to 1 (Pred B) | `parseInt("0")=0`; no client validation; `0` passed to addToCart | N/A — conditional (CF-02) |
| BVA-02 | Client | quantity `1` (min) | accepted | `parseInt("1")=1`; accepted, no validation | Yes |
| BVA-03 | Client | quantity `2` (min+1) | accepted | `parseInt("2")=2`; accepted, no validation | Yes |
| TC-05 | Client | quantity `-5` | reject / default (CF-02) | `parseInt("-5")=-5`; no validation, `-5` passed through | N/A — conditional |
| TC-06 | Client | quantity `1.5` | reject / default (CF-02) | `parseInt("1.5")=1`; truncated to `1`, no validation | N/A — conditional |
| TC-07 | Client | quantity `abc` | reject / default (CF-02) | `parseInt("abc")=NaN`; `NaN` passed to addToCart | N/A — conditional |
| BVA-04 | API (seeded) | product with `price=-1` | render without crash/NaN (OQ-19) | HTTP 200, `price="-1"`; client `Number("-1").toLocaleString()="-1"` | N/A — conditional (OQ-19) |

> Note: display-field empty/null fixtures (TC-02, TC-03, TC-08–TC-13) were exercised in the **second pass** below (seeded atypical product records via `POST /api/products`, then fetched). See "Remaining cases — second execution pass".

---

## FR-11 — Order History View

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-01 | API `GET /api/orders/my-orders` | test token; admin owns a separate order | only test's orders; admin order absent (REQ-06) | HTTP 200, ids `[2,1]`; admin order present = **false** | Yes |
| TC-02 | API `GET /api/orders/:id` | test token, own canceled order | order returned, status=canceled | HTTP 200, `status="canceled"`, `user_id=2` | Yes |
| TC-03 | API `GET /api/orders/:id` | test token, **admin's** order id | denied / not returned (403/404) | HTTP **200**, full admin order body returned (`user_id=1`) | No |
| TC-04 | API | no Authorization header | 401 unauthorized | HTTP 401 `{"error":"Unauthorized"}` | Yes |
| TC-05 | API | invalid/garbage token | 401/403 unauthorized | HTTP 403 `{"error":"Forbidden"}` | Yes |
| TC-06 | API `GET /api/orders/999999` | nonexistent id | not found (404) | HTTP 404 `{"error":"Order not found"}` | Yes |
| TC-07 | API `GET /api/orders/abc` | malformed non-integer id | malformed-id error | HTTP 404 `{"error":"Order not found"}` | N/A — conditional (OQ-13) |
| TC-08 | API | zero-order fresh account | appropriate empty state | HTTP 200, `[]` | Yes |
| BVA-01 | API `GET /api/orders/-1` | boundary id −1 | conditional (OQ-16/17) | HTTP 404 `{"error":"Order not found"}` | N/A — conditional |
| BVA-02 | API `GET /api/orders/0` | boundary id 0 | conditional (OQ-16/17) | HTTP 404 `{"error":"Order not found"}` | N/A — conditional |
| BVA-03 | API `GET /api/orders/1` | boundary id 1 | conditional (OQ-16/17) | HTTP 200, order #1 returned | N/A — conditional |

---

## FR-13 — Admin Dashboard

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-01 | API `GET /api/admin/orders` | valid admin token | success, orders returned | HTTP 200, count=3 | Yes |
| TC-02 | API | no token | denied (401) | HTTP 401 `{"error":"Unauthorized"}` | Yes |
| TC-03 | API | malformed token | denied (401/403) | HTTP 403 `{"error":"Forbidden"}` | Yes |
| TC-04 | API | **non-admin** valid token (role=user) | **denied (403)** — admin-only | HTTP **200**, 3 orders returned (access **granted**) | No |
| TC-05 | Client revenue (`App.jsx` L217-218) | 1 delivered(100) + 1 canceled(50) | revenue = 100 (delivered only) | client formula `delivered*2` → **200**; correct sum would be 100 | No |
| TC-06 | Client revenue | exclude pending/confirmed/shipping | revenue = sum of delivered only | canceled/others excluded correctly, but delivered totals are **doubled** (`*2`) | Partial |
| BVA-06 | Client revenue (multi-row) | 3 delivered orders 1000/2000/3000 | revenue = 6000 | client formula `delivered*2` → **12000**; correct sum = 6000 | No |

> Note: FR-13 `total_amount` precision BVA (BVA-01..05: negative/zero/decimal amounts) and the empty-state TCs (TC-07/TC-08) were characterized via the revenue reducer but not each run as a separate seeded scenario in this pass. The revenue-reducer behavior (`delivered.total_amount * 2`) is the same regardless of the specific amounts. Recorded honestly as partial.

---

---

## Remaining cases — second execution pass

The cases below were exercised in a second pass (raw transcript: the "PASS 2" section of `test_execution_raw.txt`) so that every designed test case has now been run at least once, except the two Confirm-Password cases that are structurally not executable (no such field exists in the UI or API — this is itself the observation).

### FR-01 (remaining)

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-10 | API+client | `password=""` (empty) | rejected, password-required | client regex `false`; backend HTTP 200 created | see note¹ |
| TC-11 | API | `password` key omitted | rejected, missing-field | HTTP 200, account created | No |
| TC-17 | — | Confirm Password ≠ Password | rejected, mismatch | **Not executable** — no `confirmPassword` field in `Register.jsx` or API (matches OQ-01) | N/A — no field |
| TC-18 | API | `name="   "` (whitespace) | conditional (OQ-04/10) | HTTP 200, account created | N/A — conditional |
| TC-19 | API | `email="user@domain"` (no TLD) | conditional (OQ-11) | HTTP 200, account created | N/A — conditional |
| TC-20 | API | `email="user+tag@mail.domain.com"` | conditional (OQ-11) | HTTP 200, account created | N/A — conditional |
| TC-21 | API | register email then its uppercased variant | conditional (OQ-09) | HTTP 200, both created | N/A — conditional |
| TC-23 | — | Confirm Password `=""` | rejected | **Not executable** — no `confirmPassword` field (same as TC-17) | N/A — no field |

### FR-06 (remaining)

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-02 | API GET (seeded) | 300-char name, price 0, 500-char desc, broken img, category 9999 | screen handles each edge | HTTP 200; `price="0"` (string, even id); name 300 chars stored; category_id=9999 stored | N/A — conditional |
| TC-03 | API GET (seeded) | `price=999999999999` | renders without overflow | HTTP 200, `price=999999999999` (number), `toLocaleString="999,999,999,999"` | N/A — conditional |
| TC-08 | Client | empty quantity | reject / default (CF-02) | `parseInt("")=NaN`; no validation | N/A — conditional |
| TC-09 | API GET (seeded) | `imageUrl=""` | handles empty image | HTTP 200, `imageUrl=""` returned | N/A — conditional |
| TC-10 | API GET (seeded) | `name=""` | handles empty name | HTTP 200, `name=""` returned | N/A — conditional |
| TC-11 | API GET (seeded) | `price=null` | handles empty price gracefully | **Backend process CRASHED** (ECONNRESET): `server.js:162` `row.price.toString()` throws on null for even-id products → unhandled TypeError → Node exits | No |
| TC-12 | API GET (seeded) | `description=""` | handles empty description | HTTP 200, `description=""` returned | N/A — conditional |
| TC-13 | API GET (seeded) | `category_id=null` | handles empty category | HTTP 200, `category_id=null` returned | N/A — conditional |

### FR-13 (remaining)

| TC | Layer | Input | Designed Expected | Actual observed | Actual matches? |
|---|---|---|---|---|---|
| TC-07 | API+client | zero orders in system | revenue=0, count=0 | count=0, computed revenue=0 | Yes |
| TC-08 | API+client | 1 pending order, 0 delivered | revenue=0 | count=1, delivered=0, revenue=0 | Yes |
| BVA-01 | API+client | delivered `total_amount=-1` | reflect −1 | stored −1 (number); doubled contribution −2 | see FR-13 revenue note² |
| BVA-02 | API+client | delivered `total_amount=0` | reflect 0 | stored 0; doubled 0 | see note² |
| BVA-03 | API+client | delivered `total_amount=1` | reflect 1 | stored 1; doubled 2 | see note² |
| BVA-04 | API+client | delivered `total_amount=-0.01` | reflect −0.01 | stored −0.01 (number); doubled −0.02 | see note² |
| BVA-05 | API+client | delivered `total_amount=0.01` | reflect 0.01 | stored 0.01; doubled 0.02 | see note² |

² For every FR-13 revenue case the client reducer contributes `total_amount * 2` per delivered order — the same doubling shown in TC-05/TC-06/BVA-06 of the first pass; the boundary amounts are stored/summed without a separate rounding fault, but each is still doubled.

---

## Coverage of the 73 designed cases

All 73 designed test cases (FR-01: 31, FR-06: 17, FR-11: 11, FR-13: 14) were exercised across the two passes, **except** FR-01 TC-17 and TC-23 (Confirm-Password match/empty), which are not executable because no `confirmPassword` field exists in the register UI or the API — that absence is itself recorded as the observation (ties to OQ-01). Several cases have **conditional** designed expected results (they hinge on an unresolved Open Question); those are recorded factually and left for the student to score.

## Raw console transcripts

The unedited console output is preserved in a single file, `test_execution_raw.txt`, which contains both the first pass and a clearly marked "PASS 2" section (the two passes were merged into one file for tidiness; the content of each is unchanged).

## What is NOT in this file (student to complete)

- **Bug reports** (which divergences are defects, severity, reproduction narrative) — `Bug_Report.md`, authored by the student.
- **Screenshots** — capture from the running web app (`frontend-web`, `npm run dev`, `:5173`) and admin app (`frontend-admin`, `npm run dev`, `:5174`) for the GitHub issues.
- **Pass/fail totals** in the README — derive from the "Actual matches?" column once you decide how to score the `N/A — conditional` rows.
