---
name: api-test-generator
description: Generate API test cases from a specification for the EShop SUT, driven step by step through domain partitions, state transitions, security (SEC-01..SEC-07) and schema validation. Use when generating, auditing or extending API test cases for HW06, or when asked to produce a Postman collection from an API specification.
---

# API Test Generator (EShop / HW06)

Generates API test cases from a specification, one coverage dimension at a
time, and stops for human review before anything is published.

This skill is the implementation of the design in
`docs/design/GENERATOR_DESIGN.md`. Keep the two in step: if you change a stage
here, change it there.

## Non-negotiables

1. **Never derive an expected result from the SUT's response.** The oracle
   comes from `refs/spec/api_specification.md` and from the FR/SEC rules in
   `refs/spec/eshop_requirements_README.md`. A case whose expectation was read
   off the running system passes by construction and cannot find a defect. This
   is the single most common way AI-generated API tests turn out worthless.
2. **Every case names the rule it enforces** — an FR id, a SEC id, or "spec
   conformance". A case that cannot name one has no oracle; drop it.
3. **Every generated request carries `X-Student-Id`.** Injected by the
   collection-level pre-request script. Required by Section 11 of the brief.
4. **Stop for human review.** Emit a review queue, never a finished collection.
   The student is responsible for correctness, and raw AI output is explicitly
   not acceptable.

## Inputs

| Input | Where |
|---|---|
| API specification | `refs/spec/api_specification.md` |
| FR / SEC requirements | `refs/spec/eshop_requirements_README.md` |
| Existing harness | `postman/collections/*.postman_collection.json` |
| Coverage checklist | `references/coverage-checklist.md` |

## Procedure

Run the stages in order. Do not collapse them into one prompt — the assignment
explicitly forbids that, and each stage's output is the next one's input.

### Stage 0 — Parse the contract

Read the spec entry for the target endpoint and restate it: method, path, every
parameter with its type and whether it is required, the response shape per
status code, and the auth requirement. Then list every FR and SEC id that
constrains this endpoint.

Stop and check the restatement against the spec before continuing. Everything
downstream inherits an error made here.

### Stage 1 — Domain partitions

For each parameter, build an equivalence-class table: valid classes, invalid
classes, and the boundary values between them. Constraints come from the
**requirement document**, not from what the endpoint happens to accept.

Then one case per class and one per boundary.

### Stage 2 — State transitions

Extract the state machine from the requirements (FR-10 for orders). Build the
full state × event matrix and generate a case for every cell — the illegal
transitions especially. Each case needs a setup path describing how to reach
its starting state.

### Stage 3 — Security

Walk SEC-01 through SEC-07. For each, either generate cases or record why it
does not apply to this endpoint — the not-applicable list is part of the
evidence.

Attack patterns worth covering: missing / expired / forged token (SEC-02);
non-admin token on an admin route (SEC-03); SQL injection in every string
parameter (SEC-05); privileged-field injection such as `role` (SEC-06);
low-entropy or reusable OTP (SEC-07).

**Use at least two actors.** IDOR, ownership and privilege escalation are
undetectable with a single user. Set up user A, user B and an admin, and cross
the boundaries deliberately.

### Stage 4 — Schema validation

One case per documented status code, asserting the response with
`pm.response.to.have.jsonSchema` and `additionalProperties: false` — strict
mode is what catches fields the SUT leaks that the spec never promised.

Run the schema assertions across **every** id partition, not one representative
id. Type drift can be data-dependent.

### Stage 5 — Validate

Reject any case that: has no rule id; took its expectation from an observed
response; duplicates an existing case; or needs a precondition it never sets up.

### Stage 6 — Human review

Emit the surviving cases as a review queue with a VALID / INVALID / INCOMPLETE
label field and a mandatory reason field. Hand it to the student. Stop.

### Stage 7 — Emit

Only for cases the human labelled VALID: append to the Postman collection under
the folder for their dimension, and to the Excel test-case table.

## Output format

Emit each case as a row:

| TC ID | Dimension | Rule | Precondition | Request | Expected | Why this can fail |
|---|---|---|---|---|---|---|

The last column is the one that matters — if you cannot say what defect the case
would catch, the case is decoration.

## References

- `references/coverage-checklist.md` — the per-dimension checklist
- `references/sec-rules.md` — SEC-01..SEC-07 with attack patterns
- `../../../docs/design/generator_pseudocode.py` — the staged design
