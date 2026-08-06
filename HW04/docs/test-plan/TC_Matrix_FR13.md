# FR-13 Dashboard — test-case matrix (Pool C)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Data file:** `automation/data/fr13_dashboard.json`
**Spec:** `automation/tests/fr13_dashboard/fr13.dashboard.spec.ts`

HW02 confirmed a revenue-doubling defect on this page. Keep at least one case that
recomputes the KPI from an independent source — a test that only checks "a number
is displayed" would have passed against that defect.

| # | TC ID | Type | Intent | HW02 source | Assertion pattern | Automated? | Notes |
|---|---|---|---|---|---|---|---|
| 1 | FR13-TC-01 | positive | all KPI cards render | | 1 | ☐ | |
| 2 | FR13-TC-02 | positive | revenue KPI = independently computed total | | 2 + 3 | ☐ | HW02 BUG: revenue doubled |
| 3 | FR13-TC-03 | negative | non-admin refused the dashboard route | | 1 | ☐ | |
| 4 | | | | | | ☐ | |
| 5 | | | | | | ☐ | |
| 6 | | | | | | ☐ | |
| 7 | | | | | | ☐ | |
| 8 | | | | | | ☐ | |
| 9 | | | | | | ☐ | |
| 10 | | | | | | ☐ | |
| 11 | | | | | | ☐ | |
| 12 | | | | | | ☐ | |

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| | | |
