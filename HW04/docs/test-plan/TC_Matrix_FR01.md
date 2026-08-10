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

**Automated here: 31** = 31 carried over − 2 dropped (TC-17, TC-23, see "Cases
deliberately NOT automated") + 2 derived (TC-01c, the implementation-path diagnostic,
and TC-24, the password-rule diagnostic).
No bulk derivation: the target is 20 per feature and FR-01 is already above it.
Keeping 31 rather than trimming to 20 — these are already
designed and already executed, and in a data-driven suite each extra case is one CSV row,
not new code. Dropping designed cases to hit a round number loses coverage for no gain.

## What the real registration page turned out to be

Read from `frontend-web/src/pages/Register.jsx`, then **confirmed against the running
page** at `http://localhost:5173/register` with a throwaway locator probe: the form
holds 3 `<input>` elements in total, each proposed locator resolved to exactly 1,
`getByLabel` resolved to 0, and `getByRole('textbox')` resolved to 3.

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

## The `bypass` column, and why 11 rows do not use the spec password

The client-side password check runs before anything else on the page, so a case about
the *name* or *email* field never reaches its own validation while it carries a
spec-conformant password: it is rejected as a weak password and reports nothing about
what it was written to test.

Rather than lose those paths, 11 rows carry `Password 123` — a value the current build
accepts — and are marked `bypass=password-gate` in the data file. Ten rows use it only
to reach a name, e-mail, or boundary rule; TC-01c is explicitly a diagnostic of the
downstream redirect-and-persistence plumbing. Four points the report must keep straight:

- **For the ten requirement-derived rows, no expected result was changed.** Only the
  input on an unrelated field changed so the case can reach its target rule.
- **TC-01c is the exception and says so in its title and note.** Its expectation is
  calibrated to observed implementation behaviour; it is not evidence of conformance.
- **The bypassed value violates the written rule** (no special character). It is not a
  claim about what a valid password is; it is a key that opens a door that should not
  be locked. Every such row is greppable by its `bypass` value.
- **The gate itself is still tested.** TC-01a submits a specification-valid password and
  expects success; TC-24 submits `Password 123` and expects rejection. Their opposite
  outcomes, together with BVA-02/03, isolate the faulty rule. If it is corrected, all 11
  bypass rows must be revisited and TC-01c retired.

Rows carrying the bypass: TC-01c, TC-06, TC-07, TC-08, TC-09, TC-18, TC-19, TC-20,
TC-21, BVA-04, BVA-05.

**D-4 baseline** (every row varies exactly one field from this, unless noted):
Full Name `Nguyen Van A` · Email a fresh unique valid address · Password `Password123!`.

HW02's baseline had a fourth element, Confirm Password. It is dropped: the field does
not exist on this build.

**Row IDs here are unprefixed (`TC-01a`); the data file prefixes them with the feature
(`FR01-TC-01a`).** The suffix is the join key between this matrix and
`automation/data/fr01_registration.csv`.

`Channel` is where the rejection is expected to appear, and it is not cosmetic —
`native` cases are stopped by the browser's own `required` handling before the app runs,
so they assert on constraint-validation state, not on any message the app renders.
`bypass` marks the 11 rows explained above.

| # | TC ID | Type | Intent | HW02 source | Level | Channel | Assertion pattern | Automated? | Notes |
|---|---|---|---|---|---|---|---|---|---|
| 1 | TC-01a | positive | all three fields valid → account created, redirected to Login | 03 §1 | UI | redirect | 1 + 3 | ☑ | REQ-15 / EC-28. Password is **specification-valid** (`Password123!`): 8+ chars, upper, lower, digit and `!` from the documented set. Not bypassed — a positive case must exercise the rule as written, so this row is expected red while the L15 regex stands |
| 2 | TC-01b | positive | `POST /api/register` → created account | 03 §1 | API | api | 2 + 3 | ☑ | REQ-16 / EC-27; status recorded on the first run: **200 OK**, per `api_specification.md` §1.1 |
| 3 | TC-01c | diagnostic | end-to-end redirect **and persistence** using a password this build accepts | derived (not in HW02) | UI | redirect · **bypass** | 1 + 3 | ☑ | **Expectation calibrated to observed behaviour, not to the specification** — it therefore proves nothing about the requirement and must never be cited as evidence that registration conforms. It exists only so the happy-path plumbing (redirect, then the account being usable with the submitted name and e-mail) stays covered while TC-01a is blocked at the client gate. Retire it when the password rule is corrected |
| 4 | TC-02 | negative | Full Name `""` | 03 §2 | UI | native | 1 | ☑ | → EC-29; `required` stops submission, no app message is produced |
| 5 | TC-03 | negative | `name` key omitted from JSON body | 03 §2 | API | api | 2 + 3 | ☑ | → EC-29 |
| 6 | TC-04 | negative | Email `""` | 03 §2 | UI | native | 1 | ☑ | → EC-29; same as TC-02 |
| 7 | TC-05 | negative | `email` key omitted from JSON body | 03 §2 | API | api | 2 | ☑ | → EC-29. Pattern 3 is **not** reachable here: `/api/login` is keyed on e-mail and the build exposes no authenticated account-list endpoint, so whether a row was written stays an open gap. The response contract (no created-account `id`) is asserted instead |
| 8 | TC-06 | negative | Email `userdomain.com` (no `@`) | 03 §2 | UI | banner · **bypass** | 1 + 3 | ☑ | → EC-30 |
| 9 | TC-07 | negative | Email `user@` (no domain) | 03 §2 | UI | banner · **bypass** | 1 + 3 | ☑ | → EC-30 |
| 10 | TC-08 | negative | Email `@domain.com` (no local part) | 03 §2 | UI | banner · **bypass** | 1 + 3 | ☑ | → EC-30 |
| 11 | TC-09 | negative | duplicate email — account already exists | 03 §2 | UI | banner · **bypass** | 1 | ☑ | → EC-31; needs a seeded account. Pattern 3 is deliberately skipped: the account exists **by design** here, so "no account was written" is not a claim this row can make |
| 12 | TC-10 | negative | Password `""` | 03 §2 | UI | native | 1 | ☑ | **Reduced from HW02.** HW02 wrote this as a combined `Password ""` + `Confirm ""` probe checking that **both** signals surface; with no Confirm field and a single one-string error region, only the password half is reachable. OQ-14 is closed by structure, not by a run |
| 13 | TC-11 | negative | `password` key omitted from JSON body | 03 §2 | API | api | 2 | ☑ | → EC-29. Same unreachable pattern 3 as TC-05: `/api/login` verifies the password, so a row created without one cannot be found through it |
| 14 | TC-12 | negative | Password `Pass1!` (6 chars, all other rules met) | 03 §2 | UI | banner | 1 + 3 | ☑ | → EC-32 |
| 15 | TC-13 | negative | Password `password123!` (no uppercase) | 03 §2 | UI | banner | 1 + 3 | ☑ | → EC-32 |
| 16 | TC-14 | negative | Password `PASSWORD123!` (no lowercase) | 03 §2 | UI | banner | 1 + 3 | ☑ | → EC-32 |
| 17 | TC-15 | negative | Password `Password!` (no digit) | 03 §2 | UI | banner | 1 + 3 | ☑ | → EC-32 |
| 18 | TC-16 | negative | Password `Password123` (no special char) | 03 §2 | UI | banner | 1 + 3 | ☑ | → EC-32 |
| 19 | TC-18 | edge | Full Name `"   "` (whitespace only) → rejected | 03 §3 | UI | banner · **bypass** | 1 + 3 | ☑ | HW02 left this conditional. The assertion now follows the **specification** (a blank name is not a name); OQ-04/OQ-10 stay open as *"what the SUT actually does"*, to be recorded from the run, not guessed in advance |
| 20 | TC-19 | edge | Email `user@domain` (no TLD) → rejected | 03 §3 | UI | banner · **bypass** | 1 + 3 | ☑ | Assertion follows the spec; OQ-11 remains open on observed behaviour |
| 21 | TC-20 | edge | Email `user+tag@mail.domain.com` → accepted | 03 §3 | UI | redirect · **bypass** | 1 + 3 | ☑ | Plus-addressing is valid per RFC; OQ-11 remains open on observed behaviour |
| 22 | TC-21 | edge | Email `Test@domain.com` vs existing `test@domain.com` → rejected | 03 §3 | UI | banner · **bypass** | 1 | ☑ | Assertion follows the spec (uniqueness is case-insensitive); OQ-09 remains open. Pattern 3 skipped for the same reason as TC-09 |
| 23 | TC-22 | edge | Password `Password123#` (`#` outside the set) → rejected | 03 §3 | UI | banner | 1 + 3 | ☑ | Assertion follows the spec (the set is exclusive); OQ-06 remains open |
| 24 | BVA-01 | edge | Password `Pa1!abc` — exactly 7 chars (min − step) | 04 §1a | UI | banner | 1 + 3 | ☑ | Pairs with BVA-02 to pin the boundary at exactly 8 |
| 25 | BVA-02 | edge | Password `Pa1!abcd` — exactly 8 chars (min) → **accepted** | 04 §1a | UI | redirect | 1 + 3 | ☑ | Catches a length check mis-specified as `<= 8` |
| 26 | BVA-03 | edge | Password `Pa1!abcde` — exactly 9 chars (min + step) → accepted | 04 §1a | UI | redirect | 1 + 3 | ☑ | |
| 27 | BVA-06 | edge | Password `P` — 1 char → must be **weak** (EC-32), not **missing** (EC-29) | 04 §1b | UI | banner | 1 + 3 | ☑ | Isolation caveat: 1 char cannot satisfy composition rules; all extra faults route to the same output class |
| 28 | BVA-07 | edge | Password `Pa` — 2 chars → weak | 04 §1b | UI | banner | 1 + 3 | ☑ | Same caveat as BVA-06 |
| 29 | BVA-04 | edge | Full Name `A` — 1 char → **accepted** | 04 §2 | UI | redirect · **bypass** | 1 + 3 | ☑ | Catches "empty" mis-specified as `length <= 1` |
| 30 | BVA-05 | edge | Full Name `An` — 2 chars → accepted | 04 §2 | UI | redirect · **bypass** | 1 + 3 | ☑ | |
| 31 | TC-24 | negative | Password `Password 123` — 12 chars, upper + lower + digit, **whitespace present, no special char** → must be rejected as weak | derived (not in HW02) | UI | banner | 1 + 3 | ☑ | **Diagnostic case**, deliberately *not* bypassed. The password rows (TC-12→TC-16, TC-22, BVA-01→BVA-03, BVA-06, BVA-07) can all be rejected by the L15 regex for reasons unrelated to what each one tests; this row inverts the input so the cause is isolated. A password satisfying the *printed* rule is rejected while one violating it is accepted — the pair pins the fault to the regex rather than to each case |

**Assertion patterns used:** 1 = UI state · 2 = API/contract · 3 = data integrity / persistence.
At least three distinct patterns must appear across the whole suite (brief §6).

**FR-01 carries all three on its own.** An earlier version of this table claimed it carried
only 1 and 2 and deferred pattern 3 to FR-13's revenue sums and FR-11's ownership check;
that was wrong, and the spec is the evidence:

- **Pattern 1 — UI state.** Banner text and the field it names, the URL after submit, and
  the browser's own `validity` state on the three `native` rows.
- **Pattern 2 — API / contract.** Status code of `POST /api/register`, plus the response
  body: a success must return a numeric `id`, and a refusal must **not** return one.
- **Pattern 3 — data integrity / persistence.** After the UI or the API claims an outcome,
  the suite asks the database through `POST /api/login` whether it is true: a claimed
  success must be loggable in and must return **the name and e-mail that were submitted**;
  a refusal must leave nothing usable behind. This is what separates *"the form redirected"*
  from *"the account exists"*, and it is the assertion that exposed refused registrations
  writing rows anyway.

Pattern 3 is unreachable on exactly four rows, and the table says so per row rather than
hiding it: TC-05 and TC-11 (the lookup key itself was omitted, and no authenticated
account-list endpoint exists on this build) and TC-09 and TC-21 (the account exists by
design, so "nothing was written" is not a claim those rows can make). FR-13 and FR-11 still
carry their own pattern-3 checks; they are no longer the only place it appears.

**Browser caveat.** The three `native` rows assert on constraint-validation *state*
(`checkValidity()`), never on `validationMessage`: that string is produced by the
browser, so it differs across the three required projects (Chromium returned
"Please fill out this field."). Asserting the text would fail on Firefox and WebKit
for a reason that has nothing to do with the SUT.

## Cases deliberately NOT automated

The brief asks you to "document any test cases you could not automate and explain
why". List them here — an honest, reasoned exclusion scores; a silent omission does not.

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| TC-17 | "Confirm ≠ Password" needs a Confirm Password field to type a differing value into. `Register.jsx` renders no such field, and the API body (`{name, email, password}`) has no `confirmPassword` key — unreachable at both interfaces. | Nobody, on this build. It becomes testable only if the field is added. Worth raising as a requirements-vs-implementation gap: HW02 designed against a spec that promised confirmation. |
| TC-23 | "Confirm Password empty" — same missing field. | Same as TC-17. |
| EC-34 (no TC) | "Confirm Password field absent" was designed as a *deviant* condition. On this build it is the **normal** state of the page, so it no longer discriminates anything. HW02 deferred it; it is now moot rather than deferred. | — |

## Open questions recorded by the assertions and resolved by run evidence/student triage

TC-18 to TC-22 carried *conditional* expected results in HW02, and an automated test
needs one concrete assertion. They are now written against the **specification**, which
is what an assertion is supposed to encode. The open questions below are therefore no
longer blockers on writing the test — they are questions about what the SUT actually
does, to be **answered from the run and recorded**, not guessed beforehand. If an
observation contradicts the assertion, that is a finding, not a reason to edit the row.

| OQ | Question | Affects |
|---|---|---|
| OQ-02 | Exact error text / code for each rejection | every negative row |
| OQ-04 / OQ-10 | Is a whitespace-only name treated as empty? | TC-18, and the BVA-04/05 derivation |
| OQ-06 | Is the special-char set exclusive (is `#` rejected)? | TC-22 |
| OQ-09 | Is email uniqueness case-insensitive? | TC-21 |
| OQ-11 | Is a TLD required? Is plus-addressing accepted? | TC-19, TC-20 |
