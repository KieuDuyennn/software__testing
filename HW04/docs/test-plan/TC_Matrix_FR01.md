# FR-01 Account registration — test-case matrix (Pool A)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Data file:** `automation/data/fr01_registration.csv` — one row per case, no inline arrays.
**Spec:** `automation/tests/fr01_account_registration/fr01.registration.spec.ts`

Trace each row back to the HW02 design artifact where one exists
(`HW02/submission/projects/fr01_account_registration/output/`), so the TA can see
that these are the same cases, now automated — not a fresh invention.

**HW02 inventory carried over: 31 cases** — 24 domain (`03_Domain_Test_Cases.md`)
+ 7 boundary (`04_Boundary_Value_Test_Cases.md`). All 31 were executed in HW02
(`TC_Checklist.md`: 11 ✅ match, 10 ❌ divergent, 8 ⚠️ conditional, 2 ⛔ not runnable).

**Automated here: 30** = 31 carried over − 2 dropped (TC-17, TC-23, see "Cases
deliberately NOT automated") + 1 derived (TC-24, the password-rule diagnostic).
No bulk derivation: the target is 20 per feature and FR-01 is already above it.
Keeping 30 rather than trimming to 20 — these are already
designed and already executed, and in a data-driven suite each extra case is one CSV row,
not new code. Dropping designed cases to hit a round number loses coverage for no gain.

## What the real registration page turned out to be

Read from `frontend-web/src/pages/Register.jsx` (source, not a run — confirm against the
rendered page before these become hard assertions):

- The form has **three** fields only: `Họ Tên`, `Email`, `Mật khẩu`, plus an `Đăng Ký`
  button. There is **no Confirm Password field** and no phone field.
- `<label>` carries no `htmlFor` and the `<input>`s carry no `id`/`aria-label`, so
  `getByLabel` cannot match them and the two text inputs share no accessible name.
- Errors render in a **single** `<div>` bound to one string, so at most one message is
  visible at a time. All three inputs are `required`, so an empty field is stopped by
  native browser validation before any app-level message appears.
- The client-side password check at L15 is
  `/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/` — it **requires a
  whitespace character** and its character class **excludes special characters**, while
  the message it prints (L18) and the hint below the field (L65) both state that a
  special character is required. Consequence: `Password123!` is rejected,
  `Password 123` is accepted. Recorded here as an observation; the defect verdict and
  bug write-up are the author's.

**D-4 baseline** (every row varies exactly one field from this, unless noted):
Full Name `Nguyen Van A` · Email a fresh unique valid address · Password `Password123!`
· Confirm Password `Password123!`.

| # | TC ID | Type | Intent | HW02 source | Level | Assertion pattern | Automated? | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | TC-01a | positive | all four fields valid → account created, redirected to Login | 03 §1 | UI | 1 | ☐ | REQ-15 / EC-28 |
| 2 | TC-01b | positive | `POST /api/register` → 200 `{message, id}` | 03 §1 | API | 2 | ☐ | REQ-16 / EC-27 |
| 3 | TC-02 | negative | Full Name `""` | 03 §2 | UI | 1 | ☐ | → EC-29 |
| 4 | TC-03 | negative | `name` key omitted from JSON body | 03 §2 | API | 2 | ☐ | → EC-29 |
| 5 | TC-04 | negative | Email `""` | 03 §2 | UI | 1 | ☐ | → EC-29 |
| 6 | TC-05 | negative | `email` key omitted from JSON body | 03 §2 | API | 2 | ☐ | → EC-29 |
| 7 | TC-06 | negative | Email `userdomain.com` (no `@`) | 03 §2 | UI | 1 | ☐ | → EC-30 |
| 8 | TC-07 | negative | Email `user@` (no domain) | 03 §2 | UI | 1 | ☐ | → EC-30 |
| 9 | TC-08 | negative | Email `@domain.com` (no local part) | 03 §2 | UI | 1 | ☐ | → EC-30 |
| 10 | TC-09 | negative | duplicate email — account already exists | 03 §2 | UI | 1 | ☐ | → EC-31; needs a seeded account |
| 11 | TC-10 | negative | Password `""` | 03 §2 | UI | 1 | ☐ | **Reduced from HW02.** HW02 wrote this as a combined `Password ""` + `Confirm ""` probe checking that **both** signals surface; with no Confirm field and a single one-string error region, only the password half is reachable. OQ-14 is closed by structure, not by a run |
| 12 | TC-11 | negative | `password` key omitted from JSON body | 03 §2 | API | 2 | ☐ | → EC-29 |
| 13 | TC-12 | negative | Password `Pass1!` (6 chars, all other rules met) | 03 §2 | UI | 1 | ☐ | → EC-32 |
| 14 | TC-13 | negative | Password `password123!` (no uppercase) | 03 §2 | UI | 1 | ☐ | → EC-32 |
| 15 | TC-14 | negative | Password `PASSWORD123!` (no lowercase) | 03 §2 | UI | 1 | ☐ | → EC-32 |
| 16 | TC-15 | negative | Password `Password!` (no digit) | 03 §2 | UI | 1 | ☐ | → EC-32 |
| 17 | TC-16 | negative | Password `Password123` (no special char) | 03 §2 | UI | 1 | ☐ | → EC-32 |
| 18 | TC-18 | edge (conditional) | Full Name `"   "` (whitespace only) | 03 §3 | UI | 1 | ☐ | **Blocked on OQ-04/OQ-10** — reject or accept not yet decidable |
| 19 | TC-19 | edge (conditional) | Email `user@domain` (no TLD) | 03 §3 | UI | 1 | ☐ | **Blocked on OQ-11** |
| 20 | TC-20 | edge (conditional) | Email `user+tag@mail.domain.com` | 03 §3 | UI | 1 | ☐ | **Blocked on OQ-11** |
| 21 | TC-21 | edge (conditional) | Email `Test@domain.com` vs existing `test@domain.com` | 03 §3 | UI | 1 | ☐ | **Blocked on OQ-09** — case-sensitivity of uniqueness |
| 22 | TC-22 | edge (conditional) | Password `Password123#` (`#` outside the set) | 03 §3 | UI | 1 | ☐ | **Blocked on OQ-06** |
| 23 | BVA-01 | edge | Password `Pa1!abc` — exactly 7 chars (min − step) | 04 §1a | UI | 1 | ☐ | Pairs with BVA-02 to pin the boundary at exactly 8 |
| 24 | BVA-02 | edge | Password `Pa1!abcd` — exactly 8 chars (min) → **accepted** | 04 §1a | UI | 1 | ☐ | Catches a length check mis-specified as `<= 8` |
| 25 | BVA-03 | edge | Password `Pa1!abcde` — exactly 9 chars (min + step) → accepted | 04 §1a | UI | 1 | ☐ | |
| 26 | BVA-06 | edge | Password `P` — 1 char → must be **weak** (EC-32), not **missing** (EC-29) | 04 §1b | UI | 1 | ☐ | Isolation caveat: 1 char cannot satisfy composition rules; all extra faults route to the same output class |
| 27 | BVA-07 | edge | Password `Pa` — 2 chars → weak | 04 §1b | UI | 1 | ☐ | Same caveat as BVA-06 |
| 28 | BVA-04 | edge | Full Name `A` — 1 char → **accepted** | 04 §2 | UI | 1 | ☐ | Catches "empty" mis-specified as `length <= 1` |
| 29 | BVA-05 | edge | Full Name `An` — 2 chars → accepted | 04 §2 | UI | 1 | ☐ | |
| 30 | TC-24 | negative | Password `Password 123` — 12 chars, upper + lower + digit, **whitespace present, no special char** → must be rejected as weak | derived (not in HW02) | UI | 1 | ☐ | **Diagnostic case.** TC-12→TC-16 and BVA-01→05 all fail together against the L15 regex; this one isolates the cause by inverting the input. A password that satisfies the *printed* rule (`Password123!`) is rejected while one that violates it (`Password 123`) is accepted — the pair pins the fault to the regex, not to each individual case |

**Assertion patterns used:** 1 = UI state · 2 = API/contract · 3 = data integrity.
At least three distinct patterns must appear across the whole suite (brief §6).
Pattern 3 is not natural for FR-01 and is carried by FR-13's revenue-sum checks instead.

## Cases deliberately NOT automated

The brief asks you to "document any test cases you could not automate and explain
why". List them here — an honest, reasoned exclusion scores; a silent omission does not.

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| TC-17 | "Confirm ≠ Password" needs a Confirm Password field to type a differing value into. `Register.jsx` renders no such field, and the API body (`{name, email, password}`) has no `confirmPassword` key — unreachable at both interfaces. | Nobody, on this build. It becomes testable only if the field is added. Worth raising as a requirements-vs-implementation gap: HW02 designed against a spec that promised confirmation. |
| TC-23 | "Confirm Password empty" — same missing field. | Same as TC-17. |
| EC-34 (no TC) | "Confirm Password field absent" was designed as a *deviant* condition. On this build it is the **normal** state of the page, so it no longer discriminates anything. HW02 deferred it; it is now moot rather than deferred. | — |

## Open Questions that must be resolved against the running SUT before assertions are written

TC-18 to TC-22 carry conditional expected results in HW02. An automated test needs one
concrete assertion, so each OQ below must be settled by observing the real SUT first,
and the observation recorded — not guessed.

| OQ | Question | Affects |
|---|---|---|
| OQ-02 | Exact error text / code for each rejection | every negative row |
| OQ-04 / OQ-10 | Is a whitespace-only name treated as empty? | TC-18, and the BVA-04/05 derivation |
| OQ-06 | Is the special-char set exclusive (is `#` rejected)? | TC-22 |
| OQ-09 | Is email uniqueness case-insensitive? | TC-21 |
| OQ-11 | Is a TLD required? Is plus-addressing accepted? | TC-19, TC-20 |
