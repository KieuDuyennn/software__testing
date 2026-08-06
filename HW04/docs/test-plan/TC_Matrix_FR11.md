# FR-11 Order history view — test-case matrix (Pool B)

**Requirement:** ≥ 12 automated cases (any mix of positive / negative / edge).
**Data file:** `automation/data/fr11_order_history.json`
**Spec:** `automation/tests/fr11_order_history/fr11.order-history.spec.ts`

| # | TC ID | Type | Intent | HW02 source | Assertion pattern | Automated? | Notes |
|---|---|---|---|---|---|---|---|
| 1 | FR11-TC-01 | positive | orders listed newest-first | | 1 + 3 | ☐ | |
| 2 | FR11-TC-02 | positive | empty state for a user with no orders | | 1 | ☐ | |
| 3 | FR11-TC-03 | negative | anonymous cannot read an order by ID | | 1 + 2 | ☐ | HW02 BUG candidate |
| 4 | | | | | | ☐ | |
| 5 | | | | | | ☐ | |
| 6 | | | | | | ☐ | |
| 7 | | | | | | ☐ | |
| 8 | | | | | | ☐ | |
| 9 | | | | | | ☐ | |
| 10 | | | | | | ☐ | |
| 11 | | | | | | ☐ | |
| 12 | | | | | | ☐ | |

## Test-data prerequisites

FR-11 asserts on seeded state, so the same 9 runs must see the same data.

| Account | Purpose | Seeded how | Recorded in |
|---|---|---|---|
| `USER_EMAIL` | has ≥ 3 orders in different statuses | manual, before the run | `.env` |
| (second user) | has zero orders | manual, before the run | `.env` |

## Cases deliberately NOT automated

| TC ID | Why it cannot be automated | Who/what could run it |
|---|---|---|
| | | |
