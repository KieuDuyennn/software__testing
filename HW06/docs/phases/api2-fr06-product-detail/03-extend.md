# API2 - FR-06 Product Detail (GET /api/products/:id) - Phase 3: Extend

> Five cases designed after the human audit cover omitted encodings, post-conditions, metamorphic consistency, and atomicity.

## Added test cases

| ID | Dimension | Title | Why the AI missed it | Expected | Final run | Bug |
|---|---|---|---|---|---|---|
| A2-HR-001 | Domain | A percent-encoded product id returns the same resource | The AI tested whitespace encoding but not a valid id represented through URL encoding. | 200 with product 1 | PASS | - |
| A2-HR-002 | Security | A query-string id cannot override the product path id | The generated suite did not test precedence when the same logical identifier appears in path and query. | 200 with product 1, not product 2 | PASS | - |
| A2-HR-003 | Schema | An explicit Accept: application/json request returns JSON | The AI asserted the response media type but did not exercise explicit content negotiation. | 200 with application/json | PASS | - |
| A2-HR-004 | Security | A double-encoded SQL payload is neutralised | The AI covered plain SQL payloads but missed a second decoding layer used to bypass filters. | clean 4xx, never a query expansion or server error | PASS | - |
| A2-HR-005 | Domain | A full-width Unicode digit is not confused with an ASCII id | The AI's malformed-id set was ASCII-only and omitted Unicode confusable characters. | 400 or 404, never product 1 and never a 5xx | PASS | - |

## Extension quality check

- Exactly five cases are marked `Student-designed`; they are not included in the AI-generated count.
- Every added case is executable in the same Postman collection and inherits the mandatory `X-Student-Id` harness.
- Each rationale identifies a concrete generation blind spot, not the generic claim that 'AI missed it'.
- Failures are linked to an existing root-cause bug where appropriate, preventing duplicate issue inflation.
