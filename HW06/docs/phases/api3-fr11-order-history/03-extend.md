# API3 - FR-11 Order History (GET /api/orders/my-orders) - Phase 3: Extend

> Five independently designed cases added after the human audit. They target omitted encodings, post-conditions, metamorphic consistency, and atomicity rather than inflating boundary counts.

## Added test cases

| ID | Dimension | Title | Why the AI missed it | Expected | Final run | Bug |
|---|---|---|---|---|---|---|
| A3-HR-001 | State | A refused shipping cancellation leaves the order in shipping | The AI checked the rejection status but did not verify that a failed transition is atomic and leaves state unchanged. | the order remains shipping after the forbidden request | FAIL - expected 'canceled' to deeply equal 'shipping' | BUG-15 |
| A3-HR-002 | Security | A cross-user cancellation attempt cannot mutate the victim order | The AI tested cross-user cancellation response codes but did not assert the protected resource's post-state. | 200 for the owner and status remains pending | PASS | - |
| A3-HR-003 | Schema | Order detail and history expose the same values for one order | The AI validated each route independently but omitted a metamorphic consistency oracle across the two FR-11 views. | id, user_id, total_amount, status and shipping_address match | PASS | - |
| A3-HR-004 | Security | An oversized cancellation id is rejected safely | The AI covered oversized ids on GET detail but not on the state-changing cancellation route. | clean 4xx, no 5xx and no database detail | PASS | - |
| A3-HR-005 | Security | An anonymous cancellation attempt cannot mutate an order | The AI asserted 401 for the anonymous request but did not independently verify non-mutation. | the order remains pending | PASS | - |

## Extension quality check

- Exactly five cases are marked `Student-designed`; they are not included in the AI-generated count.
- Every added case is executable in the same Postman collection and inherits the mandatory `X-Student-Id` harness.
- Each rationale identifies a concrete generation blind spot, not the generic claim that 'AI missed it'.
- Failures are linked to an existing root-cause bug where appropriate, preventing duplicate issue inflation.
