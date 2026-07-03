# Domain Test Design Heuristics

Reference for Phase 3 (Domain Test Design). Load only when executing this phase.

## Selecting a Minimal Representative Set

Goal: cover every valid and invalid equivalence class from Phase 2 at least once,
using as few test cases as possible.

- **One valid test case per valid-class combination under the single-fault
  assumption**: hold all fields at a valid representative value and vary one field's
  class at a time. Start by covering all-valid (the "happy path"), then create one
  test case per additional valid class that isn't already exercised.
- **One test case per invalid class, in isolation**: an invalid-class test case sets
  exactly one field to its invalid class while every other field holds a valid value.
  This isolates the cause of failure — if two fields are invalid at once, you can't
  tell which one the system reacted to.
- **Do not create a test case for every combination of classes across fields** —
  that's combinatorial and mostly redundant under the single-fault assumption. Only
  combine multiple classes into one test case when:
  - The FR explicitly defines an interaction/dependency between fields (carried over
    from Phase 2's dependency notes), or
  - Two classes are trivially compatible and combining them doesn't reduce fault
    isolation (e.g. pairing an already-covered valid class on field A with the valid
    class under test on field B — this is normal, not an exception).

## Prioritizing by Risk (when time is limited)

If the FR or user indicates a time/resource constraint, prioritize in this order:
1. Happy path (all-valid) test case(s) — proves the core feature works at all.
2. Invalid classes on mandatory fields — most likely to be exercised by real users
   and most likely to cause defects (e.g. missing required data).
3. Invalid classes on optional/edge fields.
4. Valid classes beyond the happy path (alternate valid inputs that don't change the
   outcome logic).

Mark priority as High/Medium/Low in the test case table only if the user has asked
for prioritization; otherwise omit the column rather than fabricating a priority.

## Writing Preconditions, Steps, and Expected Results

- **Preconditions**: state only what must be true before the test starts (e.g. "user
  is logged in", "cart is empty"). Derive from the FR or from Phase 1's atomic
  requirements — never invent setup steps not implied by the requirement.
- **Steps**: numbered, action-oriented, one user action per step (e.g. "Enter '15'
  into the Quantity field", "Click Submit"). Steps must be concrete enough that a
  human tester could execute them without additional interpretation.
- **Expected Result**: state the observable outcome only — what the system should
  show/do. If the FR doesn't specify the exact outcome for an invalid class (e.g. the
  exact error message text), write the expected behavior at the level of detail the
  FR supports (e.g. "system rejects the input and displays a validation error") and
  flag the missing specificity as an Open Question rather than inventing exact
  wording.

## Traceability

Every test case (`TC-xx`) must reference the equivalence class(es) it covers
(`EC-xx`) and, transitively, the atomic requirement (`REQ-xx`). Include an
"Equivalence Class(es) Covered" column in the test case table.
