# HW06 - AI-Driven API Test Generator Design

This design addresses Section 7 and Bloom-AI level G9.5. The generator accepts
the API contract and requirement rules, produces reviewed test definitions,
and renders executable artifacts.

## 1. Inputs

The generator requires:

- Markdown API specification
- FR and SEC requirement sources
- Target endpoint
- Student ID

The live SUT is used only during execution validation. Its responses are
evidence and never define the expected result.

## 2. Case model

`Parse Contract` creates an `EndpointModel` containing parameters, schemas,
authentication rules, requirement IDs, and available operations. Coverage
stages append `CaseDraft` records. Each record contains:

- Case ID and coverage dimension
- Requirement or security rule ID
- Actor and authorization context
- Preconditions and setup
- Request action
- Expected result
- Cleanup requirement
- Source stage

## 3. Generation stages

The stages execute in this order:

1. **Parse Contract:** Normalize the specification and requirement sources.
2. **Domain Partitions:** Generate valid, invalid, boundary, encoded, missing,
   and malformed inputs.
3. **State Transitions:** Generate legal transitions, illegal transitions, and
   terminal-state checks.
4. **Security Model:** Cover anonymous, owner, other-user, and admin actors.
5. **Schema Validation:** Check types, required fields, exact keys, invariants,
   and content type.
6. **Static Validator:** Reject duplicate IDs, duplicate cases, missing rule
   references, unsupported setup, observed-response oracles, and missing
   mandatory headers.
7. **Human Review:** Assign VALID, INVALID, or INCOMPLETE with a reason and any
   required correction.

INVALID and INCOMPLETE cases return to their source stage. Only reviewed cases
enter `ApprovedCases`.

## 4. Outputs

One canonical approved case set feeds four renderers:

- Postman collections
- Machine-readable JSON
- Excel review workbook
- Coverage and phase documents

The Postman collection injects and asserts `X-Student-Id: 23127184` at the
collection level.

## 5. Controls based on observed weaknesses

The design includes the following controls:

- Every oracle cites the API specification or an FR/SEC rule.
- Observed SUT behavior cannot become an expected result.
- Ownership checks use at least two user accounts.
- State coverage includes the complete illegal-transition matrix.
- Post-condition checks confirm that rejected mutations do not change state.
- Metamorphic checks compare related routes and aggregate values.
- Duplicate detection compares both IDs and normalized case definitions.

These controls address the duplicate `A2-DP-006`, the incorrect attribution in
`A1-SEC-013`, and the missing post-state check later covered by `A3-HR-001`.

## 6. Validation and triage

Approved cases are rendered and dry-run against a freshly seeded SUT. The dry
run checks route reachability, fixture determinism, setup support, and cleanup.
A runtime mismatch enters bug triage without changing the spec-derived oracle.
A structural failure returns to static validation with a reason.

## 7. Diagram and implementation

The editable sources and report image are stored in `docs/design/diagram/`:

- `generator-design.mmd`
- `generator-design.svg`
- `generator-design.png`

The pseudocode is `docs/design/generator_pseudocode.py`. The reusable
implementation is under `.claude/skills/api-test-generator/`.

## 8. Verification checklist

- [x] Input sources are identified.
- [x] All seven stages appear in order.
- [x] Arrow labels identify the transferred data.
- [x] Human review is mandatory.
- [x] Output artifacts are listed.
- [x] Rejected cases have a feedback path.
- [x] The diagram contains the student name and ID.
- [x] Pseudocode stage names match the diagram.
