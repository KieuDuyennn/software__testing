# HW06 - Bug Report

Student ID: **23127184** · SUT: **EShop** (`ttbhanh/eshop-sut`) · Base URL: `http://localhost:3000`

Every bug below must also be filed as a **GitHub Issue with a screenshot**
(Section 6.5 of the brief). Fill the *Issue* column as you file them.

---

## Status of this file

Every defect in the *Confirmed* section was **reproduced by an actual Newman
run** against the seeded SUT — the failing assertion and the observed response
are quoted verbatim from that run. BUG-01 to BUG-06 came from the scaffold's
exemplar cases; BUG-07 to BUG-12 came from the 121-case API 1 suite (phase 1,
`docs/phases/api1-fr01-register/01-generate.md`).

The final local full run on **2026-08-23** executed all four collections after
the audit and extension phases. BUG-01 through BUG-16 are grouped by root cause,
not by assertion count: 128 failed assertions reduce to 16 reportable defects.
The green regression gate is recorded separately and passed 1,262/1,262
assertions; it does not erase the defect-revealing full-suite failures.

---

## Summary

| ID | Requirement | Severity | Title | Status | Issue |
|---|---|---|---|---|---|
| BUG-01 | FR-01 | High | Registration accepts a malformed email address | Confirmed | [#7](https://github.com/KieuDuyennn/software__testing/issues/7) |
| BUG-02 | SEC-01 | Critical | Passwords stored and returned in plaintext | Confirmed | [#66](https://github.com/KieuDuyennn/software__testing/issues/66) |
| BUG-03 | FR-06 | Medium | Missing product returns `200 {}` instead of `404` | Confirmed | [#8](https://github.com/KieuDuyennn/software__testing/issues/8) |
| BUG-04 | FR-06 | Medium | `price` is a string for even product ids | Confirmed | [#9](https://github.com/KieuDuyennn/software__testing/issues/9) |
| BUG-05 | SEC-02 / FR-11 | Critical | Any order readable by anyone (IDOR, no auth) | Confirmed | [#13](https://github.com/KieuDuyennn/software__testing/issues/13) |
| BUG-06 | SEC-03 / FR-12 | Critical | Non-admin token reaches `/api/admin/orders` | Confirmed | [#14](https://github.com/KieuDuyennn/software__testing/issues/14) |
| BUG-07 | FR-01 | High | Registration enforces no mandatory-field validation | Confirmed | [#47](https://github.com/KieuDuyennn/software__testing/issues/47)-[#55](https://github.com/KieuDuyennn/software__testing/issues/55) |
| BUG-08 | FR-01 | High | Password complexity policy is not enforced at all | Confirmed | [#59](https://github.com/KieuDuyennn/software__testing/issues/59)-[#63](https://github.com/KieuDuyennn/software__testing/issues/63) |
| BUG-09 | FR-01 | High | Email uniqueness is not enforced | Confirmed | [#64](https://github.com/KieuDuyennn/software__testing/issues/64) |
| BUG-10 | FR-01 | Medium | Confirm-password is not implemented | Confirmed | [#67](https://github.com/KieuDuyennn/software__testing/issues/67) |
| BUG-11 | spec conformance | High | `Content-Type: text/plain` crashes the endpoint with HTTP 500 | Confirmed | [#68](https://github.com/KieuDuyennn/software__testing/issues/68) |
| BUG-12 | SEC-05 | Medium | Malformed JSON returns an HTML stack-trace page | Confirmed | [#69](https://github.com/KieuDuyennn/software__testing/issues/69) |
| BUG-13 | SEC-03 / FR-12 | Critical | Product create/update/delete routes perform no authorization | Confirmed | [#70](https://github.com/KieuDuyennn/software__testing/issues/70) |
| BUG-14 | SEC-02 | High | JWT remains usable after its account is deleted | Confirmed | [#33](https://github.com/KieuDuyennn/software__testing/issues/33) |
| BUG-15 | FR-10 | High | A customer can cancel an order after it reaches `shipping` | Confirmed | [#26](https://github.com/KieuDuyennn/software__testing/issues/26) |
| BUG-16 | FR-10 / FR-13 | High | Terminal `canceled` orders can transition to `delivered` | Confirmed | [#38](https://github.com/KieuDuyennn/software__testing/issues/38) |

---

## Confirmed

### BUG-01 | Registration accepts a malformed email address

- **Requirement:** FR-01 — *"Email phải có định dạng hợp lệ (`user@domain.com`)"*
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test cases:** API1 / `01 - Domain partitions / email` / `A1-DP-019` … `A1-DP-028` (10 cases)

**Steps to reproduce**

```http
POST http://localhost:3000/api/register
Content-Type: application/json
X-Student-Id: 23127184

{ "name": "Bad Email", "email": "not-an-email", "password": "Password123!" }
```

- **Expected:** `4xx` with a validation error.
- **Actual:** `200 OK`, `{"message":"User registered successfully","id":<n>}` —
  the account is created.
- **Newman output:** `AssertionError: Malformed email is rejected with 4xx —
  expected 200 to be within 400..499`
- **Note:** all ten malformed-address partitions are accepted — no `@`, no
  domain, no local part, no TLD, doubled `@`, leading/trailing dot, consecutive
  dots, embedded space, illegal characters. The suspicion recorded here
  originally has since been confirmed: see BUG-07, BUG-08 and BUG-09.

---

### BUG-02 | Passwords stored and returned in plaintext

- **Requirement:** SEC-01 — *"Mật khẩu **không** được lưu dưới dạng plaintext"*
- **Severity:** Critical · **Endpoint:** `POST /api/register`, `POST /api/login`
- **Test cases:** API1 / `03 - Security` / `A1-SEC-001`, `A1-SEC-003`, `A1-SEC-004`

**Steps to reproduce**

1. Register an account with password `Password123!`.
2. Log in with the same credentials.
3. Read `user.password` in the login response.

- **Expected:** the password is never returned; stored form is a hash.
- **Actual:** `user.password` equals `Password123!` exactly. The login response
  returns the entire `users` row, so the credential is disclosed to any caller
  who can authenticate.
- **Newman output:** `AssertionError: password field in response: expected
  'Password123!' to not deeply equal 'Password123!'`
- **Impact:** two defects in one — plaintext storage, and credential disclosure
  in an API response. Consider filing them as separate issues.

---

### BUG-03 | Missing product returns `200 {}` instead of `404`

- **Requirement:** FR-06 / REST contract
- **Severity:** Medium · **Endpoint:** `GET /api/products/:id`
- **Test cases:** API2 / `DP-002`, `DP-003`, and `02 - State transitions` / `ST-001`

Three manifestations of one root cause:

| Request | Expected | Actual |
|---|---|---|
| `GET /api/products/999999` (never existed) | `404` | `200 {}` |
| `GET /api/products/abc` (non-numeric id) | `400` | `200 {}` |
| `GET /api/products/<id>` after `DELETE` | `404` | `200 {}` |

- **Impact:** a client cannot distinguish "no such product" from "a product
  with no fields". Any consumer that checks only the status code will treat a
  missing product as a successful fetch.
- **Newman output:** `expected response to have status code 404 but got 200`

---

### BUG-04 | `price` is a string for even product ids

- **Requirement:** FR-06 + schema conformance to `api_specification.md`
- **Severity:** Medium · **Endpoint:** `GET /api/products/:id`
- **Test case:** API2 / `04 - Schema validation` / `SCH-002`

**Steps to reproduce**

1. `GET /api/products/1` → `"price": 30000000` (JSON number) ✅
2. `GET /api/products/2` → `"price": "28000000"` (JSON **string**) ❌

- **Expected:** `price` is a number for every product.
- **Actual:** the type depends on the parity of the product id.
- **Newman output:** `AssertionError: expected '28000000' to be a number` and
  `data.price should be number`
- **Impact:** the type is data-dependent, so a client that works in testing
  breaks on half of production data. Arithmetic on the string value produces
  concatenation rather than addition.

---

### BUG-05 | Any order is readable by anyone (IDOR)

- **Requirement:** SEC-02 (*"Các API có tính bảo mật phải yêu cầu JWT Token hợp
  lệ"*) and FR-11 (*"Người dùng chỉ xem được đơn hàng của chính mình"*)
- **Severity:** Critical · **Endpoint:** `GET /api/orders/:id`
- **Test cases:** API3 / `03 - Security` / `SEC-02`, `SEC-02b`

**Steps to reproduce**

1. As user A, create an order; note its id.
2. `GET /api/orders/<A's order id>` **with no `Authorization` header at all**.
3. Repeat while authenticated as an unrelated user B.

- **Expected:** `401` without a token; `403`/`404` for a non-owner.
- **Actual:** `200 OK` with the full order in both cases — id, `user_id`,
  `total_amount`, `shipping_address`, `created_at`.
- **Newman output:** `expected 200 to be one of [ 401, 403, 404 ]`
- **Impact:** every order in the system, including the customer's shipping
  address, is enumerable by an anonymous caller walking the id sequence. Note
  that the sibling route `GET /api/orders/my-orders` *is* protected — this one
  route was left without the middleware.

---

### BUG-06 | Non-admin token reaches an admin endpoint

- **Requirement:** SEC-03 (*"API Admin phải kiểm tra `role = 'admin'` trong
  Token, không chỉ kiểm tra sự tồn tại của Token"*) and FR-12
- **Severity:** Critical · **Endpoint:** `GET /api/admin/orders`
- **Test case:** API4 / `03 - Security` / `SEC-03`

**Steps to reproduce**

1. Log in as the ordinary seeded user `test@eshop.com` / `Test1234!`.
2. `GET /api/admin/orders` with that user's token.

- **Expected:** `401`/`403` — the token's role is `user`, not `admin`.
- **Actual:** `200 OK` with every order in the system, joined with the ordering
  users' names.
- **Newman output:** `expected 200 to be one of [ 401, 403 ]`
- **Impact:** the entire admin order dataset is exposed to any registered
  customer. The endpoint checks that a token exists but never inspects its
  `role` claim — exactly the failure SEC-03 was written to prevent.

---

### BUG-07 | Registration enforces no mandatory-field validation

- **Requirement:** FR-01 — *"Người dùng phải cung cấp: Họ Tên, Email, Mật khẩu"*
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test cases:** `A1-DP-002`..`005`, `A1-DP-010`, `A1-DP-011`, `A1-DP-015`..`018`,
  `A1-DP-036`, `A1-DP-039`..`041`, `A1-DP-063`, `A1-DP-068`, `A1-DP-069`,
  `A1-DP-072`, `A1-DP-074` (17 cases)

Every one of these creates an account and returns `200`:

| Request body | Expected | Actual |
|---|---|---|
| `{"email":"…","password":"…"}` (no `name`) | 4xx | `200` |
| `{"name":null,"email":null,"password":null}` | 4xx | `200` |
| `{"name":"","email":"","password":""}` | 4xx | `200` |
| `{"name":"   ", …}` (whitespace only) | 4xx | `200` |
| `{"name":12345, …}` (wrong JSON type) | 4xx | `200` |
| `{}` (empty object) | 4xx | `200` |
| *(no body at all)* | 4xx | `200` |
| `[{…}]` (array instead of object) | 4xx | `200` |

- **Newman output:** `AssertionError: status code: expected 200 to be within 400..499`
- **Impact:** the users table accumulates rows with null or blank credentials.
  An account created with a null email cannot be logged into or recovered, and
  an empty-string email collides with every other empty-string email.
- **Root cause:** the handler destructures `req.body` and goes straight to the
  `INSERT` with no guard clause.

---

### BUG-08 | Password complexity policy is not enforced at all

- **Requirement:** FR-01 — *"Tối thiểu 8 ký tự, có ít nhất 1 chữ hoa, 1 chữ
  thường, 1 chữ số và 1 ký tự đặc biệt (`@ $ ! % * ? &`)"*
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test cases:** `A1-DP-042`, `A1-DP-045`..`049`, `A1-DP-057`..`060` (10 cases)

| Password | Rule violated | Expected | Actual |
|---|---|---|---|
| `Pass12!` | 7 chars, below the 8-char minimum | 4xx | `200` |
| `password123!` | no uppercase | 4xx | `200` |
| `PASSWORD123!` | no lowercase | 4xx | `200` |
| `Password!!` | no digit | 4xx | `200` |
| `Password123` | no special character | 4xx | `200` |
| `Password123#` | `#` is outside the permitted set | 4xx | `200` |
| `12345678` | digits only | 4xx | `200` |
| `password` | three rules at once | 4xx | `200` |
| (eight spaces) | whitespace only | 4xx | `200` |

- **Newman output:** `AssertionError: status code: expected 200 to be within 400..499`
- **Impact:** every account in the system may hold a trivially guessable
  password. Combined with BUG-02 (plaintext storage) and the FR-02 lockout
  behaviour, this materially weakens authentication.
- **Note:** the boundary case `A1-DP-043` (exactly 8 compliant characters)
  passes, but only because *everything* passes — it is not evidence that the
  boundary is implemented.

---

### BUG-09 | Email uniqueness is not enforced

- **Requirement:** FR-01 — the email must be *"duy nhất trong hệ thống"*
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test cases:** `A1-DP-033` (exact duplicate), `A1-DP-034` (differing only in case)

**Steps to reproduce**

1. `POST /api/register` with `dup@domain.com` → `200`, id *n*.
2. `POST /api/register` with `dup@domain.com` again → **`200`, id *n+1*.**
3. Repeat with `DUP@DOMAIN.COM` → `200` again.

- **Expected:** `4xx` (409 Conflict) on the second and third attempts.
- **Actual:** duplicate accounts are created. The `users` table declares no
  `UNIQUE` constraint on `email` and the handler does not check first.
- **Newman output:** `AssertionError: status code: expected 200 to be within 400..499`
- **Impact:** `POST /api/login` resolves an email with
  `SELECT * FROM users WHERE email = ?` and takes the first row, so the second
  registrant can never log in — and password reset targets an ambiguous account.
  `A1-ST-002` shows the original account is at least not overwritten.

---

### BUG-10 | Confirm-password is not implemented

- **Requirement:** FR-01 — *"Phải có trường Xác nhận mật khẩu — hệ thống từ chối
  nếu hai trường không khớp"*
- **Severity:** Medium · **Endpoint:** `POST /api/register`
- **Test cases:** `A1-DP-066` (mismatch), `A1-DP-067` (field absent)

- **Expected:** `4xx` when `confirmPassword` differs from `password`, and when
  it is missing entirely.
- **Actual:** `200` in both cases — the field is ignored.
- **Newman output:** `AssertionError: status code: expected 200 to be within 400..499`
- **Scope note worth resolving before filing:** `api_specification.md` does not
  document a confirmation field at all, so this may be a requirements-
  traceability defect (the API spec omits an FR-01 rule) rather than purely an
  implementation defect. Either way FR-01 is not satisfied end to end. Say which
  reading you are filing under.

---

### BUG-11 | A non-JSON `Content-Type` crashes the endpoint with HTTP 500

- **Requirement:** spec conformance — a malformed client request is a `4xx`
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test case:** `A1-DP-071`

**Steps to reproduce**

```http
POST http://localhost:3000/api/register
Content-Type: text/plain
X-Student-Id: 23127184

name=Test&email=a@b.com&password=Password123!
```

- **Expected:** `400` or `415 Unsupported Media Type`.
- **Actual:** **`500 Internal Server Error`.** `body-parser` does not populate
  `req.body` for a non-JSON content type, so destructuring it throws.
- **Newman output:** `AssertionError: expected 500 to be one of [ 400, 415 ]`
  and `status code: expected 500 to be below 500`
- **Impact:** an unauthenticated caller can force a server-side exception with a
  single header. This was **not** in the earlier source-read candidate list — it
  was found only because the request envelope was partitioned alongside the JSON
  fields.

---

### BUG-12 | Malformed JSON returns an HTML stack-trace page

- **Requirement:** SEC-05 / general information disclosure
- **Severity:** Medium · **Endpoint:** `POST /api/register` (Express default handler)
- **Test case:** `A1-SCH-012`

**Steps to reproduce**

Send a body that is not valid JSON with `Content-Type: application/json`, for
example `{"name": "Broken",` with no closing brace.

- **Expected:** a JSON error body, e.g. `{"error": "Invalid JSON"}`.
- **Actual:** `400` with `Content-Type: text/html; charset=utf-8` and an HTML
  page containing a `<pre>` block with the server-side stack trace.
- **Newman output:** `expected 'text/html; charset=utf-8' to not include
  'text/html'` and `expected '<!doctype html>…' to not include '<pre>'`
- **Impact:** discloses framework, file paths and internal structure to an
  unauthenticated caller, and breaks the API contract for any client that
  expects JSON on every response. `A1-DP-070` confirms the status code itself
  (`400`) is correct — only the body is wrong.

---

### BUG-13 | Product write routes perform no authorization

- **Requirement:** SEC-03 / FR-12
- **Severity:** Critical · **Endpoints:** `POST /api/products`,
  `PUT /api/products/:id`, `DELETE /api/products/:id`
- **Test cases:** `A2-SEC-011` through `A2-SEC-015`

**Expected:** no token is rejected with `401`; a genuine non-admin token is
rejected with `403`.

**Actual:** every create, update and delete request returns `200` and mutates
the catalogue. Both authentication and role authorization are absent on all
three routes.

**Newman evidence:** `status code: expected 200 to be within 401..403`.

---

### BUG-14 | JWT remains usable after its account is deleted

- **Requirement:** SEC-02
- **Severity:** High · **Endpoint:** `GET /api/orders/my-orders`
- **Test case:** `A3-DP-009`

**Steps:** create and log in a throwaway user, delete that user through the
admin API, then reuse the old token for order history.

- **Expected:** `401`/`403`; a session must not outlive its account.
- **Actual:** `200 OK`. Signature validity is checked, but the token subject is
  not revalidated against the current users table.
- **Newman evidence:** `status code: expected 200 to be within 401..403`.

---

### BUG-15 | Customer can cancel an order in `shipping`

- **Requirement:** FR-10 - cancellation is allowed only from `pending` or
  `confirmed`.
- **Severity:** High · **Endpoint:** `PUT /api/orders/:id/cancel`
- **Test cases:** `A3-ST-008`, student-designed post-condition `A3-HR-001`

- **Expected:** a 4xx response and the order remains `shipping`.
- **Actual:** `200 OK`; a subsequent independent history read shows
  `status = "canceled"`.
- **Newman evidence:** `expected 'canceled' to deeply equal 'shipping'`.

The post-condition case proves this is a real mutation, not merely an
incorrect success status.

---

### BUG-16 | `canceled` orders can transition to `delivered`

- **Requirement:** FR-10 / FR-13
- **Severity:** High · **Endpoint:** `PUT /api/admin/orders/:id/status`
- **Test cases:** `A3-ST-020`, `A4-ST-016`

- **Expected:** `400`; both `canceled` and `delivered` are terminal states.
- **Actual:** `200 OK` and the canceled order becomes delivered.
- **Newman evidence:** `status code: expected 200 to be within 400..499`.
- **Business impact:** FR-13 sums delivered orders as revenue, so this invalid
  transition can turn a canceled sale into reported revenue.

---

## Candidates (source-read, not yet executed)

Leads found by reading `eshop/backend/server.js`. Write a test case, run it,
and only then promote a row into *Confirmed* — with its Newman output quoted.

*C-01 (password complexity), C-02 (email uniqueness), and C-06 (shipping
cancellation) were promoted to BUG-08, BUG-09, and BUG-15 after execution and
no longer appear here.*

| # | Requirement | Where | What the code appears to do | Test case to write |
|---|---|---|---|---|
| C-03 | FR-02 | `POST /api/login` | Failed attempts increment by **2**, lock fires at 3 | Lockout should trigger on the 3rd failure, not the 2nd |
| C-04 | SEC-07 | `POST /api/forgot-password` | Reset token is 4 digits, never expires, not invalidated by time | OTP must be >= 6 digits, expiring, single-use |
| C-05 | SEC-06 | `PUT /api/users/me` | Accepts `role` from the request body | A user must not be able to promote themselves to admin |
| C-07 | FR-10 | `PUT /api/admin/orders/:id/status` | `canceled -> delivered` is explicitly permitted | That transition must be rejected |
| C-08 | FR-13 | admin UI `App.jsx` | Revenue computed as `total_amount * 2` | Dashboard revenue must equal the API's delivered-order sum — note this one is a **frontend** defect, so cite the API total as the oracle |
| C-09 | FR-12 | `POST/PUT/DELETE /api/products` | No `authenticateToken` middleware at all | Anonymous product create/update/delete must be refused |

---

## GitHub Issue checklist

For each confirmed bug:

- [ ] Title states the observable failure, not the suspected cause
- [ ] Steps to reproduce that a TA can paste into Postman
- [ ] Expected vs actual, with the requirement or SEC id quoted
- [ ] **Screenshot attached** (Postman response or the Newman failure) — required
- [ ] Issue URL recorded in the summary table above
