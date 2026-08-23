# HW06 - Bug Report

Student ID: **23127184** · SUT: **EShop** (`ttbhanh/eshop-sut`) · Base URL: `http://localhost:3000`

Every bug below must also be filed as a **GitHub Issue with a screenshot**
(Section 6.5 of the brief). Fill the *Issue* column as you file them.

---

## Status of this file

The six defects in the *Confirmed* section were **reproduced by an actual
Newman run** of the scaffold's exemplar test cases against the seeded SUT — the
failing assertion and the observed response are quoted verbatim from that run.
They are starting evidence, not the finished set: the full pipeline (generate →
audit → extend) will add more.

The *Candidates* section lists defects identified by **reading the backend
source only**. They have not been executed yet, so they are recorded as leads,
not findings. Do not report a candidate as a bug until a test case has
reproduced it.

---

## Summary

| ID | Requirement | Severity | Title | Status | Issue |
|---|---|---|---|---|---|
| BUG-01 | FR-01 | High | Registration accepts a malformed email address | Confirmed | |
| BUG-02 | SEC-01 | Critical | Passwords stored and returned in plaintext | Confirmed | |
| BUG-03 | FR-06 | Medium | Missing product returns `200 {}` instead of `404` | Confirmed | |
| BUG-04 | FR-06 | Medium | `price` is a string for even product ids | Confirmed | |
| BUG-05 | SEC-02 / FR-11 | Critical | Any order readable by anyone (IDOR, no auth) | Confirmed | |
| BUG-06 | SEC-03 / FR-12 | Critical | Non-admin token reaches `/api/admin/orders` | Confirmed | |

---

## Confirmed

### BUG-01 | Registration accepts a malformed email address

- **Requirement:** FR-01 — *"Email phải có định dạng hợp lệ (`user@domain.com`)"*
- **Severity:** High · **Endpoint:** `POST /api/register`
- **Test case:** API1 / `01 - Domain partitions` / `DP-002`

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
- **Note:** the handler performs no validation of any kind before the `INSERT`.
  Password complexity and email uniqueness are almost certainly affected too —
  write those cases and confirm before reporting them separately.

---

### BUG-02 | Passwords stored and returned in plaintext

- **Requirement:** SEC-01 — *"Mật khẩu **không** được lưu dưới dạng plaintext"*
- **Severity:** Critical · **Endpoint:** `POST /api/register`, `POST /api/login`
- **Test case:** API1 / `03 - Security` / `SEC-01`

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

## Candidates (source-read, not yet executed)

Leads found by reading `eshop/backend/server.js`. Write a test case, run it,
and only then promote a row into *Confirmed* — with its Newman output quoted.

| # | Requirement | Where | What the code appears to do | Test case to write |
|---|---|---|---|---|
| C-01 | FR-01 | `POST /api/register` | No password-complexity check at all | Weak passwords (`a`, `12345678`, `password`) should be rejected |
| C-02 | FR-01 | `POST /api/register` | `email` has no `UNIQUE` constraint | Register the same email twice; second should be rejected |
| C-03 | FR-02 | `POST /api/login` | Failed attempts increment by **2**, lock fires at 3 | Lockout should trigger on the 3rd failure, not the 2nd |
| C-04 | SEC-07 | `POST /api/forgot-password` | Reset token is 4 digits, never expires, not invalidated by time | OTP must be >= 6 digits, expiring, single-use |
| C-05 | SEC-06 | `PUT /api/users/me` | Accepts `role` from the request body | A user must not be able to promote themselves to admin |
| C-06 | FR-10 | `PUT /api/orders/:id/cancel` | Cancel is blocked only for `delivered`/`canceled`, so `shipping` can be cancelled | Cancel must be allowed only from `pending` or `confirmed` |
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
