# FR-01 Account registration — test-case matrix (Pool A)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Data file:** `automation/data/fr01_registration.csv` — one row per case, no inline arrays.
**Spec:** `automation/tests/fr01_account_registration/fr01.registration.spec.ts`

Trace each row back to the HW02 design artifact where one exists
(`HW02/submission/projects/fr01_account_registration/output/`), so the TA can see
that these are the same cases, now automated — not a fresh invention.

| # | TC ID | Type | Intent | HW02 source | Assertion pattern | Automated? | Notes |
|---|---|---|---|---|---|---|---|
| 1 | FR01-TC-01 | positive | all valid fields → account created | | 1 + 2 | ☐ | |
| 2 | FR01-TC-02 | negative | duplicate email rejected | | 1 + 2 | ☐ | |
| 3 | FR01-TC-03 | edge | password length 7 (lower bound − 1) | | 1 | ☐ | |
| 4 | | | | | | ☐ | |
| 5 | | | | | | ☐ | |
| 6 | | | | | | ☐ | |
| 7 | | | | | | ☐ | |
| 8 | | | | | | ☐ | |
| 9 | | | | | | ☐ | |
| 10 | | | | | | ☐ | |
| 11 | | | | | | ☐ | |
| 12 | | | | | | ☐ | |

**Assertion patterns used:** 1 = UI state · 2 = API/contract · 3 = data integrity.
At least three distinct patterns must appear across the whole suite (brief §6).

## Cases deliberately NOT automated

The brief asks you to "document any test cases you could not automate and explain
why". List them here — an honest, reasoned exclusion scores; a silent omission does not.

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| | | |
