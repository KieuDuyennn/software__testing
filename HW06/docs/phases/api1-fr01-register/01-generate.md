# API 1 - FR-01 Account Registration - Phase 1: Generate with AI

> Pipeline step 1 of 4.

| Field | Value |
|---|---|
| Pool | A |
| Requirement | FR-01 |
| Endpoint under test | `POST /api/register` |
| Postman collection | `collections/API1_FR01_Register.postman_collection.json` |
| Case specification | `scripts/cases/api1_fr01_register.py` |
| Coverage tally | `reports/coverage_api1-fr01-register.md` |
| Parameters | `name` (string), `email` (string), `password` (string) |
| Target set by the brief | >= 35 test cases |
| **Generated** | **121 test cases (3.5x the minimum)** |

## 1. Contract under test

From `refs/spec/api_specification.md`:

```http
POST /api/register
Content-Type: application/json

{ "name": "Nguyen Van A", "email": "test@domain.com", "password": "Password123!" }

200 OK -> {"message": "User registered successfully", "id": 1}
```

Rules the test cases hold the implementation to, from `refs/spec/eshop_requirements_README.md`:

| Source | Rule |
|---|---|
| FR-01 | The user must supply Họ Tên, Email and Mật khẩu |
| FR-01 | Email must be well formed (`user@domain.com`) **and unique in the system** |
| FR-01 | Password: >= 8 characters, with >= 1 uppercase, 1 lowercase, 1 digit and 1 special character from `@ $ ! % * ? &` |
| FR-01 | A confirm-password field must exist; registration is refused when the two differ |
| FR-01 | After success the user is sent to the Login page (so registration must not open a session) |
| SEC-01 | Passwords must not be stored in plaintext |
| SEC-04 | User input must be escaped when displayed, never injected as markup |
| SEC-05 | Database access must use parameterised queries |
| SEC-06 | The client must not be able to set `role` |
| SEC-02 | **Not applicable** - registration is a public endpoint by design (documented by case `A1-SEC-020`) |
| SEC-03, SEC-07 | **Not applicable** - no admin role and no OTP is involved in registration |

## 2. How the AI was driven, step by step

The brief forbids a single generic prompt. The AI was taken through the five
stages defined in the `api-test-generator` skill, each stage consuming the
previous stage's output.

**Standing constraint given to the AI at every stage, and the reason for it:**
expected results must be derived from the specification and the FR/SEC rules,
**never** from what the running SUT returns. An oracle read off the
implementation makes a test that passes by construction and cannot find a
defect. This single constraint is what produced 53 failing cases below.

### Step 1 - Establish the contract

- **Tool:** Claude Code (Opus 5) · **Date:** 2026-08-23
- **Goal:** make the AI restate the endpoint's contract from the spec and
  enumerate the FR/SEC rules that constrain it, *before* writing any case.
- **Output:** the two tables in section 1 above. The restatement surfaced a
  contradiction immediately: **FR-01 mandates a confirm-password field that
  `api_specification.md` does not document.** That is recorded as a spec gap
  rather than silently resolved in either direction.
- **Human review:** phase 2.

### Step 2 - Domain partitions per parameter

- **Goal:** an equivalence-class and boundary table for every parameter, built
  from the requirement text, before any test case is written.
- **Output:** the partition tables in section 3, expanded into **79 cases** -
  13 on `name`, 24 on `email`, 27 on `password`, 3 on the confirm field, 8 on
  the request envelope and 4 on the HTTP method.
- **Note:** the request envelope (body shape, `Content-Type`) and the HTTP
  method are part of the input domain too. Restricting partitioning to the
  three documented JSON fields would have missed `A1-DP-071`, which turned out
  to be one of the two new defects found.
- **Human review:** phase 2.

### Step 3 - State transitions

- **Goal:** enumerate the states reachable from registration and the initial
  state a new account must be in, then one case per transition.
- **Output:** the machine in section 4, expanded into **10 cases**.
- **Note:** FR-10's order machine does not apply here. What does apply is the
  *account* lifecycle, plus the invariants a fresh account must satisfy - role,
  lockout counters, empty cart, empty order history. Those initial-state
  assertions are what catch a registration that silently sets more than it
  should.
- **Human review:** phase 2.

### Step 4 - Security (SEC-01..SEC-07)

- **Goal:** cases per applicable SEC rule, and an explicit statement of which
  rules do *not* apply and why.
- **Output:** **20 cases**. SEC-01 (4), SEC-04 (2), SEC-05 (5), SEC-06 (5),
  plus information-disclosure cases and `A1-SEC-020`, which documents the
  SEC-02 not-applicable judgement by asserting the endpoint stays public.
- **Note:** the AI was told to treat mass assignment as a first-class attack
  class, which produced the `id` / `login_attempts` / `locked_until` /
  `reset_token` injection cases. A prompt that only said "test SEC-06" would
  have produced the `role` case alone.
- **Human review:** phase 2.

### Step 5 - Schema validation

- **Goal:** the exact response schema per status code, asserted strictly.
- **Output:** **12 cases**, using `additionalProperties: false` so a response
  carrying fields the spec never promised fails rather than passes.
- **Note:** strictness is the point. `A1-SCH-009` asserts the success body has
  exactly the keys `id` and `message`; `A1-SCH-008` asserts no `password`,
  `role`, `token` or `reset_token` appears anywhere in the body.
- **Human review:** phase 2.

## 3. Domain partition tables

### `name`

| Class | Representative | Expected per FR-01 | Cases |
|---|---|---|---|
| Valid ordinary | `"Nguyen Van A"` | 200 | DP-001 |
| Valid, diacritics | `"Lê Phạm Kiều Duyên"` | 200, preserved | DP-007 |
| Boundary, 1 char | `"A"` | 200 | DP-006 |
| Boundary, 255 / 5000 chars | `"N"*255`, `"N"*5000` | no 5xx | DP-008, DP-009 |
| Absent / null / empty / blank | - | 4xx | DP-002..005 |
| Wrong type | `12345`, `{...}` | 4xx | DP-010, DP-011 |
| Whitespace padding, emoji | `"  A  "`, `"Duyên 🌸"` | no 5xx | DP-012, DP-013 |

### `email`

| Class | Representative | Expected per FR-01 | Cases |
|---|---|---|---|
| Valid forms | plain, `+tag`, subdomain, hyphenated domain, uppercase | 200 | DP-014, DP-029..032 |
| Absent / null / empty / blank | - | 4xx | DP-015..018 |
| Malformed | no `@`, no domain, no local part, no TLD, `@@`, leading/trailing dot, `..`, space, `()` | 4xx | DP-019..028 |
| **Not unique** | already-registered address, and the same address in a different case | 4xx | DP-033, DP-034 |
| Boundary | local part 65 chars (RFC cap is 64) | 4xx | DP-035 |
| Wrong type / padding | `12345`, trailing space | 4xx / no 5xx | DP-036, DP-037 |

### `password`

| Class | Representative | Expected per FR-01 | Cases |
|---|---|---|---|
| Valid | `"Password123!"` | 200 | DP-038 |
| **Boundary on length** | 7 / **8** / 9 characters | 4xx / 200 / 200 | DP-042, DP-043, DP-044 |
| Missing character class | no uppercase, no lowercase, no digit, no special | 4xx | DP-045..048 |
| Special char outside the set | `#` | 4xx | DP-049 |
| **Each permitted special char** | `@ $ ! % * ? &` - one case each | 200 | DP-050..056 |
| Degenerate | digits only, letters only, blank, `"password"` | 4xx | DP-057..060 |
| Absent / null / empty | - | 4xx | DP-039..041 |
| Edge | embedded space, 1000 chars, numeric type, unicode | see notes | DP-061..064 |

FR-01 enumerates the permitted special characters, so each one is its own
equivalence class - hence seven cases rather than one representative.

### Request envelope and HTTP method

| Class | Expected | Cases |
|---|---|---|
| Empty object, no body, all-null, array body | 4xx | DP-068, DP-069, DP-072, DP-074 |
| Malformed JSON | 400 | DP-070 |
| `Content-Type: text/plain` | 400 or 415 | DP-071 |
| Unknown extra fields | 200, ignored | DP-073 |
| ~100 KB payload | 400/413, no 5xx | DP-075 |
| `GET` / `PUT` / `DELETE` / `PATCH` on the route | 404 or 405 | DP-076..079 |

## 4. State machine

```
              register (valid input)
(no account) ------------------------> [registered] ---- login ----> [authenticated]
      |                                     |
      | register (invalid input)            | register again, same email
      v                                     v
 (still no account)                   (must not overwrite)
```

Initial-state invariants a freshly registered account must satisfy:
`role = "user"`, `login_attempts = 0`, `locked_until = null`, empty cart, empty
order history, no session token issued.

| Case | Transition or invariant |
|---|---|
| ST-001 | registered -> authenticated |
| ST-002 | a duplicate registration must not replace the existing account |
| ST-003 | registered -> profile readable |
| ST-004 | initial role is `user` |
| ST-005 | not locked, zero failed attempts |
| ST-006 | registered -> password reset can be initiated |
| ST-007 | two registrations receive distinct, increasing ids |
| ST-008 | a **rejected** registration leaves no usable account |
| ST-009 | new account starts with an empty cart |
| ST-010 | new account starts with no orders |

## 5. Security matrix

| SEC | Applies? | Attack modelled | Cases |
|---|---|---|---|
| SEC-01 | Yes | credential disclosure in login / register / profile responses; storage form | SEC-001..004 |
| SEC-02 | **No** | registration is public by design - asserted, not assumed | SEC-020 |
| SEC-03 | Indirect | an account created with an injected role must not reach admin APIs | SEC-013 |
| SEC-04 | Yes | stored XSS via `name` (`<script>`, `onerror`) | SEC-005, SEC-006 |
| SEC-05 | Yes | statement termination, tautology, `UNION SELECT`, comment sequence, and a data-integrity check afterwards | SEC-007..011 |
| SEC-06 | Yes | mass assignment of `role`, `id`, `login_attempts`/`locked_until`, `reset_token`, and prototype pollution | SEC-012..017 |
| SEC-07 | **No** | no OTP is involved in registration | - |
| - | Yes | no session token issued at registration; no DB internals in error bodies | SEC-018, SEC-019 |

## 6. Generated test cases

| Dimension | Cases generated |
|---|---:|
| Domain partitions | 79 |
| State transitions | 10 |
| Security (SEC-01..07) | 20 |
| Schema validation | 12 |
| **Total** | **121** |

Full index: `reports/coverage_api1-fr01-register.md`.
Excel table: `testcases/23127184_HW06_TestCases.xlsx`, sheet *API1 FR-01 Register*.
Machine-readable export: `testcases/api1-fr01-register_cases.json`.

### First execution (generation-phase smoke run, before the audit)

All 121 cases were executed against the seeded SUT to confirm they are
*executable* - not to accept their verdicts, which is the audit's job.

| Metric | Value |
|---|---:|
| Cases executed | 121 |
| Assertions | 577 |
| Assertions passed | 519 |
| Cases fully passing | 68 |
| **Cases with >= 1 failing assertion** | **53** |

Every failure was inspected: none was caused by a broken fixture or an
unreachable precondition, so all 121 cases are executable as written. The 53
failures cluster into a small number of causes, which phase 2 will confirm and
phase 4 will triage into bug reports:

| Cluster | Cases | Apparent cause |
|---|---:|---|
| No mandatory-field validation | 12 | `name`/`email`/`password` absent, null, empty or wrong-typed are all accepted |
| No email-format validation | 10 | every malformed address in DP-019..028 is accepted |
| Email uniqueness not enforced | 2 | DP-033, DP-034 - the same address registers twice |
| No password-complexity validation | 14 | length, character classes and the permitted special-character set are all unenforced |
| Confirm-password not implemented | 2 | DP-066, DP-067 |
| Envelope validation | 5 | empty/absent/array/all-null bodies accepted; `text/plain` returns **500** |
| Plaintext password | 3 | SEC-001, SEC-003, SEC-004 |
| Admin route reachable | 1 | SEC-013 |
| Unstructured / HTML error responses | 3 | SCH-007, SCH-010, SCH-012 |
| Rejected registration still creates an account | 1 | ST-008, a consequence of the validation gap |

Two of these were **not** in the pre-existing bug list and are new to this
phase: the **HTTP 500 on a non-JSON `Content-Type`** (DP-071) and the **HTML
stack-trace error page** returned for malformed JSON (SCH-012).

### What passed, and why that matters

Passing cases are evidence too. Notably:

- **SEC-005..011 all passed** - the registration handler does use parameterised
  queries, so SEC-05 is satisfied and the seeded data survives injection.
- **SEC-012 passed** - a `role` injected at registration is *ignored*, so SEC-06
  holds for this endpoint. (It does **not** hold for `PUT /api/users/me`, which
  is a different endpoint and a separate finding.)
- **SEC-014, SEC-015, SEC-017 passed** - `id`, lockout fields and `__proto__`
  injection are all ignored.
- **DP-076..079 passed** - the route is correctly POST-only.

Reporting "registration has no validation" without also reporting that its SQL
handling is sound would be an inaccurate picture of the endpoint.

## 7. Notes for the audit phase

Carry these into `02-audit.md`; each is a candidate INVALID or INCOMPLETE label.

1. **`A1-SEC-013` is mis-titled.** It fails, but not for the reason its title
   claims. `A1-SEC-012` shows the injected role *was* ignored, so the account is
   an ordinary user - it reaches `/api/admin/users` because that route never
   checks the role claim at all. The case detects a real defect but attributes
   it to the wrong cause. Retitle it, or label it INCOMPLETE and split it.
2. **11 cases carry a flagged specification gap** (highlighted in the Excel
   sheet): DP-006, DP-008, DP-009, DP-012, DP-037, DP-061, DP-062, DP-065,
   DP-067, DP-075, SEC-020. These assert only what can be justified from the
   spec. Decide case by case whether to tighten the oracle from FR-01, or to
   keep the case as a documented ambiguity.
3. **The confirm-password cases test a requirement the API spec omits.** DP-065
   to DP-067 apply FR-01 to the API. The audit must classify this scope choice
   as either an implementation defect or a requirements-traceability problem.
4. **DP-009, DP-062 and DP-075 assert only "no 5xx".** That is a weak oracle.
   Decide whether FR-01 justifies a firm limit, or accept the weakness and say so.
5. **DP-012 and DP-037 accept either trimming or rejection.** A case that
   accepts two contradictory outcomes cannot fail usefully - a strong INCOMPLETE
   candidate.
6. **Clustered failures may be one defect, not 53.** Twelve cases failing on
   missing-field validation are twelve symptoms of one missing guard clause.
   Group them before filing GitHub Issues, or the bug report will overstate the
   defect count.
