# API4 - FR-13 Admin Dashboard (GET /api/admin/orders) - Phase 3: Extend

> Five independently designed cases added after the human audit. They target omitted encodings, post-conditions, metamorphic consistency, and atomicity rather than inflating boundary counts.

## Added test cases

| ID | Dimension | Title | Why the AI missed it | Expected | Final run | Bug |
|---|---|---|---|---|---|---|
| A4-HR-001 | State | Two delivered orders contribute the exact sum of their totals | The AI tested one delivered order but not additivity across multiple rows, where aggregation bugs commonly appear. | both rows are delivered and contribute 333000 in total | PASS | - |
| A4-HR-002 | Schema | The admin order list contains no duplicate order ids | The AI checked id types and list count but omitted uniqueness, which protects both count and revenue from join duplication. | every id occurs exactly once | PASS | - |
| A4-HR-003 | State | Repeating delivered on a delivered order is refused and non-mutating | The generated transition matrix covered different-state edges but omitted same-state replay on a terminal state. | 4xx and the order remains delivered exactly once | PASS | - |
| A4-HR-004 | Security | A non-admin transition attempt is refused without changing status | The AI proved the authorization defect and one revenue impact; this case adds an explicit atomicity post-condition for another legal edge. | 401/403 and the order remains confirmed | FAIL - expected 200 to be one of [ 401, 403 ] | BUG-06 |
| A4-HR-005 | State | A newly created order appears exactly once in the admin count source | The AI asserted aggregate count but did not test that a single checkout cannot be duplicated by the admin join. | the new order id occurs exactly once | PASS | - |

## Extension quality check

- Exactly five cases are marked `Student-designed`; they are not included in the AI-generated count.
- Every added case is executable in the same Postman collection and inherits the mandatory `X-Student-Id` harness.
- Each rationale identifies a concrete generation blind spot, not the generic claim that 'AI missed it'.
- Failures are linked to an existing root-cause bug where appropriate, preventing duplicate issue inflation.
