# API 1 - FR-01 Account Registration - Phase 2: Audit (human review)

> Pipeline step 2 of 4. Every AI-generated case gets a VALID / INVALID /
> INCOMPLETE label with reasoning, and the invalid or incomplete ones get
> corrected. You are responsible for the final test cases.

| Field | Value |
|---|---|
| Endpoint | `POST /api/register` |
| Requirement | FR-01 |
| Cases reviewed | |
| VALID | |
| INVALID | |
| INCOMPLETE | |

## Labelling rules used

- **VALID** - the case is correct as written: right precondition, right input,
  right expected result per the specification, and it is actually executable.
- **INVALID** - the expected result contradicts the spec, the case is not
  executable, or it duplicates another case.
- **INCOMPLETE** - the idea is right but something is missing: no precondition,
  a vague oracle ("should work"), no cleanup, or an assertion too weak to catch
  the defect it targets.

A trap worth watching for: a case that asserts the SUT's *current* behaviour
rather than the *specified* behaviour passes but proves nothing. Label those
INVALID - they hide defects.

## Audit table

| TC ID | Dimension | Label | Reasoning | Correction applied |
|---|---|---|---|---|
| | | | | |

## Corrections made

Describe the substantive rewrites, not the typos.

## Patterns in what the AI got wrong

Feed this into `docs/AI_CRITIQUE.md`.
