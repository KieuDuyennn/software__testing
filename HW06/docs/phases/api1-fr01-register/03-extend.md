# API1 - FR-01 Account Registration (POST /api/register) - Phase 3: Extend

> Five cases designed after the human audit cover omitted encodings, post-conditions, metamorphic consistency, and atomicity.

## Added test cases

| ID | Dimension | Title | Why the AI missed it | Expected | Final run | Bug |
|---|---|---|---|---|---|---|
| A1-HR-001 | Security | An email containing a horizontal tab is rejected | The AI covered ordinary spaces but missed non-printing whitespace that often bypasses simplistic validators. | 4xx - control characters are not part of user@domain.com | PASS | - |
| A1-HR-002 | Security | An email containing CRLF is rejected without response splitting | The generated injection set focused on SQL/XSS and omitted HTTP response-splitting input. | 4xx, no 5xx and no reflected injected header | PASS | - |
| A1-HR-003 | Security | A name containing a NUL character is rejected safely | Control-character validation was absent from the AI's domain partitions. | 4xx and no internal error disclosure | PASS | - |
| A1-HR-004 | Domain | application/json with a UTF-8 charset is accepted | The AI tested application/json and text/plain but missed a common valid media-type parameter. | 200 with the documented success body | PASS | - |
| A1-HR-005 | Domain | A numeric password confirmation is rejected | The AI covered missing, matching and mismatching confirmation values but not its type partition. | 4xx - confirmation must be a string equal to password | PASS | - |

## Extension quality check

- Exactly five cases are marked `Student-designed`; they are not included in the AI-generated count.
- Every added case is executable in the same Postman collection and inherits the mandatory `X-Student-Id` harness.
- Each rationale identifies a concrete generation blind spot, not the generic claim that 'AI missed it'.
- Failures are linked to an existing root-cause bug where appropriate, preventing duplicate issue inflation.
